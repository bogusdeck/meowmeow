from pynput import keyboard

class HotkeyManager:
    def __init__(
        self,
        on_translate,
        on_move_left=None,
        on_move_right=None,
        on_move_up=None,
        on_move_down=None,
        on_reduce_size=None,
        on_expand_size=None
    ):
        self.on_translate = on_translate
        self.on_move_left = on_move_left
        self.on_move_right = on_move_right
        self.on_move_up = on_move_up
        self.on_move_down = on_move_down
        self.on_reduce_size = on_reduce_size
        self.on_expand_size = on_expand_size
        self.listener = None

    def start(self):
        hotkeys = {
            '<cmd>+<ctrl>+p': self.on_activate,
        }

        if self.on_move_left:
            hotkeys['<cmd>+<ctrl>+<left>'] = self.on_move_left
            hotkeys['<cmd>+<ctrl>+<home>'] = self.on_move_left
        if self.on_move_right:
            hotkeys['<cmd>+<ctrl>+<right>'] = self.on_move_right
            hotkeys['<cmd>+<ctrl>+<end>'] = self.on_move_right
        if self.on_move_up:
            hotkeys['<cmd>+<ctrl>+<up>'] = self.on_move_up
            hotkeys['<cmd>+<ctrl>+<page_up>'] = self.on_move_up
        if self.on_move_down:
            hotkeys['<cmd>+<ctrl>+<down>'] = self.on_move_down
            hotkeys['<cmd>+<ctrl>+<page_down>'] = self.on_move_down
        if self.on_reduce_size:
            hotkeys['<cmd>+<ctrl>+-'] = self.on_reduce_size
            hotkeys['<cmd>+<ctrl>+m'] = self.on_reduce_size
        if self.on_expand_size:
            hotkeys['<cmd>+<ctrl>+='] = self.on_expand_size

        try:
            self.listener = keyboard.GlobalHotKeys(hotkeys)
            self.listener.start()
            print("Hotkeys registered successfully:")
            print(" - Cmd+Ctrl+P (or Cmd+Ctrl+Fn+P): Translate clipboard")
            print(" - Cmd+Ctrl+Arrow (or Cmd+Ctrl+Fn+Arrow): Move window directionally")
            print(" - Cmd+Ctrl+- (or Cmd+Ctrl+Fn+-): Minimize / Reduce overlay size")
            print(" - Cmd+Ctrl+= (or Cmd+Ctrl+Fn++): Maximize / Expand overlay size")
            print(" - Cmd+Ctrl+Arrow (or Cmd+Ctrl+Fn+Arrow): Move window directionally")
            print(" - Cmd+Ctrl+M (or Cmd+Ctrl+Fn+M): Reduce overlay size")
        except Exception as e:
            print("Failed to register hotkeys. You might need to grant Accessibility permissions.")
            print("Go to System Settings > Privacy & Security > Accessibility and add your terminal/app.")
            print(f"Error details: {e}")

    def on_activate(self):
        self.on_translate()

    def stop(self):
        if self.listener:
            self.listener.stop()
