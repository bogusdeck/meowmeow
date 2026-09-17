class Overlay < Formula
  desc "Translucent macOS HUD overlay for instant coding challenge translation & AI assistance"
  homepage "https://github.com/bogusdeck/meowmeow"
  url "https://github.com/bogusdeck/meowmeow/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "5ce7a8ace3f0d1bd1ac0fb737a5887bb920bef09fb590f7c92268cf8a42cc36e"
  license "MIT"
  depends_on :macos
  depends_on "python@3.11"

  def install
    # Install Python source files into libexec
    libexec.install "main.py", "overlay.py", "hotkey.py", "translator.py", "constants.py"

    # Write a wrapper script that lazy-installs pip dependencies on first run
    # This runs outside Homebrew's build sandbox so pip has full network access
    (bin/"overlay").write <<~EOS
      #!/bin/bash
      set -e

      VENV="#{var}/overlay/venv"
      LIBEXEC="#{libexec}"
      DEPS="pyperclip pynput pyobjc requests markdown pygments"

      # Create venv and install deps on first run
      if [ ! -f "$VENV/bin/python" ]; then
        echo "🛸 Setting up overlay dependencies (first run, needs internet)..."
        mkdir -p "$(dirname "$VENV")"
        python3.11 -m venv "$VENV"
        "$VENV/bin/pip" install --upgrade pip --quiet
        "$VENV/bin/pip" install $DEPS --quiet
        echo "✅ Done!"
      fi

      exec "$VENV/bin/python" "$LIBEXEC/main.py" "$@"
    EOS
    chmod 0755, bin/"overlay"
  end

  service do
    run [opt_bin/"overlay", "--daemon"]
    keep_alive true
    error_log_path var/"log/overlay.log"
    log_path var/"log/overlay.log"
    process_type :interactive
  end

  def caveats
    <<~EOS
      🛸 Overlay installed successfully!

      On first run, dependencies will be auto-installed (requires internet).

      Start background service:
        brew services start overlay
        # OR
        overlay --start

      Stop background service:
        brew services stop overlay
        # OR
        overlay --stop

      NOTE: Overlay requires macOS Accessibility permissions for global hotkeys.
      Please grant Accessibility access in:
        System Settings -> Privacy & Security -> Accessibility
    EOS
  end

  test do
    assert_predicate bin/"overlay", :exist?
  end
end
