#!/bin/bash

# Startup script for Children's Ledger

echo "🚀 Starting Children's Ledger..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Run the application
echo "✅ Starting application on http://localhost:8000"
echo "Press Ctrl+C to stop"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


