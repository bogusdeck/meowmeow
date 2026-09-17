import sys
import threading
import pyperclip
import objc
import logging
import time
from AppKit import (
    NSApplication, NSObject, NSApp,
    NSApplicationActivationPolicyAccessory
)
from PyObjCTools import AppHelper
from overlay import OverlayWindow
from hotkey import HotkeyManager
import translator

# Set up logging early for main.py
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("log.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("MainApp")

class AppDelegate(NSObject):
    def init(self):
        self = objc.super(AppDelegate, self).init()
        if self is not None:
            self.history = []
            self.current_history_index = -1
            self.last_toggle_time = 0
            self.toggle_cooldown = 0.3
            self.current_prompt = None
            self.active_request_id = 0
            self.request_lock = threading.Lock()
        return self
    
    def setup_menu(self):
        from AppKit import NSMenu, NSMenuItem, NSEventModifierFlagControl, NSApp
        main_menu = NSMenu.alloc().init()
        NSApp.setMainMenu_(main_menu)
        
        edit_menu_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Edit", None, "")
        edit_menu = NSMenu.alloc().initWithTitle_("Edit")
        
        # Standard Mac shortcuts (Cmd + C, V, X, A)
        edit_menu.addItemWithTitle_action_keyEquivalent_("Cut", "cut:", "x")
        edit_menu.addItemWithTitle_action_keyEquivalent_("Copy", "copy:", "c")
        edit_menu.addItemWithTitle_action_keyEquivalent_("Paste", "paste:", "v")
        edit_menu.addItemWithTitle_action_keyEquivalent_("Select All", "selectAll:", "a")
        
        # Explicitly support Ctrl+P for paste as requested
        ctrl_p = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Paste Ctrl P", "paste:", "p")
        ctrl_p.setKeyEquivalentModifierMask_(NSEventModifierFlagControl)
        edit_menu.addItem_(ctrl_p)
        
        edit_menu_item.setSubmenu_(edit_menu)
        main_menu.addItem_(edit_menu_item)

    def setup(self):
        self.history = []
        self.current_history_index = -1
        self.setup_menu()
        self.window = OverlayWindow.create()
        self.window.app_delegate = self
        self.window.showText_("")
        self.hotkey_manager = HotkeyManager(
            on_translate=self.on_hotkey,
            on_move_left=self.on_move_left,
            on_move_right=self.on_move_right,
            on_move_up=self.on_move_up,
            on_move_down=self.on_move_down,
            on_reduce_size=self.on_reduce_size,
            on_expand_size=self.on_expand_size,
            on_toggle_overlay=self.on_toggle_overlay,
            on_instant_agy=self.on_instant_agy,
            on_next_card=self.on_next_card,
            on_prev_card=self.on_prev_card
        )
        self.hotkey_manager.start()
        print("QuickTranslate running.")
        print(" - Cmd+Ctrl+P (or Cmd+Ctrl+Fn+P): Translate clipboard")
        print(" - Cmd+Ctrl+> / Cmd+Ctrl+<: Next / Previous response card")
        print(" - Cmd+Ctrl+I (or Cmd+Ctrl+Fn+I): Accelerate with Antigravity (agy)")
        print(" - Cmd+Ctrl+H (or Cmd+Ctrl+Fn+H): Toggle hide/show overlay")
        print(" - Cmd+Ctrl+Arrow (or Cmd+Ctrl+Fn+Arrow): Move window")
        print(" - Cmd+Ctrl+- (or Cmd+Ctrl+Fn+-): Reduce overlay size")
        print(" - Cmd+Ctrl+= (or Cmd+Ctrl+Fn++): Maximize/Expand overlay size")
        print(" - Press Ctrl+C in terminal to stop.")
        sys.stdout.flush()

    current_prompt = None
    active_request_id = 0
    request_lock = threading.Lock()
    
    history = []
    current_history_index = -1

    def updateCardDisplay(self):
        if not self.history:
            return
        total = len(self.history)
        idx = max(0, min(total - 1, self.current_history_index))
        self.current_history_index = idx
        res = self.history[idx]
        badge = f"[{idx + 1}/{total}]"
        self.window.showText_withCounter_(res, badge)

    def on_next_card(self):
        self.performSelectorOnMainThread_withObject_waitUntilDone_(
            objc.selector(self.handleNextCard, signature=b'v@:'), None, False
        )

    def handleNextCard(self):
        if self.history and self.current_history_index < len(self.history) - 1:
            self.current_history_index += 1
            self.updateCardDisplay()

    def on_prev_card(self):
        self.performSelectorOnMainThread_withObject_waitUntilDone_(
            objc.selector(self.handlePrevCard, signature=b'v@:'), None, False
        )

    def handlePrevCard(self):
        if self.history and self.current_history_index > 0:
            self.current_history_index -= 1
            self.updateCardDisplay()

    def updateUIWithResult_(self, result):
        if result and not result.startswith("OCR failed") and not result.startswith("Screenshot failed") and not result.startswith("Clipboard is empty"):
            self.history.append(result)
            self.current_history_index = len(self.history) - 1
            self.updateCardDisplay()
        else:
            self.window.showText_(result)

    def start_request(self, prompt_text):
        with self.request_lock:
            self.active_request_id += 1
            req_id = self.active_request_id
            self.current_prompt = prompt_text
            
        self.window.showText_("Translating...")
        
        def fetch_primary():
            result = translator.translate_text(prompt_text, is_raw_prompt=True)
            with self.request_lock:
                if self.active_request_id == req_id:
                    self.performSelectorOnMainThread_withObject_waitUntilDone_(
                        objc.selector(self.updateUIWithResult_, signature=b'v@:@'), result, False
                    )
                    self.current_prompt = None

        threading.Thread(target=fetch_primary, daemon=True).start()

    def on_instant_agy(self):
        self.performSelectorOnMainThread_withObject_waitUntilDone_(
            objc.selector(self.handleInstantAgy, signature=b'v@:'), None, False
        )

    def handleInstantAgy(self):
        with self.request_lock:
            prompt = self.current_prompt
            req_id = self.active_request_id
            
        if not prompt:
            self.window.showText_("No active request to accelerate.")
            return

        self.window.showText_("⚡ Accelerating with Antigravity (agy)...")
        
        def fetch_fast():
            try:
                result = translator.translate_with_antigravity(prompt)
                with self.request_lock:
                    if self.active_request_id == req_id:
                        self.performSelectorOnMainThread_withObject_waitUntilDone_(
                            objc.selector(self.updateUIWithResult_, signature=b'v@:@'), result, False
                        )
                        self.current_prompt = None
            except Exception as e:
                logger.error(f"Instant Antigravity acceleration error: {e}")

        threading.Thread(target=fetch_fast, daemon=True).start()

    def handleScreenshot(self):
        import subprocess, tempfile, os
        self.window.showText_("Taking screenshot...")
        
        def capture_and_answer():
            fd, path = tempfile.mkstemp(suffix=".png")
            os.close(fd)
            subprocess.run(["screencapture", "-x", path])
            
            if os.path.exists(path) and os.path.getsize(path) > 0:
                self.performSelectorOnMainThread_withObject_waitUntilDone_(
                    objc.selector(self.updateUIWithStatus_, signature=b'v@:@'), "Running OCR...", False
                )
                extracted_text = self.window.performOCR_(path)
                
                if extracted_text and extracted_text.strip() and not extracted_text.startswith("OCR error") and not extracted_text.startswith("Failed"):
                    question = f"Answer this question based on the screenshot text:\n\n{extracted_text}"
                    self.start_request(question)
                else:
                    self.performSelectorOnMainThread_withObject_waitUntilDone_(
                        objc.selector(self.updateUIWithResult_, signature=b'v@:@'), f"OCR failed: {extracted_text}", False
                    )
            else:
                self.performSelectorOnMainThread_withObject_waitUntilDone_(
                    objc.selector(self.updateUIWithResult_, signature=b'v@:@'), "Screenshot failed.", False
                )
            try:
                os.remove(path)
            except OSError:
                pass

        threading.Thread(target=capture_and_answer, daemon=True).start()

    def updateUIWithStatus_(self, status):
        self.window.showText_(status)
        
    def handleTranslation(self):
        text = pyperclip.paste()
        if not text or not text.strip():
            self.window.showText_("Clipboard is empty")
            return
        prompt = translator.TRANSLATE_TEXT_PROMPT.format(text=text.strip())
        self.start_request(prompt)

    def handleManualTranslation_(self, text):
        if not text or not text.strip():
            return
        prompt = translator.TRANSLATE_TEXT_PROMPT.format(text=text.strip())
        self.start_request(prompt)

    def updateUIWithResult_(self, result):
        self.window.showText_(result)

    def on_hotkey(self):
        self.performSelectorOnMainThread_withObject_waitUntilDone_(
            objc.selector(self.handleTranslation, signature=b'v@:'), None, False
        )

    def on_toggle_overlay(self):
        now = time.time()
        if now - self.last_toggle_time < self.toggle_cooldown:
            return
        self.last_toggle_time = now
        self.performSelectorOnMainThread_withObject_waitUntilDone_(
            objc.selector(self.handleToggleOverlay, signature=b'v@:'), None, False
        )

    def handleToggleOverlay(self):
        self.window.toggle_overlay()

    def toggle_overlay(self):
        self.handleToggleOverlay()

    def on_move_left(self):
        self.performSelectorOnMainThread_withObject_waitUntilDone_(
            objc.selector(self.handleMoveLeft, signature=b'v@:'), None, False
        )

    def handleMoveLeft(self):
        self.window.moveWindow_("left")

    def on_move_right(self):
        self.performSelectorOnMainThread_withObject_waitUntilDone_(
            objc.selector(self.handleMoveRight, signature=b'v@:'), None, False
        )

    def handleMoveRight(self):
        self.window.moveWindow_("right")

    def on_move_up(self):
        self.performSelectorOnMainThread_withObject_waitUntilDone_(
            objc.selector(self.handleMoveUp, signature=b'v@:'), None, False
        )

    def handleMoveUp(self):
        self.window.moveWindow_("up")

    def on_move_down(self):
        self.performSelectorOnMainThread_withObject_waitUntilDone_(
            objc.selector(self.handleMoveDown, signature=b'v@:'), None, False
        )

    def handleMoveDown(self):
        self.window.moveWindow_("down")

    def on_reduce_size(self):
        self.performSelectorOnMainThread_withObject_waitUntilDone_(
            objc.selector(self.handleReduceSize, signature=b'v@:'), None, False
        )

    def handleReduceSize(self):
        self.window.reduceSize()

    def on_expand_size(self):
        self.performSelectorOnMainThread_withObject_waitUntilDone_(
            objc.selector(self.handleExpandSize, signature=b'v@:'), None, False
        )

    def handleExpandSize(self):
        self.window.expandSize()

    def on_reduce_size(self):
        self.performSelectorOnMainThread_withObject_waitUntilDone_(
            objc.selector(self.handleReduceSize, signature=b'v@:'), None, False
        )

    def handleReduceSize(self):
        self.window.reduceSize()

    def applicationDidFinishLaunching_(self, notification):
        # Fallback if it does fire
        pass

    def handleScreenshot(self):
        import subprocess, tempfile, os
        self.window.showText_("Taking screenshot...")
        
        def capture_and_answer():
            fd, path = tempfile.mkstemp(suffix=".png")
            os.close(fd)
            
            # Take full screen screenshot (non-interactive)
            subprocess.run(["screencapture", "-x", path])
            
            if os.path.exists(path) and os.path.getsize(path) > 0:
                self.performSelectorOnMainThread_withObject_waitUntilDone_(
                    objc.selector(self.updateUIWithStatus_, signature=b'v@:@'), "Running OCR...", False
                )
                
                # Perform OCR using Vision framework
                extracted_text = self.window.performOCR_(path)
                
                if extracted_text and extracted_text.strip() and not extracted_text.startswith("OCR error") and not extracted_text.startswith("Failed"):
                    self.performSelectorOnMainThread_withObject_waitUntilDone_(
                        objc.selector(self.updateUIWithStatus_, signature=b'v@:@'), "Asking agy...", False
                    )
                    
                    # Ask agy for answer
                    question = f"Answer this question based on the screenshot text:\n\n{extracted_text}"
                    answer = self.window.askAgy_(question)
                    
                    self.performSelectorOnMainThread_withObject_waitUntilDone_(
                        objc.selector(self.updateUIWithResult_, signature=b'v@:@'), answer, False
                    )
                else:
                    self.performSelectorOnMainThread_withObject_waitUntilDone_(
                        objc.selector(self.updateUIWithResult_, signature=b'v@:@'), f"OCR failed: {extracted_text}", False
                    )
            else:
                self.performSelectorOnMainThread_withObject_waitUntilDone_(
                    objc.selector(self.updateUIWithResult_, signature=b'v@:@'), "Screenshot failed.", False
                )
            
            try:
                os.remove(path)
            except OSError:
                pass

        threading.Thread(target=capture_and_answer, daemon=True).start()

    def updateUIWithStatus_(self, status):
        self.window.showText_(status)
        
    def handleTranslation(self):
        text = pyperclip.paste()
        if not text or not text.strip():
            self.window.showText_("Clipboard is empty")
            return
            
        self.window.showText_("Translating...")
        
        def fetch_translation():
            result = translator.translate_text(text.strip())
            self.performSelectorOnMainThread_withObject_waitUntilDone_(
                objc.selector(self.updateUIWithResult_, signature=b'v@:@'), result, False
            )
            
        threading.Thread(target=fetch_translation, daemon=True).start()

    def handleManualTranslation_(self, text):
        if not text or not text.strip():
            return
            
        self.window.showText_("Translating...")
        
        def fetch_translation():
            result = translator.translate_text(text.strip())
            self.performSelectorOnMainThread_withObject_waitUntilDone_(
                objc.selector(self.updateUIWithResult_, signature=b'v@:@'), result, False
            )
            
        threading.Thread(target=fetch_translation, daemon=True).start()

    def updateUIWithResult_(self, result):
        self.window.showText_(result)

# Global list to keep a strong reference to our delegate
# so it isn't garbage collected by Python.
_retained_objects = []

def main():
    print("Starting QuickTranslate...")
    sys.stdout.flush()
    
    app = NSApplication.sharedApplication()
    app.setActivationPolicy_(NSApplicationActivationPolicyAccessory)
    
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    
    # Retain the delegate
    _retained_objects.append(delegate)
    
    # Explicitly start listening and setup
    delegate.setup()
    
    # Catch Ctrl+C in terminal
    AppHelper.installMachInterrupt()
    AppHelper.runEventLoop()

if __name__ == "__main__":
    main()