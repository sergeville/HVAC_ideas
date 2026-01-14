# HVAC Ideas Project Context

**Version:** 1.0
**Last Updated:** January 14, 2026
**Purpose:** Reference file for AI assistants (Claude, Gemini, etc.) working with this repository

---

## 🎯 Quick Overview

This repository contains TWO COMPLETELY DIFFERENT AI-powered diagnostic systems for HVAC troubleshooting:

1. **Virtual HVAC Technician** - FREE, runs locally with Ollama + CrewAI
2. **Oil Tank Diagnostics** - PAID, uses Claude API (cloud-based)

**CRITICAL:** These are separate systems with different costs, privacy, and setup requirements. Never confuse them.

---

## 📊 Two AI Systems - Key Differences

### System 1: Virtual HVAC Technician 🟢 FREE & LOCAL

| Aspect | Details |
|--------|---------|
| **Location** | `hvac-technician/` folder |
| **AI Engine** | CrewAI + Ollama (llama3.2:3b model) |
| **Runtime** | Docker container (local) |
| **Cost** | $0.00 - Completely free |
| **Privacy** | 100% local, no cloud, works offline |
| **Setup** | Docker Desktop + Ollama |
| **API Keys** | None needed |
| **Use Cases** | General HVAC questions, troubleshooting, maintenance |
| **Agents** | 2 specialized agents (Master Technician + Diagnostics Specialist) |

**Docker Setup Location:** `/Users/sergevilleneuve/Documents/MyExperiments/opencode/`
- `docker-compose.yml` - Container orchestration
- `Dockerfile` - CrewAI environment with Python 3.11

**Volume Mounts:**
- `.:/app` - opencode directory
- `/Users/sergevilleneuve/Documents/MyExperiments/HVAC_ideas:/app/HVAC_ideas` - This repository

**Shell Command:** `hvac "your question"` (configured in `~/.zshrc`)

### System 2: Oil Tank Diagnostics 🔵 PAID (Claude API)

| Aspect | Details |
|--------|---------|
| **Location** | Root directory scripts |
| **AI Engine** | Claude API (Anthropic, cloud) |
| **Runtime** | Direct API calls |
| **Cost** | ~$0.01-0.05 per session |
| **Privacy** | Data sent to Anthropic servers |
| **Setup** | ANTHROPIC_API_KEY in `.env.diagnostic` |
| **API Keys** | Required from console.anthropic.com |
| **Use Cases** | Oil heating, fuel pumps, tank transfer issues |
| **Scripts** | 4 diagnostic scripts |

**Available Scripts:**
- `run_tank1_diagnostic.sh` - Tank 1 auto-fill diagnostics
- `run_tank2_diagnostic.sh` - Tank 2 transfer pump diagnostics
- `run_ai_tank2_diagnostic.sh` - AI-enhanced Tank 2 diagnostics
- `run_ai_diagnostic.sh` - General oil tank AI assistant

---

## 📁 Repository Structure

```
HVAC_ideas/
├── hvac-technician/              # Virtual HVAC Technician (FREE/LOCAL)
│   ├── hvac_expert.py           # Main application (2 AI agents)
│   ├── README.md                # Full documentation
│   ├── quick-start.sh           # Launch script
│   ├── example-questions.txt    # 70+ sample questions
│   └── .project-info.md         # Project metadata
│
├── run_tank1_diagnostic.sh      # Oil tank diagnostics (PAID/CLOUD)
├── run_tank2_diagnostic.sh      # Oil tank diagnostics (PAID/CLOUD)
├── run_ai_tank2_diagnostic.sh   # Oil tank diagnostics (PAID/CLOUD)
├── run_ai_diagnostic.sh         # Oil tank diagnostics (PAID/CLOUD)
│
├── TANK_DIAGNOSTICS_GUIDE.md    # Tank diagnostics documentation
├── AI_DIAGNOSTIC_README.md      # AI diagnostic documentation
├── TANK1_DIAGNOSTIC_APP_README.md
├── ALL_DIAGNOSTIC_APPS.md
├── DIAGNOSTIC_APPS_COMPARISON.md
│
├── README.md                    # Main repository documentation
├── DOCUMENTATION_STANDARDS.md   # Documentation guidelines
├── PROJECT_CONTEXT.md           # This file
│
├── AGENTS.md                    # Multi-agent system docs
├── CLAUDE.md                    # 3-layer architecture guide
├── GEMINI.md                    # Gemini AI configuration
│
├── HVAC.md                      # Technical heat pump analysis
├── hvac.jpeg                    # HVAC diagram
├── Oil Tank Transfer Box Verification Procedure.md
├── PLC Fault Code Guide.md
│
├── directives/                  # SOP instructions
├── execution/                   # Python execution scripts
├── .tmp/                        # Temporary files
├── venv/                        # Python virtual environment
│
├── .env.diagnostic              # API key for oil tank tools (not in git)
└── requirements.txt             # Python dependencies
```

---

## 🚀 How to Work with This Repository

### When User Asks About HVAC in General

**Use:** Virtual HVAC Technician (FREE/LOCAL)

**Command:**
```bash
hvac "user's question"
```

**Or directly:**
```bash
docker compose -f /Users/sergevilleneuve/Documents/MyExperiments/opencode/docker-compose.yml exec crewai python /app/HVAC_ideas/hvac-technician/hvac_expert.py "question"
```

**Features:**
- Unlimited free questions
- Works offline
- Privacy guaranteed
- Two specialized agents

### When User Asks About Oil Tanks/Fuel Pumps

**Use:** Oil Tank Diagnostics (PAID/CLOUD)

**Prerequisites Check:**
1. Verify `.env.diagnostic` exists with `ANTHROPIC_API_KEY`
2. User understands this costs money (~$0.01-0.05 per session)
3. Internet connection available

**Commands:**
```bash
./run_tank1_diagnostic.sh          # Auto-fill issues
./run_tank2_diagnostic.sh          # Transfer pump issues
./run_ai_tank2_diagnostic.sh       # AI-enhanced diagnostics
./run_ai_diagnostic.sh             # General oil tank help
```

---

## 🛠️ Technical Setup

### Virtual HVAC Technician Setup

1. **Ollama Running:**
   ```bash
   docker ps | grep ollama
   # Should show ollama container running on port 11434
   ```

2. **Verify Model:**
   ```bash
   ollama list | grep llama3.2:3b
   ```

3. **CrewAI Container:**
   ```bash
   cd /Users/sergevilleneuve/Documents/MyExperiments/opencode
   docker compose ps
   # Should show crewai-agent container running
   ```

4. **Test:**
   ```bash
   hvac "test question"
   ```

### Oil Tank Diagnostics Setup

1. **Check API Key:**
   ```bash
   cat .env.diagnostic | grep ANTHROPIC_API_KEY
   ```

2. **Test:**
   ```bash
   ./run_ai_diagnostic.sh
   ```

---

## 📖 Documentation Files Reference

### Main Documentation
- **README.md** - Repository overview, both AI systems documented
- **DOCUMENTATION_STANDARDS.md** - Standards for maintaining docs
- **PROJECT_CONTEXT.md** - This file

### Virtual HVAC Technician
- **hvac-technician/README.md** - Complete guide
- **hvac-technician/example-questions.txt** - 70+ sample questions
- **hvac-technician/.project-info.md** - Project metadata

### Oil Tank Diagnostics
- **TANK_DIAGNOSTICS_GUIDE.md** - Tank diagnostics overview
- **AI_DIAGNOSTIC_README.md** - AI diagnostic details
- **TANK1_DIAGNOSTIC_APP_README.md** - Tank 1 specific guide
- **ALL_DIAGNOSTIC_APPS.md** - All diagnostic apps overview
- **DIAGNOSTIC_APPS_COMPARISON.md** - Comparison of diagnostic tools

### Technical Guides
- **HVAC.md** - Heat pump electrical wiring analysis
- **Oil Tank Transfer Box Verification Procedure.md**
- **PLC Fault Code Guide.md**

### AI Configuration
- **AGENTS.md** - Multi-agent system documentation
- **CLAUDE.md** - 3-layer architecture guide
- **GEMINI.md** - Gemini AI configuration

---

## ⚠️ Critical Don'ts

### ❌ Never Mix the Two Systems

```
❌ WRONG: "Use the hvac command for oil tank diagnostics"
✅ RIGHT: "Oil tank diagnostics use separate scripts with Claude API"

❌ WRONG: "All tools are free and local"
✅ RIGHT: "HVAC Technician is free/local, oil tank tools are paid/cloud"

❌ WRONG: "Setup is the same for all tools"
✅ RIGHT: "Different setup: Docker+Ollama vs API key+internet"
```

### ❌ Never Assume

- Check which system the user needs
- Verify prerequisites before recommending commands
- Explain costs upfront for oil tank tools
- Confirm internet connection for cloud tools

### ❌ Never Be Vague

```
❌ WRONG: "See full documentation"
✅ RIGHT: "See Virtual HVAC Technician Full Documentation"

❌ WRONG: "This uses AI"
✅ RIGHT: "This uses CrewAI + Ollama (local, free)"

❌ WRONG: "Run the diagnostic"
✅ RIGHT: "Run ./run_tank1_diagnostic.sh (requires API key, costs ~$0.01-0.05)"
```

---

## ✅ Best Practices

### When Documenting

1. **Always specify the system:**
   - "Virtual HVAC Technician (FREE/LOCAL)"
   - "Oil Tank Diagnostics (PAID/CLOUD)"

2. **Use badges:**
   - 🟢 FREE & LOCAL
   - 🔵 PAID (Claude API)

3. **Be cost-transparent:**
   - "$0.00 - Completely free"
   - "~$0.01-0.05 per session"

4. **Explain privacy:**
   - "100% local, no cloud"
   - "Data sent to Anthropic servers"

5. **List prerequisites:**
   - Docker + Ollama (free system)
   - API key + internet (paid system)

### When Helping Users

1. **Identify the need:**
   - General HVAC → Virtual HVAC Technician
   - Oil tank/fuel pump → Oil Tank Diagnostics

2. **Check prerequisites:**
   - Is Ollama running? (free system)
   - Do they have API key? (paid system)

3. **Explain costs:**
   - Free system = unlimited usage
   - Paid system = per-session cost

4. **Provide exact commands:**
   - Copy-pasteable code blocks
   - Full paths when needed

5. **Reference documentation:**
   - Use descriptive link text
   - Point to specific sections

---

## 🔍 Common Questions

### "Which system should I use?"

**General HVAC questions** (How often to change filter? What's a SEER rating? AC not cooling?)
→ Virtual HVAC Technician (FREE/LOCAL)

**Oil heating specific** (Fuel pump issues? Tank transfer problems? Float switch?)
→ Oil Tank Diagnostics (PAID/CLOUD)

### "Why two different systems?"

- **Virtual HVAC:** General HVAC knowledge works great with local Ollama (free, private, fast)
- **Oil Tank:** Highly specialized domain benefits from Claude's advanced reasoning (accurate, structured)

### "Can I use the free system for oil tank questions?"

You can ask general oil heating questions to the Virtual HVAC Technician (it has broad HVAC knowledge), but for specialized fuel pump diagnostics and step-by-step troubleshooting workflows, the Oil Tank Diagnostics tools are more accurate.

### "What if Ollama isn't running?"

```bash
docker ps | grep ollama
# If not running:
docker start ollama
# Verify model:
ollama list | grep llama3.2
# If model missing:
ollama pull llama3.2:3b
```

### "What if I don't have an API key?"

Oil tank diagnostics require a paid Anthropic API key. User needs to:
1. Sign up at https://console.anthropic.com/
2. Add payment method
3. Generate API key
4. Add to `.env.diagnostic`

---

## 🎓 Learning Resources

### For Understanding the Code

1. **CrewAI Framework:** https://docs.crewai.com/
2. **Ollama:** https://ollama.ai/
3. **Docker Compose:** https://docs.docker.com/compose/
4. **Anthropic API:** https://docs.anthropic.com/

### For Understanding HVAC

1. **hvac-technician/example-questions.txt** - 70+ example questions
2. **HVAC.md** - Technical analysis of heat pump systems
3. **Virtual HVAC Technician** - Ask it! That's what it's for.

---

## 📝 Git Information

**Repository:** https://github.com/sergeville/HVAC_ideas.git
**Branch:** main
**Working Directory:** `/Users/sergevilleneuve/Documents/MyExperiments/HVAC_ideas`

**Recent Important Commits:**
- Added Virtual HVAC Technician multi-agent system
- Clarified two different AI systems (FREE vs PAID)
- Added comprehensive documentation standards
- Improved link clarity in documentation

---

## 🤝 Contributing Guidelines

When working with this repository:

1. **Follow DOCUMENTATION_STANDARDS.md**
2. **Always distinguish FREE vs PAID systems**
3. **Use descriptive link text**
4. **Update this context file when architecture changes**
5. **Test commands before documenting them**
6. **Verify costs and prerequisites**

---

## 🆘 Troubleshooting

### Virtual HVAC Technician Issues

**Problem:** `hvac` command not found
**Solution:** Check `~/.zshrc` for hvac() function, reload with `source ~/.zshrc`

**Problem:** Docker container not running
**Solution:** `docker compose up -d` from opencode directory

**Problem:** Ollama model missing
**Solution:** `ollama pull llama3.2:3b`

### Oil Tank Diagnostics Issues

**Problem:** API key error
**Solution:** Verify `.env.diagnostic` has `ANTHROPIC_API_KEY=...`

**Problem:** Network error
**Solution:** Check internet connection, verify Anthropic API is accessible

**Problem:** Script not found
**Solution:** Run from HVAC_ideas root directory, ensure scripts are executable

---

## 📞 Quick Reference Commands

### Check System Status
```bash
# Check Ollama
docker ps | grep ollama
ollama list

# Check CrewAI container
docker compose -f /Users/sergevilleneuve/Documents/MyExperiments/opencode/docker-compose.yml ps

# Check API key
cat .env.diagnostic | grep ANTHROPIC_API_KEY
```

### Use Virtual HVAC Technician
```bash
# Shell command (easiest)
hvac "your question"

# Direct Docker
docker compose -f /path/to/opencode/docker-compose.yml exec crewai python /app/HVAC_ideas/hvac-technician/hvac_expert.py "question"

# Interactive mode
hvac  # no arguments
```

### Use Oil Tank Diagnostics
```bash
# From HVAC_ideas directory
./run_tank1_diagnostic.sh
./run_tank2_diagnostic.sh
./run_ai_tank2_diagnostic.sh
./run_ai_diagnostic.sh
```

---

**End of Context File**

This file should be read at the start of any session working with the HVAC_ideas repository to ensure proper understanding of the two AI systems, their differences, and how to work with each.
