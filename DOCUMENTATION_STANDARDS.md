# Documentation Standards

This guide ensures all documentation in the HVAC_ideas repository is clear, comprehensive, and user-friendly.

## Core Principles

1. **Clarity First** - New users should never be confused
2. **Be Specific** - Avoid vague terms like "Full Documentation" or "Click here"
3. **Two Systems** - Always distinguish between FREE/LOCAL (Ollama) and PAID/CLOUD (Claude API)
4. **Cost Transparency** - Make costs clear upfront (free vs paid)
5. **Privacy Transparency** - Explain where data goes (local vs cloud)

## Link Text Standards

### ✅ Good Link Examples

All documentation links should be descriptive and self-explanatory:

```markdown
📖 [Virtual HVAC Technician Full Documentation](hvac-technician/README.md)
📖 [Tank Diagnostics Guide](TANK_DIAGNOSTICS_GUIDE.md)
📖 [AI Diagnostic README](AI_DIAGNOSTIC_README.md)
📄 [Oil Tank Transfer Troubleshooting (PDF)](Oil_Tank_Transfer_Troubleshooting_Guide.pdf)
```

### ❌ Avoid Vague Links

```markdown
❌ [Full Documentation](...)
❌ [Click here](...)
❌ [Read more](...)
❌ [Documentation](...)
```

## Recent Documentation Improvement

### What Was Changed

**Before:**
```markdown
📖 [Full Documentation](hvac-technician/README.md)
```

**After:**
```markdown
📖 [Virtual HVAC Technician Full Documentation](hvac-technician/README.md)
```

**Why:** Users scanning the README should immediately know what documentation the link points to without having to click it.

## Verified Link Standards

### Main README Links ✅

All links verified for clarity and descriptiveness:

- Tank Diagnostics Guide
- Tank 1 Diagnostic App README
- AI Diagnostic README
- All Diagnostic Apps Overview
- Diagnostic Apps Comparison
- Oil Tank Transfer Box Verification Procedure
- PLC Fault Code Guide
- AGENTS.md
- Multi-Agent Log Resolution
- CLAUDE.md / GEMINI.md
- AI Co-authorship Legal Implications

### hvac-technician README Links ✅

All links verified for clarity:

- Tank Diagnostics Guide
- AI Diagnostic README
- All Diagnostic Apps Overview
- Tank 1 Auto Fill Guide (PDF)
- Oil Tank Transfer Troubleshooting (PDF)

## Two AI Systems - Documentation Requirements

### System 1: Virtual HVAC Technician 🟢 FREE & LOCAL

When documenting this system, always include:

```markdown
**AI System:** CrewAI + Ollama (llama3.2:3b) running in Docker
**Cost:** $0.00 - Completely free, runs 100% locally
**Privacy:** All data stays on your machine, no cloud, no internet required
**Setup:** Docker Desktop + Ollama (no API keys needed)
```

### System 2: Oil Tank Diagnostics 🔵 PAID (Claude API)

When documenting this system, always include:

```markdown
**AI System:** Claude API (Anthropic, cloud-based)
**Cost:** Paid API - Requires Anthropic API key (~$0.01-0.05 per diagnostic session)
**Privacy:** Data sent to Anthropic's servers for processing
**Setup Required:** ANTHROPIC_API_KEY in `.env.diagnostic` file

⚠️ Important: You need:
1. An Anthropic API account at https://console.anthropic.com/
2. A paid API key configured in `.env.diagnostic`
3. Internet connection for API calls
```

## Section Badges

Use clear visual indicators:

- 🟢 FREE & LOCAL - For Ollama-based tools
- 🔵 PAID (Claude API) - For cloud-based tools
- 📖 - For markdown documentation
- 📄 - For PDF files
- ⚠️ - For important warnings
- ✅ - For verified items or completed tasks

## Prerequisites Documentation

### Good Example

```markdown
## Prerequisites

### For Virtual HVAC Technician (Local/Free)

1. **Docker Desktop** - Running on your machine
2. **Ollama** - Local LLM runtime with `llama3.2:3b` model
   ```bash
   ollama pull llama3.2:3b
   ```
3. **CrewAI Container** - Built from docker-compose.yml

### For Oil Tank Diagnostics (Claude API/Paid)

1. **Anthropic API Account** - Sign up at https://console.anthropic.com/
2. **API Key** - Generate a paid API key
3. **Configuration File** - Create `.env.diagnostic`
4. **Internet Connection** - Required for API calls
```

## Quick Start Documentation

Always provide:
1. **Command examples** - Copy-pasteable code blocks
2. **Expected behavior** - What users should see
3. **Common issues** - Troubleshooting tips
4. **System requirements** - Which AI system is used

### Good Example

```markdown
## Quick Start

**Note:** This uses the LOCAL/FREE system (Ollama + CrewAI)

```bash
# Using the hvac command (if configured)
hvac "How often should I change my HVAC filter?"

# Or directly via Docker
docker compose exec crewai python /app/HVAC_ideas/hvac-technician/hvac_expert.py
```
```

## Cost Transparency

Always be upfront about costs:

### Free Tools
```markdown
**Cost:** $0.00 - Completely free, unlimited usage
```

### Paid Tools
```markdown
**Cost:** ~$0.01-0.05 per diagnostic session
**Billing:** Pay-as-you-go through Anthropic
**Estimated monthly cost:** Depends on usage
```

## Privacy & Data Handling

Always explain where data goes:

### Local Tools
```markdown
**Privacy:**
✅ 100% local processing
✅ No data sent to external servers
✅ Works completely offline
✅ No telemetry or tracking
```

### Cloud Tools
```markdown
**Privacy:**
🔵 Data sent to Anthropic's servers
🔵 Processed via Claude API
🔵 Requires internet connection
🔵 Subject to Anthropic's privacy policy
```

## Warning Boxes

Use warning boxes for critical information:

```markdown
⚠️ **Important:** These scripts use the Claude API (not local). You need:
1. An Anthropic API account
2. A paid API key
3. Internet connection
```

## Cross-References

When referencing related tools, explain the differences:

```markdown
## Related Tools

### Oil Tank Diagnostics ⛽ 🔵 PAID (Different System)

⚠️ **Important:** These tools use a DIFFERENT AI system:
- **This tool:** FREE - Local Ollama + CrewAI
- **Oil tank tools:** PAID - Claude API

[Why two systems?] General HVAC works with local models,
specialized oil tank diagnostics requires Claude's advanced reasoning.
```

## Documentation Review Checklist

Before committing documentation changes, verify:

- [ ] All links have descriptive text (not "click here" or "full documentation")
- [ ] AI system clearly identified (Ollama vs Claude API)
- [ ] Costs are transparent ($0 vs paid)
- [ ] Privacy implications explained (local vs cloud)
- [ ] Prerequisites listed with setup commands
- [ ] Quick start examples included
- [ ] Badges used appropriately (🟢 FREE vs 🔵 PAID)
- [ ] Warning boxes for important notices
- [ ] Cross-references explain differences between systems

## Commit Message Standards

When documenting changes, use clear commit messages:

### Good Examples

```
docs: improve link clarity for Virtual HVAC Technician documentation
docs: CRITICAL - clarify two different AI systems used
docs(hvac): clarify local Ollama setup and requirements
```

### Include in Commit Body

- What changed and why
- Benefits for users
- What confusion this prevents

## User-First Approach

Always ask: "Will a new user understand this without confusion?"

### User Should Immediately Know:

1. Which AI system they're using (local vs cloud)
2. What it costs ($0 vs paid)
3. Where their data goes (local vs cloud)
4. How to set it up (prerequisites)
5. How to use it (quick start commands)
6. What each tool does (clear descriptions)
7. Where to find more info (descriptive links)

## Maintenance

This documentation should be reviewed whenever:
- New AI tools are added
- Links are added or changed
- Prerequisites change
- Cost structure changes
- Privacy policies change

---

**Last Updated:** January 14, 2026
**Maintained By:** Repository contributors
**Questions?** Open an issue on GitHub
