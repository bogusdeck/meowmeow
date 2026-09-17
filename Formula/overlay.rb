class Overlay < Formula
  desc "Translucent macOS HUD overlay for instant coding challenge translation & AI assistance"
  homepage "https://github.com/bogusdeck/overlay"
  url "https://github.com/bogusdeck/overlay/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "REPLACE_WITH_SHA256_HASH_OF_V1.0.0_TARBALL"
  license "MIT"
  depends_on :macos
  depends_on "python@3.11"

  include Language::Python::Virtualenv

  def install
    virtualenv_install_with_resources
  end

  def caveats
    <<~EOS
      🛸 Overlay installed successfully!

      Keyboard Shortcut: Cmd + Ctrl + Fn + P (Clipboard translate)

      NOTE: Overlay requires macOS Accessibility permissions for global hotkeys.
      Please grant Accessibility access in:
        System Settings -> Privacy & Security -> Accessibility
    EOS
  end

  test do
    assert_predicate bin/"overlay", :exist?
  end
end
