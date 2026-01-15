#!/bin/bash
# CodeWeaver AI - Run Script (Unix/Linux/Mac)
# Activates the virtual environment and starts the Streamlit app

echo "🧬 Starting CodeWeaver AI..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run Streamlit
echo "🚀 Launching on http://localhost:8501"
streamlit run main.py
