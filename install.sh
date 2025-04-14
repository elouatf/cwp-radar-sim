#!/bin/bash

set -e  # Stop on first error

echo "🔹 Creating virtual environment (.venv)..."
python3 -m venv .venv
source .venv/bin/activate

echo "🔹 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

echo "🔹 Building executable with PyInstaller..."
pyinstaller --onefile --name radar ihm/main.py

echo "✅ Build complete. Run with ./dist/radar"
