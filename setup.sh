#!/bin/bash
set -e

PYTHON_VERSION="3.11.9"
ENV_NAME="quicktranslate"

echo "Checking for pyenv..."
if ! command -v pyenv &> /dev/null; then
    echo "Error: pyenv is not installed. Please install pyenv and pyenv-virtualenv first."
    exit 1
fi

echo "Installing Python ${PYTHON_VERSION} (this may take a few minutes if not already installed)..."
pyenv install -s ${PYTHON_VERSION}

# Check if pyenv-virtualenv plugin is available
if ! pyenv help virtualenv &> /dev/null; then
    echo "pyenv-virtualenv plugin not found. Using standard Python venv instead."
    pyenv local ${PYTHON_VERSION}
    echo "Creating local .venv..."
    python -m venv .venv
    echo "Activating .venv..."
    source .venv/bin/activate
else
    echo "Creating pyenv virtualenv '${ENV_NAME}' for Python ${PYTHON_VERSION}..."
    # Try to create the virtual environment; ignore error if it already exists
    pyenv virtualenv ${PYTHON_VERSION} ${ENV_NAME} 2>/dev/null || true
    
    echo "Setting local pyenv environment to '${ENV_NAME}'..."
    pyenv local ${ENV_NAME}
fi

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo ""
echo "========================================================="
echo "Setup complete!"
echo "Your pyenv environment is configured and dependencies are installed."
echo "You can now start the app by running: python main.py"
echo "========================================================="
