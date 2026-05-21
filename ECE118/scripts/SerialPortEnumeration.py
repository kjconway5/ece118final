import tkinter as tk
from tkinter import messagebox
import platform
import subprocess
import sys

try:
    from serial.tools import list_ports
except ImportError:
    list_ports = None

if platform.system() == "Windows":
    import ctypes
    import winreg
else:
    ctypes = None
    winreg = None


WINDOWS_COMDB_KEY = r"SYSTEM\CurrentControlSet\Control\COM Name Arbiter"
WINDOWS_COMDB_VALUE = "ComDB"


def get_serial_ports():
    if list_ports is None:
        return None

    ports = []
    for port in list_ports.comports():
        description = (port.description or "").strip()
        if description and description != port.device:
            ports.append(f"{port.device} - {description}")
        else:
            ports.append(port.device)

    return sorted(ports)


def build_message():
    ports = get_serial_ports()

    if ports is None:
        return (
            "This script requires pyserial.\n\n"
            "Install it with:\n"
            "python -m pip install pyserial"
        )
    if ports:
        return "Current serial ports:\n\n" + "\n".join(ports)
    return "No serial ports are currently enumerated."


def reset_windows_com_numbers():
    if winreg is None:
        raise OSError("COM number reset is only supported on Windows.")

    with winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        WINDOWS_COMDB_KEY,
        0,
        winreg.KEY_QUERY_VALUE | winreg.KEY_SET_VALUE,
    ) as key:
        current_value, value_type = winreg.QueryValueEx(key, WINDOWS_COMDB_VALUE)
        if value_type != winreg.REG_BINARY:
            raise OSError("Unexpected COM reservation format in the registry.")

        winreg.SetValueEx(
            key,
            WINDOWS_COMDB_VALUE,
            0,
            winreg.REG_BINARY,
            bytes(len(current_value)),
        )


def is_windows_admin():
    if ctypes is None:
        return False

    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except OSError:
        return False


def relaunch_as_admin_for_reset():
    if ctypes is None:
        raise OSError("Administrator relaunch is only supported on Windows.")

    if getattr(sys, "frozen", False):
        executable = sys.executable
        parameters = "--reset-com-db"
    else:
        executable = sys.executable
        parameters = subprocess.list2cmdline([sys.argv[0], "--reset-com-db"])

    result = ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        executable,
        parameters,
        None,
        1,
    )
    if result <= 32:
        raise OSError("Administrator elevation was cancelled or failed.")


def on_reset(root, message_var):
    confirmed = messagebox.askyesno(
        "Reset COM Numbers",
        (
            "This will clear the Windows COM port reservation table in the registry.\n\n"
            "Use this only if you want Windows to reassign COM numbers.\n"
            "Administrator privileges may be required.\n\n"
            "Continue?"
        ),
        parent=root,
    )
    if not confirmed:
        return

    try:
        if is_windows_admin():
            reset_windows_com_numbers()
        else:
            relaunch_as_admin_for_reset()
            messagebox.showinfo(
                "Elevation Requested",
                (
                    "An elevated copy of this script was launched.\n\n"
                    "Approve the Windows UAC prompt to clear the COM reservation table, "
                    "then use Refresh here after it completes."
                ),
                parent=root,
            )
            return
    except OSError as exc:
        messagebox.showerror("Reset Failed", str(exc), parent=root)
        return

    messagebox.showinfo(
        "Reset Complete",
        (
            "The COM reservation table was cleared.\n\n"
            "You may need to unplug/replug devices or reboot Windows before new COM assignments appear."
        ),
        parent=root,
    )
    message_var.set(build_message())


def main():
    root = tk.Tk()
    root.title("Serial Port Enumeration")
    root.resizable(False, False)

    frame = tk.Frame(root, padx=12, pady=12)
    frame.pack(fill="both", expand=True)

    message_var = tk.StringVar(value=build_message())
    tk.Label(frame, textvariable=message_var, justify="left", anchor="w").pack(
        fill="both", expand=True
    )

    button_frame = tk.Frame(frame, pady=8)
    button_frame.pack(fill="x")

    tk.Button(
        button_frame,
        text="Refresh",
        command=lambda: message_var.set(build_message()),
    ).pack(side="left")

    reset_button = tk.Button(
        button_frame,
        text="Reset COM Numbers",
        command=lambda: on_reset(root, message_var),
    )
    reset_button.pack(side="left", padx=(8, 0))

    if platform.system() != "Windows":
        reset_button.configure(state="disabled")

    tk.Button(button_frame, text="Close", command=root.destroy).pack(side="right")

    root.mainloop()


if __name__ == "__main__":
    if "--reset-com-db" in sys.argv:
        try:
            reset_windows_com_numbers()
        except Exception as exc:
            temp_root = tk.Tk()
            temp_root.withdraw()
            messagebox.showerror("Reset Failed", str(exc), parent=temp_root)
            temp_root.destroy()
            raise SystemExit(1)

        temp_root = tk.Tk()
        temp_root.withdraw()
        messagebox.showinfo(
            "Reset Complete",
            (
                "The COM reservation table was cleared.\n\n"
                "You may need to unplug/replug devices or reboot Windows before new COM assignments appear."
            ),
            parent=temp_root,
        )
        temp_root.destroy()
        raise SystemExit(0)

    main()
