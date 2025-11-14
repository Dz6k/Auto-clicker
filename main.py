from hook import MouseHook
import threading
from time import sleep

class AutoClicker:
    def __init__(self) -> None:
        self.hook = MouseHook()
        threading.Thread(None, lambda: self.hook.run(), daemon=True).start()