#!/bin/bash
################################################################################
# AI-Powered Tank #1 Diagnostic Assistant Launcher
################################################################################
#
# DESCRIPTION:
#   Launches the AI-powered diagnostic assistant for Tank #1 auto-fill system.
#   Uses Claude API for intelligent troubleshooting and diagnostics.
#
# USAGE:
#   ./scripts/run_ai_diagnostic.sh
#
# REQUIREMENTS:
#   - Anthropic API key (Claude API)
#   - Python 3 with 'anthropic' library
#   - .env.diagnostic file with ANTHROPIC_API_KEY
#
# COST:
#   ~$0.01-0.05 per diagnostic session (Claude API usage)
#
# ENVIRONMENT:
#   Automatically creates .env.diagnostic template if not found.
#   Supports both virtual environment (venv) and system Python.
#
# SEE ALSO:
#   - HVAC_Docs/Technical_Guides/AI_DIAGNOSTIC_README.md
#   - HVAC_Docs/Technical_Guides/TANK1_DIAGNOSTIC_APP_README.md
#
################################################################################

# Navigate to project root directory (parent of scripts/)
cd "$(dirname "$0")/.."

# Display banner
echo "=========================================================================="
echo "  AI-POWERED TANK #1 DIAGNOSTIC ASSISTANT"
echo "=========================================================================="
echo ""

################################################################################
# Check for API Key Configuration
################################################################################

# Verify .env.diagnostic exists with API key configuration
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

    # Create template .env.diagnostic file with placeholder values
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

################################################################################
# Python Environment Setup and Execution
################################################################################

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    # Use virtual environment if available
    source venv/bin/activate

    # Verify anthropic library is installed in venv
    if ! python -c "import anthropic" 2>/dev/null; then
        echo "Installing required library: anthropic"
        pip install anthropic
        echo ""
    fi

    # Run the AI diagnostic script
    python execution/ai_tank1_diagnostic.py
else
    # Fall back to system Python 3 if no venv
    # Verify anthropic library is installed system-wide
    if ! python3 -c "import anthropic" 2>/dev/null; then
        echo "Installing required library: anthropic"
        pip3 install anthropic
        echo ""
    fi

    # Run the AI diagnostic script with system Python
    python3 execution/ai_tank1_diagnostic.py
fi
