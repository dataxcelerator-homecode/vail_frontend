#!/bin/bash

# Keyboard Visualizer Startup Script
# Starts the web application on port 9010
# If port is in use, kills the existing process first

PORT=9010
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$APP_DIR/venv"
PYTHON_SCRIPT="$APP_DIR/run_web.py"

echo "=========================================="
echo "Keyboard Visualizer - Startup Script"
echo "=========================================="
echo "Port: $PORT"
echo "Directory: $APP_DIR"
echo ""

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Error: Virtual environment not found at $VENV_PATH"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if port is in use
echo "🔍 Checking if port $PORT is in use..."
PID=$(lsof -ti:$PORT)

if [ ! -z "$PID" ]; then
    echo "⚠️  Port $PORT is in use by process $PID"
    echo "🔪 Killing process $PID..."
    kill -9 $PID 2>/dev/null
    
    # Wait a moment for the port to be released
    sleep 1
    
    # Verify the process was killed
    if lsof -ti:$PORT > /dev/null 2>&1; then
        echo "❌ Error: Failed to kill process on port $PORT"
        exit 1
    else
        echo "✅ Process killed successfully"
    fi
else
    echo "✅ Port $PORT is available"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source "$VENV_PATH/bin/activate"

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to activate virtual environment"
    exit 1
fi

# Start the application
echo ""
echo "🚀 Starting Keyboard Visualizer on port $PORT..."
echo "📍 Access the application at: http://localhost:$PORT"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Set the port environment variable and run the app
export FLASK_PORT=$PORT
python "$PYTHON_SCRIPT"

