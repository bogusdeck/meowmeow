package main

/*
#cgo CFLAGS: -x objective-c -Wno-deprecated-declarations
#cgo LDFLAGS: -framework Cocoa

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
		case "-h", "--help":
			fmt.Println("Usage: overlay [--start | --stop | --status | --daemon]")
			return
		}
	}

	_ = os.WriteFile(pidFile, []byte(fmt.Sprintf("%d", os.Getpid())), 0644)

	fmt.Println("Starting Overlay HUD in Go...")
	startHotkeyListener()

	C.RunAppKitLoop()
}
