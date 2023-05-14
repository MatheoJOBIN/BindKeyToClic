# -*- coding: utf-8 -*-
import win32gui
import win32con
import pywinauto
import tkinter as tk
import pyautogui
from pynput import keyboard

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
    pyautogui.click(x, y)

def on_press(key):
    global window_connections
    if key == keyboard.KeyCode(char='²'):
        # Stop listener when 'Esc' key is pressed
        print('Exiting...')
        return False
    elif key == keyboard.Key.left:
        print('Left key pressed')
        for window_title, window_connection in window_connections.items():
            window_connection.set_focus()
            click_on_border(window_title, 'left')
            print('Left click performed')
    elif key == keyboard.Key.right:
        for window_title, window_connection in window_connections.items():
            window_connection.set_focus()
            click_on_border(window_title, 'right')
    elif key == keyboard.Key.up:
        for window_title, window_connection in window_connections.items():
            window_connection.set_focus()
            click_on_border(window_title, 'top')
    elif key == keyboard.Key.down:
        for window_title, window_connection in window_connections.items():
            window_connection.set_focus()
            click_on_border(window_title, 'bottom')
    else:
        print('Key pressed: ' + str(key))

def execute_script():
    # Create a listener for keyboard inputs
    listener = keyboard.Listener(on_press=on_press)
    # Start the listener in a separate thread
    listener.start()

    # Keep the main thread running
    listener.join()

def submit_parameters():
    global window_connections
    titles = entry_window_titles.get().split(',')
    window_titles = [title.strip() for title in titles]

    window.destroy()

    # Connect to the applications and store the window connections
    window_connections = {}
    for window_title in window_titles:
        app = pywinauto.Application(backend="uia").connect(title_re=window_title)
        window_connections[window_title] = app.window(title_re=window_title)

    execute_script()

# Create the GUI window
window = tk.Tk()
window.title("Parameter Input")
window.geometry("300x150")

# Window Titles Label and Entry
label_window_titles = tk.Label(window, text="Window Titles (comma-separated):")
label_window_titles.pack()
entry_window_titles = tk.Entry(window)
entry_window_titles.pack()

# Submit Button
submit_button = tk.Button(window, text="Submit", command=submit_parameters)
submit_button.pack()

# Quit Button
quit_button = tk.Button(window, text="Quit", command=window.quit)
quit_button.pack()

# Start the GUI event loop
window.mainloop()