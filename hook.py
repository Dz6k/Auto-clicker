import ctypes
import os
import threading
import time
from ctypes import wintypes
from dataclasses import dataclass
from typing import NoReturn


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_void_p),
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("mi", MOUSEINPUT),
    ]

class POINT(ctypes.Structure):
    _fields_ = [
        ("x", wintypes.LONG),
        ("y", wintypes.LONG),
    ]

class MSLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("pt", POINT),
        ("mouseData", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_void_p),
    ]

@dataclass(frozen=True)
class Mouse:
    INPUT_MOUSE = 0
    WH_MOUSE_LL = 14
    WM_LBUTTONDOWN = 0x0201
    WM_LBUTTONUP = 0x0202
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    MOUSEEVENTF_RIGHTDOWN = 0x0008
    MOUSEEVENTF_RIGHTUP = 0x0010
    LLMHF_INJECTED = 0x00000001
    LLMHF_LOWER_IL_INJECTED = 0x00000002


class MouseHook:
    isPressed: bool = False
    _timer_id: int = 0

    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    LowLevelMouseProc = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
    TIMERPROC = ctypes.WINFUNCTYPE(None, wintypes.HWND, wintypes.UINT, ctypes.c_size_t, wintypes.DWORD)


    user32.SendInput.argtypes = [wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int]
    user32.SendInput.restype = wintypes.UINT
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
            msll = ctypes.cast(lParam, ctypes.POINTER(MSLLHOOKSTRUCT)).contents
            injected = (msll.flags & (Mouse.LLMHF_INJECTED | Mouse.LLMHF_LOWER_IL_INJECTED)) != 0
            if not injected:
                if wParam == Mouse.WM_LBUTTONDOWN:
                    MouseHook.isPressed = True
                elif wParam == Mouse.WM_LBUTTONUP:
                    MouseHook.isPressed = False

        return MouseHook.user32.CallNextHookEx(None, nCode, wParam, lParam)

    @staticmethod
    def run() -> NoReturn:
        hook_id = MouseHook.user32.SetWindowsHookExW(Mouse.WH_MOUSE_LL, MouseHook.hook_proc, 0, 0)
        msg = wintypes.MSG()
         
        while MouseHook.user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            MouseHook.user32.TranslateMessage(ctypes.byref(msg))
            MouseHook.user32.DispatchMessageW(ctypes.byref(msg))
        MouseHook.user32.UnhookWindowsHookEx(hook_id)

    @staticmethod
    def send_click():
        inp_down = INPUT(type=Mouse.INPUT_MOUSE, mi=MOUSEINPUT(0,0,0,Mouse.MOUSEEVENTF_LEFTDOWN,0,None))
        MouseHook.user32.SendInput(1, ctypes.byref(inp_down), ctypes.sizeof(INPUT))
        time.sleep(0.057)
        inp_up = INPUT(type=Mouse.INPUT_MOUSE, mi=MOUSEINPUT(0,0,0,Mouse.MOUSEEVENTF_LEFTUP,0,None))
        MouseHook.user32.SendInput(1, ctypes.byref(inp_up), ctypes.sizeof(INPUT))

 