#!/bin/bash
################################################################################
# Tank #2 Basic Diagnostic Application Launcher
################################################################################
#
# DESCRIPTION:
#   Launches the basic (non-AI) diagnostic application for Tank #2 transfer pump.
#   This is a questionnaire-based tool that doesn't require an API key.
#
# USAGE:
#   ./scripts/run_tank2_diagnostic.sh
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
#   - Fuel transfer pump diagnostics
#   - Relay and electrical problem detection
#   - No internet connection required
#
# SEE ALSO:
#   - HVAC_Docs/Technical_Guides/TANK_DIAGNOSTICS_GUIDE.md
#   - HVAC_Docs/Technical_Guides/Oil_Tank_Transfer_Troubleshooting_Guide.pdf
#   - For AI-powered version: run_ai_tank2_diagnostic.sh
#
################################################################################

# Navigate to project root directory (parent of scripts/)
cd "$(dirname "$0")/.."

# Display informational message
echo "Starting Tank #2 Diagnostic Application..."
echo ""

################################################################################
# Python Environment Setup and Execution
################################################################################

# Check if virtual environment exists and use it
if [ -d "venv" ]; then
    # Activate virtual environment
    source venv/bin/activate

    # Run the basic diagnostic application
    python execution/tank2_diagnostic_app.py
else
    # Fall back to system Python 3 if no venv exists
    python3 execution/tank2_diagnostic_app.py
fi
