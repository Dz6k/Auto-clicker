import ctypes
import os
import threading
import time
from ctypes import wintypes
from dataclasses import dataclass

@dataclass(frozen=True)
class Constants:
    WH_MOUSE_LL = 14
    WM_LBUTTONDOWN = 0x0201
    WM_LBUTTONUP = 0x0202
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
