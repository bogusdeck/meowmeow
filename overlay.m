#import "overlay.h"
#import "_cgo_export.h"

@interface HUDWindow : NSPanel <NSTextFieldDelegate>
@property (strong) NSTextView *textView;
@property (strong) NSTextField *inputField;
@property (strong) NSTextField *indexLabel;
@property (strong) NSVisualEffectView *effectView;
@end

@implementation HUDWindow

- (BOOL)canBecomeKeyWindow {
    return YES;
}

- (BOOL)canBecomeMainWindow {
    return YES;
}

- (void)onInputSubmit:(id)sender {
    NSString *text = [self.inputField stringValue];
    if ([text length] > 0) {
        [self.inputField setStringValue:@""];
        goOnSubmitPrompt((char *)[text UTF8String]);
    }
}

@end

@interface HUDCursorView : NSView
@end

@implementation HUDCursorView
- (void)resetCursorRects {
    [super resetCursorRects];
    [self addCursorRect:[self bounds] cursor:[NSCursor arrowCursor]];
}
@end

static HUDWindow *gHUDWindow = nil;

static HUDWindow* createHUDWindow() {
    NSRect screenFrame = [[NSScreen mainScreen] frame];
    CGFloat width = 600;
    CGFloat height = 450;
    CGFloat x = (screenFrame.size.width - width) / 2.0;
    CGFloat y = (screenFrame.size.height - height) / 2.0;

    NSRect frame = NSMakeRect(x, y, width, height);
    HUDWindow *window = [[HUDWindow alloc] initWithContentRect:frame
                                                     styleMask:NSWindowStyleMaskNonactivatingPanel | NSWindowStyleMaskResizable
                                                       backing:NSBackingStoreBuffered
                                                         defer:NO];

    [window setLevel:NSFloatingWindowLevel];
    [window setOpaque:NO];
    [window setBackgroundColor:[NSColor clearColor]];
    [window setHasShadow:YES];
    [window setIgnoresMouseEvents:NO];
    [window setCollectionBehavior:NSWindowCollectionBehaviorCanJoinAllSpaces | NSWindowCollectionBehaviorStationary];

    HUDCursorView *contentView = [[HUDCursorView alloc] initWithFrame:frame];
    [window setContentView:contentView];

    NSVisualEffectView *effectView = [[NSVisualEffectView alloc] initWithFrame:[contentView bounds]];
    [effectView setAutoresizingMask:NSViewWidthSizable | NSViewHeightSizable];
    [effectView setMaterial:NSVisualEffectMaterialDark];
    [effectView setBlendingMode:NSVisualEffectBlendingModeBehindWindow];
    [effectView setState:NSVisualEffectStateActive];
    [effectView setWantsLayer:YES];
    [effectView.layer setCornerRadius:14.0];
    [effectView.layer setMasksToBounds:YES];
    [contentView addSubview:effectView];
    window.effectView = effectView;

    // Header bar
    NSRect headerRect = NSMakeRect(12, height - 36, width - 24, 28);
    NSView *headerView = [[NSView alloc] initWithFrame:headerRect];
    [headerView setAutoresizingMask:NSViewMinYMargin | NSViewWidthSizable];
    [contentView addSubview:headerView];

    NSTextField *titleLabel = [[NSTextField alloc] initWithFrame:NSMakeRect(0, 4, 160, 20)];
    [titleLabel setStringValue:@"🛸 Overlay HUD"];
    [titleLabel setBezeled:NO];
    [titleLabel setDrawsBackground:NO];
    [titleLabel setEditable:NO];
    [titleLabel setSelectable:NO];
    [titleLabel setTextColor:[NSColor colorWithCalibratedWhite:0.95 alpha:1.0]];
    [titleLabel setFont:[NSFont boldSystemFontOfSize:13]];
    [headerView addSubview:titleLabel];

    NSTextField *indexLabel = [[NSTextField alloc] initWithFrame:NSMakeRect(165, 4, 60, 20)];
    [indexLabel setStringValue:@"[0/0]"];
    [indexLabel setBezeled:NO];
    [indexLabel setDrawsBackground:NO];
    [indexLabel setEditable:NO];
    [indexLabel setSelectable:NO];
    [indexLabel setTextColor:[NSColor colorWithCalibratedWhite:0.7 alpha:1.0]];
    [indexLabel setFont:[NSFont systemFontOfSize:11]];
    [headerView addSubview:indexLabel];
    window.indexLabel = indexLabel;

    // Scrollable Text View
    NSRect scrollFrame = NSMakeRect(12, 48, width - 24, height - 90);
    NSScrollView *scrollView = [[NSScrollView alloc] initWithFrame:scrollFrame];
    [scrollView setAutoresizingMask:NSViewWidthSizable | NSViewHeightSizable];
    [scrollView setHasVerticalScroller:YES];
    [scrollView setDrawsBackground:NO];
    [scrollView setBorderType:NSNoBorder];

    NSTextView *textView = [[NSTextView alloc] initWithFrame:[scrollView bounds]];
    [textView setAutoresizingMask:NSViewWidthSizable | NSViewHeightSizable];
    [textView setDrawsBackground:NO];
    [textView setEditable:NO];
    [textView setSelectable:YES];
    [textView setTextColor:[NSColor whiteColor]];
    [textView setFont:[NSFont userFixedPitchFontOfSize:13]];
    [scrollView setDocumentView:textView];
    [contentView addSubview:scrollView];
    window.textView = textView;

    // Bottom Input Bar
    NSRect inputFrame = NSMakeRect(12, 10, width - 24, 30);
    NSTextField *inputField = [[NSTextField alloc] initWithFrame:inputFrame];
    [inputField setAutoresizingMask:NSViewWidthSizable | NSViewMaxYMargin];
    [inputField setPlaceholderString:@"Ask AI assistant... (Press Enter to submit)"];
    [inputField setBezeled:YES];
    [inputField setBezelStyle:NSTextFieldSquareBezel];
    [inputField setDrawsBackground:YES];
    [inputField setBackgroundColor:[NSColor colorWithCalibratedWhite:0.1 alpha:0.6]];
    [inputField setTextColor:[NSColor whiteColor]];
    [inputField setFont:[NSFont systemFontOfSize:13]];
    [inputField setTarget:window];
    [inputField setAction:@selector(onInputSubmit:)];
    [contentView addSubview:inputField];
    window.inputField = inputField;

    return window;
}

void SetupHUDWindow(void) {
    dispatch_async(dispatch_get_main_queue(), ^{
        if (!gHUDWindow) {
            gHUDWindow = createHUDWindow();
            [gHUDWindow makeKeyAndOrderFront:nil];
            [NSApp activateIgnoringOtherApps:YES];
        }
    });
}

void ShowHUDText(const char* text) {
    NSString *nsText = [NSString stringWithUTF8String:text ? text : ""];
    dispatch_async(dispatch_get_main_queue(), ^{
        if (gHUDWindow) {
            [gHUDWindow.textView setString:nsText];
            [gHUDWindow makeKeyAndOrderFront:nil];
            [NSApp activateIgnoringOtherApps:YES];
        }
    });
}

void SetHUDIndexText(const char* text) {
    NSString *nsText = [NSString stringWithUTF8String:text ? text : ""];
    dispatch_async(dispatch_get_main_queue(), ^{
        if (gHUDWindow && gHUDWindow.indexLabel) {
            [gHUDWindow.indexLabel setStringValue:nsText];
        }
    });
}

void ToggleHUDVisibility(void) {
    dispatch_async(dispatch_get_main_queue(), ^{
        if (gHUDWindow) {
            if ([gHUDWindow isVisible]) {
                [gHUDWindow orderOut:nil];
            } else {
                [gHUDWindow makeKeyAndOrderFront:nil];
                [NSApp activateIgnoringOtherApps:YES];
            }
        }
    });
}

void MoveHUDWindow(int dx, int dy) {
    dispatch_async(dispatch_get_main_queue(), ^{
        if (gHUDWindow) {
            NSRect frame = [gHUDWindow frame];
            frame.origin.x += dx;
            frame.origin.y += dy;
            [gHUDWindow setFrame:frame display:YES animate:YES];
        }
    });
}

void ResizeHUDWindow(int dw, int dh) {
    dispatch_async(dispatch_get_main_queue(), ^{
        if (gHUDWindow) {
            NSRect frame = [gHUDWindow frame];
            frame.size.width += dw;
            frame.size.height += dh;
            if (frame.size.width < 300) frame.size.width = 300;
            if (frame.size.height < 200) frame.size.height = 200;
            [gHUDWindow setFrame:frame display:YES animate:YES];
        }
    });
}

void SetHUDCursorStandard(void) {
    dispatch_async(dispatch_get_main_queue(), ^{
        [[NSCursor arrowCursor] set];
    });
}

void RunAppKitLoop(void) {
    [NSApplication sharedApplication];
    [NSApp setActivationPolicy:NSApplicationActivationPolicyAccessory];
    SetupHUDWindow();
    [NSApp run];
}
