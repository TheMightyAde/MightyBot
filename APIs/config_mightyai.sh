#!/bin/sh

if command -v ollama >/dev/null 2>&1; then
    echo "Ollama is already installed: $(ollama --version)"
else
    echo "Ollama not found. Installing..."
    # Install curl if missing (Debian/Ubuntu)
    if ! command -v curl >/dev/null 2>&1; then
        sudo apt-get update && sudo apt-get install -y curl
    fi
    # Run the official Ollama Linux install script
    curl -fsSL https://ollama.com | sh
fi

# Create the model (change 'mightybot' to your preferred name)
ollama create mightybot -f Modelfile

# Prompt to run the model
printf "Run your model? (y/n): "
read -r answer

if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
    echo "Starting your AI Model..."
    ollama run mightybot
fi
