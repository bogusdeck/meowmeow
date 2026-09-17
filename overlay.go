package main

/*
#cgo CFLAGS: -x objective-c -Wno-deprecated-declarations
#cgo LDFLAGS: -framework Cocoa -framework QuartzCore

#include "overlay.h"
#include <stdlib.h>
*/
import "C"
import (
	"fmt"
	"log"
	"sync"
	"unsafe"

	"github.com/atotto/clipboard"
)

type HistoryCard struct {
	Prompt string
	Result string
}

var (
	historyLock         sync.Mutex
	historyCards        []HistoryCard
	currentHistoryIndex = -1
	currentActivePrompt string
)

//export goOnSubmitPrompt
func goOnSubmitPrompt(cText *C.char) {
	text := C.GoString(cText)
	if text == "" {
		return
	}
	log.Printf("User submitted prompt from HUD: %s", text)
	go processTranslation(text, true)
}

//export goOnNextCard
func goOnNextCard() {
	historyLock.Lock()
	defer historyLock.Unlock()

	if len(historyCards) == 0 {
		return
	}
	if currentHistoryIndex < len(historyCards)-1 {
		currentHistoryIndex++
		updateHUDDisplay()
	}
}

//export goOnPrevCard
func goOnPrevCard() {
	historyLock.Lock()
	defer historyLock.Unlock()

	if len(historyCards) == 0 {
		return
	}
	if currentHistoryIndex > 0 {
		currentHistoryIndex--
		updateHUDDisplay()
	}
}

//export goOnInstantAgy
func goOnInstantAgy() {
	historyLock.Lock()
	prompt := currentActivePrompt
	historyLock.Unlock()

	if prompt == "" {
		cMsg := C.CString("ℹ️ No active request to accelerate with Antigravity.")
		defer C.free(unsafe.Pointer(cMsg))
		C.ShowHUDText(cMsg)
		return
	}

	cMsg := C.CString("⚡ Accelerating request with Antigravity CLI...")
	defer C.free(unsafe.Pointer(cMsg))
	C.ShowHUDText(cMsg)

	go func(p string) {
		res := askAntigravity(p)
		historyLock.Lock()
		historyCards = append(historyCards, HistoryCard{Prompt: p, Result: res})
		currentHistoryIndex = len(historyCards) - 1
		historyLock.Unlock()
		updateHUDDisplay()
	}(prompt)
}

func updateHUDDisplay() {
	if currentHistoryIndex >= 0 && currentHistoryIndex < len(historyCards) {
		card := historyCards[currentHistoryIndex]
		idxText := fmt.Sprintf("[%d/%d]", currentHistoryIndex+1, len(historyCards))

		cRes := C.CString(card.Result)
		cIdx := C.CString(idxText)
		defer C.free(unsafe.Pointer(cRes))
		defer C.free(unsafe.Pointer(cIdx))

		C.ShowHUDText(cRes)
		C.SetHUDIndexText(cIdx)
	}
}

func processTranslation(text string, isRawPrompt bool) {
	historyLock.Lock()
	currentActivePrompt = text
	historyLock.Unlock()

	cLoading := C.CString("⏳ Thinking... (Translating coding challenge)")
	defer C.free(unsafe.Pointer(cLoading))
	C.ShowHUDText(cLoading)

	result := translateText(text, isRawPrompt)

	historyLock.Lock()
	historyCards = append(historyCards, HistoryCard{Prompt: text, Result: result})
	currentHistoryIndex = len(historyCards) - 1
	currentActivePrompt = ""
	historyLock.Unlock()

	updateHUDDisplay()
}

func onTranslateClipboard() {
	text, err := clipboard.ReadAll()
	if err != nil || text == "" {
		cErr := C.CString("⚠️ Clipboard is empty or unreadable.")
		defer C.free(unsafe.Pointer(cErr))
		C.ShowHUDText(cErr)
		return
	}
	go processTranslation(text, false)
}
