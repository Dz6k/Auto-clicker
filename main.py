from hook import MouseHook
import threading
from time import sleep
import time
from typing import NoReturn
import keyboard
import os
import json


class AutoClicker:
    def __init__(self) -> NoReturn:
        self._enable = True
        self._last_state = False
        self._base_interval = 0.022
        self._delta = 0.0015
        self._last_bump = time.time()
        threading.Thread(None, lambda: MouseHook.run(), daemon=True).start()

    def _load_config(self) -> NoReturn:
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
        
        if not os.path.exists(config_path):
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
            
        
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