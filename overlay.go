package main

/*
#cgo CFLAGS: -x objective-c -Wno-deprecated-declarations -mmacosx-version-min=13.0
#cgo LDFLAGS: -framework Cocoa -framework QuartzCore -framework Vision -mmacosx-version-min=13.0

#include "overlay.h"
#include <stdlib.h>
*/
import "C"
import (
	"fmt"
	"log"
	"sync"
	"time"
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
	go processTranslationWithPrimary(text, true, "ollama")
}

//export goOnSubmitScreenCapture
func goOnSubmitScreenCapture(cText *C.char) {
	text := C.GoString(cText)
	if text == "" {
		return
	}
	log.Printf("User submitted screen capture OCR prompt: %s", text)
	go processTranslationWithPrimary(text, true, "antigravity")
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
	if prompt == "" && currentHistoryIndex >= 0 && currentHistoryIndex < len(historyCards) {
		prompt = historyCards[currentHistoryIndex].Prompt
	}
	historyLock.Unlock()

	if prompt == "" {
		cMsg := C.CString("ℹ️ No active or history request to accelerate with Antigravity.")
		defer C.free(unsafe.Pointer(cMsg))
		C.ShowHUDText(cMsg)
		return
	}

	modelName := getModelNameForProvider("antigravity")
	stopTimer := make(chan struct{})

	go func() {
		start := time.Now()
		updateTimer := func() {
			secs := int(time.Since(start).Seconds())
			loadingText := fmt.Sprintf("%s (%ds)...", modelName, secs)
			cLoading := C.CString(loadingText)
			C.ShowHUDText(cLoading)
			C.free(unsafe.Pointer(cLoading))
		}
		updateTimer()

		ticker := time.NewTicker(1 * time.Second)
		defer ticker.Stop()

		for {
			select {
			case <-stopTimer:
				return
			case <-ticker.C:
				updateTimer()
			}
		}
	}()

	go func(p string) {
		res := askAntigravity(p)
		close(stopTimer)

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
	processTranslationWithPrimary(text, isRawPrompt, "ollama")
}

func processTranslationWithPrimary(text string, isRawPrompt bool, primaryProvider string) {
	historyLock.Lock()
	currentActivePrompt = text
	historyLock.Unlock()

	modelName := getModelNameForProvider(primaryProvider)
	stopTimer := make(chan struct{})

	go func() {
		start := time.Now()
		updateTimer := func() {
			secs := int(time.Since(start).Seconds())
			loadingText := fmt.Sprintf("%s (%ds)...", modelName, secs)
			cLoading := C.CString(loadingText)
			C.ShowHUDText(cLoading)
			C.free(unsafe.Pointer(cLoading))
		}
		updateTimer()

		ticker := time.NewTicker(1 * time.Second)
		defer ticker.Stop()

		for {
			select {
			case <-stopTimer:
				return
			case <-ticker.C:
				updateTimer()
			}
		}
	}()

	result := translateTextWithPrimary(text, isRawPrompt, primaryProvider)
	close(stopTimer)

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
	go processTranslationWithPrimary(text, false, "ollama")
}
