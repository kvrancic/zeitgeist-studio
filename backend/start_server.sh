#!/bin/bash
# Start Zeitgeist Studio Backend

cd "$(dirname "$0")"

# Activate virtual environment
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

source .venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Copy .env.example to .env and add your API keys"
    exit 1
fi

echo "🚀 Starting Zeitgeist Studio API..."
echo "📍 Server will be available at: http://localhost:8000"
echo "📚 API docs at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start server
uvicorn main:app --reload --host 127.0.0.1 --port 8000
