class Overlay < Formula
  desc "Translucent macOS HUD overlay for instant coding challenge translation & AI assistance"
  homepage "https://github.com/bogusdeck/meowmeow"
  url "https://github.com/bogusdeck/meowmeow/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "e854316b42b243a0f29bf737a0f490d4e71e49a792c697d29d254d62d04ec04b"
  license "MIT"
  depends_on :macos
  depends_on "python@3.11"

  include Language::Python::Virtualenv

  resource "pyperclip" do
    url "https://files.pythonhosted.org/packages/a7/2c/4c64579f847bd5d539803c8b909e54ba087a79d01bb3aba433a95879a6c5/pyperclip-1.8.2.tar.gz"
    sha256 "105254a8b04934f0bc84e9c24eb360a591aaf6535c9def5f29d92af107a9bf57"
  end

  resource "pynput" do
    url "https://files.pythonhosted.org/packages/02/27/4de87850ff87c8dcecaaf8d27f28cec89ef17eeb6938f250449cb2635e06/pynput-1.7.6-py2.py3-none-any.whl"
    sha256 "19861b2a0c430d646489852f89500e0c9332e295f2c020e7c2775e7046aa2e2f"
  end

  resource "six" do
    url "https://files.pythonhosted.org/packages/d9/5a/e7c31adbe875f2abbb91bd84cf2dc52d792b5a01506781dbcf25c91daf11/six-1.16.0-py2.py3-none-any.whl"
    sha256 "8abb2f1d86890a2dfb989f9a77cfcfd3e47c2a354b01111771326f8aa26e0254"
  end

  resource "requests" do
    url "https://files.pythonhosted.org/packages/70/8e/0e2d847013cb52cd35b38c009ea167a8954763820573966a35b0e6a6a601/requests-2.31.0-py3-none-any.whl"
    sha256 "58cd2187c01e70e6e26505bca751777aa9f2ee0b7f4300988b709f44e013003f"
  end

  resource "urllib3" do
    url "https://files.pythonhosted.org/packages/a2/73/a68704750a7679d0b6d3ad7aa8d4da8e14e151ae82e6fee774e6e0d05ec8/urllib3-2.2.1-py3-none-any.whl"
    sha256 "450b20ec296a467077128bff42b73080516e71b56ff59a60a02bef2232c4fa9d"
  end

  resource "certifi" do
    url "https://files.pythonhosted.org/packages/ba/06/a07f096c664aeb9f01624f858c3add0a4e913d6c96257acb4fce61e7de14/certifi-2024.2.2-py3-none-any.whl"
    sha256 "dc383c07b76109f368f6106eee2b593b04a011ea4d55f652c6ca24a754d1cdd1"
  end

  resource "idna" do
    url "https://files.pythonhosted.org/packages/e5/3e/741d8c82801c347547f8a2a06aa57dbb1992be9e948df2ea0eda2c8b79e8/idna-3.7-py3-none-any.whl"
    sha256 "82fee1fc78add43492d3a1898bfa6d8a904cc97d8427f683ed8e798d07761aa0"
  end

  resource "charset-normalizer" do
    url "https://files.pythonhosted.org/packages/68/77/02839016f6fbbf808e8b38601df6e0e66c17bbab76dff4613f7511413597/charset_normalizer-3.3.2-cp311-cp311-macosx_10_9_universal2.whl"
    sha256 "802fe99cca7457642125a8a88a084cef28ff0cf9407060f7b93dca5aa25480db"
  end

  resource "markdown" do
    url "https://files.pythonhosted.org/packages/fc/b3/0c0c994fe49cd661084f8d5dc06562af53818cc0abefaca35bdc894577c3/Markdown-3.6-py3-none-any.whl"
    sha256 "48f276f4d8cfb8ce6527c8f79e2ee29708508bf4d40aa410fbc3b4ee832c850f"
  end

  resource "pygments" do
    url "https://files.pythonhosted.org/packages/97/9c/372fef8377a6e340b1704768d20daaded98bf13282b5327beb2e2fe2c7ef/pygments-2.17.2-py3-none-any.whl"
    sha256 "b27c2826c47d0f3219f29554824c30c5e8945175d888647acd804ddd04af846c"
  end

  resource "pyobjc-core" do
    url "https://files.pythonhosted.org/packages/ba/69/e782f176bb5ac71473563f4e5cf825c48b1d7d1fbe1fadde201027804e45/pyobjc_core-10.3.1-cp311-cp311-macosx_10_9_universal2.whl"
    sha256 "899d3c84d2933d292c808f385dc881a140cf08632907845043a333a9d7c899f9"
  end

  resource "pyobjc-framework-Cocoa" do
    url "https://files.pythonhosted.org/packages/d4/ad/436c3619d1a84f83d55ff9c709b122e4d1ac2ee9af467b68fcb60e5ad3a6/pyobjc_framework_Cocoa-10.3.1-cp311-cp311-macosx_10_9_universal2.whl"
    sha256 "5f31021f4f8fdf873b57a97ee1f3c1620dbe285e0b4eaed73dd0005eb72fd773"
  end

  resource "pyobjc-framework-Quartz" do
    url "https://files.pythonhosted.org/packages/62/b3/ba33c4a3406fec862a5107da03d8daacbc11daa355f446a8849e1bf2c73e/pyobjc_framework_Quartz-10.3.1-cp311-cp311-macosx_10_9_universal2.whl"
    sha256 "96578d4a3e70164efe44ad7dc320ecd4e211758ffcde5dcd694de1bbdfe090a4"
  end

  resource "pyobjc-framework-ApplicationServices" do
    url "https://files.pythonhosted.org/packages/78/24/31fdd15f88d3a0a88ba88b27d1f134c7819221886bf56644af12fe672c6d/pyobjc_framework_ApplicationServices-10.3.1-cp311-cp311-macosx_10_9_universal2.whl"
    sha256 "d886ba1f65df47b77ff7546f3fc9bc7d08cfb6b3c04433b719f6b0689a2c0d1f"
  end

  def install
    virtualenv_install_with_resources
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
