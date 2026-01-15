#!/bin/bash
################################################################################
# Multi-Agent Log Resolution System - Main Wrapper Script
################################################################################
#
# DESCRIPTION:
#   Orchestrates a 3-phase multi-agent system to analyze macOS system logs
#   and generate actionable resolution plans. Each phase uses specialized
#   AI agents to diagnose, debate, and coordinate fixes.
#
# USAGE:
#   ./scripts/resolve_system_issues.sh <log_file.txt>     # Analyze existing logs
#   ./scripts/resolve_system_issues.sh --live             # Capture live logs
#
# EXAMPLES:
#   # Capture logs manually and analyze:
#   log show --last 1h --level error > system_errors.txt
#   ./scripts/resolve_system_issues.sh system_errors.txt
#
#   # Or capture and analyze in one step:
#   ./scripts/resolve_system_issues.sh --live
#
# PHASES:
#   Phase 1 - DIAGNOSTIC (Agent Alpha - The Investigator)
#     Parses logs, categorizes errors, identifies patterns
#     Output: Detailed diagnostic report
#
#   Phase 2 - DELIBERATION (Agent Alpha & Beta Debate)
#     Two agents debate best fix approaches, reach consensus
#     Output: Agreed-upon solution strategy
#
#   Phase 3 - MASTER PLAN (Agent Gamma - The Coordinator)
#     Generates step-by-step implementation plan
#     Output: Master resolution plan with verification steps
#
# OUTPUT FILES (saved to .tmp/):
#   - phase1_diagnostic.txt    # Diagnostic analysis
#   - phase2_debate.txt        # Agent debate consensus
#   - master_plan_TIMESTAMP.md # Final implementation plan
#
# REQUIREMENTS:
#   - Python 3
#   - macOS system (for log show command)
#   - Scripts: parse_macos_logs.py, agent_debate.py, agent_coordinator.py
#
# SEE ALSO:
#   - HVAC_Docs/Development_Docs/multi-agents-log-resolution.md
#   - HVAC_Docs/Development_Docs/README_LOG_RESOLUTION.md
#
################################################################################

# Exit immediately if any command fails
set -e

################################################################################
# Terminal Colors for Output Formatting
################################################################################

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

################################################################################
# Directory Setup
################################################################################

# Determine script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Display banner
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Multi-Agent Log Resolution System                           ║${NC}"
echo -e "${BLUE}║   3-Phase Analysis: Diagnostic → Debate → Master Plan         ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

################################################################################
# Input Validation and Help
################################################################################

# Check if input was provided
if [ $# -eq 0 ]; then
    echo -e "${YELLOW}Usage:${NC}"
    echo "  $0 <log_file.txt>          # Analyze existing log file"
    echo "  $0 --live                  # Capture live logs (1 hour)"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo "  # Capture logs and analyze"
    echo "  log show --last 1h --level error > logs.txt"
    echo "  $0 logs.txt"
    echo ""
    echo "  # Or capture live"
    echo "  $0 --live"
    exit 1
fi

################################################################################
# Temporary Directory Setup
################################################################################

# Create temporary directory for intermediate files
TMP_DIR="$PROJECT_ROOT/.tmp"
mkdir -p "$TMP_DIR"

################################################################################
# Log File Handling
################################################################################

# Handle live capture mode vs existing file
if [ "$1" == "--live" ]; then
    # Live capture mode: grab last hour of error-level logs
    echo -e "${YELLOW}📡 Capturing live system logs (last 1 hour)...${NC}"
    LOG_FILE="$TMP_DIR/captured_logs_$(date +%Y%m%d_%H%M%S).txt"

    # Capture logs using macOS log show command
    log show --last 1h --level error > "$LOG_FILE"

    echo -e "${GREEN}✓${NC} Captured logs to: $LOG_FILE"
else
    # Existing file mode: validate file exists
    LOG_FILE="$1"
    if [ ! -f "$LOG_FILE" ]; then
        echo -e "${RED}✗ Error: File not found: $LOG_FILE${NC}"
        exit 1
    fi
fi

################################################################################
# PHASE 1: DIAGNOSTIC ANALYSIS
################################################################################

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}PHASE 1: DIAGNOSTIC (Agent Alpha - The Investigator)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Run diagnostic analysis on logs
PHASE1_OUTPUT="$TMP_DIR/phase1_diagnostic.txt"
python3 "$PROJECT_ROOT/execution/parse_macos_logs.py" "$LOG_FILE" > "$PHASE1_OUTPUT"

# Display Phase 1 summary
echo -e "${GREEN}✓${NC} Phase 1 Complete - Diagnostic Report Generated"
echo ""
grep -A 3 "Total Log Entries:" "$PHASE1_OUTPUT" || true
echo ""

################################################################################
# PHASE 2: AGENT DEBATE AND DELIBERATION
################################################################################

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}PHASE 2: DELIBERATION (Agent Alpha & Agent Beta)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Run agent debate to reach consensus on best fix
PHASE2_OUTPUT="$TMP_DIR/phase2_debate.txt"
python3 "$PROJECT_ROOT/execution/agent_debate.py" "$PHASE1_OUTPUT" > "$PHASE2_OUTPUT"

# Display Phase 2 summary
echo -e "${GREEN}✓${NC} Phase 2 Complete - Consensus Reached"
echo ""
grep -A 2 "Selected Fix:" "$PHASE2_OUTPUT" || true
echo ""

################################################################################
# PHASE 3: MASTER PLAN GENERATION
################################################################################

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}PHASE 3: MASTER PLAN (Agent Gamma - The Coordinator)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Generate comprehensive master plan with implementation steps
MASTER_PLAN="$TMP_DIR/master_plan_$(date +%Y%m%d_%H%M%S).md"
python3 "$PROJECT_ROOT/execution/agent_coordinator.py" "$PHASE1_OUTPUT" "$PHASE2_OUTPUT" > "$MASTER_PLAN"

echo -e "${GREEN}✓${NC} Phase 3 Complete - Master Plan Generated"
echo ""

# Display the complete master plan
cat "$MASTER_PLAN"

################################################################################
# Completion Summary
################################################################################

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ ANALYSIS COMPLETE${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}📁 Output files saved to:${NC}"
echo "  Phase 1 (Diagnostic):  $PHASE1_OUTPUT"
echo "  Phase 2 (Debate):      $PHASE2_OUTPUT"
echo "  Master Plan:           $MASTER_PLAN"
echo ""
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "  1. Review the master plan above"
echo "  2. Follow implementation steps carefully"
echo "  3. Run verification steps after applying fixes"
echo "  4. Re-run this tool if issues persist"
echo ""
