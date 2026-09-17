import objc
from AppKit import NSApplication, NSWindow, NSMakeRect, NSColor
from PyObjCTools import AppHelper
from pynput import keyboard

class AppDelegate(objc.lookUpClass("NSObject")):
    def applicationDidFinishLaunching_(self, notification):
        self.win = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(NSMakeRect(100,100,200,200), 15, 2, False)
        self.win.setBackgroundColor_(NSColor.redColor())
        self.win.makeKeyAndOrderFront_(None)
        
        self.listener = keyboard.GlobalHotKeys({
            '<cmd>+<shift>+h': self.on_h
        })
        self.listener.start()
        print("Ready. Press Cmd+Shift+H")

    def on_h(self):
        print("Hotkey pressed!")

app = NSApplication.sharedApplication()
delegate = AppDelegate.alloc().init()
app.setDelegate_(delegate)
AppHelper.runEventLoop()
