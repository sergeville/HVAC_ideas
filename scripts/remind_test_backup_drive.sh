#!/bin/bash
################################################################################
# Quick Reminder: Test Backup Drive Configuration
################################################################################
#
# DESCRIPTION:
#   Creates a reminder to test that backup drives stay connected on AC power.
#   This is a convenience script that calls create_reminder.sh with preset
#   content for backup drive testing.
#
# USAGE:
#   ./scripts/remind_test_backup_drive.sh [HOURS]
#
# EXAMPLES:
#   ./scripts/remind_test_backup_drive.sh      # Remind in 4 hours (default)
#   ./scripts/remind_test_backup_drive.sh 2    # Remind in 2 hours
#
################################################################################

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Hours from now (default: 4)
HOURS=${1:-4}

# Reminder content
TITLE="Test Backup Drive - Leave Mac idle 30 min on AC power"

NOTES="Test Steps:
1. Mac plugged into 120V AC ✓
2. Leave idle for 30+ minutes
3. Run: ls /Volumes/ | grep Backup
4. Should see both backup drives = SUCCESS!

Power config applied:
- AC Power: disksleep 0 (drives never unmount)
- Battery: disksleep 10 (drives unmount after 10 min)

To verify settings anytime:
pmset -g custom

Location: HVAC_ideas project"

# Create the reminder using the general tool
HOURS=$HOURS "$SCRIPT_DIR/create_reminder.sh" "$TITLE" "$NOTES"
