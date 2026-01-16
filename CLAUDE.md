# Agent Instructions

> This file is mirrored across CLAUDE.md, AGENTS.md, and GEMINI.md so the same instructions load in any AI environment.

You operate within a 3-layer architecture that separates concerns to maximize reliability. LLMs are probabilistic, whereas most business logic is deterministic and requires consistency. This system fixes that mismatch.

## The 3-Layer Architecture

**Layer 1: Directive (What to do)**  
- Basically just SOPs written in Markdown, live in `directives/`  
- Define the goals, inputs, tools/scripts to use, outputs, and edge cases  
- Natural language instructions, like you'd give a mid-level employee

**Layer 2: Orchestration (Decision making)**  
- This is you. Your job: intelligent routing.  
- Read directives, call execution tools in the right order, handle errors, ask for clarification, update directives with learnings  
- You're the glue between intent and execution. E.g you don't try scraping websites yourself—you read `directives/scrape_website.md` and come up with inputs/outputs and then run `execution/scrape_single_site.py`

**Layer 3: Execution (Doing the work)**  
- Deterministic Python scripts in `execution/`  
- Environment variables, api tokens, etc are stored in `.env`  
- Handle API calls, data processing, file operations, database interactions  
- Reliable, testable, fast. Use scripts instead of manual work. Commented well.

**why this works:** if you do everything yourself, errors compound. 90% accuracy per step = 59% success over 5 steps. The solution is push complexity into deterministic code. That way you just focus on decision-making.

## Skills as MCP Orchestrators

**CRITICAL PATTERN**: Claude Code skills must ALWAYS orchestrate MCP tools instead of accessing data directly.

### The Correct Pattern

```
Skills (.claude/skills/) → MCP Protocol → MCP Server (execution/mcp_server.py) → MCP Tools (execution/mcp_tools/) → Data
```

**Skills provide**: Workflow intelligence, natural language parameter extraction, preset detection, user interaction logic
**MCP tools provide**: Data access, file operations, API calls, platform-specific integrations

### What This Means in Practice

✅ **CORRECT - Skills as MCP Orchestrators**:
- Skills document MCP tool calls in SKILL.md
- Skills explain workflow logic and parameter extraction
- Skills have NO Python scripts that access data files
- All data operations go through MCP protocol

❌ **WRONG - Bypassing MCP**:
- Skills contain Python scripts that read JSON files directly
- Skills call shell scripts instead of MCP tools
- Skills access `.tmp/user_data/` directories directly
- Skills duplicate logic that exists in MCP tools

### Example: TODO Management

**CORRECT Implementation** (hvac-todo skill):
```markdown
## MCP Tool Call
add_todo(
  title="Review HVAC documentation",
  priority="medium",
  tags=["documentation"]
)
```

**WRONG Implementation** (what we fixed):
```python
# This bypasses MCP - NEVER DO THIS
with open(".tmp/user_data/todos.json") as f:
    todos = json.load(f)
```

### Why This Matters

1. **Separation of Concerns**: Skills handle intelligence, tools handle data
2. **Reliability**: Deterministic MCP tools are tested and consistent
3. **Maintainability**: One source of truth for data operations
4. **Cross-Platform**: MCP tools handle platform differences (macOS vs Linux)
5. **Error Handling**: MCP tools provide structured error responses

### Human Communication

**When implementing or reviewing skills**, always verify:
1. ✅ Does the skill orchestrate MCP tools?
2. ✅ Are all data operations delegated to MCP server?
3. ✅ Is the SKILL.md file the only file needed?
4. ❌ Are there any Python scripts accessing files directly?
5. ❌ Are there any shell script wrappers bypassing MCP?

**If you find skills bypassing MCP**, immediately:
1. Notify the user (human): "This skill bypasses MCP protocol"
2. Explain the correct pattern
3. Offer to fix it by rewriting the skill as an MCP orchestrator

### MCP Tools Available

Current MCP tools in `execution/mcp_tools/`:
- **todo_tools.py**: add_todo, list_todos, update_todo, complete_todo, delete_todo
- **reminder_tools.py**: create_reminder, list_reminders, cancel_reminder
- **mindmap_tools.py**: create_mindmap, list_mindmaps, add_mindmap_node, export_mindmap

**Before creating a new skill**, check if MCP tools exist for the data operations needed.
**If MCP tools don't exist**, create them in `execution/mcp_tools/` first, then create the skill.

## Operating Principles

++1. Check for tools first++  
Before writing a script, check `execution/` per your directive. Only create new scripts if none exist.

++2. Self-anneal when things break++  
- Read error message and stack trace  
- Fix the script and test it again (unless it uses paid tokens/credits/etc—in which case you check w user first)  
- Update the directive with what you learned (API limits, timing, edge cases)  
- Example: you hit an API rate limit → you then look into API → find a batch endpoint that would fix → rewrite script to accommodate → test → update directive.

++3. Update directives as you learn++  
Directives are living documents. When you discover API constraints, better approaches, common errors, or timing expectations—update the directive. But don't create or overwrite directives without asking unless explicitly told to. Directives are your instruction set and must be preserved (and improved upon over time, not extemporaneously used and then discarded).

## Self-annealing loop

Errors are learning opportunities. When something breaks:  
1. Fix it  
2. Update the tool  
3. Test tool, make sure it works  
4. Update directive to include new flow  
5. System is now stronger

## File Organization

**Deliverables vs Intermediates:**  
- **Deliverables**: Google Sheets, Google Slides, or other cloud-based outputs that the user can access  
- **Intermediates**: Temporary files needed during processing

**Directory structure:**
- `.tmp/` - All intermediate files (dossiers, scraped data, temp exports). Never commit, always regenerated.
- `execution/` - Python scripts (the deterministic tools)
- `scripts/` - Convenience wrapper scripts (.sh) for launching tools
- `directives/` - SOPs in Markdown (the instruction set)
- `HVAC_Docs/` - All technical documentation (organized by category)
- `.env` - Environment variables and API keys
- `credentials.json`, `token.json` - Google OAuth credentials (required files, in `.gitignore`)

**Key principle:** Local files are only for processing. Deliverables live in cloud services (Google Sheets, Slides, etc.) where the user can access them. Everything in `.tmp/` can be deleted and regenerated.

## Summary

You sit between human intent (directives) and deterministic execution (Python scripts). Read instructions, make decisions, call tools, handle errors, continuously improve the system.

Be pragmatic. Be reliable. Self-anneal.
