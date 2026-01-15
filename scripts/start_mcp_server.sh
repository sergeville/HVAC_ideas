#!/bin/bash
################################################################################
# MCP Thought-to-Action Server Launcher
################################################################################
#
# DESCRIPTION:
#   Launches the MCP server for natural language interaction with reminders,
#   TODO lists, and mind mapping.
#
# USAGE:
#   ./scripts/start_mcp_server.sh
#
# REQUIREMENTS:
#   - Python 3.8+
#   - MCP SDK (pip install mcp>=1.25.0)
#   - .env.diagnostic with configuration
#
################################################################################

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== MCP Thought-to-Action Server ===${NC}"
echo ""

# Check if .env.diagnostic exists
if [ ! -f "$PROJECT_ROOT/.env.diagnostic" ]; then
    echo -e "${RED}❌ Error: .env.diagnostic not found${NC}"
    echo ""
    echo "Please create .env.diagnostic with:"
    echo "  ANTHROPIC_API_KEY=your-api-key"
    echo "  MCP_TODO_FILE=.tmp/user_data/todos.json"
    echo "  MCP_MINDMAP_DIR=.tmp/user_data/mindmaps"
    echo "  MCP_REMINDER_LIST_NAME=Claude Reminders"
    echo "  MCP_LOG_FILE=.tmp/mcp_server.log"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: python3 not found${NC}"
    echo "Please install Python 3.8 or later"
    exit 1
fi

# Check if virtual environment should be used
if [ -d "$PROJECT_ROOT/venv" ]; then
    echo -e "${YELLOW}📦 Activating virtual environment...${NC}"
    source "$PROJECT_ROOT/venv/bin/activate"
fi

# Check if MCP is installed
if ! python3 -c "import mcp" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  MCP SDK not installed${NC}"
    echo ""
    echo "Installing dependencies..."
    pip install -r "$PROJECT_ROOT/requirements.txt"
    echo ""
fi

# Create .tmp/user_data directory
mkdir -p "$PROJECT_ROOT/.tmp/user_data/mindmaps"
echo -e "${GREEN}✅ Created user data directory${NC}"

# Start the server
echo ""
echo -e "${GREEN}🚀 Starting MCP server...${NC}"
echo -e "${BLUE}Log file: $PROJECT_ROOT/.tmp/mcp_server.log${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

cd "$PROJECT_ROOT"
python3 execution/mcp_server.py
