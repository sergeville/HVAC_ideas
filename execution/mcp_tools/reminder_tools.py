#!/usr/bin/env python3
"""
Reminder Management Tools for MCP Thought-to-Action System

Provides integration with macOS Reminders app through AppleScript.
Wraps the existing scripts/create_reminder.sh for reminder creation.

Cross-platform: macOS full support, graceful fallback on other platforms.
"""

import os
import platform
import subprocess
import logging
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, List
from datetime import datetime, timedelta

logger = logging.getLogger("mcp_server.reminder_tools")


@dataclass
class CreateReminderOutput:
    """Output from reminder creation."""
    success: bool
    reminder_id: str
    scheduled_time: str
    message: str


@dataclass
class ReminderItem:
    """Reminder data structure."""
    id: str
    title: str
    notes: str
    due_date: str
    completed: bool


class ReminderBackend:
    """Abstract base for reminder backends."""

    def create_reminder(self, title: str, notes: str = "", hours_from_now: int = 4) -> CreateReminderOutput:
        """Create a reminder."""
        raise NotImplementedError

    def list_reminders(self) -> List[ReminderItem]:
        """List all reminders."""
        raise NotImplementedError

    def cancel_reminder(self, reminder_id: str) -> bool:
        """Cancel a reminder."""
        raise NotImplementedError


class MacOSReminderBackend(ReminderBackend):
    """
    macOS-specific backend using AppleScript.

    Wraps the existing scripts/create_reminder.sh for creation.
    Uses direct AppleScript for listing and cancellation.
    """

    def __init__(self, reminder_list_name: str = "Claude Reminders"):
        """
        Initialize macOS reminder backend.

        Args:
            reminder_list_name: Name of Reminders list to use
        """
        self.reminder_list_name = reminder_list_name
        self.project_root = Path(__file__).parent.parent.parent
        self.create_script = self.project_root / "scripts" / "create_reminder.sh"

        if not self.create_script.exists():
            logger.warning(f"create_reminder.sh not found at {self.create_script}")

    def create_reminder(self, title: str, notes: str = "", hours_from_now: int = 4) -> CreateReminderOutput:
        """
        Create reminder using existing create_reminder.sh script.

        Args:
            title: Reminder title
            notes: Additional notes (optional)
            hours_from_now: Hours until reminder (default: 4)

        Returns:
            CreateReminderOutput with success status and details
        """
        if not self.create_script.exists():
            return CreateReminderOutput(
                success=False,
                reminder_id="",
                scheduled_time="",
                message=f"Script not found: {self.create_script}"
            )

        try:
            # Set environment variable for hours
            env = os.environ.copy()
            env['HOURS'] = str(hours_from_now)

            # Call the existing script
            result = subprocess.run(
                [str(self.create_script), title, notes],
                capture_output=True,
                text=True,
                env=env,
                timeout=30
            )

            if result.returncode == 0:
                # Calculate scheduled time
                scheduled_time = (datetime.now() + timedelta(hours=hours_from_now)).strftime("%Y-%m-%d %H:%M:%S")

                # Generate reminder ID (timestamp-based)
                reminder_id = f"reminder_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

                return CreateReminderOutput(
                    success=True,
                    reminder_id=reminder_id,
                    scheduled_time=scheduled_time,
                    message=f"Reminder '{title}' set for {hours_from_now} hours from now"
                )
            else:
                logger.error(f"Script failed: {result.stderr}")
                return CreateReminderOutput(
                    success=False,
                    reminder_id="",
                    scheduled_time="",
                    message=f"Failed to create reminder: {result.stderr}"
                )

        except subprocess.TimeoutExpired:
            logger.error("Script timeout")
            return CreateReminderOutput(
                success=False,
                reminder_id="",
                scheduled_time="",
                message="Reminder creation timed out"
            )
        except Exception as e:
            logger.error(f"Error creating reminder: {e}")
            return CreateReminderOutput(
                success=False,
                reminder_id="",
                scheduled_time="",
                message=f"Error: {str(e)}"
            )

    def list_reminders(self) -> List[ReminderItem]:
        """
        List reminders from Claude Reminders list using AppleScript.

        Returns:
            List of ReminderItem objects
        """
        applescript = f'''
tell application "Reminders"
    set output to ""
    repeat with aList in lists
        if name of aList is "{self.reminder_list_name}" then
            repeat with aReminder in reminders of aList
                set reminderName to name of aReminder
                set reminderBody to body of aReminder
                set reminderDue to remind me date of aReminder as string
                set reminderCompleted to completed of aReminder as string
                set reminderID to id of aReminder
                set output to output & reminderID & "|||" & reminderName & "|||" & reminderBody & "|||" & reminderDue & "|||" & reminderCompleted & "\\n"
            end repeat
        end if
    end repeat
    return output
end tell
'''

        try:
            result = subprocess.run(
                ['osascript', '-e', applescript],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                logger.error(f"AppleScript failed: {result.stderr}")
                return []

            reminders = []
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if not line:
                    continue
                parts = line.split('|||')
                if len(parts) >= 5:
                    reminders.append(ReminderItem(
                        id=parts[0],
                        title=parts[1],
                        notes=parts[2],
                        due_date=parts[3],
                        completed=parts[4].lower() == 'true'
                    ))

            logger.info(f"Listed {len(reminders)} reminders")
            return reminders

        except Exception as e:
            logger.error(f"Error listing reminders: {e}")
            return []

    def cancel_reminder(self, reminder_id: str) -> bool:
        """
        Cancel (delete) a reminder by ID or fuzzy title match.

        Args:
            reminder_id: ID or title of reminder to cancel

        Returns:
            True if cancelled, False otherwise
        """
        # Try exact ID match first
        applescript = f'''
tell application "Reminders"
    repeat with aList in lists
        if name of aList is "{self.reminder_list_name}" then
            repeat with aReminder in reminders of aList
                if id of aReminder is "{reminder_id}" then
                    delete aReminder
                    return "success"
                end if
            end repeat
        end if
    end repeat

    -- Try fuzzy title match
    repeat with aList in lists
        if name of aList is "{self.reminder_list_name}" then
            repeat with aReminder in reminders of aList
                if name of aReminder contains "{reminder_id}" then
                    delete aReminder
                    return "success"
                end if
            end repeat
        end if
    end repeat

    return "not_found"
end tell
'''

        try:
            result = subprocess.run(
                ['osascript', '-e', applescript],
                capture_output=True,
                text=True,
                timeout=10
            )

            if "success" in result.stdout:
                logger.info(f"Cancelled reminder: {reminder_id}")
                return True
            else:
                logger.warning(f"Reminder not found: {reminder_id}")
                return False

        except Exception as e:
            logger.error(f"Error cancelling reminder: {e}")
            return False


class GenericReminderBackend(ReminderBackend):
    """
    Fallback backend for non-macOS platforms.

    Stores reminders in JSON file and warns user that OS integration
    is not available.
    """

    def __init__(self, storage_file: Path):
        """
        Initialize generic reminder backend.

        Args:
            storage_file: Path to JSON file for storing reminders
        """
        from .storage import JSONStorage
        self.storage = JSONStorage(storage_file)
        self._ensure_initialized()

    def _ensure_initialized(self):
        """Initialize storage file if needed."""
        data = self.storage.read()
        if data is None:
            self.storage.write({
                "version": "1.0",
                "reminders": []
            })

    def create_reminder(self, title: str, notes: str = "", hours_from_now: int = 4) -> CreateReminderOutput:
        """
        Store reminder in JSON (no OS integration).

        Args:
            title: Reminder title
            notes: Additional notes
            hours_from_now: Hours until reminder

        Returns:
            CreateReminderOutput with warning message
        """
        try:
            scheduled_time = (datetime.now() + timedelta(hours=hours_from_now)).isoformat()
            reminder_id = f"reminder_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            data = self.storage.read()
            data["reminders"].append({
                "id": reminder_id,
                "title": title,
                "notes": notes,
                "due_date": scheduled_time,
                "completed": False,
                "created_at": datetime.now().isoformat()
            })
            self.storage.write(data)

            return CreateReminderOutput(
                success=True,
                reminder_id=reminder_id,
                scheduled_time=scheduled_time,
                message=f"Reminder stored (OS integration not available on {platform.system()})"
            )

        except Exception as e:
            logger.error(f"Error storing reminder: {e}")
            return CreateReminderOutput(
                success=False,
                reminder_id="",
                scheduled_time="",
                message=f"Error: {str(e)}"
            )

    def list_reminders(self) -> List[ReminderItem]:
        """List reminders from JSON storage."""
        try:
            data = self.storage.read()
            if data is None:
                return []

            return [
                ReminderItem(
                    id=r["id"],
                    title=r["title"],
                    notes=r["notes"],
                    due_date=r["due_date"],
                    completed=r["completed"]
                )
                for r in data.get("reminders", [])
            ]

        except Exception as e:
            logger.error(f"Error listing reminders: {e}")
            return []

    def cancel_reminder(self, reminder_id: str) -> bool:
        """Delete reminder from JSON storage."""
        try:
            data = self.storage.read()
            if data is None:
                return False

            original_count = len(data["reminders"])
            data["reminders"] = [r for r in data["reminders"] if r["id"] != reminder_id]

            if len(data["reminders"]) < original_count:
                self.storage.write(data)
                logger.info(f"Cancelled reminder: {reminder_id}")
                return True

            return False

        except Exception as e:
            logger.error(f"Error cancelling reminder: {e}")
            return False


class ReminderManager:
    """
    High-level manager for reminders with automatic platform detection.

    Usage:
        manager = ReminderManager()
        result = manager.create_reminder("Test backup drive", "Run: ls /Volumes/", hours_from_now=2)
        print(result.message)
    """

    def __init__(self, reminder_list_name: str = "Claude Reminders"):
        """
        Initialize reminder manager with platform-appropriate backend.

        Args:
            reminder_list_name: Name of Reminders list (macOS only)
        """
        self.platform = platform.system()
        self.reminder_list_name = reminder_list_name

        if self.platform == "Darwin":
            # macOS - use AppleScript backend
            self.backend = MacOSReminderBackend(reminder_list_name)
            logger.info("Using macOS Reminders backend")
        else:
            # Other platforms - use JSON fallback
            fallback_file = Path.home() / ".tmp" / "user_data" / "reminders.json"
            self.backend = GenericReminderBackend(fallback_file)
            logger.warning(f"Using fallback backend for {self.platform}")

    def create_reminder(self, title: str, notes: str = "", hours_from_now: int = 4) -> CreateReminderOutput:
        """
        Create a reminder.

        Args:
            title: Reminder title
            notes: Additional notes (optional)
            hours_from_now: Hours until reminder (default: 4)

        Returns:
            CreateReminderOutput with success status and details
        """
        return self.backend.create_reminder(title, notes, hours_from_now)

    def list_reminders(self) -> List[ReminderItem]:
        """
        List all reminders.

        Returns:
            List of ReminderItem objects
        """
        return self.backend.list_reminders()

    def cancel_reminder(self, reminder_id: str) -> bool:
        """
        Cancel a reminder.

        Args:
            reminder_id: ID or title fragment of reminder to cancel

        Returns:
            True if cancelled, False if not found
        """
        return self.backend.cancel_reminder(reminder_id)
