import ctypes
import os
import threading
import time
from ctypes import wintypes
from dataclasses import dataclass
from typing import NoReturn

@dataclass(frozen=True)
class Constants:
    WH_MOUSE_LL = 14
    WM_LBUTTONDOWN = 0x0201
    WM_LBUTTONUP = 0x0202
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004

class MouseHook:
    isPressed: bool = False

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    LowLevelMouseProc = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)

    user32.SetWindowsHookExW.argtypes = [ctypes.c_int, LowLevelMouseProc, wintypes.HINSTANCE, wintypes.DWORD]
    user32.SetWindowsHookExW.restype = ctypes.c_void_p
    user32.CallNextHookEx.argtypes = [ctypes.c_void_p, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM]
    user32.CallNextHookEx.restype = ctypes.c_int
    user32.UnhookWindowsHookEx.argtypes = [ctypes.c_void_p]
    user32.UnhookWindowsHookEx.restype = wintypes.BOOL
    user32.GetMessageW.argtypes = [ctypes.POINTER(wintypes.MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT]
    user32.GetMessageW.restype = wintypes.BOOL
    user32.TranslateMessage.argtypes = [ctypes.POINTER(wintypes.MSG)]
    user32.DispatchMessageW.argtypes = [ctypes.POINTER(wintypes.MSG)]

    @staticmethod
    @LowLevelMouseProc
    def hook_proc(nCode, wParam, lParam) -> ctypes.c_int:
        if nCode == 0:
            match (wParam):
                case Constants.WM_LBUTTONDOWN:
                    MouseHook.isPressed = True

                case Constants.WM_LBUTTONUP:
                    MouseHook.isPressed = False

        return MouseHook.user32.CallNextHookEx(None, nCode, wParam, lParam)

    @staticmethod
    def run() -> NoReturn:
        hook_id = MouseHook.user32.SetWindowsHookExW(Constants.WH_MOUSE_LL, MouseHook.hook_proc, 0, 0)
        msg = wintypes.MSG()

        if os.getenv("TEST_HOOK") == "1":
            def _click():
                time.sleep(0.1)
                MouseHook.user32.mouse_event(Constants.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                MouseHook.user32.mouse_event(Constants.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            threading.Thread(target=_click, daemon=True).start()

        while MouseHook.user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            MouseHook.user32.TranslateMessage(ctypes.byref(msg))
            MouseHook.user32.DispatchMessageW(ctypes.byref(msg))
        MouseHook.user32.UnhookWindowsHookEx(hook_id)
