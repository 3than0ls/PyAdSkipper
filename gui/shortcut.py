import os, sys
import pythoncom
from win32com.shell import shell, shellcon  # type: ignore


# http://timgolden.me.uk/python/win32_how_do_i/create-a-shortcut.html


def create_desktop_shortcut():
    shortcut = pythoncom.CoCreateInstance(
        shell.CLSID_ShellLink,
        None,
        pythoncom.CLSCTX_INPROC_SERVER,
        shell.IID_IShellLink,
    )

    # diverge from the straight copypaste to set the working directory
    shortcut.SetWorkingDirectory(os.path.abspath(os.getcwd()))

    shortcut.SetPath(os.path.abspath(r".\PyAdSkipper.exe"))
    shortcut.SetDescription("PyAdSkipper GUI shortcut")
    shortcut.SetIconLocation(os.path.abspath(r".\icon.ico"), 0)

    desktop_path = shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, 0, 0)
    persist_file = shortcut.QueryInterface(pythoncom.IID_IPersistFile)
    persist_file.Save(os.path.join(desktop_path, "PyAdSkipper.lnk"), 0)
