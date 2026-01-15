# Changelog

All notable changes to the HVAC_ideas project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [2026-01-15] - Documentation Reorganization

### Changed
- **Major refactor:** Reorganized 28 documentation files into structured HVAC_Docs/ directory
- Moved all technical documentation from root to categorized subdirectories
- Updated README.md with new file paths and enhanced architecture overview
- Updated CLAUDE.md, AGENTS.md, and GEMINI.md with HVAC_Docs/ directory reference
- Implemented "Essential Root" organization principle - root now contains only essential execution files

### Added
- Created HVAC_Docs/ directory with 5 organized subdirectories:
  - `Technical_Guides/` - Diagnostic guides, troubleshooting PDFs, HVAC diagrams (8 files)
  - `Procedures/` - Step-by-step verification procedures and checklists (4 files)
  - `Development_Docs/` - Project context, standards, improvement logs (8 files)
  - `Prompts_and_Guides/` - AI prompt guides and AR glasses documentation (3 files)
  - `Miscellaneous/` - Research notes, legal considerations (4 files)
- Created comprehensive HVAC_Docs/README.md as documentation navigation index
- Added DOCUMENTATION_TRACKING.md guide for tracking documentation changes
- Added CHANGELOG.md (this file) for high-level change tracking
- Created git tag: `docs-v1.0-reorganization`

### Technical Details
- Preserved 3-layer architecture structure (directives/, execution/, .tmp/)
- All file moves tracked as renames in git (history preserved)
- 203 lines added, 32 lines removed across 30 files
- CLAUDE.md made project-specific (vs universal template)

---

## [2026-01-14] - System Improvements & Documentation

### Added
- Comprehensive IMPROVEMENTS_SUMMARY.md documenting all system enhancements
- Documentation standards guide (DOCUMENTATION_STANDARDS.md)
- LLM switching capability with `--llm` flag for choosing between Claude and Ollama
- LLM_SWITCHING_GUIDE.md with usage instructions

### Changed
- Improved Ollama accuracy by switching to llama3.2:3b model
- Enhanced Ollama output formatting with improved prompts
- Clarified distinction between two AI systems (Virtual HVAC Technician vs Oil Tank Diagnostics)
- Improved README.md link clarity for Virtual HVAC Technician documentation

### Documentation
- Added comprehensive PROJECT_CONTEXT.md for AI assistants
- Enhanced documentation for all AI tools with clear cost/privacy information

---

## [Earlier] - Initial Development

### Added
- Virtual HVAC Technician (FREE, local Ollama + CrewAI)
- Oil Tank Diagnostic Tools (PAID, Claude API)
  - Tank 1 diagnostics (auto-fill system)
  - Tank 2 diagnostics (transfer pump)
  - AI-enhanced diagnostic scripts
- Multi-agent system architecture (AGENTS.md, CLAUDE.md, GEMINI.md)
- 3-layer architecture implementation
  - Layer 1: Directives (SOPs in Markdown)
  - Layer 2: Orchestration (AI decision-making)
  - Layer 3: Execution (Python scripts)
- Technical documentation
  - HVAC component reference guides
  - Oil tank troubleshooting PDFs
  - PLC fault code guides
  - Verification procedures
- Python execution scripts for diagnostics
- Shell scripts for running diagnostic tools

---

## Tracking Methods

This project uses a **3-tier documentation tracking system**:

1. **Git Commits** - Detailed file-level tracking (automatic)
2. **CHANGELOG.md** - High-level summary (this file, manual)
3. **Git Tags** - Version milestones (manual)

For detailed changes, use: `git log`
For tracking documentation, see: [HVAC_Docs/Development_Docs/DOCUMENTATION_TRACKING.md](HVAC_Docs/Development_Docs/DOCUMENTATION_TRACKING.md)
