package main

/*
#cgo CFLAGS: -x objective-c -Wno-deprecated-declarations
#cgo LDFLAGS: -framework Cocoa -framework CoreGraphics

#import <Cocoa/Cocoa.h>
#include "overlay.h"

static CFMachPortRef gEventTap = NULL;

static CGEventRef eventTapCallback(CGEventTapProxy proxy, CGEventType type, CGEventRef event, void *refcon) {
    if (type == kCGEventKeyDown) {
        CGEventFlags flags = CGEventGetFlags(event);
        bool isCmd = (flags & kCGEventFlagMaskCommand) != 0;
        bool isControl = (flags & kCGEventFlagMaskControl) != 0;

        if (isCmd && isControl) {
            int64_t keycode = CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode);
            switch (keycode) {
                case 35: // 'p'
                    goHotkeyTranslate();
                    return NULL;
                case 4: // 'h'
                case 7: // 'x'
                    goHotkeyToggleOverlay();
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
                    goHotkeyMoveLeft();
                    return NULL;
                case 124: // Right Arrow
                    goHotkeyMoveRight();
                    return NULL;
                case 126: // Up Arrow
                    goHotkeyMoveUp();
                    return NULL;
                case 125: // Down Arrow
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

//export goHotkeyToggleOverlay
func goHotkeyToggleOverlay() {
	C.ToggleHUDVisibility()
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
