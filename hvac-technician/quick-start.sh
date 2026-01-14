#!/bin/bash
# Quick start script for Virtual HVAC Technician

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
    docker compose exec crewai python /app/hvac-technician/hvac_expert.py
    ;;
  2)
    echo ""
    read -p "Enter your HVAC question: " question
    docker compose exec crewai python /app/hvac-technician/hvac_expert.py "$question"
    ;;
  3)
    echo ""
    echo "Testing with example question..."
    docker compose exec crewai python /app/hvac-technician/hvac_expert.py "How often should I change my HVAC filter?"
    ;;
  *)
    echo "Invalid choice"
    exit 1
    ;;
esac
