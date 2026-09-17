import objc
from AppKit import NSApplication, NSWindow, NSTextView, NSColor, NSAttributedString, NSMakeRect
app = NSApplication.sharedApplication()
win = NSWindow.alloc().initWithContentRect_styleMask_backing_defer_(NSMakeRect(0,0,200,200), 15, 2, False)
tv = NSTextView.alloc().initWithFrame_(NSMakeRect(0,0,200,200))
tv.setTextColor_(NSColor.whiteColor())
tv.setBackgroundColor_(NSColor.blackColor())
attr_str, _ = NSAttributedString.alloc().initWithMarkdownString_options_baseURL_error_('# Hello\n**Bold** and *Italic*', None, None, None)
tv.textStorage().setAttributedString_(attr_str)
print("String loaded.")
