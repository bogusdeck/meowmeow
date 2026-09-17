from setuptools import setup

setup(
    name="overlay-hud",
    version="1.0.0",
    description="Translucent macOS HUD overlay for instant coding challenge translation & AI assistance using Ollama and Antigravity.",
    long_description=open("README.md", "r", encoding="utf-8").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/bogusdeck/meowmeow",
    author="bogusdeck",
    license="MIT",
    py_modules=["main", "overlay", "translator", "constants", "hotkey"],
    install_requires=[
        "pyobjc>=10.0",
        "pynput>=1.7.6",
        "pyperclip>=1.8.2",
        "requests>=2.31.0",
        "markdown>=3.6",
        "pygments>=2.17.2",
    ],
    entry_points={
        "console_scripts": [
            "overlay=main:main",
        ],
    },
    classifiers=[
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
    ],
    python_requires=">=3.9",
)
