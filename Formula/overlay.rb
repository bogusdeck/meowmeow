class Overlay < Formula
  desc "Translucent macOS HUD overlay for instant coding challenge translation & AI assistance"
  homepage "https://github.com/bogusdeck/meowmeow"
  url "https://github.com/bogusdeck/meowmeow/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "3776f29979ca5bda5ce623501f6d32118ac0e6caf3ffe8d26d50bfb3be11264f"
  license "MIT"
  depends_on :macos
  depends_on "python@3.11"

  def install
    system "python3.11", "-m", "venv", "--with-pip", libexec
    system libexec/"bin/python", "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"
    system libexec/"bin/python", "-m", "pip", "install", "."
    bin.install_symlink libexec/"bin/overlay"
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
