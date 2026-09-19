class Overlay < Formula
  desc "Translucent macOS HUD overlay for instant coding challenge translation & AI assistance"
  homepage "https://github.com/bogusdeck/meowmeow"
  url "https://github.com/bogusdeck/meowmeow/archive/refs/tags/v1.0.3.tar.gz"
  sha256 "f96f996d8c8728bc57b3910eae31f18d43f57d5866d9d0870fcba56e411a3b4d"
  license "MIT"
  depends_on :macos
  depends_on "go" => :build

  def install
    system "go", "build", *std_go_args(ldflags: "-s -w")
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
