#!/bin/bash
# Launcher script for Tank #1 Diagnostic Application

cd "$(dirname "$0")"

echo "Starting Tank #1 Diagnostic Application..."
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    source venv/bin/activate
    python execution/tank1_diagnostic_app.py
else
    # Try system python3
    python3 execution/tank1_diagnostic_app.py
fi
