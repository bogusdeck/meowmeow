import os
import requests
import logging
import subprocess
from constants import (
    OLLAMA_URL, OLLAMA_TAGS_URL, MODEL, TRANSLATE_TEXT_PROMPT, API_KEY,
    AGY_PATH, PREFERRED_PROVIDER
)

# Set up logging to both terminal and file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("log.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("Translator")

def translate_with_antigravity(prompt: str) -> str:
    """Executes prompt non-interactively using Antigravity (agy -p)."""
    try:
        logger.info(f"Executing prompt via Antigravity CLI ({AGY_PATH} -p)...")
        result = subprocess.run(
            [AGY_PATH, "-p", prompt],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0 and result.stdout.strip():
            logger.info("Antigravity request succeeded.")
            return result.stdout.strip()
        else:
            err_msg = result.stderr.strip() or "Empty stdout returned"
            logger.error(f"Antigravity CLI error (code {result.returncode}): {err_msg}")
            raise RuntimeError(f"Antigravity error: {err_msg}")
    except Exception as e:
        logger.error(f"Antigravity request failed ({type(e).__name__}: {e})")
        raise

def get_available_ollama_model() -> str:
    """Gets configured model or picks first available installed model from Ollama."""
    try:
        resp = requests.get(OLLAMA_TAGS_URL, timeout=5)
        if resp.status_code == 200:
            models = [m.get("name") for m in resp.json().get("models", []) if m.get("name")]
            if MODEL in models or f"{MODEL}:latest" in models:
                return MODEL
            if models:
                gen_models = [m for m in models if "embed" not in m.lower()]
                selected = gen_models[0] if gen_models else models[0]
                logger.info(f"Model '{MODEL}' not found on Ollama. Using available model '{selected}'")
                return selected
    except Exception as e:
        logger.warning(f"Could not query Ollama tags endpoint: {e}")
    return MODEL

def translate_with_ollama(prompt: str) -> str:
    """Translates prompt using local or cloud Ollama API instance."""
    model_name = get_available_ollama_model()
    logger.info(f"Starting translation request to {OLLAMA_URL} with model '{model_name}'")
    
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    
    payload = {"model": model_name, "prompt": prompt, "stream": False}
    
    response = requests.post(
        OLLAMA_URL,
        json=payload,
        headers=headers,
        timeout=120
    )
    logger.info(f"Ollama responded with HTTP {response.status_code}")
    response.raise_for_status()
    
    result = response.json().get("response", "").strip()
    if not result:
        raise ValueError("Ollama returned an empty response.")
    logger.info("Successfully extracted Ollama response.")
    return result

def translate_text(text: str, is_raw_prompt: bool = False) -> str:
    """
    Translates or solves text using configured provider with automatic fallback.
    If PREFERRED_PROVIDER is 'antigravity', tries agy -p first then Ollama.
    If 'ollama', tries Ollama first then agy -p.
    """
    prompt = text if is_raw_prompt else TRANSLATE_TEXT_PROMPT.format(text=text)
    
    if PREFERRED_PROVIDER == "ollama":
        providers = [("Ollama", translate_with_ollama), ("Antigravity", translate_with_antigravity)]
    else:  # 'antigravity' or 'auto'
        providers = [("Antigravity", translate_with_antigravity), ("Ollama", translate_with_ollama)]
        
    last_error = None
    for provider_name, provider_fn in providers:
        try:
            logger.info(f"Attempting request using {provider_name}...")
            return provider_fn(prompt)
        except Exception as e:
            logger.warning(f"{provider_name} failed: {e}. Trying fallback if available...")
            last_error = e
            
    return f"Execution failed on all available providers. Error: {last_error}"

def ask_antigravity(question: str) -> str:
    """Direct helper for querying Antigravity CLI."""
    return translate_text(question, is_raw_prompt=True)

def translate_image(image_data):
    """Placeholder for image translation."""
    return "Image translation placeholder. (Vision API not yet connected)"
