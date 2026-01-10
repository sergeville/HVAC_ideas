#!/bin/bash
# Launcher script for AI-Powered Tank #2 Diagnostic Assistant

cd "$(dirname "$0")"

echo "=========================================================================="
echo "  AI-POWERED TANK #2 DIAGNOSTIC ASSISTANT"
echo "=========================================================================="
echo ""

# Check if .env.diagnostic exists
if [ ! -f ".env.diagnostic" ]; then
    echo "⚠️  WARNING: .env.diagnostic file not found."
    echo ""
    echo "To use this AI-powered assistant, you need a Claude API key."
    echo ""
    echo "Steps:"
    echo "  1. Get your API key from: https://console.anthropic.com/"
    echo "  2. Create .env.diagnostic file with:"
    echo "     ANTHROPIC_API_KEY=your-api-key-here"
    echo ""
    echo "A template file will be created for you..."
    echo ""

    # Create template .env.diagnostic file
    cat > .env.diagnostic << 'EOF'
# AI Diagnostic Assistant Configuration
# Get your API key from: https://console.anthropic.com/

# Your Anthropic API key (required)
ANTHROPIC_API_KEY=your-api-key-here

# Optional: Change the Claude model (default: claude-3-5-sonnet-20240620)
# MODEL=claude-3-5-sonnet-20240620
EOF

    echo "✓ Created .env.diagnostic template"
    echo ""
    echo "Please edit .env.diagnostic and add your API key, then run again."
    echo ""
    exit 1
fi

# Check if virtual environment exists and activate
if [ -d "venv" ]; then
    source venv/bin/activate

    # Check if anthropic library is installed
    if ! python -c "import anthropic" 2>/dev/null; then
        echo "Installing required library: anthropic"
        pip install anthropic
        echo ""
    fi

    python execution/ai_tank2_diagnostic.py
else
    # Try system python3
    if ! python3 -c "import anthropic" 2>/dev/null; then
        echo "Installing required library: anthropic"
        pip3 install anthropic
        echo ""
    fi

    python3 execution/ai_tank2_diagnostic.py
fi
