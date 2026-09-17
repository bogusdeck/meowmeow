import requests
import sys

def check_ollama_health():
    url = "http://localhost:11434/"
    tags_url = "http://localhost:11434/api/tags"
    
    print("Checking Ollama connection...")
    try:
        # Check base endpoint
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print("✅ Ollama server is reachable!")
            print(f"   Server message: {response.text.strip()}")
        else:
            print(f"⚠️ Ollama returned an unexpected status code: {response.status_code}")
            
        # Check available models
        print("\nChecking available models...")
        tags_response = requests.get(tags_url, timeout=5)
        if tags_response.status_code == 200:
            models = tags_response.json().get("models", [])
            if models:
                print(f"✅ Found {len(models)} model(s) installed:")
                for model in models:
                    print(f"   - {model.get('name')}")
            else:
                print("⚠️ Connected to Ollama, but no models are installed.")
        else:
            print(f"⚠️ Failed to fetch models. Status code: {tags_response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to Ollama.")
        print("   Make sure the Ollama app is running locally on your Mac.")
    except requests.exceptions.Timeout:
        print("❌ ERROR: Connection to Ollama timed out.")
    except Exception as e:
        print(f"❌ ERROR: An unexpected error occurred: {e}")
        
if __name__ == "__main__":
    check_ollama_health()
