from time import sleep
import win32gui
import win32api
import win32con

def mouse_click_left(hwnd, x, y, hold_time=0):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    x = int(left + x if x > 0 else right + x)
    y = int(top + y if y > 0 else bottom + y)
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    sleep(hold_time)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def mouse_click_right(hwnd, x, y):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    x = int(left + x if x > 0 else right + x)
    y = int(top + y if y > 0 else bottom + y)
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)