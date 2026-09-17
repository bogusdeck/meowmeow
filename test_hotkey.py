from pynput import keyboard
import time

def on_t():
    print("T pressed")

def on_h():
    print("H pressed")

with keyboard.GlobalHotKeys({
    '<cmd>+<shift>+t': on_t,
    '<cmd>+<shift>+h': on_h
}) as h:
    print("Listening... press Cmd+Shift+H or Cmd+Shift+T. Will exit after 3 seconds.")
    time.sleep(3)
