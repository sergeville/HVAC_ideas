#!/usr/bin/env python3
"""
MCP Server for Thought-to-Action System

Provides natural language interface for:
- Reminders (macOS Reminders app integration)
- TODO lists (JSON storage with filtering)
- Mind maps (Tree structure with export)

Follows 3-layer architecture:
- Layer 1: directives/thought_to_action.md (SOP)
- Layer 2: AI orchestration (Claude via MCP)
- Layer 3: This server (deterministic execution)
"""

import os
import sys
import logging
import asyncio
from pathlib import Path
from typing import Any, Sequence
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment
project_root = Path(__file__).parent.parent
load_dotenv(project_root / ".env.diagnostic")

# Setup logging
log_file = Path(os.getenv("MCP_LOG_FILE", ".tmp/mcp_server.log"))
log_file.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("mcp_server")

# Import MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_AVAILABLE = True
    logger.info("MCP SDK imported successfully")
except ImportError as e:
    logger.warning(f"MCP SDK not available: {e}")
    logger.warning("Run: pip install mcp>=1.25.0")
    MCP_AVAILABLE = False

# Import tool managers
from execution.mcp_tools.reminder_tools import ReminderManager
from execution.mcp_tools.todo_tools import TodoManager
from execution.mcp_tools.mindmap_tools import MindMapManager

# Initialize managers
try:
    todo_file = Path(os.getenv("MCP_TODO_FILE", ".tmp/user_data/todos.json"))
    mindmap_dir = Path(os.getenv("MCP_MINDMAP_DIR", ".tmp/user_data/mindmaps"))
    reminder_list = os.getenv("MCP_REMINDER_LIST_NAME", "Claude Reminders")

    reminder_mgr = ReminderManager(reminder_list)
    todo_mgr = TodoManager(todo_file)
    mindmap_mgr = MindMapManager(mindmap_dir)

    logger.info("All managers initialized successfully")
except Exception as e:
    logger.error(f"Error initializing managers: {e}")
    raise


# Create MCP server
if MCP_AVAILABLE:
    server = Server("thought-to-action")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List all available MCP tools."""
        return [
            # Reminder tools
            Tool(
                name="create_reminder",
                description="Create a reminder in macOS Reminders app (or JSON storage on other platforms)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Reminder title (required)"
                        },
                        "notes": {
                            "type": "string",
                            "description": "Additional notes (optional)",
                            "default": ""
                        },
                        "hours_from_now": {
                            "type": "integer",
                            "description": "Hours until reminder (default: 4)",
                            "default": 4
                        }
                    },
                    "required": ["title"]
                }
            ),
            Tool(
                name="list_reminders",
                description="List all reminders from Claude Reminders list",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="cancel_reminder",
                description="Cancel (delete) a reminder by ID or title",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "reminder_id": {
                            "type": "string",
                            "description": "Reminder ID or title fragment"
                        }
                    },
                    "required": ["reminder_id"]
                }
            ),

            # TODO tools
            Tool(
                name="add_todo",
                description="Add a new TODO item with priority, tags, and due date",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "TODO title (required)"
                        },
                        "description": {
                            "type": "string",
                            "description": "Detailed description (optional)",
                            "default": ""
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high"],
                            "description": "Priority level (default: medium)",
                            "default": "medium"
                        },
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of tags (optional)",
                            "default": []
                        },
                        "due_date": {
                            "type": "string",
                            "description": "Due date in ISO format (optional)",
                            "default": None
                        }
                    },
                    "required": ["title"]
                }
            ),
            Tool(
                name="list_todos",
                description="List TODO items with optional filtering by status, tags, or priority",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["pending", "in_progress", "completed", "cancelled"],
                            "description": "Filter by status (optional)"
                        },
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Filter by tags (optional)"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high"],
                            "description": "Filter by priority (optional)"
                        }
                    }
                }
            ),
            Tool(
                name="update_todo",
                description="Update an existing TODO item (title, description, status, priority, tags, or due_date)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "todo_id": {
                            "type": "string",
                            "description": "ID of TODO to update"
                        },
                        "title": {"type": "string"},
                        "description": {"type": "string"},
                        "status": {
                            "type": "string",
                            "enum": ["pending", "in_progress", "completed", "cancelled"]
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high"]
                        },
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "due_date": {"type": "string"}
                    },
                    "required": ["todo_id"]
                }
            ),
            Tool(
                name="complete_todo",
                description="Mark a TODO as completed",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "todo_id": {
                            "type": "string",
                            "description": "ID of TODO to complete"
                        }
                    },
                    "required": ["todo_id"]
                }
            ),
            Tool(
                name="delete_todo",
                description="Delete a TODO item",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "todo_id": {
                            "type": "string",
                            "description": "ID of TODO to delete"
                        }
                    },
                    "required": ["todo_id"]
                }
            ),

            # Mind map tools
            Tool(
                name="create_mindmap",
                description="Create a new mind map with a root topic",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Mind map title"
                        },
                        "root_topic": {
                            "type": "string",
                            "description": "Central topic (root node text)"
                        },
                        "initial_nodes": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional initial branch texts",
                            "default": None
                        }
                    },
                    "required": ["title", "root_topic"]
                }
            ),
            Tool(
                name="add_mindmap_node",
                description="Add a node to an existing mind map",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "mindmap_id": {
                            "type": "string",
                            "description": "ID of mind map"
                        },
                        "parent_node_id": {
                            "type": "string",
                            "description": "ID of parent node"
                        },
                        "text": {
                            "type": "string",
                            "description": "Node text"
                        },
                        "metadata": {
                            "type": "object",
                            "description": "Optional metadata (color, icon, etc.)",
                            "default": None
                        }
                    },
                    "required": ["mindmap_id", "parent_node_id", "text"]
                }
            ),
            Tool(
                name="get_mindmap",
                description="Get a mind map by ID",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "mindmap_id": {
                            "type": "string",
                            "description": "ID of mind map"
                        }
                    },
                    "required": ["mindmap_id"]
                }
            ),
            Tool(
                name="list_mindmaps",
                description="List all mind maps",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="export_mindmap",
                description="Export mind map to markdown, JSON, or mermaid format",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "mindmap_id": {
                            "type": "string",
                            "description": "ID of mind map to export"
                        },
                        "format": {
                            "type": "string",
                            "enum": ["markdown", "json", "mermaid"],
                            "description": "Export format (default: markdown)",
                            "default": "markdown"
                        }
                    },
                    "required": ["mindmap_id"]
                }
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> Sequence[TextContent]:
        """Handle tool calls and route to appropriate manager."""
        logger.info(f"Tool called: {name}")
        logger.debug(f"Arguments: {arguments}")

        try:
            # Reminder tools
            if name == "create_reminder":
                result = reminder_mgr.create_reminder(**arguments)
                return [TextContent(
                    type="text",
                    text=f"{'✅' if result.success else '❌'} {result.message}\n"
                         f"{'Scheduled: ' + result.scheduled_time if result.success else ''}"
                )]

            elif name == "list_reminders":
                reminders = reminder_mgr.list_reminders()
                if not reminders:
                    return [TextContent(type="text", text="No reminders found")]

                text = f"**{len(reminders)} Reminders:**\n\n"
                for r in reminders:
                    status = "✅" if r.completed else "⏰"
                    text += f"{status} **{r.title}**\n"
                    text += f"  Due: {r.due_date}\n"
                    if r.notes:
                        text += f"  Notes: {r.notes}\n"
                    text += "\n"
                return [TextContent(type="text", text=text)]

            elif name == "cancel_reminder":
                success = reminder_mgr.cancel_reminder(arguments["reminder_id"])
                return [TextContent(
                    type="text",
                    text=f"{'✅ Reminder cancelled' if success else '❌ Reminder not found'}"
                )]

            # TODO tools
            elif name == "add_todo":
                result = todo_mgr.add_todo(**arguments)
                if result.success and result.todo:
                    text = f"✅ {result.message}\n\n"
                    text += f"**Details:**\n"
                    text += f"- ID: `{result.todo.id}`\n"
                    text += f"- Priority: {result.todo.priority}\n"
                    text += f"- Status: {result.todo.status}\n"
                    if result.todo.tags:
                        text += f"- Tags: {', '.join(result.todo.tags)}\n"
                    return [TextContent(type="text", text=text)]
                else:
                    return [TextContent(type="text", text=f"❌ {result.message}")]

            elif name == "list_todos":
                result = todo_mgr.list_todos(**arguments)
                if result.count == 0:
                    return [TextContent(type="text", text="No TODOs found")]

                text = f"**{result.count} TODOs:**\n\n"
                for todo in result.todos:
                    status_icon = {"pending": "⏸️", "in_progress": "🔄", "completed": "✅", "cancelled": "❌"}
                    icon = status_icon.get(todo.status, "📝")
                    text += f"{icon} **{todo.title}** (`{todo.id}`)\n"
                    text += f"  Priority: {todo.priority} | Status: {todo.status}\n"
                    if todo.description:
                        text += f"  {todo.description[:100]}{'...' if len(todo.description) > 100 else ''}\n"
                    text += "\n"
                return [TextContent(type="text", text=text)]

            elif name == "update_todo":
                result = todo_mgr.update_todo(**arguments)
                return [TextContent(
                    type="text",
                    text=f"{'✅ ' + result.message if result.success else '❌ ' + result.message}"
                )]

            elif name == "complete_todo":
                result = todo_mgr.complete_todo(arguments["todo_id"])
                return [TextContent(
                    type="text",
                    text=f"{'✅ TODO completed' if result.success else '❌ ' + result.message}"
                )]

            elif name == "delete_todo":
                result = todo_mgr.delete_todo(arguments["todo_id"])
                return [TextContent(
                    type="text",
                    text=f"{'✅ ' + result.message if result.success else '❌ ' + result.message}"
                )]

            # Mind map tools
            elif name == "create_mindmap":
                result = mindmap_mgr.create_mindmap(**arguments)
                if result.success and result.mindmap:
                    text = f"✅ {result.message}\n\n"
                    text += f"**Mind Map Created:**\n"
                    text += f"- ID: `{result.mindmap.id}`\n"
                    text += f"- Title: {result.mindmap.title}\n"
                    text += f"- Root: {result.mindmap.root.text}\n"
                    text += f"- Nodes: {result.mindmap.root.count_nodes()}\n"
                    return [TextContent(type="text", text=text)]
                else:
                    return [TextContent(type="text", text=f"❌ {result.message}")]

            elif name == "add_mindmap_node":
                result = mindmap_mgr.add_mindmap_node(**arguments)
                return [TextContent(
                    type="text",
                    text=f"{'✅ ' + result.message if result.success else '❌ ' + result.message}"
                )]

            elif name == "get_mindmap":
                result = mindmap_mgr.get_mindmap(arguments["mindmap_id"])
                if result.success and result.mindmap:
                    text = f"**{result.mindmap.title}**\n\n"
                    text += f"- ID: `{result.mindmap.id}`\n"
                    text += f"- Created: {result.mindmap.created_at}\n"
                    text += f"- Total Nodes: {result.mindmap.root.count_nodes()}\n"
                    return [TextContent(type="text", text=text)]
                else:
                    return [TextContent(type="text", text=f"❌ {result.message}")]

            elif name == "list_mindmaps":
                mindmaps = mindmap_mgr.list_mindmaps()
                if not mindmaps:
                    return [TextContent(type="text", text="No mind maps found")]

                text = f"**{len(mindmaps)} Mind Maps:**\n\n"
                for mm in mindmaps:
                    text += f"🗺️ **{mm['title']}**\n"
                    text += f"  ID: `{mm['id']}`\n"
                    text += f"  Created: {mm['created_at']}\n\n"
                return [TextContent(type="text", text=text)]

            elif name == "export_mindmap":
                result = mindmap_mgr.export_mindmap(**arguments)
                if result.success:
                    return [TextContent(
                        type="text",
                        text=f"✅ {result.message}\n\n```{result.format}\n{result.content}\n```"
                    )]
                else:
                    return [TextContent(type="text", text=f"❌ {result.message}")]

            else:
                return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]

        except Exception as e:
            logger.error(f"Error in {name}: {e}", exc_info=True)
            return [TextContent(type="text", text=f"❌ Error: {str(e)}")]


    async def main():
        """Main server entry point."""
        logger.info("Starting Thought-to-Action MCP Server...")
        logger.info(f"  TODO storage: {todo_file}")
        logger.info(f"  MindMap storage: {mindmap_dir}")
        logger.info(f"  Reminder list: {reminder_list}")

        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )


    if __name__ == "__main__":
        asyncio.run(main())

else:
    # MCP not available - print installation instructions
    def main():
        print("=" * 60)
        print("MCP Thought-to-Action Server")
        print("=" * 60)
        print()
        print("⚠️  MCP SDK not installed")
        print()
        print("To install:")
        print("  pip install mcp>=1.25.0 anthropic>=0.40.0")
        print()
        print("Or:")
        print("  pip install -r requirements.txt")
        print()
        print("Then run this script again.")
        print("=" * 60)
        sys.exit(1)

    if __name__ == "__main__":
        main()
