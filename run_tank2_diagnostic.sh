#!/bin/bash
# Launcher script for Tank #2 Diagnostic Application (Basic Version - No AI)

cd "$(dirname "$0")"

echo "Starting Tank #2 Diagnostic Application..."
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    source venv/bin/activate
    python execution/tank2_diagnostic_app.py
else
    # Try system python3
    python3 execution/tank2_diagnostic_app.py
fi
