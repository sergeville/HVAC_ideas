#!/bin/bash
################################################################################
# Tank #1 Basic Diagnostic Application Launcher
################################################################################
#
# DESCRIPTION:
#   Launches the basic (non-AI) diagnostic application for Tank #1 auto-fill system.
#   This is a questionnaire-based tool that doesn't require an API key.
#
# USAGE:
#   ./scripts/run_tank1_diagnostic.sh
#
# REQUIREMENTS:
#   - Python 3
#   - No API key needed (FREE)
#
# COST:
#   $0.00 - Completely free, no API required
#
# ENVIRONMENT:
#   Supports both virtual environment (venv) and system Python.
#
# FEATURES:
#   - Interactive questionnaire for troubleshooting
#   - Step-by-step diagnostic workflow
#   - Float switch and control box diagnostics
#   - No internet connection required
#
# SEE ALSO:
#   - HVAC_Docs/Technical_Guides/TANK1_DIAGNOSTIC_APP_README.md
#   - HVAC_Docs/Technical_Guides/Tank1_Auto_Fill_Diagnostic_Guide.pdf
#   - For AI-powered version: run_ai_diagnostic.sh
#
################################################################################

# Navigate to project root directory (parent of scripts/)
cd "$(dirname "$0")/.."

# Display informational message
echo "Starting Tank #1 Diagnostic Application..."
echo ""

################################################################################
# Python Environment Setup and Execution
################################################################################

# Check if virtual environment exists and use it
if [ -d "venv" ]; then
    # Activate virtual environment
    source venv/bin/activate

    # Run the basic diagnostic application
    python execution/tank1_diagnostic_app.py
else
    # Fall back to system Python 3 if no venv exists
    python3 execution/tank1_diagnostic_app.py
fi
