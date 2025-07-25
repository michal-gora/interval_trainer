#!/bin/bash

echo "🔧 Creating virtual environment..."
python3 -m venv venv

echo "📦 Activating environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Try to install espeak if it's not already installed
if ! command -v espeak >/dev/null 2>&1; then
    echo "📢 espeak not found. Attempting to install it..."

    if command -v apt >/dev/null 2>&1; then
        sudo apt update && sudo apt install -y espeak

    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y espeak

    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -Sy --noconfirm espeak

    elif command -v zypper >/dev/null 2>&1; then
        sudo zypper install -y espeak

    else
        echo "⚠️ Could not detect a supported package manager."
        echo "❗ Please install 'espeak' manually using your system's tools."
        exit 1
    fi
else
    echo "✅ espeak is already installed."
fi


# Try to install FluidSynth if not already installed
if ! command -v fluidsynth >/dev/null 2>&1; then
    echo "📢 FluidSynth not found. Attempting to install it..."

    if command -v apt >/dev/null 2>&1; then
        sudo apt update
        sudo apt install -y fluidsynth
    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y fluidsynth
    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -Sy --noconfirm fluidsynth
    elif command -v zypper >/dev/null 2>&1; then
        sudo zypper install -y fluidsynth
    else
        echo "⚠️  Automatic installation of FluidSynth is not supported on this system."
        echo "❗ Please install it manually (e.g., 'sudo apt install fluidsynth')."
    fi
else
    echo "✅ FluidSynth is already installed."
fi



echo "✅ Setup complete! Virtual environment is ready."
echo "👉 To start using the app:"
echo "   source venv/bin/activate"
echo "   python3 main.py <lesson_number> [options]"
