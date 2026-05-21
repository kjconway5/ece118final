import sys
import traceback

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ece118 import UsbSerial, guiWidgets


MIN_UI_FONT_POINT_SIZE = 11


def normalize_application_font(app):
    if app is None:
        return

    font = QFont(app.font())
    if not font.family():
        font.setFamily("Segoe UI")
    if font.pointSizeF() < MIN_UI_FONT_POINT_SIZE:
        font.setPointSizeF(MIN_UI_FONT_POINT_SIZE)
    app.setFont(font)


class MainInterface(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(1280, 720)
        self.setWindowTitle("ECE118 Programmer")

        self.portInstance = UsbSerial.UsbSerial()
        self.portInstance.setAutoConnectMode(True)

        self._build_ui()
        self._connect_signals()
        self._start_status_timer()
        QTimer.singleShot(0, self._install_screen_tracking)
        self.refreshUiState()

    def _build_ui(self):
        centralWidget = QWidget()
        centralLayout = QVBoxLayout()
        centralWidget.setLayout(centralLayout)
        self.setCentralWidget(centralWidget)

        actionRow = QHBoxLayout()
        centralLayout.addLayout(actionRow)

        self.connectButton = QPushButton("Connect")
        self.disconnectButton = QPushButton("Disconnect")
        self.checkForBLButton = QPushButton("Check Bootloader")
        self.burnButton = QPushButton("Burn Hex")

        actionRow.addWidget(self.connectButton)
        actionRow.addWidget(self.disconnectButton)
        actionRow.addWidget(self.checkForBLButton)
        actionRow.addWidget(self.burnButton)
        actionRow.addStretch()

        self.tabs = QTabWidget()
        centralLayout.addWidget(self.tabs)

        self.serialControl = guiWidgets.SerialControl.SerialControl(self.portInstance)
        self.ds30Loader = guiWidgets.ds30Loader.ds30Loader(self.portInstance)
        self.serialIo = guiWidgets.SerialIO.SerialIO(self.portInstance)

        self.tabs.addTab(self.ds30Loader, guiWidgets.ds30Loader.widgetName)
        self.tabs.addTab(self.serialControl, guiWidgets.SerialControl.widgetName)
        self.tabs.addTab(self.serialIo, guiWidgets.SerialIO.widgetName)

        self.serialStatus = QLabel("")
        self.loaderStatus = QLabel("")
        self.statusBar().addPermanentWidget(self.serialStatus)
        self.statusBar().addPermanentWidget(self.loaderStatus)

    def _connect_signals(self):
        self.connectButton.clicked.connect(self.serialControl.connect)
        self.disconnectButton.clicked.connect(self.serialControl.disconnect)
        self.checkForBLButton.clicked.connect(self.openDs30LoaderTab)
        self.checkForBLButton.clicked.connect(self.ds30Loader.startBLCheck)
        self.burnButton.clicked.connect(self.openDs30LoaderTab)
        self.burnButton.clicked.connect(self.ds30Loader.startBurn)

        self.ds30Loader.statusMessage.connect(self.showTransientStatus)
        self.ds30Loader.operationFinished.connect(self.handleLoaderOperationFinished)
        self.ds30Loader.busyChanged.connect(lambda _: self.refreshUiState())
        self.ds30Loader.pathSelection.currentTextChanged.connect(lambda _: self.refreshUiState())
        self.ds30Loader.toolPathChanged.connect(lambda _: self.refreshUiState())
        self.serialControl.serialPortSelection.currentTextChanged.connect(lambda _: self.refreshUiState())

    def _start_status_timer(self):
        self.statusTimer = QTimer(self)
        self.statusTimer.timeout.connect(self.refreshUiState)
        self.statusTimer.start(200)

    def openDs30LoaderTab(self):
        self.tabs.setCurrentWidget(self.ds30Loader)

    def openSerialIoTab(self):
        self.tabs.setCurrentWidget(self.serialIo)

    def handleLoaderOperationFinished(self, operationName, successful):
        if operationName == "burn" and successful:
            self.openSerialIoTab()

    def _install_screen_tracking(self):
        window_handle = self.windowHandle()
        if window_handle is None:
            QTimer.singleShot(0, self._install_screen_tracking)
            return

        try:
            window_handle.screenChanged.disconnect(self._handle_screen_changed)
        except TypeError:
            pass
        window_handle.screenChanged.connect(self._handle_screen_changed)
        self._handle_screen_changed(window_handle.screen())

    def _handle_screen_changed(self, _screen):
        normalize_application_font(QApplication.instance())

    def showTransientStatus(self, message):
        self.statusBar().showMessage(message, 5000)
        self.refreshUiState()

    def refreshUiState(self):
        if not self.portInstance.activeConnection and not self.ds30Loader.isBusy():
            selectedComboPort = self.serialControl.serialPortSelection.currentText().strip()
            self.portInstance.Port = selectedComboPort or None

        activeConnection = self.portInstance.activeConnection
        selectedPort = self.portInstance.Port
        loaderBusy = self.ds30Loader.isBusy()
        toolReady = self.ds30Loader.hasExecutable()
        hasHex = bool(self.ds30Loader.selectedHexPath())

        if activeConnection:
            serialText = f"Serial: {selectedPort} connected"
        elif selectedPort:
            serialText = f"Serial: {selectedPort} available"
        else:
            serialText = "Serial: no port selected"
        self.serialStatus.setText(serialText)

        if toolReady:
            loaderText = f"Loader: {self.ds30Loader.platformDisplayName()} ready"
        else:
            loaderText = f"Loader: {self.ds30Loader.platformDisplayName()} missing"
        if loaderBusy:
            loaderText += " (busy)"
        self.loaderStatus.setText(loaderText)

        canConnect = not activeConnection and not loaderBusy
        canDisconnect = activeConnection and not loaderBusy
        canRunLoader = bool(selectedPort) and toolReady and not loaderBusy

        self.connectButton.setEnabled(canConnect)
        self.disconnectButton.setEnabled(canDisconnect)
        self.checkForBLButton.setEnabled(canRunLoader)
        self.burnButton.setEnabled(canRunLoader and hasHex)

        self.ds30Loader.updateActionState()


mainInterface = MainInterface


sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, tracevalue):
    with open("LastCrash.txt", "w") as crashFile:
        traceback.print_exception(exctype, value, tracevalue, file=crashFile)
    sys._excepthook(exctype, value, tracevalue)
    sys.exit(1)


def main():
    sys.excepthook = my_exception_hook
    app = QApplication(sys.argv)
    normalize_application_font(app)
    gui = MainInterface()
    gui.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
