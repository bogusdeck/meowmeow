#ifndef OVERLAY_H
#define OVERLAY_H

#import <Cocoa/Cocoa.h>

#ifdef __cplusplus
extern "C" {
#endif

void SetupHUDWindow(void);
void ShowHUDText(const char* text);
void SetHUDIndexText(const char* text);
void ToggleHUDVisibility(void);
void MoveHUDWindow(int dx, int dy);
void ResizeHUDWindow(int dw, int dh);
void SetHUDCursorStandard(void);
void RunAppKitLoop(void);

void goHotkeyTranslate(void);
void goHotkeyToggleOverlay(void);
void goHotkeyInstantAgy(void);
void goHotkeyNextCard(void);
void goHotkeyPrevCard(void);
void goHotkeyMoveLeft(void);
void goHotkeyMoveRight(void);
void goHotkeyMoveUp(void);
void goHotkeyMoveDown(void);
void goHotkeyReduceSize(void);
void goHotkeyExpandSize(void);

#ifdef __cplusplus
}
#endif

#endif
