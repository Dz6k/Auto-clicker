from hook import MouseHook
import threading
from time import sleep
import time
from typing import NoReturn
import keyboard
import os
from utils import Var, Config
from threading import Thread

class AutoClicker:
    def __init__(self) -> NoReturn:
        self._wellcome()
        self.config = Config()
        self._enable = True
        self._last_state = False
        self._last_bump = time.time()
        self._load_config()
        threading.Thread(None, lambda: MouseHook.run(), daemon=True).start()
        
    def _load_config(self) -> NoReturn:
        if not os.path.exists(self.config.path):
            self.config.create()
        self.config.load()
        
    def _stop(self) -> NoReturn:
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
            self._stop()
            self._exit()
            
            if self._enable and MouseHook.isPressed:
                MouseHook.send_click()

                if now - self._last_bump >= Var.time_bump:
                    self._last_bump = now
                    sleep(Var.interval + (Var.variation))
                    continue

            sleep(Var.interval)

if __name__ == '__main__':

    app = AutoClicker()
    Thread(target=app.run()).start()	
