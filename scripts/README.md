# Scripts Directory

This directory contains convenience wrapper scripts for launching diagnostic tools and utilities.

## 🔧 Diagnostic Scripts

### Oil Tank Diagnostics (AI-Powered - Claude API)

**`run_ai_diagnostic.sh`** - AI-powered Tank #1 diagnostics
- Requires: Claude API key, internet connection
- Cost: ~$0.01-0.05 per session

**`run_ai_tank2_diagnostic.sh`** - AI-powered Tank #2 diagnostics
- Requires: Claude API key, internet connection
- Cost: ~$0.01-0.05 per session

### Oil Tank Diagnostics (Basic - FREE)

**`run_tank1_diagnostic.sh`** - Basic Tank #1 questionnaire
- No API required, completely free
- Offline capable

**`run_tank2_diagnostic.sh`** - Basic Tank #2 questionnaire
- No API required, completely free
- Offline capable

### Multi-Agent Log Resolution

**`resolve_system_issues.sh`** - 3-phase multi-agent log analysis
- Analyzes macOS system logs
- Generates master resolution plans
- Requires: macOS, Python 3

---

## 🛠️ Utility Scripts

### macOS Reminder Creation

**`create_reminder.sh`** - General-purpose reminder creator

**Interactive Mode:**
```bash
./scripts/create_reminder.sh
# Prompts for title, notes, and time
```

**Quick Mode:**
```bash
./scripts/create_reminder.sh "Title" "Notes"
```

**Custom Time:**
```bash
HOURS=2 ./scripts/create_reminder.sh "Title" "Notes"
```

---

**`remind_test_backup_drive.sh`** - Quick reminder for backup drive testing

**Usage:**
```bash
# Remind in 4 hours (default)
./scripts/remind_test_backup_drive.sh

# Remind in 2 hours
./scripts/remind_test_backup_drive.sh 2
```

Creates a reminder with preset content for testing backup drive power management configuration.

---

### MCP Thought-to-Action System

**`start_mcp_server.sh`** - Launch MCP server for thought-to-action system

**Usage:**
```bash
./scripts/start_mcp_server.sh
```

Provides natural language interface for reminders, TODOs, and mind mapping through MCP tools.

**Features:**
- 12 MCP tools exposed to Claude
- Reminders integration (macOS Reminders app)
- TODO list management (JSON storage)
- Mind mapping (tree structure with export)

**Tools Available:**
- `create_reminder`, `list_reminders`, `cancel_reminder`
- `add_todo`, `list_todos`, `update_todo`, `complete_todo`, `delete_todo`
- `create_mindmap`, `add_mindmap_node`, `get_mindmap`, `list_mindmaps`, `export_mindmap`

**Requirements:**
- Python 3.8+
- MCP SDK: `pip install mcp>=1.25.0`
- Anthropic API key in `.env.diagnostic`

**Documentation:**
- 📖 [Thought-to-Action Directive](../directives/thought_to_action.md)
- 📖 [Main README - MCP Section](../README.md#3-mcp-thought-to-action-system-)

---

## 📁 Script Organization

```
scripts/
├── run_ai_diagnostic.sh           # AI Tank #1 (Claude API)
├── run_ai_tank2_diagnostic.sh     # AI Tank #2 (Claude API)
├── run_tank1_diagnostic.sh        # Basic Tank #1 (FREE)
├── run_tank2_diagnostic.sh        # Basic Tank #2 (FREE)
├── resolve_system_issues.sh       # Multi-agent log analysis
├── create_reminder.sh             # General reminder tool
└── remind_test_backup_drive.sh    # Backup drive test reminder
```

---

## 🚀 Usage Examples

### Create a Custom Reminder
```bash
# Interactive mode
./scripts/create_reminder.sh

# Quick mode - remind in 4 hours
./scripts/create_reminder.sh "Review PR" "Check GitHub PR #123"

# Remind in 1 hour
HOURS=1 ./scripts/create_reminder.sh "Meeting" "Team standup"
```

### Test Backup Drive Configuration
```bash
# Set reminder to test backup drive (4 hours)
./scripts/remind_test_backup_drive.sh

# Set reminder for 6 hours from now
./scripts/remind_test_backup_drive.sh 6
```

### Run Diagnostics
```bash
# AI-powered diagnostics (requires API key)
./scripts/run_ai_diagnostic.sh

# Basic diagnostics (free, no API)
./scripts/run_tank1_diagnostic.sh
```

---

## 📋 Requirements

### For Diagnostic Scripts:
- Python 3.8+
- Virtual environment (optional)
- `.env.diagnostic` with `ANTHROPIC_API_KEY` (for AI scripts only)

### For Utility Scripts:
- macOS (for reminder scripts)
- AppleScript enabled
- Reminders app

---

## 🔗 Related Documentation

- [Main README](../README.md) - Project overview
- [AI Diagnostic Guide](../HVAC_Docs/Technical_Guides/AI_DIAGNOSTIC_README.md)
- [Tank Diagnostics Guide](../HVAC_Docs/Technical_Guides/TANK_DIAGNOSTICS_GUIDE.md)
- [Dependency Hierarchy](../HVAC_Docs/Development_Docs/DEPENDENCY_HIERARCHY.md)

---

**All scripts are executable and documented with detailed header comments.**
