#!/bin/bash
# Quick start script for Virtual HVAC Technician
#
# IMPORTANT: This script assumes you're running it from the directory
# containing docker-compose.yml (e.g., /path/to/opencode/)
#
# If docker-compose.yml is elsewhere, update the COMPOSE_FILE variable below:
# COMPOSE_FILE="-f /path/to/docker-compose.yml"

COMPOSE_FILE=""
HVAC_PATH="/app/HVAC_ideas/hvac-technician/hvac_expert.py"

echo "🔧 Virtual HVAC Technician Quick Start"
echo "======================================"
echo ""
echo "Choose an option:"
echo "1. Interactive Mode (chat with HVAC expert)"
echo "2. Single Question Mode"
echo "3. Test with example question"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
  1)
    echo ""
    echo "Starting interactive mode..."
    docker compose $COMPOSE_FILE exec crewai python $HVAC_PATH
    ;;
  2)
    echo ""
    read -p "Enter your HVAC question: " question
    docker compose $COMPOSE_FILE exec crewai python $HVAC_PATH "$question"
    ;;
  3)
    echo ""
    echo "Testing with example question..."
    docker compose $COMPOSE_FILE exec crewai python $HVAC_PATH "How often should I change my HVAC filter?"
    ;;
  *)
    echo "Invalid choice"
    exit 1
    ;;
esac
