#!/usr/bin/env python3
"""
JSON Storage Abstraction for MCP Thought-to-Action System

Provides atomic writes, file locking, and backup utilities for:
- TODO lists (todos.json)
- Mind maps (mindmaps/{id}.json)
- System metadata (metadata.json)

Following existing patterns from agent_coordinator.py and cluster_stories.py.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import fcntl
import time

logger = logging.getLogger("mcp_server.storage")


class StorageError(Exception):
    """Base exception for storage operations."""
    pass


class JSONStorage:
    """
    Base class for JSON file storage with atomic writes and file locking.

    Features:
    - Automatic directory creation
    - Atomic writes (write to temp, then rename)
    - File locking for concurrent access
    - Backup on corruption
    - Version tracking
    """

    def __init__(self, file_path: Path):
        """
        Initialize storage for a JSON file.

        Args:
            file_path: Path to the JSON file
        """
        self.file_path = Path(file_path)
        self.lock_file = Path(str(file_path) + ".lock")
        self._ensure_directory()

    def _ensure_directory(self):
        """Create parent directory if it doesn't exist."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def _acquire_lock(self, timeout: int = 5) -> Optional[int]:
        """
        Acquire file lock with timeout.

        Args:
            timeout: Maximum seconds to wait for lock

        Returns:
            File descriptor if lock acquired, None otherwise
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                fd = open(self.lock_file, 'w')
                fcntl.flock(fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return fd.fileno()
            except (IOError, OSError):
                time.sleep(0.1)  # Wait 100ms before retry

        logger.warning(f"Failed to acquire lock for {self.file_path} after {timeout}s")
        return None

    def _release_lock(self, fd: int):
        """Release file lock."""
        if fd is not None:
            try:
                fcntl.flock(fd, fcntl.LOCK_UN)
                import os
                os.close(fd)
                if self.lock_file.exists():
                    self.lock_file.unlink()
            except Exception as e:
                logger.warning(f"Error releasing lock: {e}")

    def _read_raw(self) -> Optional[Dict[str, Any]]:
        """
        Read JSON file without locking (internal use).

        Returns:
            Parsed JSON data or None if file doesn't exist
        """
        if not self.file_path.exists():
            return None

        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Corrupted JSON in {self.file_path}: {e}")
            self._backup_corrupted_file()
            return None
        except Exception as e:
            logger.error(f"Error reading {self.file_path}: {e}")
            return None

    def _write_raw(self, data: Dict[str, Any]):
        """
        Write JSON file atomically without locking (internal use).

        Args:
            data: Data to write
        """
        # Update timestamp
        data["last_updated"] = datetime.now().isoformat()

        # Write to temporary file first
        temp_file = Path(str(self.file_path) + ".tmp")
        try:
            with open(temp_file, 'w') as f:
                json.dump(data, f, indent=2)

            # Atomic rename
            temp_file.replace(self.file_path)
            logger.debug(f"Wrote {self.file_path}")
        except Exception as e:
            logger.error(f"Error writing {self.file_path}: {e}")
            if temp_file.exists():
                temp_file.unlink()
            raise StorageError(f"Failed to write {self.file_path}: {e}")

    def _backup_corrupted_file(self):
        """Create backup of corrupted file."""
        if not self.file_path.exists():
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = Path(str(self.file_path) + f".corrupted.{timestamp}")

        try:
            import shutil
            shutil.copy2(self.file_path, backup_path)
            logger.info(f"Backed up corrupted file to {backup_path}")
        except Exception as e:
            logger.error(f"Failed to backup corrupted file: {e}")

    def read(self) -> Optional[Dict[str, Any]]:
        """
        Read JSON file with locking.

        Returns:
            Parsed JSON data or None if file doesn't exist
        """
        fd = self._acquire_lock()
        if fd is None:
            raise StorageError(f"Could not acquire lock for {self.file_path}")

        try:
            return self._read_raw()
        finally:
            self._release_lock(fd)

    def write(self, data: Dict[str, Any]):
        """
        Write JSON file with locking.

        Args:
            data: Data to write
        """
        fd = self._acquire_lock()
        if fd is None:
            raise StorageError(f"Could not acquire lock for {self.file_path}")

        try:
            self._write_raw(data)
        finally:
            self._release_lock(fd)


class TodoStorage(JSONStorage):
    """
    Storage manager for TODO lists.

    File format:
    {
        "version": "1.0",
        "last_updated": "ISO timestamp",
        "todos": [
            {
                "id": "todo_YYYYMMDD_HHMMSS_uuid",
                "title": "...",
                "description": "...",
                "priority": "low|medium|high",
                "status": "pending|in_progress|completed",
                "tags": [...],
                "created_at": "ISO timestamp",
                "updated_at": "ISO timestamp",
                "due_date": "ISO timestamp or null",
                "completed_at": "ISO timestamp or null"
            }
        ]
    }
    """

    def __init__(self, file_path: Path):
        super().__init__(file_path)
        self._ensure_initialized()

    def _ensure_initialized(self):
        """Initialize file with empty structure if it doesn't exist."""
        if not self.file_path.exists():
            initial_data = {
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "todos": []
            }
            self.write(initial_data)
            logger.info(f"Initialized TODO storage at {self.file_path}")

    def get_all_todos(self) -> List[Dict[str, Any]]:
        """
        Get all TODO items.

        Returns:
            List of TODO dictionaries
        """
        data = self.read()
        if data is None:
            return []
        return data.get("todos", [])

    def add_todo(self, todo: Dict[str, Any]) -> bool:
        """
        Add a new TODO item.

        Args:
            todo: TODO dictionary with all required fields

        Returns:
            True if added successfully
        """
        data = self.read()
        if data is None:
            data = {"version": "1.0", "todos": []}

        data["todos"].append(todo)
        self.write(data)
        logger.info(f"Added TODO: {todo['id']}")
        return True

    def update_todo(self, todo_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update an existing TODO item.

        Args:
            todo_id: ID of TODO to update
            updates: Dictionary of fields to update

        Returns:
            True if updated, False if not found
        """
        data = self.read()
        if data is None:
            return False

        for todo in data["todos"]:
            if todo["id"] == todo_id:
                todo.update(updates)
                todo["updated_at"] = datetime.now().isoformat()
                self.write(data)
                logger.info(f"Updated TODO: {todo_id}")
                return True

        logger.warning(f"TODO not found for update: {todo_id}")
        return False

    def delete_todo(self, todo_id: str) -> bool:
        """
        Delete a TODO item.

        Args:
            todo_id: ID of TODO to delete

        Returns:
            True if deleted, False if not found
        """
        data = self.read()
        if data is None:
            return False

        original_count = len(data["todos"])
        data["todos"] = [t for t in data["todos"] if t["id"] != todo_id]

        if len(data["todos"]) < original_count:
            self.write(data)
            logger.info(f"Deleted TODO: {todo_id}")
            return True

        logger.warning(f"TODO not found for deletion: {todo_id}")
        return False

    def get_todo_by_id(self, todo_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific TODO by ID.

        Args:
            todo_id: ID of TODO to retrieve

        Returns:
            TODO dictionary or None if not found
        """
        data = self.read()
        if data is None:
            return None

        for todo in data["todos"]:
            if todo["id"] == todo_id:
                return todo

        return None


class MindMapStorage:
    """
    Storage manager for mind maps.

    Each mind map is stored in a separate JSON file:
    mindmaps/{mindmap_id}.json

    Index file tracks all mind maps:
    mindmaps/index.json
    """

    def __init__(self, mindmaps_dir: Path):
        """
        Initialize mind map storage.

        Args:
            mindmaps_dir: Directory to store mind map files
        """
        self.mindmaps_dir = Path(mindmaps_dir)
        self.mindmaps_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.mindmaps_dir / "index.json"
        self._ensure_index()

    def _ensure_index(self):
        """Initialize index file if it doesn't exist."""
        if not self.index_file.exists():
            initial_index = {
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "mindmaps": []
            }
            with open(self.index_file, 'w') as f:
                json.dump(initial_index, f, indent=2)
            logger.info(f"Initialized mind map index at {self.index_file}")

    def save_mindmap(self, mindmap: Dict[str, Any]) -> bool:
        """
        Save a mind map to disk.

        Args:
            mindmap: Mind map dictionary

        Returns:
            True if saved successfully
        """
        mindmap_id = mindmap["id"]
        file_path = self.mindmaps_dir / f"{mindmap_id}.json"

        try:
            # Save mind map file
            storage = JSONStorage(file_path)
            storage.write(mindmap)

            # Update index
            self._update_index(mindmap_id, mindmap["title"])

            logger.info(f"Saved mind map: {mindmap_id}")
            return True
        except Exception as e:
            logger.error(f"Error saving mind map {mindmap_id}: {e}")
            return False

    def load_mindmap(self, mindmap_id: str) -> Optional[Dict[str, Any]]:
        """
        Load a mind map from disk.

        Args:
            mindmap_id: ID of mind map to load

        Returns:
            Mind map dictionary or None if not found
        """
        file_path = self.mindmaps_dir / f"{mindmap_id}.json"

        if not file_path.exists():
            logger.warning(f"Mind map not found: {mindmap_id}")
            return None

        try:
            storage = JSONStorage(file_path)
            return storage.read()
        except Exception as e:
            logger.error(f"Error loading mind map {mindmap_id}: {e}")
            return None

    def delete_mindmap(self, mindmap_id: str) -> bool:
        """
        Delete a mind map.

        Args:
            mindmap_id: ID of mind map to delete

        Returns:
            True if deleted, False if not found
        """
        file_path = self.mindmaps_dir / f"{mindmap_id}.json"

        if not file_path.exists():
            logger.warning(f"Mind map not found for deletion: {mindmap_id}")
            return False

        try:
            file_path.unlink()
            self._remove_from_index(mindmap_id)
            logger.info(f"Deleted mind map: {mindmap_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting mind map {mindmap_id}: {e}")
            return False

    def list_mindmaps(self) -> List[Dict[str, str]]:
        """
        List all mind maps.

        Returns:
            List of {id, title, created_at} dictionaries
        """
        try:
            with open(self.index_file, 'r') as f:
                index = json.load(f)
            return index.get("mindmaps", [])
        except Exception as e:
            logger.error(f"Error listing mind maps: {e}")
            return []

    def _update_index(self, mindmap_id: str, title: str):
        """Update index with new/updated mind map."""
        try:
            with open(self.index_file, 'r') as f:
                index = json.load(f)

            # Check if already in index
            existing = [m for m in index["mindmaps"] if m["id"] == mindmap_id]

            if not existing:
                # Add new entry
                index["mindmaps"].append({
                    "id": mindmap_id,
                    "title": title,
                    "created_at": datetime.now().isoformat()
                })
            else:
                # Update title
                for m in index["mindmaps"]:
                    if m["id"] == mindmap_id:
                        m["title"] = title

            index["last_updated"] = datetime.now().isoformat()

            with open(self.index_file, 'w') as f:
                json.dump(index, f, indent=2)
        except Exception as e:
            logger.error(f"Error updating index: {e}")

    def _remove_from_index(self, mindmap_id: str):
        """Remove mind map from index."""
        try:
            with open(self.index_file, 'r') as f:
                index = json.load(f)

            index["mindmaps"] = [m for m in index["mindmaps"] if m["id"] != mindmap_id]
            index["last_updated"] = datetime.now().isoformat()

            with open(self.index_file, 'w') as f:
                json.dump(index, f, indent=2)
        except Exception as e:
            logger.error(f"Error removing from index: {e}")
