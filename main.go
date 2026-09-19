package main

/*
#cgo CFLAGS: -x objective-c -Wno-deprecated-declarations -mmacosx-version-min=13.0
#cgo LDFLAGS: -framework Cocoa -mmacosx-version-min=13.0

#include "overlay.h"
*/
import "C"
import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) > 1 {
		switch os.Args[1] {
		case "--start":
			startBackground()
			return
		case "--stop":
			stopBackground()
			return
		case "--status":
			showStatus()
			return
		case "--config":
			handleConfigCommand(os.Args[2:])
			return
		case "-h", "--help":
			fmt.Println("Usage: overlay [--start | --stop | --status | --config leader \"ctrl+cmd+fn\"]")
			return
		}
	}

	_ = os.WriteFile(pidFile, []byte(fmt.Sprintf("%d", os.Getpid())), 0644)

	cfg := loadConfig()
	applyFullConfig(cfg)

	fmt.Printf("Starting Overlay HUD (Leader: %s, Font: %s %.1fpt, Opacity: %.0f%%)...\n", cfg.Leader, cfg.FontFamily, cfg.FontSize, cfg.Opacity)
	startHotkeyListener()

	C.RunAppKitLoop()
}
