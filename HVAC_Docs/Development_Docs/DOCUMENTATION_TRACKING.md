# Documentation Tracking Strategy

This guide outlines the best practices for tracking documentation changes in the HVAC_ideas project.

## 📋 Overview

We use a **3-tier tracking system** to maintain complete visibility into documentation changes:

1. **Git Commits** - Detailed, file-level change tracking (automatic)
2. **CHANGELOG.md** - High-level summary of major changes (manual)
3. **Git Tags** - Version milestones for major documentation releases (manual)

---

## 🎯 Tier 1: Git Commits (Primary Tracking)

**Status:** ✅ Already implemented

Git automatically tracks every change with full history. This is your **detailed audit trail**.

### View Recent Changes
```bash
# See last 10 commits
git log --oneline -10

# See what changed in each commit
git log --stat -5

# See detailed changes with diffs
git log -p -3

# See commits affecting specific file
git log --follow -- HVAC_Docs/Technical_Guides/TANK_DIAGNOSTICS_GUIDE.md
```

### View Specific Changes
```bash
# See what changed in last commit
git show HEAD

# Compare current version to 3 commits ago
git diff HEAD~3 README.md

# See who changed a file line-by-line
git blame HVAC_Docs/README.md
```

### Restore Previous Versions
```bash
# View file as it was 5 commits ago
git show HEAD~5:README.md

# Restore entire file to previous version
git checkout HEAD~3 -- HVAC_Docs/Technical_Guides/AI_DIAGNOSTIC_README.md
```

**Benefits:**
- Automatic tracking of all changes
- Complete history with timestamps and authors
- Ability to restore any previous version
- Blame tracking (who changed what line)
- Detailed commit messages explain **why** changes were made

---

## 📝 Tier 2: CHANGELOG.md (High-Level Summary)

**Status:** 🔧 Recommended addition

A CHANGELOG provides a **human-readable summary** of major changes, making it easy to understand project evolution without reading git logs.

### Structure
```markdown
# Changelog

All notable changes to HVAC_ideas documentation will be documented in this file.

## [2026-01-15] - Documentation Reorganization

### Changed
- Reorganized 28 documentation files into HVAC_Docs/ directory structure
- Created categorized subdirectories: Technical_Guides, Procedures, Development_Docs, Prompts_and_Guides, Miscellaneous
- Updated README.md with new file paths and 3-layer architecture overview
- Implemented "Essential Root" organization principle

### Added
- Created HVAC_Docs/README.md as comprehensive documentation index
- Added documentation tracking strategy guide

### Removed
- Removed 28 files from root directory (moved to HVAC_Docs/)

## [2026-01-14] - System Improvements

### Added
- LLM switching capability with --llm flag
- Comprehensive PROJECT_CONTEXT.md for AI assistants
- Improved Ollama accuracy with better prompts

### Changed
- Enhanced Ollama output formatting
- Updated model configuration

## [Previous entries...]
```

### Update Strategy
Update CHANGELOG.md when making **significant** changes:
- New features or capabilities
- Major documentation reorganizations
- Breaking changes to directory structure
- New diagnostic tools or guides
- Deprecated/removed features

**Don't** update for:
- Typo fixes
- Minor formatting tweaks
- Single-line edits

### Create CHANGELOG.md?
Would you like me to create a CHANGELOG.md file with entries based on your recent git history?

---

## 🏷️ Tier 3: Git Tags (Version Milestones)

**Status:** 💡 Optional enhancement

Git tags mark **major milestones** in documentation evolution.

### Usage
```bash
# Create tag for major documentation release
git tag -a docs-v1.0 -m "Initial organized documentation structure"

# Create tag for specific milestone
git tag -a docs-reorganization-2026-01 -m "Implemented HVAC_Docs structure"

# View all tags
git tag -l

# View tag details
git show docs-v1.0

# Checkout documentation at specific tag
git checkout docs-v1.0
```

### When to Tag
- Major documentation reorganizations (like today's change)
- Completion of major documentation efforts
- Before significant refactoring
- When documentation reaches "stable" state

---

## 🔍 Recommended Workflow

### Daily Work
1. Make documentation changes
2. **Git commit** with descriptive message (automatic tracking)

### Significant Changes
1. Make changes and commit
2. **Update CHANGELOG.md** with summary
3. Commit the CHANGELOG update

### Major Milestones
1. Complete major documentation effort
2. Update CHANGELOG.md
3. **Create git tag** for the milestone
4. Push everything to remote

---

## 📊 Comparison Table

| Method | Granularity | Effort | Best For |
|--------|-------------|--------|----------|
| **Git Commits** | File-level, line-by-line | Low (automatic) | Detailed audit trail |
| **CHANGELOG.md** | Feature/project level | Medium (manual) | Human-readable summary |
| **Git Tags** | Milestone level | Low (occasional) | Version markers |

---

## 🎯 Recommended Setup for HVAC_ideas

### ✅ Currently Using
- Git commits with descriptive messages
- Co-authored commits with Claude Sonnet 4.5

### 🔧 Recommended Additions
1. **Create CHANGELOG.md** - Track major documentation changes
2. **Tag major milestones** - Use semantic tags like `docs-v1.0-reorganization`

### 🚀 Quick Start
```bash
# View your documentation change history
git log --oneline --follow -- HVAC_Docs/

# Create a tag for today's reorganization
git tag -a docs-v1.0-reorganization -m "HVAC_Docs structure implementation"

# Push tags to remote (if using remote repository)
git push --tags
```

---

## 💡 Pro Tips

### 1. Search Commit History
```bash
# Find commits mentioning specific topic
git log --all --grep="diagnostic"

# Find commits that changed specific text
git log -S "TANK_DIAGNOSTICS_GUIDE"
```

### 2. Visual History
```bash
# See branching/merging graphically
git log --graph --oneline --all

# See file rename history
git log --follow --stat -- HVAC_Docs/Technical_Guides/AI_DIAGNOSTIC_README.md
```

### 3. Export History
```bash
# Export last 20 commits to file
git log -20 --pretty=format:"%h - %an, %ar : %s" > git-history.txt

# Export detailed changelog
git log --since="2026-01-01" --pretty=format:"- %s (%h)" > recent-changes.txt
```

---

## 📌 Summary

**Best practice for your workflow:**

1. **Always commit** with descriptive messages (you're already doing this!)
2. **Add CHANGELOG.md** for high-level tracking
3. **Use git tags** for major milestones
4. **Review history** using `git log` commands above

This gives you:
- ✅ Complete audit trail (git commits)
- ✅ Easy-to-read summary (CHANGELOG)
- ✅ Version markers (git tags)
- ✅ Ability to restore any previous state

---

**Next Steps:**
- Create CHANGELOG.md (recommended)
- Tag today's reorganization milestone (optional)
- Reference this guide when tracking future changes
