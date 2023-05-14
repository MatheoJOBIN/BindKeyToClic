import win32gui
import win32api
import win32con
from pynput import keyboard
from pywinauto import Application

def get_window_client_rect(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    rect = win32gui.GetClientRect(hwnd)
    left, top, right, bottom = rect
    # Convert client coordinates to screen coordinates
    left, top = win32gui.ClientToScreen(hwnd, (left, top))
    right, bottom = win32gui.ClientToScreen(hwnd, (right, bottom))
    return left, top, right, bottom

def click_on_border(window_title, border):
    left, top, right, bottom = get_window_client_rect(window_title)
    if border == 'top':
        x = (left + right) // 2
        y = top + 1
    elif border == 'bottom':
        x = (left + right) // 2
        y = bottom - 1
    elif border == 'left':
        x = left + 1
        y = (top + bottom) // 2
    elif border == 'right':
        x = right - 1
        y = (top + bottom) // 2
    else:
        return

    # Perform a click at the specified coordinates
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def on_press(key):
    if key == keyboard.KeyCode(char='²'):
        # Stop listener when 'Esc' key is pressed
        print('Exiting...')
        return False
    elif key == keyboard.Key.left:
        for window_title in window_titles:
            app = Application(backend="uia").connect(title_re=window_title)
            window = app.window(title_re=window_title)
            window.set_focus()
            click_on_border(window_title, 'left')
    elif key == keyboard.Key.right:
        for window_title in window_titles:
            app = Application(backend="uia").connect(title_re=window_title)
            window = app.window(title_re=window_title)
            window.set_focus()
            click_on_border(window_title, 'right')
    elif key == keyboard.Key.up:
        for window_title in window_titles:
            app = Application(backend="uia").connect(title_re=window_title)
            window = app.window(title_re=window_title)
            window.set_focus()
            click_on_border(window_title, 'top')
    elif key == keyboard.Key.down:
        for window_title in window_titles:
            app = Application(backend="uia").connect(title_re=window_title)
            window = app.window(title_re=window_title)
            window.set_focus()
            click_on_border(window_title, 'bottom')

# Specify the titles of the application windows you want to target
window_titles = ['Scoupsoin - Dofus 2.67.10.13', 'Scoupp - Dofus 2.67.10.13']

# Create a listener for keyboard inputs
listener = keyboard.Listener(on_press=on_press)
# Start the listener in a separate thread
listener.start()

# Keep the main thread running
listener.join()
