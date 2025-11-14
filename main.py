from hook import MouseHook, Mouse
import threading
from time import sleep
import win32api
from typing import NoReturn

class AutoClicker:
    def __init__(self) -> NoReturn:
        self.hook = MouseHook()
        threading.Thread(None, lambda: self.hook.run(), daemon=True).start()

    @property
    def is_leftmouse_down(self) -> bool:
        return win32api.GetKeyState(Mouse.MOUSEEVENTF_LEFTDOWN) < 0
