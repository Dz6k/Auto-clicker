from hook import MouseHook
import threading
from time import sleep
import time
import win32api
from typing import NoReturn
import keyboard
import os

class AutoClicker:
    def __init__(self) -> NoReturn:
        self._enable = True
        self._last_state = False
        self._base_interval = 0.022
        self._delta = 0.0015
        self._last_bump = time.time()
        threading.Thread(None, lambda: MouseHook.run(), daemon=True).start()

    def stop(self) -> NoReturn:
        key_home = keyboard.is_pressed('home')
        if key_home != self._last_state:
                self._last_state = key_home
                if self._last_state:
                    self._enable = not self._enable

    def _exit(self) -> NoReturn:
        if keyboard.is_pressed('ctrl+f1'):
            os._exit(0)
        
    def run(self) -> NoReturn:
        while True:
            now = time.time()
            self.stop()
            self._exit()
            
            if self._enable and MouseHook.isPressed:
                MouseHook.send_click()

                if now - self._last_bump >= 1.0:
                    self._last_bump = now
                    sleep(self._base_interval + self._delta)
                    continue

            sleep(self._base_interval)


AutoClicker().run()