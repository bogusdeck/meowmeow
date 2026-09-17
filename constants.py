import os
import shutil

# AI Provider settings ('ollama', 'antigravity', or 'auto')
# Default to 'ollama' with fallback to Antigravity (agy -p)
PREFERRED_PROVIDER = os.getenv("OVERLAY_PROVIDER", "ollama")

# Ollama Settings
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_TAGS_URL = os.getenv("OLLAMA_TAGS_URL", "http://localhost:11434/api/tags")
MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
API_KEY = os.getenv("OLLAMA_API_KEY", "")

# Antigravity CLI Settings
def resolve_agy_path() -> str:
    """Find absolute path to agy CLI executable."""
    found = shutil.which("agy")
    if found:
        return found
    home_agy = os.path.expanduser("~/.local/bin/agy")
    if os.path.exists(home_agy):
        return home_agy
    return "agy"

AGY_PATH = resolve_agy_path()

# Prompt Template
TRANSLATE_TEXT_PROMPT = (
    "Here is my coding challenge problem. Act like a candidate in a technical interview.\n\n"
    "Provide:\n"
    "1. A simple, clean, and easy-to-understand solution (nothing fancy, use basic code).\n"
    "2. A short, clear, and user-friendly explanation as you would explain to an interviewer.\n\n"
    "Problem:\n{text}"
)
