package main

/*
#cgo CFLAGS: -x objective-c -Wno-deprecated-declarations -mmacosx-version-min=13.0
#cgo LDFLAGS: -framework Cocoa -framework CoreGraphics -mmacosx-version-min=13.0

#import <Cocoa/Cocoa.h>
#include "overlay.h"

static CFMachPortRef gEventTap = NULL;

static CGEventRef eventTapCallback(CGEventTapProxy proxy, CGEventType type, CGEventRef event, void *refcon) {
    if (type == kCGEventKeyDown) {
        CGEventFlags flags = CGEventGetFlags(event);
        if (CheckLeaderModifiers(flags)) {
            int64_t keycode = CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode);
            switch (keycode) {
                case 35: // 'p'
                    goHotkeyTranslate();
                    return NULL;
                case 1: // 's' (Screen Capture & Vision OCR)
                    goHotkeySnapOCR();
                    return NULL;
                case 4: // 'h' (Toggle Hide/Show Overlay)
                    goHotkeyToggleOverlay();
                    return NULL;
                case 7: // 'x' (Kill / Stop Overlay Process completely)
                    goHotkeyKillApp();
                    return NULL;
                case 34: // 'i'
                    goHotkeyInstantAgy();
                    return NULL;
                case 47: // '.' (>)
                    goHotkeyNextCard();
                    return NULL;
                case 43: // ',' (<)
                    goHotkeyPrevCard();
                    return NULL;
                case 123: // Left Arrow
                case 115: // Home (Fn + Left Arrow)
                    goHotkeyMoveLeft();
                    return NULL;
                case 124: // Right Arrow
                case 119: // End (Fn + Right Arrow)
                    goHotkeyMoveRight();
                    return NULL;
                case 126: // Up Arrow
                case 116: // Page Up (Fn + Up Arrow)
                    goHotkeyMoveUp();
                    return NULL;
                case 125: // Down Arrow
                case 121: // Page Down (Fn + Down Arrow)
                    goHotkeyMoveDown();
                    return NULL;
                case 27: // '-'
                case 46: // 'm'
                    goHotkeyReduceSize();
                    return NULL;
                case 24: // '=' / '+'
                    goHotkeyExpandSize();
                    return NULL;
            }
        }
    }
    return event;
}

static void StartGlobalHotkeys() {
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        CGEventMask mask = CGEventMaskBit(kCGEventKeyDown);
        gEventTap = CGEventTapCreate(
            kCGSessionEventTap,
            kCGHeadInsertEventTap,
            kCGEventTapOptionDefault,
            mask,
            eventTapCallback,
            NULL
        );

        if (!gEventTap) {
            NSLog(@"Failed to create CGEventTap. Please grant Accessibility permissions in System Settings.");
            return;
        }

        CFRunLoopSourceRef runLoopSource = CFMachPortCreateRunLoopSource(kCFAllocatorDefault, gEventTap, 0);
        CFRunLoopAddSource(CFRunLoopGetCurrent(), runLoopSource, kCFRunLoopCommonModes);
        CGEventTapEnable(gEventTap, true);
        CFRunLoopRun();
    });
}
*/
import "C"

//export goHotkeyTranslate
func goHotkeyTranslate() {
	onTranslateClipboard()
}

//export goHotkeySnapOCR
func goHotkeySnapOCR() {
	C.PerformScreenCaptureOCR()
}

//export goHotkeyToggleOverlay
func goHotkeyToggleOverlay() {
	C.ToggleHUDVisibility()
}

//export goHotkeyKillApp
func goHotkeyKillApp() {
	stopBackground()
}

//export goHotkeyInstantAgy
func goHotkeyInstantAgy() {
	goOnInstantAgy()
}

//export goHotkeyNextCard
func goHotkeyNextCard() {
	goOnNextCard()
}

//export goHotkeyPrevCard
func goHotkeyPrevCard() {
	goOnPrevCard()
}

//export goHotkeyMoveLeft
func goHotkeyMoveLeft() {
	C.MoveHUDWindow(C.int(-40), C.int(0))
}

//export goHotkeyMoveRight
func goHotkeyMoveRight() {
	C.MoveHUDWindow(C.int(40), C.int(0))
}

//export goHotkeyMoveUp
func goHotkeyMoveUp() {
	C.MoveHUDWindow(C.int(0), C.int(40))
}

//export goHotkeyMoveDown
func goHotkeyMoveDown() {
	C.MoveHUDWindow(C.int(0), C.int(-40))
}

//export goHotkeyReduceSize
func goHotkeyReduceSize() {
	C.ResizeHUDWindow(C.int(-40), C.int(-30))
}

//export goHotkeyExpandSize
func goHotkeyExpandSize() {
	C.ResizeHUDWindow(C.int(40), C.int(30))
}

func startHotkeyListener() {
	C.StartGlobalHotkeys()
}
