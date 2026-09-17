import objc
import subprocess
import tempfile
import os
import threading
import translator
from AppKit import (
    NSWindow, NSWindowStyleMaskTitled, NSWindowStyleMaskFullSizeContentView, 
    NSWindowStyleMaskResizable, NSWindowStyleMaskClosable, NSBackingStoreBuffered,
    NSColor, NSFloatingWindowLevel, NSWindowSharingNone,
    NSTextField, NSTextAlignmentLeft, NSFont, NSMakeRect,
    NSApplication, NSWindowCollectionBehaviorCanJoinAllSpaces,
    NSVisualEffectView, NSVisualEffectMaterialHUDWindow, NSVisualEffectBlendingModeBehindWindow,
    NSButton, NSImage, NSImageSymbolConfiguration,
    NSScrollView, NSTextView,
    NSViewWidthSizable, NSViewHeightSizable, NSViewMinYMargin, NSViewMinXMargin, NSViewMaxYMargin,
    NSBitmapImageRep, NSPNGFileType,
    NSCursor
)
from Foundation import NSObject, NSURL, NSData
from Vision import VNRecognizeTextRequest, VNImageRequestHandler
from Quartz import (
    CGImageSourceCreateWithData, CGImageSourceCreateImageAtIndex, kCGImageSourceShouldCache
)

class ArrowCursorTextField(NSTextField):
    def resetCursorRects(self):
        self.discardCursorRects()
        self.addCursorRect_cursor_(self.bounds(), NSCursor.arrowCursor())

    def fieldEditor_forObject_(self, control, object):
        # Return our custom text view as field editor
        if not hasattr(self, '_custom_field_editor'):
            self._custom_field_editor = ArrowCursorTextView.alloc().initWithFrame_(NSMakeRect(0, 0, 0, 0))
            self._custom_field_editor.setFieldEditor_(True)
        return self._custom_field_editor

class ArrowCursorTextView(NSTextView):
    def resetCursorRects(self):
        self.discardCursorRects()
        self.addCursorRect_cursor_(self.bounds(), NSCursor.arrowCursor())

class OverlayWindow(NSWindow):
    def canBecomeKeyWindow(self):
        return True
        
    def canBecomeMainWindow(self):
        return True
    
    def resetCursorRects(self):
        self.discardCursorRects()
        self.addCursorRect_cursor_(self.bounds(), NSCursor.arrowCursor())

    def fieldEditor_forObject_(self, client, object):
        # Override to use our custom field editor with arrow cursor
        if hasattr(self, 'input_field') and client == self.input_field:
            if not hasattr(self, '_custom_field_editor'):
                self._custom_field_editor = ArrowCursorTextView.alloc().initWithFrame_(NSMakeRect(0, 0, 0, 0))
                self._custom_field_editor.setFieldEditor_(True)
                self._custom_field_editor.setEditable_(True)
                self._custom_field_editor.setSelectable_(True)
            return self._custom_field_editor
        return None

    @classmethod
    def create(cls):
        rect = NSMakeRect(0, 0, 450, 60) 
        
        mask = NSWindowStyleMaskTitled | NSWindowStyleMaskFullSizeContentView | NSWindowStyleMaskResizable | NSWindowStyleMaskClosable
        
        window = cls.alloc().initWithContentRect_styleMask_backing_defer_(
            rect, mask, NSBackingStoreBuffered, False
        )
        if window:
            window.app_delegate = None
            window._hidden = False
            
            window.setTitlebarAppearsTransparent_(True)
            window.setTitleVisibility_(1) 
            window.standardWindowButton_(0).setHidden_(True)
            window.standardWindowButton_(1).setHidden_(True)
            window.standardWindowButton_(2).setHidden_(True)
            
            window.setOpaque_(False)
            window.setBackgroundColor_(NSColor.clearColor())
            window.setLevel_(NSFloatingWindowLevel)
            window.setSharingType_(NSWindowSharingNone)
            window.setCollectionBehavior_(NSWindowCollectionBehaviorCanJoinAllSpaces)
            window.setMovableByWindowBackground_(True)
            window.setHasShadow_(True)
            
            window.effect_view = NSVisualEffectView.alloc().initWithFrame_(rect)
            window.effect_view.setMaterial_(11)
            window.effect_view.setBlendingMode_(NSVisualEffectBlendingModeBehindWindow)
            window.effect_view.setState_(1)
            window.effect_view.setWantsLayer_(True)
            window.effect_view.layer().setCornerRadius_(16.0)
            window.effect_view.layer().setMasksToBounds_(True)
            window.effect_view.setAutoresizingMask_(NSViewWidthSizable | NSViewHeightSizable)
            window.setContentView_(window.effect_view)

            padding = 16.0
            icon_size = 40.0
            icon_spacing = 8.0
            text_icon_spacing = 16.0
            
            # OUTPUT TEXT (Bottom, Scrollable)
            window.scroll_view = NSScrollView.alloc().initWithFrame_(NSMakeRect(padding, padding, rect.size.width - (padding*2), 0))
            window.scroll_view.setHasVerticalScroller_(True)
            window.scroll_view.setDrawsBackground_(False)
            window.scroll_view.setAutoresizingMask_(NSViewWidthSizable | NSViewHeightSizable)
            window.effect_view.addSubview_(window.scroll_view)
            
            content_size = window.scroll_view.contentSize()
            window.output_view = ArrowCursorTextView.alloc().initWithFrame_(NSMakeRect(0, 0, content_size.width, content_size.height))
            window.output_view.setEditable_(False)
            window.output_view.setDrawsBackground_(False)
            window.output_view.setTextColor_(NSColor.whiteColor())
            window.output_view.setFont_(NSFont.systemFontOfSize_weight_(16.0, 0.2))
            window.output_view.setVerticallyResizable_(True)
            window.output_view.setHorizontallyResizable_(False)
            window.output_view.setAutoresizingMask_(NSViewWidthSizable)
            window.output_view.textContainer().setWidthTracksTextView_(True)
            window.scroll_view.setDocumentView_(window.output_view)

            # TOP ROW (Input and Buttons)
            input_y = 15.0
            icon_y = 10.0
            
            input_w = rect.size.width - padding - (icon_size * 4) - (icon_spacing * 3) - text_icon_spacing - padding
            window.input_field = ArrowCursorTextField.alloc().initWithFrame_(NSMakeRect(padding, input_y, input_w, 30))
            window.input_field.setEditable_(True)
            window.input_field.setSelectable_(True)
            window.input_field.setBordered_(False)
            window.input_field.setDrawsBackground_(True)
            window.input_field.setBackgroundColor_(NSColor.colorWithWhite_alpha_(1.0, 0.1))
            window.input_field.setTextColor_(NSColor.whiteColor())
            window.input_field.setAlignment_(NSTextAlignmentLeft)
            window.input_field.setFont_(NSFont.systemFontOfSize_weight_(16.0, 0.2))
            window.input_field.setPlaceholderString_("Type to translate...")
            window.input_field.setWantsLayer_(True)
            window.input_field.layer().setCornerRadius_(8.0)
            window.input_field.setTarget_(window)
            window.input_field.setAction_(objc.selector(window.onEnterPressed_, signature=b'v@:@'))
            window.input_field.setAutoresizingMask_(NSViewWidthSizable | NSViewMinYMargin)
            window.effect_view.addSubview_(window.input_field)

            try:
                config = NSImageSymbolConfiguration.configurationWithPointSize_weight_scale_(20.0, 4, 3)
            except AttributeError:
                config = None

            # 1. Close Button (Far Right)
            close_x = rect.size.width - padding - icon_size
            window.btn_close = NSButton.alloc().initWithFrame_(NSMakeRect(close_x, icon_y, icon_size, icon_size))
            img_close = NSImage.imageWithSystemSymbolName_accessibilityDescription_("xmark.circle.fill", None)
            if img_close:
                if config: img_close = img_close.imageWithSymbolConfiguration_(config)
                img_close.setTemplate_(True)
                window.btn_close.setImage_(img_close)
            else:
                window.btn_close.setTitle_("X")
            window.btn_close.setTarget_(window)
            window.btn_close.setAction_(objc.selector(window.onClose_, signature=b'v@:@'))
            window.btn_close.setBordered_(False)
            window.btn_close.setAutoresizingMask_(NSViewMinXMargin | NSViewMinYMargin)
            window.effect_view.addSubview_(window.btn_close)

            # 2. Hide Button
            hide_x = close_x - icon_spacing - icon_size
            window.btn_hide = NSButton.alloc().initWithFrame_(NSMakeRect(hide_x, icon_y, icon_size, icon_size))
            img_hide = NSImage.imageWithSystemSymbolName_accessibilityDescription_("eye.slash.fill", None)
            if img_hide:
                if config: img_hide = img_hide.imageWithSymbolConfiguration_(config)
                img_hide.setTemplate_(True)
                window.btn_hide.setImage_(img_hide)
            else:
                window.btn_hide.setTitle_("Hide")
            window.btn_hide.setTarget_(window)
            window.btn_hide.setAction_(objc.selector(window.onHide_, signature=b'v@:@'))
            window.btn_hide.setBordered_(False)
            window.btn_hide.setAutoresizingMask_(NSViewMinXMargin | NSViewMinYMargin)
            window.effect_view.addSubview_(window.btn_hide)

            # 3. Paste Button
            paste_x = hide_x - icon_spacing - icon_size
            window.btn_paste = NSButton.alloc().initWithFrame_(NSMakeRect(paste_x, icon_y, icon_size, icon_size))
            img_paste = NSImage.imageWithSystemSymbolName_accessibilityDescription_("doc.on.clipboard", None)
            if img_paste:
                if config: img_paste = img_paste.imageWithSymbolConfiguration_(config)
                img_paste.setTemplate_(True)
                window.btn_paste.setImage_(img_paste)
            else:
                window.btn_paste.setTitle_("Paste")
            window.btn_paste.setTarget_(window)
            window.btn_paste.setAction_(objc.selector(window.onPaste_, signature=b'v@:@'))
            window.btn_paste.setBordered_(False)
            window.btn_paste.setAutoresizingMask_(NSViewMinXMargin | NSViewMinYMargin)
            window.effect_view.addSubview_(window.btn_paste)

            # 4. Snap Button
            snap_x = paste_x - icon_spacing - icon_size
            window.btn_shot = NSButton.alloc().initWithFrame_(NSMakeRect(snap_x, icon_y, icon_size, icon_size))
            img_shot = NSImage.imageWithSystemSymbolName_accessibilityDescription_("camera.viewfinder", None)
            if img_shot:
                if config: img_shot = img_shot.imageWithSymbolConfiguration_(config)
                img_shot.setTemplate_(True)
                window.btn_shot.setImage_(img_shot)
            else:
                window.btn_shot.setTitle_("Snap")
            window.btn_shot.setTarget_(window)
            window.btn_shot.setAction_(objc.selector(window.onScreenshot_, signature=b'v@:@'))
            window.btn_shot.setBordered_(False)
            window.btn_shot.setAutoresizingMask_(NSViewMinXMargin | NSViewMinYMargin)
            window.effect_view.addSubview_(window.btn_shot)
            
        return window

    def onEnterPressed_(self, sender):
        if self.app_delegate:
            text = self.input_field.stringValue()
            if text:
                self.input_field.setStringValue_("")
                self.app_delegate.handleManualTranslation_(text)

    def onPaste_(self, sender):
        if self.app_delegate:
            self.app_delegate.handleTranslation()
            
    def onScreenshot_(self, sender):
        if self.app_delegate:
            self.app_delegate.handleScreenshot()

    def onHide_(self, sender):
        if self.app_delegate:
            self.app_delegate.toggle_overlay()
            
    def onClose_(self, sender):
        from AppKit import NSApp
        NSApp.terminate_(None)

    def performOCR_(self, image_path):
        try:
            image_url = NSURL.fileURLWithPath_(image_path)
            image_data = NSData.dataWithContentsOfURL_(image_url)
            if not image_data:
                return "Failed to load image"
            
            image_source = CGImageSourceCreateWithData(image_data, None)
            if not image_source:
                return "Failed to create image source"
            
            cg_image = CGImageSourceCreateImageAtIndex(image_source, 0, {kCGImageSourceShouldCache: True})
            if not cg_image:
                return "Failed to create CGImage"
            
            request = VNRecognizeTextRequest.alloc().init()
            request.setRecognitionLevel_(1)
            request.setUsesLanguageCorrection_(True)
            request.setRecognitionLanguages_(["en-US"])
            
            handler = VNImageRequestHandler.alloc().initWithCGImage_options_(cg_image, {})
            error = None
            success = handler.performRequests_error_([request], error)
            
            if not success:
                return f"OCR failed: {error}"
            
            results = request.results()
            if not results:
                return "No text found in image"
            
            text_lines = []
            for observation in results:
                candidates = observation.topCandidates_(1)
                if candidates and len(candidates) > 0:
                    text_lines.append(candidates[0].string())
            
            return "\n".join(text_lines)
            
        except Exception as e:
            import logging
            logging.getLogger("OverlayWindow").error(f"OCR error: {e}", exc_info=True)
            return f"OCR error: {e}"

    def askAgy_(self, question):
        return translator.ask_antigravity(question)

    def showText_(self, text):
        from AppKit import NSAttributedString, NSData, NSDictionary, NSHTMLTextDocumentType
        
        try:
            import markdown
            from pygments.formatters import HtmlFormatter
            
            html_body = markdown.markdown(text, extensions=['fenced_code', 'codehilite'])
            
            css = HtmlFormatter(style='monokai').get_style_defs('.codehilite')
            
            full_html = f"""
            <html>
            <head>
            <style>
            body {{ font-family: -apple-system, sans-serif; font-size: 14px; color: white; }}
            strong {{ color: #5ac8fa; font-weight: bold; }}
            pre {{ background-color: rgba(0,0,0,0.3); padding: 8px; border-radius: 6px; font-size: 13px; }}
            {css}
            </style>
            </head>
            <body>
            {html_body}
            </body>
            </html>
            """
            
            html_data = NSData.dataWithBytes_length_(full_html.encode('utf-8'), len(full_html.encode('utf-8')))
            options = NSDictionary.dictionaryWithDictionary_({
                "DocumentType": NSHTMLTextDocumentType
            })
            
            res = NSAttributedString.alloc().initWithHTML_options_documentAttributes_(html_data, options, None)
            if res:
                attr_str, _ = res
                self.output_view.textStorage().setAttributedString_(attr_str)
            else:
                self.output_view.setString_(text)
        except Exception as e:
            import logging
            logging.getLogger("MainApp").error(f"Failed to render HTML markdown: {e}", exc_info=True)
            self.output_view.setString_(text)
            
        current_frame = self.frame()
        
        if text and current_frame.size.height < 100:
            new_height = 300.0
            
            screen = self.screen()
            if not screen:
                screen = NSWindow.screens().objectAtIndex_(0)
                
            max_h = screen.visibleFrame().size.height * 0.8
            if new_height > max_h:
                new_height = max_h
                
            y = current_frame.origin.y + current_frame.size.height - new_height
            self.setFrame_display_(NSMakeRect(current_frame.origin.x, y, current_frame.size.width, new_height), True)
            
        elif not text and current_frame.size.height >= 100:
            new_height = 60.0
            y = current_frame.origin.y + current_frame.size.height - new_height
            self.setFrame_display_(NSMakeRect(current_frame.origin.x, y, current_frame.size.width, new_height), True)
            
        elif not hasattr(self, '_has_been_positioned'):
            self._has_been_positioned = True
            screen = self.screen()
            if not screen:
                screen = NSWindow.screens().objectAtIndex_(0)
            screen_frame = screen.visibleFrame()
            
            x = screen_frame.origin.x + (screen_frame.size.width / 2.0) - (current_frame.size.width / 2.0)
            y = screen_frame.origin.y + screen_frame.size.height - current_frame.size.height
            self.setFrame_display_(NSMakeRect(x, y, current_frame.size.width, current_frame.size.height), True)
            
        if not self._hidden:
            self.setAlphaValue_(0.85)
            self.makeKeyAndOrderFront_(None)
        
    def hide_overlay(self):
        self._hidden = True
        self.setAlphaValue_(0.0)
        self.setIgnoresMouseEvents_(True)
        
    def show_overlay(self):
        self._hidden = False
        self.setAlphaValue_(0.85)
        self.setIgnoresMouseEvents_(False)
        self.makeKeyAndOrderFront_(None)
        
    def is_overlay_visible(self):
        return not self._hidden and self.alphaValue() > 0.0

    def toggle_overlay(self):
        if self.is_overlay_visible():
            self.hide_overlay()
        else:
            self.show_overlay()

    def moveWindow_(self, direction):
        step = 60.0
        frame = self.frame()
        x, y, w, h = frame.origin.x, frame.origin.y, frame.size.width, frame.size.height
        
        screen = self.screen()
        if not screen:
            screen = NSWindow.screens().objectAtIndex_(0)
        screen_frame = screen.visibleFrame()
        
        if direction == "left":
            x = max(screen_frame.origin.x, x - step)
        elif direction == "right":
            x = min(screen_frame.origin.x + screen_frame.size.width - w, x + step)
        elif direction == "up":
            y = min(screen_frame.origin.y + screen_frame.size.height - h, y + step)
        elif direction == "down":
            y = max(screen_frame.origin.y, y - step)
            
        self.setFrame_display_(NSMakeRect(x, y, w, h), True)

    def reduceSize(self):
        current_frame = self.frame()
        min_height = 60.0
        if current_frame.size.height > min_height:
            new_height = min_height
            y = current_frame.origin.y + current_frame.size.height - new_height
            self.output_view.setString_("")
            self.setFrame_display_(NSMakeRect(current_frame.origin.x, y, current_frame.size.width, new_height), True)

    def expandSize(self):
        current_frame = self.frame()
        screen = self.screen()
        if not screen:
            screen = NSWindow.screens().objectAtIndex_(0)
        max_h = screen.visibleFrame().size.height * 0.8
        target_height = min(350.0, max_h)
        if current_frame.size.height < target_height:
            y = current_frame.origin.y + current_frame.size.height - target_height
            self.setFrame_display_(NSMakeRect(current_frame.origin.x, y, current_frame.size.width, target_height), True)