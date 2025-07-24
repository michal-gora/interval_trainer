#!/bin/bash

echo "🔧 Creating virtual environment..."
python3 -m venv venv

echo "📦 Activating environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Try to install espeak if it's not already installed
if ! command -v espeak >/dev/null 2>&1; then
    echo "📢 espeak not found. Attempting to install it..."

    if [ -f /etc/debian_version ]; then
        sudo apt update
        sudo apt install -y espeak
    else
        echo "⚠️  Automatic installation of espeak is only supported on Debian/Ubuntu."
        echo "❗ Please install it manually (e.g., 'sudo apt install espeak')."
    fi
else
    echo "✅ espeak is already installed."
fi

echo "✅ Setup complete! Virtual environment is ready."
echo "👉 To start using the app:"
echo "   source venv/bin/activate"
echo "   python3 main.py <lesson_number> [options]"
