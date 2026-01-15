# MCP Thought-to-Action Tools Reference

Quick reference for all 12 MCP tools available in the Thought-to-Action system.

## 📱 Reminder Tools (3)

### `create_reminder`
Create a reminder in macOS Reminders app (or JSON storage on other platforms)

**Parameters:**
- `title` (required) - Reminder title
- `notes` (optional) - Additional notes
- `hours_from_now` (optional, default: 4) - Hours until reminder

**Example:**
```
"Remind me to test backup drive in 2 hours"
```

---

### `list_reminders`
List all reminders from Claude Reminders list

**Parameters:** None

**Example:**
```
"Show me my reminders"
```

---

### `cancel_reminder`
Cancel (delete) a reminder by ID or title

**Parameters:**
- `reminder_id` (required) - Reminder ID or title fragment

**Example:**
```
"Cancel the backup drive reminder"
```

---

## 📝 TODO Tools (5)

### `add_todo`
Add a new TODO item with priority, tags, and due date

**Parameters:**
- `title` (required) - TODO title
- `description` (optional) - Detailed description
- `priority` (optional, default: "medium") - low, medium, or high
- `tags` (optional) - List of tags
- `due_date` (optional) - Due date in ISO format

**Example:**
```
"Add to my TODO: Review HVAC documentation, high priority"
```

---

### `list_todos`
List TODO items with optional filtering by status, tags, or priority

**Parameters:**
- `status` (optional) - pending, in_progress, completed, or cancelled
- `tags` (optional) - Filter by tags
- `priority` (optional) - low, medium, or high

**Example:**
```
"Show me all pending TODOs"
"List high priority TODOs tagged with 'documentation'"
```

---

### `update_todo`
Update an existing TODO item

**Parameters:**
- `todo_id` (required) - ID of TODO to update
- `title` (optional) - New title
- `description` (optional) - New description
- `status` (optional) - New status
- `priority` (optional) - New priority
- `tags` (optional) - New tags list
- `due_date` (optional) - New due date

**Example:**
```
"Update TODO todo_20260115_143000_abc123, set status to in_progress"
```

---

### `complete_todo`
Mark a TODO as completed

**Parameters:**
- `todo_id` (required) - ID of TODO to complete

**Example:**
```
"Mark TODO todo_20260115_143000_abc123 as completed"
```

---

### `delete_todo`
Delete a TODO item

**Parameters:**
- `todo_id` (required) - ID of TODO to delete

**Example:**
```
"Delete TODO todo_20260115_143000_abc123"
```

---

## 🗺️ Mind Map Tools (4)

### `create_mindmap`
Create a new mind map with a root topic

**Parameters:**
- `title` (required) - Mind map title
- `root_topic` (required) - Central topic (root node text)
- `initial_nodes` (optional) - Optional initial branch texts

**Example:**
```
"Create a mind map for the MCP integration project"
```

---

### `add_mindmap_node`
Add a node to an existing mind map

**Parameters:**
- `mindmap_id` (required) - ID of mind map
- `parent_node_id` (required) - ID of parent node
- `text` (required) - Node text
- `metadata` (optional) - Optional metadata (color, icon, etc.)

**Example:**
```
"Add node to mind map mindmap_20260115_143500_xyz789: Architecture"
```

---

### `get_mindmap`
Get a mind map by ID

**Parameters:**
- `mindmap_id` (required) - ID of mind map

**Example:**
```
"Show me mind map mindmap_20260115_143500_xyz789"
```

---

### `list_mindmaps`
List all mind maps

**Parameters:** None

**Example:**
```
"List all my mind maps"
```

---

### `export_mindmap`
Export mind map to markdown, JSON, or mermaid format

**Parameters:**
- `mindmap_id` (required) - ID of mind map to export
- `format` (optional, default: "markdown") - markdown, json, or mermaid

**Example:**
```
"Export the MCP mind map to Markdown"
"Export mind map mindmap_20260115_143500_xyz789 as Mermaid diagram"
```

---

## 📊 Tool Summary

| Category | Tools | Description |
|----------|-------|-------------|
| Reminders | 3 | macOS Reminders app integration |
| TODOs | 5 | Full CRUD with priority and tagging |
| Mind Maps | 4 | Hierarchical trees with export |
| **TOTAL** | **12** | Complete thought-to-action system |

## 🚀 Starting the Server

```bash
./scripts/start_mcp_server.sh
```

## 📖 Documentation

- **Directive:** [directives/thought_to_action.md](directives/thought_to_action.md)
- **Main README:** [README.md#3-mcp-thought-to-action-system](README.md#3-mcp-thought-to-action-system-)
- **Server Code:** [execution/mcp_server.py](execution/mcp_server.py)
