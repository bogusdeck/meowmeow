from pynput import keyboard

class HotkeyManager:
    def __init__(self, on_translate):
        self.on_translate = on_translate
        self.listener = None

    def start(self):
        try:
            self.listener = keyboard.GlobalHotKeys({
                '<cmd>+<shift>+t': self.on_activate,
            })
            self.listener.start()
            print("Hotkeys registered: Cmd+Shift+T (translate)")
        except Exception as e:
            print("Failed to register hotkey. You might need to grant Accessibility permissions.")
            print("Go to System Settings > Privacy & Security > Accessibility and add your terminal/app.")
            print(f"Error details: {e}")

    def on_activate(self):
        self.on_translate()
        
    def stop(self):
        if self.listener:
            self.listener.stop()
