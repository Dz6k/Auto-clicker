from hook import MouseHook
import threading
from time import sleep
import win32api
from typing import NoReturn
import keyboard


class AutoClicker:
    def __init__(self) -> NoReturn:
        self._enable = True
        self._last_state = False
        threading.Thread(None, lambda: MouseHook.run(), daemon=True).start()

    @property
    def is_leftmouse_down(self) -> bool: 
        return win32api.GetKeyState(0x01) < 0
     
    def stop(self) -> NoReturn:
        key_home = keyboard.is_pressed('home')
        if key_home != self._last_state:
                self._last_state = key_home
                if self._last_state:
                    self._enable = not self._enable

    def run(self) -> NoReturn:
        while True:
            self.stop()
            if self._enable:
                if MouseHook.isPressed:
                    MouseHook.send_click()

            sleep(0.026)


AutoClicker().run()