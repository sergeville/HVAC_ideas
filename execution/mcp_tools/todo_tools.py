#!/usr/bin/env python3
"""
TODO List Management Tools for MCP Thought-to-Action System

Provides CRUD operations for TODO items with filtering, tagging, and priority management.
Uses dataclass pattern from agent_coordinator.py for structured data.
"""

import logging
import uuid
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any
from pathlib import Path

from .storage import TodoStorage

logger = logging.getLogger("mcp_server.todo_tools")


@dataclass
class TodoItem:
    """
    TODO item data structure.

    Following dataclass pattern from agent_coordinator.py.
    """
    id: str
    title: str
    description: str
    priority: str  # low, medium, high
    tags: List[str]
    status: str  # pending, in_progress, completed, cancelled
    created_at: str  # ISO timestamp
    updated_at: str  # ISO timestamp
    due_date: Optional[str] = None  # ISO timestamp or None
    completed_at: Optional[str] = None  # ISO timestamp or None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TodoItem':
        """Create TodoItem from dictionary."""
        return cls(**data)

    def __post_init__(self):
        """Validate fields after initialization."""
        if self.priority not in ['low', 'medium', 'high']:
            raise ValueError(f"Invalid priority: {self.priority}")
        if self.status not in ['pending', 'in_progress', 'completed', 'cancelled']:
            raise ValueError(f"Invalid status: {self.status}")


@dataclass
class AddTodoOutput:
    """Output from adding a TODO."""
    success: bool
    todo: Optional[TodoItem]
    message: str


@dataclass
class UpdateTodoOutput:
    """Output from updating a TODO."""
    success: bool
    todo: Optional[TodoItem]
    message: str


@dataclass
class ListTodosOutput:
    """Output from listing TODOs."""
    todos: List[TodoItem]
    count: int
    filters_applied: Dict[str, Any]


@dataclass
class DeleteTodoOutput:
    """Output from deleting a TODO."""
    success: bool
    message: str


class TodoManager:
    """
    High-level manager for TODO list operations.

    Usage:
        manager = TodoManager(Path(".tmp/user_data/todos.json"))
        result = manager.add_todo("Review documentation", priority="high", tags=["docs"])
        print(result.message)
    """

    def __init__(self, storage_file: Path):
        """
        Initialize TODO manager.

        Args:
            storage_file: Path to todos.json file
        """
        self.storage = TodoStorage(storage_file)
        logger.info(f"TODO manager initialized with storage: {storage_file}")

    def _generate_todo_id(self) -> str:
        """
        Generate unique TODO ID.

        Format: todo_YYYYMMDD_HHMMSS_uuid
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        return f"todo_{timestamp}_{unique_id}"

    def add_todo(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        tags: Optional[List[str]] = None,
        due_date: Optional[str] = None
    ) -> AddTodoOutput:
        """
        Add a new TODO item.

        Args:
            title: TODO title (required)
            description: Detailed description (optional)
            priority: Priority level: low, medium, high (default: medium)
            tags: List of tags (optional)
            due_date: Due date in ISO format (optional)

        Returns:
            AddTodoOutput with success status and TODO item
        """
        # Validate inputs
        if not title or not title.strip():
            return AddTodoOutput(
                success=False,
                todo=None,
                message="Title cannot be empty"
            )

        if priority not in ['low', 'medium', 'high']:
            return AddTodoOutput(
                success=False,
                todo=None,
                message=f"Invalid priority: {priority}. Must be low, medium, or high"
            )

        # Validate title length
        if len(title) > 200:
            return AddTodoOutput(
                success=False,
                todo=None,
                message="Title too long (max 200 characters)"
            )

        # Validate description length
        if len(description) > 2000:
            return AddTodoOutput(
                success=False,
                todo=None,
                message="Description too long (max 2000 characters)"
            )

        try:
            # Create TODO item
            now = datetime.now().isoformat()
            todo = TodoItem(
                id=self._generate_todo_id(),
                title=title.strip(),
                description=description.strip(),
                priority=priority,
                tags=tags or [],
                status="pending",
                created_at=now,
                updated_at=now,
                due_date=due_date,
                completed_at=None
            )

            # Save to storage
            self.storage.add_todo(todo.to_dict())

            logger.info(f"Added TODO: {todo.id} - {todo.title}")
            return AddTodoOutput(
                success=True,
                todo=todo,
                message=f"TODO created: {todo.title}"
            )

        except Exception as e:
            logger.error(f"Error adding TODO: {e}")
            return AddTodoOutput(
                success=False,
                todo=None,
                message=f"Error: {str(e)}"
            )

    def list_todos(
        self,
        status: Optional[str] = None,
        tags: Optional[List[str]] = None,
        priority: Optional[str] = None
    ) -> ListTodosOutput:
        """
        List TODO items with optional filtering.

        Args:
            status: Filter by status (pending, in_progress, completed, cancelled)
            tags: Filter by tags (any tag match)
            priority: Filter by priority (low, medium, high)

        Returns:
            ListTodosOutput with filtered TODOs and count
        """
        try:
            # Get all TODOs
            all_todos = self.storage.get_all_todos()
            todos = [TodoItem.from_dict(t) for t in all_todos]

            # Apply filters
            filters_applied = {}

            if status:
                todos = [t for t in todos if t.status == status]
                filters_applied['status'] = status

            if tags:
                todos = [t for t in todos if any(tag in t.tags for tag in tags)]
                filters_applied['tags'] = tags

            if priority:
                todos = [t for t in todos if t.priority == priority]
                filters_applied['priority'] = priority

            logger.info(f"Listed {len(todos)} TODOs (filters: {filters_applied})")
            return ListTodosOutput(
                todos=todos,
                count=len(todos),
                filters_applied=filters_applied
            )

        except Exception as e:
            logger.error(f"Error listing TODOs: {e}")
            return ListTodosOutput(
                todos=[],
                count=0,
                filters_applied={}
            )

    def update_todo(
        self,
        todo_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[List[str]] = None,
        due_date: Optional[str] = None
    ) -> UpdateTodoOutput:
        """
        Update an existing TODO item.

        Args:
            todo_id: ID of TODO to update
            title: New title (optional)
            description: New description (optional)
            status: New status (optional)
            priority: New priority (optional)
            tags: New tags list (optional)
            due_date: New due date (optional)

        Returns:
            UpdateTodoOutput with success status and updated TODO
        """
        try:
            # Get existing TODO
            todo_dict = self.storage.get_todo_by_id(todo_id)
            if not todo_dict:
                return UpdateTodoOutput(
                    success=False,
                    todo=None,
                    message=f"TODO not found: {todo_id}"
                )

            # Build updates dictionary
            updates = {}
            if title is not None:
                if not title.strip():
                    return UpdateTodoOutput(
                        success=False,
                        todo=None,
                        message="Title cannot be empty"
                    )
                updates['title'] = title.strip()

            if description is not None:
                updates['description'] = description.strip()

            if status is not None:
                if status not in ['pending', 'in_progress', 'completed', 'cancelled']:
                    return UpdateTodoOutput(
                        success=False,
                        todo=None,
                        message=f"Invalid status: {status}"
                    )
                updates['status'] = status

                # Set completed_at if status is completed
                if status == 'completed' and not todo_dict.get('completed_at'):
                    updates['completed_at'] = datetime.now().isoformat()

            if priority is not None:
                if priority not in ['low', 'medium', 'high']:
                    return UpdateTodoOutput(
                        success=False,
                        todo=None,
                        message=f"Invalid priority: {priority}"
                    )
                updates['priority'] = priority

            if tags is not None:
                updates['tags'] = tags

            if due_date is not None:
                updates['due_date'] = due_date

            # Update in storage
            self.storage.update_todo(todo_id, updates)

            # Get updated TODO
            updated_dict = self.storage.get_todo_by_id(todo_id)
            updated_todo = TodoItem.from_dict(updated_dict)

            logger.info(f"Updated TODO: {todo_id}")
            return UpdateTodoOutput(
                success=True,
                todo=updated_todo,
                message=f"TODO updated: {updated_todo.title}"
            )

        except Exception as e:
            logger.error(f"Error updating TODO {todo_id}: {e}")
            return UpdateTodoOutput(
                success=False,
                todo=None,
                message=f"Error: {str(e)}"
            )

    def complete_todo(self, todo_id: str) -> UpdateTodoOutput:
        """
        Mark a TODO as completed.

        Args:
            todo_id: ID of TODO to complete

        Returns:
            UpdateTodoOutput with success status
        """
        return self.update_todo(
            todo_id,
            status='completed'
        )

    def delete_todo(self, todo_id: str) -> DeleteTodoOutput:
        """
        Delete a TODO item.

        Args:
            todo_id: ID of TODO to delete

        Returns:
            DeleteTodoOutput with success status
        """
        try:
            success = self.storage.delete_todo(todo_id)

            if success:
                logger.info(f"Deleted TODO: {todo_id}")
                return DeleteTodoOutput(
                    success=True,
                    message=f"TODO deleted: {todo_id}"
                )
            else:
                return DeleteTodoOutput(
                    success=False,
                    message=f"TODO not found: {todo_id}"
                )

        except Exception as e:
            logger.error(f"Error deleting TODO {todo_id}: {e}")
            return DeleteTodoOutput(
                success=False,
                message=f"Error: {str(e)}"
            )

    def get_todo_by_id(self, todo_id: str) -> Optional[TodoItem]:
        """
        Get a specific TODO by ID.

        Args:
            todo_id: ID of TODO to retrieve

        Returns:
            TodoItem or None if not found
        """
        try:
            todo_dict = self.storage.get_todo_by_id(todo_id)
            if todo_dict:
                return TodoItem.from_dict(todo_dict)
            return None
        except Exception as e:
            logger.error(f"Error getting TODO {todo_id}: {e}")
            return None

    def search_todos(self, query: str) -> List[TodoItem]:
        """
        Search TODOs by title or description.

        Args:
            query: Search query

        Returns:
            List of matching TodoItems
        """
        try:
            all_todos = self.storage.get_all_todos()
            query_lower = query.lower()

            matching_todos = []
            for todo_dict in all_todos:
                title = todo_dict.get('title', '').lower()
                description = todo_dict.get('description', '').lower()

                if query_lower in title or query_lower in description:
                    matching_todos.append(TodoItem.from_dict(todo_dict))

            logger.info(f"Found {len(matching_todos)} TODOs matching '{query}'")
            return matching_todos

        except Exception as e:
            logger.error(f"Error searching TODOs: {e}")
            return []
