from hook import MouseHook
import threading
from time import sleep
import time
from typing import NoReturn
import keyboard
import os
from utils import Var, Config
from threading import Thread
from colorama import init, Fore, Style
import sys
import shutil


class AutoClicker:
    def __init__(self) -> NoReturn:
        self.config = Config()
        self._enable = True
        self._last_state = False
        self._last_bump = time.time()
        self._shutdown = False
        self._config_updated = False
        self._config_updated_time = 0.0
        self._last_pageup_state = False
        self.var: Var = self._load_config()
        Thread(None, lambda: MouseHook.run(), daemon=True).start()

    def _load_config(self) -> Var:
        if not os.path.exists(self.config.path):
            self.config.create()
        return self.config.load()

    def _stop(self) -> NoReturn:
        key_home = keyboard.is_pressed('home')
        if key_home != self._last_state:
            self._last_state = key_home
            if self._last_state:
                self._enable = not self._enable

    def _exit(self) -> NoReturn:
        if keyboard.is_pressed('ctrl+f1'):
            self._shutdown = True
            
    def _check_config_update(self) -> NoReturn:
        pressed = keyboard.is_pressed('page up') or keyboard.is_pressed('page_up')
        if pressed and not self._last_pageup_state:
            self._update_config()
            self._config_updated = True
            self._config_updated_time = time.time()
        self._last_pageup_state = pressed

    def _update_config(self) -> NoReturn:
        self.var = self._load_config()
        
    def run(self) -> NoReturn:
        while True:
            now = time.time()
            if self._shutdown:
                break
            if self._enable and MouseHook.isPressed:
                MouseHook.send_click()
                if now - self._last_bump >= self.var.time_bump:
                    self._last_bump = now
                    sleep(self.var.interval + (self.var.variation))
                else:
                    sleep(self.var.interval)	

            self._stop()
            self._exit()
            self._check_config_update()
            sleep(0.001)
            


def run_ui(app):
    os.system('cls')
    init(autoreset=True)
    title = 'AUTO CLICKER'
    subtitle = 'By: dz6k'
    binds = 'binds: \n\bHOME para pausar/voltar\n\bCTRL+F1 para sair\n\bPAGEUP: atualizar config'
    status_stopped = '[ - ] STOPPED'
    status_running = '[ + ] RUNNING'
    max_status_len = max(len(status_stopped), len(status_running))
    
    term_width = lambda: shutil.get_terminal_size(fallback=(80, 20)).columns
    
    def animate(text, color, delay, spacing):
        width = term_width()
        total_len = len(text) + max(len(text) - 1, 0) * spacing
        left_pad = max((width - total_len) // 2, 0)
        sys.stdout.write(' ' * left_pad)
        for ch in text:
            sys.stdout.write(color + ch)
            if spacing:
                sys.stdout.write(' ' * spacing)
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write('\n')
        
    def render_header():
        animate(title, Fore.MAGENTA, 0.04, 2)
        w = term_width()
        pad_sub = max((w - len(subtitle)) // 2, 0)
        sys.stdout.write(' ' * pad_sub + Fore.YELLOW + subtitle + Style.RESET_ALL + '\n')
        for line in binds.splitlines():
            pad_bind = max((w - len(line)) // 2, 0)
            sys.stdout.write(' ' * pad_bind + Fore.CYAN + line + Style.RESET_ALL + '\n')
            
    def show_config_updated():
        os.system('cls')
        msg = '[ ! ] CONFIG UPDATED'
        w = term_width()
        pad = max((w - len(msg)) // 2, 0)
        sys.stdout.write(' ' * pad + Fore.YELLOW + msg + Style.RESET_ALL + '\n')
        sys.stdout.flush()
        time.sleep(1.0)
        os.system('cls')
        render_header()
        
    render_header()
    last = None
    while True:
        running = app._enable
        status = status_running if running else status_stopped
        color = Fore.GREEN if running else Fore.RED
        if app._config_updated:
            show_config_updated()
            app._config_updated = False
            last = None
        if status != last:
            w = term_width()
            left_pad = max((w - max_status_len) // 2, 0)
            sys.stdout.write('\r' + ' ' * left_pad + color + status.ljust(max_status_len) + Style.RESET_ALL)
            sys.stdout.flush()
            last = status
        if app._shutdown:
            os.system('cls')
            animate('EXITING...', Fore.RED, 0.06, 2)
            os.system('cls')
            sys.exit(0)
        time.sleep(0.05)

if __name__ == '__main__':
    app = AutoClicker()
    Thread(target=app.run).start()
    run_ui(app)
