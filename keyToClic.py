# -*- coding: utf-8 -*-
import win32gui
import pywinauto
import tkinter as tk
import pyautogui
from pynput import keyboard

def get_dofus_window():
    global window_connections

    window_titles = []
    def callback(hwnd, window_titles):
        if win32gui.GetWindowText(hwnd).find('Dofus') >= 0:
            window_titles.append(win32gui.GetWindowText(hwnd))
        return True
    win32gui.EnumWindows(callback, window_titles)

    # Connect to the applications and store the window connections
    window_connections = {}
    for window_title in window_titles:
        app = pywinauto.Application(backend="uia").connect(title_re=window_title)
        window_connections[window_title] = app.window(title_re=window_title)

    execute_script()

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

def checkCoordinates(text):
    # Allow empty input
    if not text:
        return True

    try:
        if(int(text) < -100 or int(text) > 100):
            print("Invalid input, please enter a number between -100 and 100")
            return False
        else:
            return True
    except ValueError:
        if text == '-' or (text.startswith("-") and text[1:].isdigit()):
            return True
        return False


def travel():
    # Create the GUI window
    window = tk.Tk()
    window.title("Travel to")
    window.geometry("600x300")

    # Create label and entry widgets for x and y coordinates
    x_label = tk.Label(window, text="X coordinate (-100 to 100)")
    x_label.pack()
    x_entry = tk.Entry(window, validate="key")
    x_entry.config(validatecommand=(window.register(checkCoordinates), '%P'))
    x_entry.pack()

    y_label = tk.Label(window, text="Y coordinate (-100 to 100)")
    y_label.pack()
    y_entry = tk.Entry(window, validate="key")
    y_entry.config(validatecommand=(window.register(checkCoordinates), '%P'))
    y_entry.pack()

    def submitCoordinates():
        global command
        x = int(x_entry.get())
        y = int(y_entry.get())
        command = "/travel " + str(x) + " " + str(y)

        # Close the window
        window.destroy()

        # Use the obtained coordinates as needed
        # For example, print the values
        print(f"X: {x}, Y: {y}, command: {command}")

    # Submit Button
    submit_button = tk.Button(window, text="Submit", command=submitCoordinates)
    submit_button.pack()

    # Quit Button
    quit_button = tk.Button(window, text="Quit", command=window.quit())
    quit_button.pack()

    # Start the GUI event loop
    window.mainloop()

def showHideInterfaces():
    # Simulate Alt key press
    pyautogui.keyDown('alt')

    # Simulate ² key press
    pyautogui.press('asciicircum')

    # Simulate Alt key release
    pyautogui.keyUp('alt')

def on_press(key):
    try:
        if key == keyboard.KeyCode(char='\x11') or key == keyboard.Key.esc:
            # Stop listener when 'Esc' key is pressed
            print('Exiting...')
            return False
        elif key == keyboard.Key.left:
            print('Left key pressed')
            for window_title, window_connection in window_connections.items():
                window_connection.set_focus()
                click_on_border(window_title, 'left')
                print('Left clic performed for ' + window_title.split(' - ')[0])
        elif key == keyboard.Key.right:
            print('Right key pressed')
            for window_title, window_connection in window_connections.items():
                window_connection.set_focus()
                click_on_border(window_title, 'right')
                print('Right clic performed for ' + window_title.split(' - ')[0])
        elif key == keyboard.Key.up:
            print('Up key pressed')
            for window_title, window_connection in window_connections.items():
                window_connection.set_focus()
                click_on_border(window_title, 'top')
                print('Top clic performed for ' + window_title.split(' - ')[0])
        elif key == keyboard.Key.down:
            print('Down key pressed')
            for window_title, window_connection in window_connections.items():
                window_connection.set_focus()
                pyautogui.press('F10')
                click_on_border(window_title, 'bottom')
                pyautogui.press('F10')
                print('Bottom clic performed for ' + window_title.split(' - ')[0])
        elif key == keyboard.KeyCode(char=','):
            print('Travel interface launched')
            travel()
            for window_title, window_connection in window_connections.items():
                window_connection.set_focus()
                pyautogui.press('space')
                pyautogui.typewrite(command)
                pyautogui.press('enter')
                pyautogui.press('enter')
                print('Travel command sent to ' + window_title.split(' - ')[0])
            print('Travel command sent to all accounts')
        else:
            print('Key pressed: ' + str(key))
            return
    except AttributeError:
        print(AttributeError)

def execute_script():
    # Create a listener for keyboard inputs
    listener = keyboard.Listener(on_press=on_press)
    # Start the listener in a separate thread
    listener.start()

    # Keep the main thread running
    listener.join()

get_dofus_window()