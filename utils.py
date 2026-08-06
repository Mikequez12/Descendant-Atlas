import os
import sys
import re

ansi_supported = True

if os.name == "nt":
    try:
        import ctypes
        STD_OUTPUT_HANDLE = -11
        handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        kernel32 = ctypes.windll.kernel32
        mode = ctypes.c_uint()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            ansi_supported = bool(kernel32.SetConsoleMode(handle, mode.value | 0x0004))
        else:
            ansi_supported = False
    except Exception:
        ansi_supported = False

unicode_supported = (
    sys.stdout.encoding
    and sys.stdout.encoding.lower().startswith("utf")
)

class Empty:
    def __init__(self):pass
    def __getattribute__(self, name):return ''

class Console:
    def __init__(self):pass
    def print(self,*args):
        args = [re.sub(r"\[/?[^\[\]]+\]", "", arg) for arg in args]
        print(*args)

Color = Empty()
Effect = Empty()