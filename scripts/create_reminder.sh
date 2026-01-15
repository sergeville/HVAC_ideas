#!/bin/bash
################################################################################
# macOS Reminder Creation Tool
################################################################################
#
# DESCRIPTION:
#   Creates reminders in macOS Reminders app with customizable content.
#   Can be used for project tasks, testing reminders, or general todos.
#
# USAGE:
#   ./scripts/create_reminder.sh                    # Interactive mode
#   ./scripts/create_reminder.sh "Title" "Notes"    # Quick mode
#
# EXAMPLES:
#   # Interactive mode - will prompt for details
#   ./scripts/create_reminder.sh
#
#   # Quick mode - create reminder with title and notes
#   ./scripts/create_reminder.sh "Test backup drive" "Run ls /Volumes/"
#
#   # Create a reminder for 2 hours from now
#   HOURS=2 ./scripts/create_reminder.sh "Check logs" "Review system logs"
#
# ENVIRONMENT VARIABLES:
#   HOURS - Number of hours from now to set reminder (default: 4)
#
# REQUIREMENTS:
#   - macOS with Reminders app
#   - AppleScript enabled
#
################################################################################

# Default reminder time (hours from now)
HOURS=${HOURS:-4}

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

################################################################################
# Interactive Mode - Prompt for reminder details
################################################################################

if [ $# -eq 0 ]; then
    echo -e "${BLUE}=== macOS Reminder Creator ===${NC}"
    echo ""

    # Get reminder title
    echo -e "${YELLOW}Enter reminder title:${NC}"
    read -r REMINDER_TITLE

    if [ -z "$REMINDER_TITLE" ]; then
        echo "Error: Title cannot be empty"
        exit 1
    fi

    # Get reminder notes
    echo ""
    echo -e "${YELLOW}Enter reminder notes (press Ctrl+D when done):${NC}"
    REMINDER_NOTES=$(cat)

    # Get hours from now
    echo ""
    echo -e "${YELLOW}Hours from now to remind (default: $HOURS):${NC}"
    read -r HOURS_INPUT

    if [ -n "$HOURS_INPUT" ]; then
        HOURS=$HOURS_INPUT
    fi

################################################################################
# Quick Mode - Use command line arguments
################################################################################

elif [ $# -eq 2 ]; then
    REMINDER_TITLE="$1"
    REMINDER_NOTES="$2"
    echo -e "${BLUE}Creating reminder: $REMINDER_TITLE${NC}"

else
    echo "Usage:"
    echo "  $0                    # Interactive mode"
    echo "  $0 \"Title\" \"Notes\"   # Quick mode"
    echo ""
    echo "Environment Variables:"
    echo "  HOURS=2 $0 ...       # Set reminder for 2 hours from now"
    exit 1
fi

################################################################################
# Create Reminder Using AppleScript
################################################################################

echo ""
echo -e "${BLUE}Creating reminder in Reminders app...${NC}"

osascript << APPLESCRIPT
tell application "Reminders"
    -- Get the first available list
    set theList to list 1

    -- Create the reminder
    tell theList
        set newReminder to make new reminder with properties {name:"$REMINDER_TITLE"}

        -- Set reminder date
        set remind me date of newReminder to (current date) + ($HOURS * hours)

        -- Add notes if provided
        set body of newReminder to "$REMINDER_NOTES"
    end tell

    -- Show notification
    display notification "Reminder set for $HOURS hours from now" with title "✓ Reminder Created" subtitle "$REMINDER_TITLE"
end tell
APPLESCRIPT

################################################################################
# Verify and Display Result
################################################################################

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Reminder created successfully!${NC}"
    echo ""
    echo "📱 Details:"
    echo "  Title: $REMINDER_TITLE"
    echo "  Time:  $HOURS hours from now"
    echo "  Notes: $(echo "$REMINDER_NOTES" | head -c 50)..."
    echo ""
    echo "Check your Reminders app to view or edit the reminder."
else
    echo ""
    echo -e "${RED}❌ Error creating reminder${NC}"
    echo "Please check that Reminders app is accessible and try again."
    exit 1
fi
