# 🛸 Overlay — macOS AI Assistant & Code Translator HUD

**Overlay** is a lightweight, floating translucent HUD application for macOS designed for instant coding challenge translation, OCR text extraction, and technical interview problem-solving powered by **Ollama** and **Antigravity (`agy -p`)**.

---

## ✨ Features

- 🖥️ **Translucent Floating HUD Overlay**: Built natively with macOS AppKit (`NSVisualEffectView`) and Quartz rendering.
- ⚡ **Global Hotkey Trigger**: Press <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>T</kbd> anywhere to instantly translate and solve code copied to your clipboard.
- 📸 **Built-in Screen Capture & OCR**: Click **Snap** to take a screenshot and automatically extract text using macOS Vision framework (`VNRecognizeTextRequest`).
- 🤖 **Dual AI Backend Support**:
  - **Primary**: Local or Cloud [Ollama](https://ollama.com) (defaults to `qwen2.5-coder:7b`).
  - **Backup / Fallback**: Antigravity (`agy -p`) CLI integration for seamless reliability if Ollama is offline.
- 🎨 **Rich Markdown & Code Highlighting**: Renders markdown output with Pygments code syntax highlighting.

---

## 🍺 Installation via Homebrew

You can install `overlay` on macOS using Homebrew:

```bash
# Add the Homebrew tap
brew tap bogusdeck/tap

# Install overlay
brew install overlay
```

Once installed, start the overlay anytime by running:

```bash
overlay
```

---

## 💻 Manual Installation (From Source)

### Prerequisites
- macOS 12+ (Monterey or newer recommended)
- Python 3.9+ (Python 3.11 recommended)
- [Ollama](https://ollama.com) and/or [Antigravity CLI (`agy`)](https://github.com/google/antigravity)

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bogusdeck/overlay.git
   cd overlay
   ```

2. **Run setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Or install via pip in editable mode:**
   ```bash
   pip install -e .
   ```

4. **Launch Application:**
   ```bash
   python main.py
   # or simply
   overlay
   ```

---

## 🔒 Required macOS Permissions

Since `overlay` registers system-wide hotkeys (<kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>T</kbd>), macOS requires **Accessibility** permission:

1. Open **System Settings** -> **Privacy & Security** -> **Accessibility**.
2. Add your Terminal app (e.g. `iTerm`, `Terminal`, or `ghostty`).
3. Toggle the switch to **ON**.

---

## ⚙️ Configuration & Environment Variables

You can customize the AI provider behavior by setting environment variables in your shell (`~/.zshrc` or `~/.bashrc`):

| Variable | Description | Default |
| :--- | :--- | :--- |
| `OVERLAY_PROVIDER` | Preferred provider order (`ollama`, `antigravity`, or `auto`) | `ollama` |
| `OLLAMA_URL` | Ollama API generate endpoint | `http://localhost:11434/api/generate` |
| `OLLAMA_MODEL` | Ollama model to use | `qwen2.5-coder:7b` |
| `OLLAMA_API_KEY` | Optional API Key for Cloud Ollama endpoints | `""` |

---

## ⌨️ Hotkeys & UI Controls

| Action | Control / Hotkey |
| :--- | :--- |
| **Clipboard Translate** | <kbd>Cmd</kbd> + <kbd>Shift</kbd> + <kbd>T</kbd> |
| **Snap Screenshot (OCR)** | Click **Snap** button (Camera icon) |
| **Paste & Translate** | Click **Paste** button (Clipboard icon) |
| **Hide / Show HUD** | Click **Hide** button (Eye icon) |
| **Close Overlay** | Click **X** button (Close icon) |

---

## 📜 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for details.
