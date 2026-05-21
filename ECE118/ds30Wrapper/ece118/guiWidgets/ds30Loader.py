import os
import platform
import re
import subprocess
import stat
import tempfile
from pathlib import Path

from PyQt5.QtCore import QProcess, QSettings, pyqtSignal
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import (
    QComboBox,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


widgetName = "ds30 Loader"

DEFAULT_DEVICE = "PIC32MX320F128H"
ALTERNATE_DEVICE = "PIC32MX340F512H"
DEFAULT_BAUD_RATE = 115200
FALLBACK_BAUD_RATES = [57600, 38400, 9600]
NATIVE_BOOTLOADER_TYPE = "ds30_hex"
ALTERNATE_BOOTLOADER_TYPE = "ds30"
DS30_BOOTLOADER_PLACEMENT_PAGES = "1"
DS30_BOOTLOADER_SIZE_PAGES = "8"
FOUND_BOOTLOADER_PATTERN = re.compile(
    r"(Found\s+PIC32.*fw ver\.)|(Found\s+boot\s+loader\s+version)|(Contacting\s+boot\s+loader\.ok)",
    re.IGNORECASE,
)
SUCCESSFUL_WRITE_STRING = "Write successfully completed"
DEFAULT_RESET_PROFILE = "active_low"
ALTERNATE_RESET_PROFILE = "active_high"
RTS_RESET_PROFILE = "rts_active_low"
RTS_ALTERNATE_RESET_PROFILE = "rts_active_high"
MANUAL_RESET_PROFILE = "manual_no_line_reset"
DEFAULT_RESET_TIME_MS = "10"

class ds30Loader(QWidget):
    statusMessage = pyqtSignal(str)
    busyChanged = pyqtSignal(bool)
    toolPathChanged = pyqtSignal(str)
    operationStarted = pyqtSignal(str)
    operationFinished = pyqtSignal(str, bool)

    def __init__(self, portInstance, parent=None):
        super().__init__(parent)
        self.portInstance = portInstance
        self.curSetting = QSettings("UCSC_SOE", "ECE118")
        self.process = None
        self.processOutput = ""
        self.currentOperation = None
        self.executablePath = None
        self.statusSignal = self.statusMessage
        self.transientOutputPath = None
        self.pendingLaunchAttempts = []
        self.lastSuccessfulAttempt = None

        self._build_ui()
        self.loadFileList()
        self.refreshExecutablePath()

    def _build_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        infoGrid = QGridLayout()
        layout.addLayout(infoGrid)

        infoGrid.addWidget(QLabel("Platform:"), 0, 0)
        self.platformValue = QLabel(self.platformDisplayName())
        infoGrid.addWidget(self.platformValue, 0, 1)

        infoGrid.addWidget(QLabel("Loader Tool:"), 1, 0)
        self.executableValue = QLabel("Not found")
        self.executableValue.setWordWrap(True)
        self.executableValue.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        infoGrid.addWidget(self.executableValue, 1, 1)

        self.refreshToolButton = QPushButton("Refresh Tool")
        self.refreshToolButton.clicked.connect(self.handleToolButton)
        infoGrid.addWidget(self.refreshToolButton, 1, 2)
        infoGrid.setColumnStretch(1, 1)

        fileRow = QHBoxLayout()
        layout.addLayout(fileRow)

        self.pathSelection = QComboBox()
        self.pathSelection.setEditable(False)
        self.pathSelection.currentTextChanged.connect(lambda _: self.updateActionState())
        fileRow.addWidget(self.pathSelection, 1)

        self.browseHex = QPushButton("Browse Hex")
        self.browseHex.clicked.connect(self.askForFilePath)
        fileRow.addWidget(self.browseHex)

        self.removeHexButton = QPushButton("Remove Entry")
        self.removeHexButton.clicked.connect(self.removeCurrentHexPath)
        fileRow.addWidget(self.removeHexButton)

        actionRow = QHBoxLayout()
        layout.addLayout(actionRow)

        self.checkBLButton = QPushButton("Check for Bootloader")
        self.checkBLButton.clicked.connect(self.startBLCheck)
        actionRow.addWidget(self.checkBLButton)

        self.burnButton = QPushButton("Burn Program")
        self.burnButton.clicked.connect(self.startBurn)
        actionRow.addWidget(self.burnButton)

        actionRow.addStretch()

        self.consoleOutput = QPlainTextEdit()
        self.consoleOutput.setReadOnly(True)
        layout.addWidget(self.consoleOutput)

    def platformDisplayName(self):
        return platform.system() or "Unknown"

    def platformKey(self):
        return self.platformDisplayName().lower()

    def hasExecutable(self):
        return self.executablePath is not None

    def processErrorName(self, processError):
        processErrorNames = {
            QProcess.FailedToStart: "FailedToStart",
            QProcess.Crashed: "Crashed",
            QProcess.Timedout: "Timedout",
            QProcess.WriteError: "WriteError",
            QProcess.ReadError: "ReadError",
            QProcess.UnknownError: "UnknownError",
        }
        return processErrorNames.get(processError, str(processError))

    def ensureExecutablePermissions(self):
        if self.executablePath is None or os.name == "nt":
            return True

        try:
            currentMode = self.executablePath.stat().st_mode
            if currentMode & stat.S_IXUSR:
                return True
            self.executablePath.chmod(currentMode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            return True
        except OSError:
            return os.access(self.executablePath, os.X_OK)

    def isNativeConsole(self):
        if self.executablePath is None:
            return False
        return self.executablePath.name.startswith("ds30_loader_native_console_")

    def commonLoaderArguments(self, launchAttempt):
        wantedDevice = launchAttempt.get("device", DEFAULT_DEVICE)
        wantedBootloaderType = launchAttempt.get("bootloader_type", NATIVE_BOOTLOADER_TYPE)
        wantedBaudRate = launchAttempt.get("baudrate", DEFAULT_BAUD_RATE)
        useAutoBaud = launchAttempt.get(
            "auto_baud",
            wantedBootloaderType == ALTERNATE_BOOTLOADER_TYPE,
        )
        resetProfile = launchAttempt.get("reset_profile", DEFAULT_RESET_PROFILE)
        if resetProfile == MANUAL_RESET_PROFILE:
            portOpenDelay = "50"
            pollTime = "500"
            timeout = "3000"
            helloTimeout = "1000"
        else:
            portOpenDelay = "10"
            pollTime = "10"
            timeout = "100"
            helloTimeout = "10"
        if self.isNativeConsole():
            arguments = [
                "--device",
                wantedDevice,
                "--bl",
                wantedBootloaderType,
                "--comm",
                "uart",
                "--baudrate",
                str(wantedBaudRate),
                "--port-open-delay",
                portOpenDelay,
                "--polltime",
                pollTime,
                "--timeout",
                timeout,
                "--ht",
                helloTimeout,
            ]
            if useAutoBaud:
                arguments.append("--auto-baud")
            if wantedBootloaderType == ALTERNATE_BOOTLOADER_TYPE:
                arguments.extend(
                    [
                        "--blplp",
                        DS30_BOOTLOADER_PLACEMENT_PAGES,
                        "--blsizep",
                        DS30_BOOTLOADER_SIZE_PAGES,
                    ]
                )
            return arguments

        return [
            f"-d={wantedDevice}",
            f"-r={DEFAULT_BAUD_RATE}",
            "-m",
            "-b=10",
            "-a=500",
            "-t=3000",
            "--ht=1000",
        ]

    def operationArguments(self, operationName):
        if self.isNativeConsole():
            if operationName == "burn":
                return [
                    "--file",
                    self.selectedHexPath(),
                    "--writef",
                ]
            if operationName == "check":
                return [
                    "--check-bl",
                ]
            return []

        if operationName == "burn":
            return [
                "-o",
                "-p",
                f"--file={self.selectedHexPath()}",
            ]
        return ["--find"]

    def portArguments(self, portName=None):
        selectedPort = portName or self.loaderPortName()
        if self.isNativeConsole():
            return ["--port", selectedPort]
        return [f"-k={selectedPort}"]

    def temporaryProbePath(self):
        if self.transientOutputPath is None:
            tempFile = tempfile.NamedTemporaryFile(prefix="ds30_probe_", suffix=".hex", delete=False)
            tempFile.close()
            self.transientOutputPath = Path(tempFile.name)
        return str(self.transientOutputPath)

    def isBusy(self):
        return self.process is not None

    def askForFilePath(self):
        wantedFile, _ = QFileDialog.getOpenFileName(
            self,
            "Select Hex File",
            self.pathSelection.currentText(),
            "Hex files (*.hex)",
        )
        if not wantedFile:
            return

        wantedPath = str(Path(wantedFile).resolve())
        existingIndex = self.pathSelection.findText(wantedPath)
        if existingIndex == -1:
            self.pathSelection.addItem(wantedPath)
            existingIndex = self.pathSelection.findText(wantedPath)
        self.pathSelection.setCurrentIndex(existingIndex)
        self.saveFileList()

    def removeCurrentHexPath(self):
        currentIndex = self.pathSelection.currentIndex()
        if currentIndex >= 0:
            self.pathSelection.removeItem(currentIndex)
            self.saveFileList()

    def candidateSearchRoots(self):
        envPath = os.environ.get("DS30LOADER_PATH")
        savedPath = self.curSetting.value("ds30Loader/tool_path", "", type=str)
        envTargetDir = os.environ.get("ECE118_TARGET_DIR")
        envTargetRoot = os.environ.get("ECE118_TARGET_ROOT")

        searchRoots = []
        if envPath:
            envCandidate = Path(envPath)
            searchRoots.append(envCandidate.parent if envCandidate.is_file() else envCandidate)
        if savedPath:
            savedCandidate = Path(savedPath)
            searchRoots.append(savedCandidate.parent if savedCandidate.is_file() else savedCandidate)

        searchRoots.extend(
            [
                Path(r"C:\ECE118\ds30Loader\bin"),
                Path(r"C:\ece118\ds30 Loader\bin"),
                Path.home() / "ECE118" / "ds30 Loader" / "bin",
                Path(__file__).resolve().parents[3] / "Utilities" / "ds30_Loader" / "bin",
                Path(__file__).resolve().parents[3] / "Utilities" / "Package_Code" / "ECE118" / "ds30 Loader" / "bin",
            ]
        )

        if envTargetDir:
            searchRoots.append(Path(envTargetDir).expanduser() / "ds30 Loader" / "bin")
        if envTargetRoot:
            searchRoots.append(Path(envTargetRoot).expanduser() / "ECE118" / "ds30 Loader" / "bin")
        return searchRoots

    def candidateExecutableNames(self):
        platformKey = self.platformKey()
        machine = platform.machine().lower()

        if platformKey == "windows":
            return ["ds30LoaderConsole.exe"]

        if platformKey == "linux":
            if any(token in machine for token in ("x86_64", "amd64")):
                return [
                    "ds30_loader_native_console_linux_x64_static",
                    "ds30_loader_native_console_linux_x86_static",
                ]
            return [
                "ds30_loader_native_console_linux_x86_static",
                "ds30_loader_native_console_linux_x64_static",
            ]

        if platformKey == "darwin":
            if any(token in machine for token in ("arm64", "aarch64")):
                return [
                    "ds30_loader_native_console_macos_arm64",
                    "ds30_loader_native_console_macos_universal",
                    "ds30_loader_native_console_macos_x64",
                ]
            return [
                "ds30_loader_native_console_macos_x64",
                "ds30_loader_native_console_macos_universal",
                "ds30_loader_native_console_macos_arm64",
            ]

        return [
            "ds30LoaderConsole",
            "ds30LoaderConsole.exe",
        ]

    def canLaunchCandidateExecutable(self, candidatePath):
        if not candidatePath.exists() or not candidatePath.is_file():
            return False, "missing"

        if os.name != "nt":
            try:
                currentMode = candidatePath.stat().st_mode
                if not (currentMode & stat.S_IXUSR):
                    candidatePath.chmod(currentMode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            except OSError as exc:
                if not os.access(candidatePath, os.X_OK):
                    return False, f"not executable ({exc})"

        if os.name == "nt":
            return True, ""

        try:
            subprocess.run(
                [str(candidatePath), "--help"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=2,
                check=False,
            )
            return True, ""
        except PermissionError as exc:
            return False, f"permission denied ({exc})"
        except FileNotFoundError as exc:
            return False, f"not found ({exc})"
        except subprocess.TimeoutExpired:
            return True, ""
        except OSError as exc:
            return False, str(exc)

    def refreshExecutablePath(self):
        self.executablePath = None
        skippedCandidates = []
        for root in self.candidateSearchRoots():
            for candidateName in self.candidateExecutableNames():
                candidatePath = root / candidateName
                if candidatePath.exists() and candidatePath.is_file():
                    canLaunch, reason = self.canLaunchCandidateExecutable(candidatePath)
                    if canLaunch:
                        self.executablePath = candidatePath.resolve()
                        break
                    skippedCandidates.append(f"{candidatePath} ({reason})")
            if self.executablePath is not None:
                break

        if self.executablePath is None:
            self.executableValue.setText("Not found")
            if skippedCandidates:
                self.statusSignal.emit("No launchable ds30 loader binary found")
                self.consoleOutput.appendPlainText(
                    "Skipped loader candidates:\n" + "\n".join(skippedCandidates)
                )
            else:
                self.statusSignal.emit("No ds30LoaderConsole binary found")
            self.toolPathChanged.emit("")
            self.refreshToolButton.setText("Locate Tool")
        else:
            self.executableValue.setText(str(self.executablePath))
            self.rememberToolPath(self.executablePath)
            self.toolPathChanged.emit(str(self.executablePath))
            self.refreshToolButton.setText("Refresh Tool")

        self.updateActionState()

    def handleToolButton(self):
        if self.hasExecutable():
            self.refreshExecutablePath()
            return
        self.locateExecutablePath()

    def locateExecutablePath(self):
        selectedPath, _ = QFileDialog.getOpenFileName(
            self,
            "Locate ds30LoaderConsole",
            self.defaultToolBrowseDirectory(),
            self.toolFileDialogFilter(),
        )
        if not selectedPath:
            return

        candidatePath = Path(selectedPath).resolve()
        if not candidatePath.exists() or not candidatePath.is_file():
            QMessageBox.warning(self, "Invalid Tool", "The selected ds30 loader tool could not be used.")
            return

        self.executablePath = candidatePath
        self.rememberToolPath(candidatePath)
        os.environ["DS30LOADER_PATH"] = str(candidatePath.parent)
        self.executableValue.setText(str(candidatePath))
        self.statusSignal.emit("Using manually selected ds30 loader tool")
        self.toolPathChanged.emit(str(candidatePath))
        self.refreshToolButton.setText("Refresh Tool")
        self.updateActionState()

    def rememberToolPath(self, toolPath):
        self.curSetting.setValue("ds30Loader/tool_path", str(toolPath))
        self.curSetting.sync()

    def defaultToolBrowseDirectory(self):
        if self.executablePath is not None:
            return str(self.executablePath.parent)

        savedPath = self.curSetting.value("ds30Loader/tool_path", "", type=str)
        if savedPath:
            savedCandidate = Path(savedPath)
            return str(savedCandidate.parent if savedCandidate.is_file() else savedCandidate)

        envPath = os.environ.get("DS30LOADER_PATH")
        if envPath:
            envCandidate = Path(envPath)
            return str(envCandidate.parent if envCandidate.is_file() else envCandidate)

        for root in self.candidateSearchRoots():
            if root.exists():
                return str(root)
        return str(Path.home())

    def toolFileDialogFilter(self):
        if self.platformKey() == "windows":
            return "ds30 Loader (ds30LoaderConsole.exe);;All files (*)"
        return "ds30 Loader (ds30_loader_native_console_*);;All files (*)"

    def selectedHexPath(self):
        return self.pathSelection.currentText().strip()

    def currentPortName(self):
        return self.portInstance.Port

    def loaderPortName(self):
        portName = self.currentPortName()
        if not portName:
            return portName
        if self.isNativeConsole() and self.platformKey() == "darwin" and portName.startswith("/dev/cu."):
            return "/dev/tty." + portName[len("/dev/cu.") :]
        return portName

    def candidateLoaderPorts(self):
        portName = self.currentPortName()
        if not portName:
            return []

        if self.isNativeConsole() and self.platformKey() == "darwin":
            candidates = []
            if portName.startswith("/dev/cu."):
                candidates = [
                    "/dev/tty." + portName[len("/dev/cu.") :],
                    portName,
                ]
            elif portName.startswith("/dev/tty."):
                candidates = [
                    portName,
                    "/dev/cu." + portName[len("/dev/tty.") :],
                ]
            else:
                candidates = [portName]

            deduped = []
            for candidate in candidates:
                if candidate not in deduped:
                    deduped.append(candidate)
            return deduped

        return [self.loaderPortName()]

    def candidateDevices(self):
        preferredDevice = self.curSetting.value("ds30Loader/preferred_device", "", type=str).strip()
        candidates = []
        if preferredDevice:
            candidates.append(preferredDevice)
        for device in (DEFAULT_DEVICE, ALTERNATE_DEVICE):
            if device not in candidates:
                candidates.append(device)
        return candidates

    def _settingBool(self, key, defaultValue=False):
        rawValue = self.curSetting.value(key, defaultValue)
        if isinstance(rawValue, bool):
            return rawValue
        if isinstance(rawValue, (int, float)):
            return bool(rawValue)
        if isinstance(rawValue, str):
            normalized = rawValue.strip().lower()
            return normalized in ("1", "true", "yes", "on")
        return defaultValue

    def preferredLaunchSettings(self):
        preferred = {}
        preferredPort = self.curSetting.value("ds30Loader/preferred_port", "", type=str).strip()
        preferredReset = self.curSetting.value("ds30Loader/preferred_reset_profile", "", type=str).strip()
        preferredBaud = self.curSetting.value("ds30Loader/preferred_baudrate", 0, type=int)
        preferredAutoBaud = self._settingBool("ds30Loader/preferred_auto_baud", False)
        preferredBl = self.curSetting.value("ds30Loader/preferred_bl_type", "", type=str).strip()
        preferredDevice = self.curSetting.value("ds30Loader/preferred_device", "", type=str).strip()

        if preferredPort:
            preferred["port"] = preferredPort
        if preferredReset:
            preferred["reset_profile"] = preferredReset
        if preferredBaud:
            preferred["baudrate"] = preferredBaud
        preferred["auto_baud"] = preferredAutoBaud
        if preferredBl:
            preferred["bootloader_type"] = preferredBl
        if preferredDevice:
            preferred["device"] = preferredDevice
        return preferred

    def candidateBootloaderTypes(self):
        preferredType = self.curSetting.value("ds30Loader/preferred_bl_type", "", type=str).strip()
        candidates = []
        if preferredType:
            candidates.append(preferredType)
        for blType in (NATIVE_BOOTLOADER_TYPE, ALTERNATE_BOOTLOADER_TYPE):
            if blType not in candidates:
                candidates.append(blType)
        return candidates

    def candidateLaunchAttempts(self):
        ports = self.candidateLoaderPorts()
        if not ports:
            return []

        if self.isNativeConsole() and self.platformKey() == "darwin":
            portResetAttempts = [{"port": port, "reset_profile": DEFAULT_RESET_PROFILE} for port in ports]
            primaryWorkingPort = ports[-1]
            portResetAttempts.append({"port": primaryWorkingPort, "reset_profile": ALTERNATE_RESET_PROFILE})
            portResetAttempts.append({"port": primaryWorkingPort, "reset_profile": RTS_RESET_PROFILE})
            portResetAttempts.append({"port": primaryWorkingPort, "reset_profile": RTS_ALTERNATE_RESET_PROFILE})
            portResetAttempts.append({"port": primaryWorkingPort, "reset_profile": MANUAL_RESET_PROFILE})
        else:
            portResetAttempts = [{"port": ports[0], "reset_profile": DEFAULT_RESET_PROFILE}]

        allAttempts = []
        for bootloaderType in self.candidateBootloaderTypes():
            for device in self.candidateDevices():
                for portResetAttempt in portResetAttempts:
                    baudrateCandidates = [DEFAULT_BAUD_RATE]
                    autoBaudCandidates = [bootloaderType == ALTERNATE_BOOTLOADER_TYPE]

                    # On Intel macOS adapters, manual reset mode may require
                    # slower UART rates or disabling auto-baud for ds30.
                    if portResetAttempt.get("reset_profile") == MANUAL_RESET_PROFILE:
                        baudrateCandidates.extend(
                            rate for rate in FALLBACK_BAUD_RATES if rate not in baudrateCandidates
                        )
                        if bootloaderType == ALTERNATE_BOOTLOADER_TYPE:
                            autoBaudCandidates = [True, False]

                    for baudrate in baudrateCandidates:
                        for autoBaudMode in autoBaudCandidates:
                            fullAttempt = dict(portResetAttempt)
                            fullAttempt["bootloader_type"] = bootloaderType
                            fullAttempt["device"] = device
                            fullAttempt["baudrate"] = baudrate
                            fullAttempt["auto_baud"] = autoBaudMode
                            allAttempts.append(fullAttempt)
        preferred = self.preferredLaunchSettings()
        if preferred:
            def mismatchCount(attempt):
                mismatch = 0
                for key, preferredValue in preferred.items():
                    if key in attempt and attempt.get(key) != preferredValue:
                        mismatch += 1
                return mismatch

            allAttempts.sort(key=mismatchCount)

        return allAttempts

    def resetArguments(self, launchAttempt):
        if not self.isNativeConsole():
            return []

        profile = launchAttempt.get("reset_profile", DEFAULT_RESET_PROFILE)
        if profile == MANUAL_RESET_PROFILE:
            return []
        if profile == ALTERNATE_RESET_PROFILE:
            return ["--reset-dtr", "--reset-time", DEFAULT_RESET_TIME_MS, "--activate-dtr"]
        if profile == RTS_RESET_PROFILE:
            return ["--reset-rts", "--reset-time", DEFAULT_RESET_TIME_MS]
        if profile == RTS_ALTERNATE_RESET_PROFILE:
            return ["--reset-rts", "--reset-time", DEFAULT_RESET_TIME_MS, "--activate-rts"]
        return ["--reset-dtr", "--reset-time", DEFAULT_RESET_TIME_MS]

    def validateRunPrerequisites(self, requireHex):
        if self.isBusy():
            self.statusSignal.emit("Bootloader tool is already running")
            return False

        if not self.hasExecutable():
            self.refreshExecutablePath()
            if not self.hasExecutable():
                QMessageBox.critical(
                    self,
                    "ds30 Loader Not Found",
                    "No ds30LoaderConsole binary was found for this platform.",
                )
                return False

        if not self.currentPortName():
            self.statusSignal.emit("No serial port selected")
            QMessageBox.warning(self, "No Serial Port", "Select a serial port before running the bootloader.")
            return False

        if self.platformKey() != "windows" and self.executablePath.suffix.lower() == ".exe":
            self.statusSignal.emit("Select a native ds30 loader binary for this platform")
            QMessageBox.critical(
                self,
                "Native Loader Required",
                "The selected ds30 loader is a Windows .exe file.\n\n"
                "On macOS or Linux, choose the matching native binary instead, such as:\n"
                "macOS: ds30_loader_native_console_macos_arm64, _universal, or _x64\n"
                "Linux: ds30_loader_native_console_linux_x64_static or _x86_static",
            )
            return False

        if not self.ensureExecutablePermissions():
            self.statusSignal.emit("Loader binary is not executable")
            QMessageBox.critical(
                self,
                "Loader Not Executable",
                f"The selected loader could not be marked executable:\n{self.executablePath}\n\n"
                "On macOS/Linux, the native ds30 loader must have execute permission.",
            )
            return False

        if requireHex:
            wantedHex = self.selectedHexPath()
            if not wantedHex:
                self.statusSignal.emit("No hex file selected")
                QMessageBox.warning(self, "No Hex File", "Choose a hex file before programming.")
                return False
            if not Path(wantedHex).exists():
                self.statusSignal.emit("Selected hex file is missing")
                QMessageBox.warning(
                    self,
                    "Hex File Missing",
                    f"The selected hex file does not exist:\n{wantedHex}",
                )
                return False

        return True

    def startBurn(self):
        if not self.validateRunPrerequisites(requireHex=True):
            return
        self.saveFileList()
        self._startProcess(
            operationName="burn",
            statusText="Beginning programming",
            successMessage="Programming complete",
            failureMessage="Programming failed",
        )

    def startBLCheck(self):
        if not self.validateRunPrerequisites(requireHex=False):
            return
        self._startProcess(
            operationName="check",
            statusText="Checking for bootloader",
            successMessage="Bootloader found",
            failureMessage="Bootloader not found",
        )

    def _startProcess(self, operationName, statusText, successMessage, failureMessage):
        self.consoleOutput.clear()
        self.processOutput = ""
        self.currentOperation = {
            "name": operationName,
            "success": successMessage,
            "failure": failureMessage,
        }
        self.pendingLaunchAttempts = self.candidateLaunchAttempts()
        self._launchProcessAttempt(statusText)

    def _launchProcessAttempt(self, statusText):
        if not self.pendingLaunchAttempts:
            self.statusSignal.emit("No loader port available")
            self.operationFinished.emit(self.currentOperation.get("name", ""), False)
            self._cleanupAfterProcess()
            return

        launchAttempt = self.pendingLaunchAttempts[0]
        portName = launchAttempt["port"]
        arguments = self.commonLoaderArguments(launchAttempt)
        arguments.extend(self.resetArguments(launchAttempt))
        arguments.extend(self.operationArguments(self.currentOperation["name"]))
        arguments.extend(self.portArguments(portName))

        self.consoleOutput.appendPlainText(
            "Running: {} {}".format(self.executablePath, " ".join(arguments))
        )

        self.portInstance.Disconnect()

        process = QProcess(self)
        process.setProgram(str(self.executablePath))
        process.setArguments(arguments)
        process.setProcessChannelMode(QProcess.MergedChannels)
        process.readyReadStandardOutput.connect(self._consumeProcessOutput)
        process.finished.connect(self._handleProcessFinished)
        process.errorOccurred.connect(self._handleProcessError)

        self.process = process
        self.statusSignal.emit(statusText)
        self.updateActionState()
        self.busyChanged.emit(True)
        self.operationStarted.emit(self.currentOperation["name"])
        process.start()

    def _consumeProcessOutput(self):
        if self.process is None:
            return
        newText = bytes(self.process.readAllStandardOutput()).decode("utf-8", errors="replace")
        if not newText:
            return
        self.processOutput += newText
        self.consoleOutput.moveCursor(QTextCursor.End)
        self.consoleOutput.insertPlainText(newText)
        self.consoleOutput.ensureCursorVisible()

    def _handleProcessFinished(self, exitCode, exitStatus):
        if self.process is None:
            return

        operation = self.currentOperation or {}
        output = self.processOutput
        launchAttempt = self.pendingLaunchAttempts[0] if self.pendingLaunchAttempts else {}

        success = False
        if operation.get("name") == "check":
            success = bool(FOUND_BOOTLOADER_PATTERN.search(output))
        elif operation.get("name") == "burn":
            success = SUCCESSFUL_WRITE_STRING in output

        operationName = operation.get("name", "")
        retryAlternatePort = (
            not success
            and len(self.pendingLaunchAttempts) > 1
            and (
                ("Opening port" in output and "failed" in output.lower())
                or "invalid hi response" in output.lower()
                or "hi timed out" in output.lower()
                or "contacting boot loader..timed out" in output.lower()
                or "contacting boot loader...timed out" in output.lower()
                or "auto baud rate synchronization character...timed out" in output.lower()
                or "sending auto baud rate synchronization character...timed out" in output.lower()
                or "sending auto baud rate synchronization character...invalid response" in output.lower()
                or "invalid response:" in output.lower()
                or "timed out" in output.lower()
                or "tx timeout" in output.lower()
            )
        )

        if retryAlternatePort:
            failedAttempt = self.pendingLaunchAttempts.pop(0)
            nextAttempt = self.pendingLaunchAttempts[0]
            self.consoleOutput.appendPlainText(
                "\nRetrying with alternate loader attempt: "
                f"port={nextAttempt['port']}, reset={nextAttempt['reset_profile']}, "
                f"bl={nextAttempt.get('bootloader_type', NATIVE_BOOTLOADER_TYPE)}, "
                f"device={nextAttempt.get('device', DEFAULT_DEVICE)}, "
                f"baud={nextAttempt.get('baudrate', DEFAULT_BAUD_RATE)}, "
                f"auto_baud={nextAttempt.get('auto_baud', False)} "
                f"(after port={failedAttempt['port']}, reset={failedAttempt['reset_profile']}, "
                f"bl={failedAttempt.get('bootloader_type', NATIVE_BOOTLOADER_TYPE)}, "
                f"device={failedAttempt.get('device', DEFAULT_DEVICE)}, "
                f"baud={failedAttempt.get('baudrate', DEFAULT_BAUD_RATE)}, "
                f"auto_baud={failedAttempt.get('auto_baud', False)} failed)."
            )
            self.process.deleteLater()
            self.process = None
            self.processOutput = ""
            self._launchProcessAttempt(
                f"Retrying bootloader on {nextAttempt['port']} with {nextAttempt['reset_profile']}"
            )
            return

        if success:
            self.lastSuccessfulAttempt = launchAttempt
            rememberedType = launchAttempt.get("bootloader_type", NATIVE_BOOTLOADER_TYPE)
            rememberedDevice = launchAttempt.get("device", DEFAULT_DEVICE)
            self.curSetting.setValue("ds30Loader/preferred_bl_type", rememberedType)
            self.curSetting.setValue("ds30Loader/preferred_device", rememberedDevice)
            self.curSetting.setValue("ds30Loader/preferred_port", launchAttempt.get("port", ""))
            self.curSetting.setValue(
                "ds30Loader/preferred_reset_profile",
                launchAttempt.get("reset_profile", DEFAULT_RESET_PROFILE),
            )
            self.curSetting.setValue("ds30Loader/preferred_baudrate", launchAttempt.get("baudrate", DEFAULT_BAUD_RATE))
            self.curSetting.setValue("ds30Loader/preferred_auto_baud", launchAttempt.get("auto_baud", False))
            self.curSetting.sync()
            self.consoleOutput.appendPlainText(
                f"\nMatched bootloader profile: --bl {rememberedType}, --device {rememberedDevice}"
            )
            self.statusSignal.emit(operation.get("success", "Operation complete"))
        else:
            if "would overwrite the boot loader" in output.lower():
                self.consoleOutput.appendPlainText(
                    "\nSelected hex appears to be a bootloader image. "
                    "Choose your project/application .hex (typically from "
                    "dist/default/production) instead of ds30_Loader/firmware/*.hex."
                )
            self.statusSignal.emit(operation.get("failure", "Operation failed"))
            if exitStatus != QProcess.NormalExit:
                self.consoleOutput.appendPlainText("\nProcess crashed before completion.")
            elif exitCode != 0:
                self.consoleOutput.appendPlainText(f"\nProcess exited with code {exitCode}.")

        self.operationFinished.emit(operationName, success)
        self._cleanupAfterProcess()

    def _handleProcessError(self, processError):
        if self.process is None:
            return

        errorName = self.processErrorName(processError)
        self.consoleOutput.appendPlainText(f"\nProcess error: {processError} ({errorName})")
        if processError == QProcess.FailedToStart:
            self.consoleOutput.appendPlainText(
                "The loader could not be started. On macOS/Linux this usually means the file "
                "is not executable, is blocked by Gatekeeper/quarantine, or does not match the CPU architecture."
            )
        failureMessage = "Unable to launch ds30LoaderConsole"
        operationName = ""
        if self.currentOperation is not None:
            failureMessage = self.currentOperation.get("failure", failureMessage)
            operationName = self.currentOperation.get("name", "")
        self.statusSignal.emit(failureMessage)
        self.operationFinished.emit(operationName, False)
        self._cleanupAfterProcess()

    def _cleanupAfterProcess(self):
        if self.process is not None:
            self.process.deleteLater()
        self.process = None
        self.currentOperation = None
        self.pendingLaunchAttempts = []
        if self.transientOutputPath is not None:
            try:
                self.transientOutputPath.unlink(missing_ok=True)
            except OSError:
                pass
            self.transientOutputPath = None
        self.portInstance.Connect()
        self.updateActionState()
        self.busyChanged.emit(False)

    def updateActionState(self):
        hasPort = bool(self.currentPortName())
        hasHex = bool(self.selectedHexPath())
        toolReady = self.hasExecutable()
        busy = self.isBusy()

        self.checkBLButton.setEnabled(hasPort and toolReady and not busy)
        self.burnButton.setEnabled(hasPort and hasHex and toolReady and not busy)
        self.browseHex.setEnabled(not busy)
        self.removeHexButton.setEnabled(self.pathSelection.count() > 0 and not busy)
        self.refreshToolButton.setEnabled(not busy)

    def saveFileList(self):
        self.curSetting.beginGroup("ds30Loader")
        self.curSetting.beginWriteArray("used_files")
        for index in range(self.pathSelection.count()):
            self.curSetting.setArrayIndex(index)
            self.curSetting.setValue("Path", self.pathSelection.itemText(index))
        self.curSetting.endArray()
        self.curSetting.setValue("cur_index", self.pathSelection.currentIndex())
        self.curSetting.endGroup()
        self.curSetting.sync()

    def loadFileList(self):
        self.curSetting.beginGroup("ds30Loader")
        itemCount = self.curSetting.beginReadArray("used_files")
        paths = []
        for index in range(itemCount):
            self.curSetting.setArrayIndex(index)
            currentPath = self.curSetting.value("Path")
            if currentPath and currentPath not in paths:
                paths.append(currentPath)
                self.pathSelection.addItem(currentPath)
        self.curSetting.endArray()

        currentIndex = self.curSetting.value("cur_index", 0, type=int)
        if self.pathSelection.count() > 0:
            currentIndex = max(0, min(currentIndex, self.pathSelection.count() - 1))
            self.pathSelection.setCurrentIndex(currentIndex)
        self.curSetting.endGroup()
        self.updateActionState()
        return paths
