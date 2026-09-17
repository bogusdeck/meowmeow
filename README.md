# Overlay — macOS AI Assistant & Code Translator HUD

Overlay is a lightweight, floating translucent HUD application for macOS designed for instant coding challenge translation, OCR text extraction, and technical interview problem-solving powered by Ollama and Antigravity (`agy -p`).

## Features

- Translucent floating HUD overlay built natively with macOS AppKit (`NSVisualEffectView`) and Quartz rendering.
- Global hotkey trigger: Press `Cmd` + `Ctrl` + `P` (or `Cmd` + `Ctrl` + `Fn` + `P`) to instantly translate and solve code copied to your clipboard.
- Built-in screen capture & OCR: Click **Snap** to take a screenshot and automatically extract text using macOS Vision framework (`VNRecognizeTextRequest`).
- Dual AI backend support:
  - Primary: Local or Cloud Ollama (defaults to `qwen2.5-coder:7b`).
  - Backup/Fallback: Antigravity (`agy -p`) CLI integration for seamless reliability if Ollama is offline.
- Rich Markdown & code highlighting: Renders output with Pygments syntax highlighting.

## Installation

### Homebrew

```bash
brew tap bogusdeck/tap
brew install overlay
```

### Manual Installation

#### Prerequisites

- macOS 12+ (Monterey or newer recommended)
- Python 3.9+ (Python 3.11 recommended)
- Ollama and/or Antigravity CLI (`agy`)

#### Setup Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/bogusdeck/meowmeow.git
   cd meowmeow
   ```

2. Run the setup script:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   Alternatively, install via pip in editable mode:
   ```bash
   pip install -e .
   ```

3. Launch the application:
   ```bash
   python main.py
   # or simply
   overlay
   ```

## Configuration

Customize AI provider behavior by setting environment variables in your shell (`~/.zshrc` or `~/.bashrc`):

| Variable | Description | Default |
|----------|-------------|---------|
| `OVERLAY_PROVIDER` | Preferred provider order (`ollama`, `antigravity`, or `auto`) | `ollama` |
| `OLLAMA_URL` | Ollama API generate endpoint | `http://localhost:11434/api/generate` |
| `OLLAMA_MODEL` | Ollama model to use | `qwen2.5-coder:7b` |
| `OLLAMA_API_KEY` | Optional API key for Cloud Ollama endpoints | `""` |

## Hotkeys & UI Controls

| Action | Control / Hotkey |
|--------|------------------|
| Translate clipboard | `Cmd` + `Ctrl` + `P` (or `Cmd` + `Ctrl` + `Fn` + `P`) |
| Next response card | `Cmd` + `Ctrl` + `.` (or `Cmd` + `Ctrl` + `Fn` + `.`) |
| Previous response card | `Cmd` + `Ctrl` + `,` (or `Cmd` + `Ctrl` + `Fn` + `,`) |
| Accelerate with Antigravity (agy) | `Cmd` + `Ctrl` + `I` (or `Cmd` + `Ctrl` + `Fn` + `I`) |
| Toggle hide/show overlay | `Cmd` + `Ctrl` + `H` (or `Cmd` + `Ctrl` + `Fn` + `H`) / `X` |
| Move window left | `Cmd` + `Ctrl` + `Left Arrow` (or `Cmd` + `Ctrl` + `Fn` + `Left Arrow`) |
| Move window right | `Cmd` + `Ctrl` + `Right Arrow` (or `Cmd` + `Ctrl` + `Fn` + `Right Arrow`) |
| Move window up | `Cmd` + `Ctrl` + `Up Arrow` (or `Cmd` + `Ctrl` + `Fn` + `Up Arrow`) |
| Move window down | `Cmd` + `Ctrl` + `Down Arrow` (or `Cmd` + `Ctrl` + `Fn` + `Down Arrow`) |
| Reduce overlay size | `Cmd` + `Ctrl` + `-` (or `Cmd` + `Ctrl` + `Fn` + `-`) / `M` |
| Expand overlay size | `Cmd` + `Ctrl` + `=` (or `Cmd` + `Ctrl` + `Fn` + `=`) |
| Snap screenshot (OCR) | Click **Snap** button (Camera icon) |
| Paste & translate | Click **Paste** button (Clipboard icon) |
| Close overlay | Click **X** button (Close icon) |

## Required macOS Permissions

Since Overlay registers system-wide hotkeys (`Cmd` + `Ctrl` + `Fn` + `P`), macOS requires Accessibility permission:

1. Open **System Settings** → **Privacy & Security** → **Accessibility**.
2. Add your Terminal app (e.g., iTerm, Terminal, or Ghostty).
3. Toggle the switch to **ON**.

## License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.