# Overlay — macOS AI Assistant & Code Translator HUD

Overlay is a lightweight, floating translucent HUD application for macOS written in Go for instant coding challenge translation and AI technical interview assistance powered by Ollama and Antigravity (`agy -p`).

## Features

- **Single Native Binary**: 100% Go & macOS AppKit (CGo). Zero Python/pip runtime dependencies.
- **Translucent HUD Overlay**: Native macOS AppKit panel with dark visual effects (`NSVisualEffectView`).
- **Global Hotkey Trigger**: Press `Cmd` + `Ctrl` + `P` (or `Cmd` + `Ctrl` + `Fn` + `P`) to instantly solve code from your clipboard.
- **Directional Controls & Resizing**: Move window with `Cmd` + `Ctrl` + `Arrows`, resize with `Cmd` + `Ctrl` + `+`/`-`.
- **Response History Cards**: Switch between past responses using `Cmd` + `Ctrl` + `>` and `Cmd` + `Ctrl` + `<`.
- **Antigravity Acceleration**: Press `Cmd` + `Ctrl` + `I` to run an instant parallel request with Antigravity CLI.
- **Dual AI Backend Support**:
  - Primary: Local or Cloud Ollama API.
  - Backup/Fallback: Antigravity CLI (`agy -p`).

## Installation

### Homebrew (Recommended)

```bash
brew tap bogusdeck/meowmeow https://github.com/bogusdeck/meowmeow.git
brew install overlay
```

#### Run as Background Service
```bash
brew services start overlay
```

#### CLI Daemon Commands
```bash
overlay --start
overlay --stop
overlay --status
```

### Manual Build

#### Prerequisites
- macOS 12+
- Go 1.20+
- Ollama and/or Antigravity CLI (`agy`)

#### Build Steps
```bash
git clone https://github.com/bogusdeck/meowmeow.git
cd meowmeow
go build -o overlay .
./overlay --start
```

## Hotkeys Quick Reference

| Action | Shortcut |
|---|---|
| Translate Clipboard | `Cmd` + `Ctrl` + `P` |
| Toggle Hide/Show Overlay | `Cmd` + `Ctrl` + `H` or `Cmd` + `Ctrl` + `X` |
| Accelerate with Antigravity | `Cmd` + `Ctrl` + `I` |
| Next Response Card | `Cmd` + `Ctrl` + `.` (`>`) |
| Previous Response Card | `Cmd` + `Ctrl` + `,` (`<`) |
| Move Window | `Cmd` + `Ctrl` + `Arrows` |
| Reduce Window Size | `Cmd` + `Ctrl` + `-` |
| Expand Window Size | `Cmd` + `Ctrl` + `=` |