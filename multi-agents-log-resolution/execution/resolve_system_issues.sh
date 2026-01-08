#!/bin/bash
# Multi-Agent Log Resolution System - Main Wrapper Script
# Runs all 3 phases and generates a master resolution plan

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Multi-Agent Log Resolution System                           ║${NC}"
echo -e "${BLUE}║   3-Phase Analysis: Diagnostic → Debate → Master Plan         ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check for input
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

# Create temp directory
TMP_DIR="$PROJECT_ROOT/.tmp"
mkdir -p "$TMP_DIR"

# Handle live capture
if [ "$1" == "--live" ]; then
    echo -e "${YELLOW}📡 Capturing live system logs (last 1 hour)...${NC}"
    LOG_FILE="$TMP_DIR/captured_logs_$(date +%Y%m%d_%H%M%S).txt"
    log show --last 1h --level error > "$LOG_FILE"
    echo -e "${GREEN}✓${NC} Captured logs to: $LOG_FILE"
else
    LOG_FILE="$1"
    if [ ! -f "$LOG_FILE" ]; then
        echo -e "${RED}✗ Error: File not found: $LOG_FILE${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}PHASE 1: DIAGNOSTIC (Agent Alpha - The Investigator)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

PHASE1_OUTPUT="$TMP_DIR/phase1_diagnostic.txt"
python3 "$SCRIPT_DIR/parse_macos_logs.py" "$LOG_FILE" > "$PHASE1_OUTPUT"

# Display Phase 1 summary
echo -e "${GREEN}✓${NC} Phase 1 Complete - Diagnostic Report Generated"
echo ""
grep -A 3 "Total Log Entries:" "$PHASE1_OUTPUT" || true
echo ""

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}PHASE 2: DELIBERATION (Agent Alpha & Agent Beta)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

PHASE2_OUTPUT="$TMP_DIR/phase2_debate.txt"
python3 "$SCRIPT_DIR/agent_debate.py" "$PHASE1_OUTPUT" > "$PHASE2_OUTPUT"

# Display Phase 2 summary
echo -e "${GREEN}✓${NC} Phase 2 Complete - Consensus Reached"
echo ""
grep -A 2 "Selected Fix:" "$PHASE2_OUTPUT" || true
echo ""

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}PHASE 3: MASTER PLAN (Agent Gamma - The Coordinator)${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

MASTER_PLAN="$TMP_DIR/master_plan_$(date +%Y%m%d_%H%M%S).md"
python3 "$SCRIPT_DIR/agent_coordinator.py" "$PHASE1_OUTPUT" "$PHASE2_OUTPUT" > "$MASTER_PLAN"

echo -e "${GREEN}✓${NC} Phase 3 Complete - Master Plan Generated"
echo ""

# Display the master plan
cat "$MASTER_PLAN"

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
