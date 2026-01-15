# HVAC_ideas Dependency Hierarchy

This document provides a comprehensive view of all dependencies in the HVAC_ideas project, organized by category and showing the complete dependency tree.

**Last Updated:** 2026-01-15

---

## 📊 Dependency Tree Overview

```
HVAC_ideas Project
├── System Dependencies (OS-level)
├── Runtime Dependencies (Docker, Ollama, Python)
├── Python Package Dependencies (pip)
├── Script Dependencies (Shell → Python)
├── Internal Module Dependencies (Python → Python)
└── Documentation Dependencies
```

---

## 🖥️ System Dependencies

### Required Operating Systems
- **macOS** - Primary development and testing platform
  - Required for: `resolve_system_issues.sh` (uses macOS `log show` command)
  - Version: macOS 11.0+ recommended

### Optional
- **Linux** - Compatible for most features except macOS-specific log resolution
- **Windows** - Compatible via WSL (Windows Subsystem for Linux)

---

## 🐳 Runtime Dependencies

### 1. Python Environment

```
Python 3.8+
├── Virtual Environment (venv) - OPTIONAL
│   └── Isolates project dependencies
└── System Python 3 - FALLBACK
    └── Used when venv not available
```

**Installation:**
```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

### 2. Docker Ecosystem (for Virtual HVAC Technician only)

```
Docker Desktop
└── CrewAI Container
    ├── Python Runtime
    ├── CrewAI Framework
    └── Network Connection to Ollama
```

**Required for:** `hvac-technician/` subproject only
**Not required for:** Oil tank diagnostic tools

### 3. Ollama (for Virtual HVAC Technician only)

```
Ollama Runtime
└── llama3.2:3b Model
    └── 3 billion parameter local language model
```

**Installation:**
```bash
# Install Ollama from https://ollama.ai
ollama pull llama3.2:3b
```

**Required for:** `hvac-technician/` subproject only
**Cost:** FREE (runs locally)

---

## 📦 Python Package Dependencies

### From requirements.txt

```
requirements.txt
├── feedparser              # RSS feed parsing
├── google-generativeai     # Google Gemini AI (optional)
├── python-dotenv          # Environment variable loading
├── beautifulsoup4         # HTML parsing
├── requests               # HTTP requests
├── scikit-learn           # Machine learning (clustering)
├── numpy                  # Numerical computing
└── python-dateutil        # Date parsing utilities
```

### Additional Dependencies (Not in requirements.txt)

```
Additional Python Packages
├── anthropic              # Claude API for AI diagnostics
│   └── Used by: ai_tank1_diagnostic.py, ai_tank2_diagnostic.py
│
└── reportlab              # PDF generation
    └── Used by: generate_tank1_diagnostic_pdf.py, generate_troubleshooting_pdf.py
```

**Installation:**
```bash
# Install from requirements.txt
pip install -r requirements.txt

# Install additional dependencies
pip install anthropic reportlab
```

---

## 🔧 Script → Execution Dependencies

### Shell Scripts (scripts/) → Python Files (execution/)

```
scripts/
│
├── run_ai_diagnostic.sh
│   ├── Requires: anthropic library
│   ├── Requires: .env.diagnostic with ANTHROPIC_API_KEY
│   └── Executes: execution/ai_tank1_diagnostic.py
│
├── run_ai_tank2_diagnostic.sh
│   ├── Requires: anthropic library
│   ├── Requires: .env.diagnostic with ANTHROPIC_API_KEY
│   └── Executes: execution/ai_tank2_diagnostic.py
│
├── run_tank1_diagnostic.sh
│   ├── Requires: No external API
│   └── Executes: execution/tank1_diagnostic_app.py
│
├── run_tank2_diagnostic.sh
│   ├── Requires: No external API
│   └── Executes: execution/tank2_diagnostic_app.py
│
└── resolve_system_issues.sh
    ├── Requires: macOS system
    ├── Requires: log show command
    ├── Executes (Phase 1): execution/parse_macos_logs.py
    ├── Executes (Phase 2): execution/agent_debate.py
    └── Executes (Phase 3): execution/agent_coordinator.py
```

---

## 🐍 Python Module Dependencies

### Execution Scripts Internal Dependencies

```
execution/
│
├── ai_tank1_diagnostic.py
│   ├── anthropic (external)
│   ├── os, sys, json (stdlib)
│   ├── dotenv (load_dotenv)
│   └── datetime (stdlib)
│
├── ai_tank2_diagnostic.py
│   ├── anthropic (external)
│   ├── os, sys, json (stdlib)
│   ├── dotenv (load_dotenv)
│   └── datetime (stdlib)
│
├── tank1_diagnostic_app.py
│   ├── sys (stdlib)
│   └── datetime (stdlib)
│
├── tank2_diagnostic_app.py
│   ├── sys (stdlib)
│   └── datetime (stdlib)
│
├── parse_macos_logs.py
│   ├── sys, re (stdlib)
│   ├── collections.defaultdict, Counter
│   └── datetime
│
├── agent_debate.py
│   ├── sys, json (stdlib)
│   └── dataclasses
│
├── agent_coordinator.py
│   ├── sys, json (stdlib)
│   ├── datetime
│   └── pathlib.Path
│
├── generate_tank1_diagnostic_pdf.py
│   ├── reportlab.* (external)
│   ├── datetime
│   └── pathlib.Path
│
├── generate_troubleshooting_pdf.py
│   ├── reportlab.* (external)
│   └── datetime
│
├── fetch_rss.py
│   ├── feedparser (external)
│   ├── json
│   └── datetime, timedelta
│
├── clean_reddit_data.py
│   ├── json
│   └── dateutil.parser (external)
│
├── evaluate_posts.py
│   ├── google.generativeai (external)
│   ├── dotenv (external)
│   ├── os, json, sys, time
│   └── typing
│
├── cluster_stories.py
│   ├── sklearn.cluster.AgglomerativeClustering (external)
│   ├── numpy (external)
│   ├── json, sys
│   └── typing
│
├── summarize_posts.py
│   ├── google.generativeai (external)
│   ├── dotenv (external)
│   ├── os, json, sys
│   └── typing
│
├── evaluate_clusters.py
│   ├── google.generativeai (external)
│   ├── json, sys
│   └── typing
│
└── summarize_clusters.py
    ├── google.generativeai (external)
    ├── json, sys
    └── typing
```

---

## 🌐 External API Dependencies

### Required API Keys

```
External APIs
│
├── Anthropic Claude API
│   ├── Required for: AI-powered diagnostics
│   ├── Configuration: .env.diagnostic
│   ├── Environment Variable: ANTHROPIC_API_KEY
│   ├── Cost: ~$0.01-0.05 per diagnostic session
│   └── Used by:
│       ├── ai_tank1_diagnostic.py
│       └── ai_tank2_diagnostic.py
│
└── Google Gemini API (Optional)
    ├── Required for: Reddit/RSS processing features
    ├── Configuration: .env or python-dotenv
    ├── Environment Variable: GOOGLE_API_KEY
    ├── Cost: Varies by usage
    └── Used by:
        ├── evaluate_posts.py
        ├── summarize_posts.py
        ├── evaluate_clusters.py
        └── summarize_clusters.py
```

---

## 📁 Configuration File Dependencies

### Environment Files

```
Configuration Files
│
├── .env.diagnostic
│   ├── Format: KEY=value
│   ├── Required Keys:
│   │   └── ANTHROPIC_API_KEY
│   ├── Optional Keys:
│   │   └── MODEL (Claude model selection)
│   └── Used by:
│       ├── ai_tank1_diagnostic.py
│       └── ai_tank2_diagnostic.py
│
├── .env.diagnostic.example
│   └── Template for .env.diagnostic
│
├── env.example
│   └── Generic environment template
│
└── requirements.txt
    └── Python package dependencies
```

---

## 📚 Documentation Dependencies

### Document Cross-References

```
Documentation Hierarchy
│
├── README.md (Root)
│   ├── → HVAC_Docs/README.md
│   ├── → CLAUDE.md
│   ├── → CHANGELOG.md
│   └── → HVAC_Docs/Technical_Guides/*.md
│
├── CLAUDE.md, AGENTS.md, GEMINI.md
│   ├── → directives/ (Layer 1)
│   ├── → execution/ (Layer 3)
│   └── → HVAC_Docs/
│
├── HVAC_Docs/README.md
│   ├── → Technical_Guides/*.md
│   ├── → Procedures/*.md
│   ├── → Development_Docs/*.md
│   └── → Prompts_and_Guides/*.md
│
└── CHANGELOG.md
    └── → DOCUMENTATION_TRACKING.md (this file)
```

---

## 🔄 Data Flow Dependencies

### Runtime Data Flow

```
User Input
    ↓
Shell Script (scripts/)
    ↓
Python Execution Script (execution/)
    ↓
    ├─→ External API (Anthropic/Google) [if required]
    │     ↓
    │   API Response
    │     ↓
    └─→ Processing Logic
          ↓
        Output Files (.tmp/)
          ↓
        User Output (Terminal/File)
```

### Example: AI Tank Diagnostic Flow

```
User runs: ./scripts/run_ai_diagnostic.sh
    ↓
run_ai_diagnostic.sh
    ├─→ Checks: .env.diagnostic exists
    ├─→ Loads: venv or system Python
    ├─→ Verifies: anthropic library installed
    └─→ Executes: execution/ai_tank1_diagnostic.py
              ↓
         ai_tank1_diagnostic.py
              ├─→ Loads: .env.diagnostic (ANTHROPIC_API_KEY)
              ├─→ Imports: anthropic library
              ├─→ Creates: Claude API client
              ├─→ Prompts: User for diagnostic information
              ├─→ Sends: User input to Claude API
              ├─→ Receives: AI diagnostic response
              ├─→ Saves: Conversation to .tmp/Tank1_AI_Conversation_*.txt
              └─→ Outputs: Diagnostic results to terminal
```

---

## 🎯 Dependency Groups by Feature

### Feature 1: AI Tank Diagnostics (Claude API - PAID)

**Dependencies:**
```
System:
  - Python 3.8+
  - Internet connection

Python Packages:
  - anthropic
  - python-dotenv

Configuration:
  - .env.diagnostic with ANTHROPIC_API_KEY

Scripts:
  - scripts/run_ai_diagnostic.sh
  - scripts/run_ai_tank2_diagnostic.sh

Execution:
  - execution/ai_tank1_diagnostic.py
  - execution/ai_tank2_diagnostic.py
```

### Feature 2: Basic Tank Diagnostics (FREE)

**Dependencies:**
```
System:
  - Python 3.8+

Python Packages:
  - None (stdlib only)

Scripts:
  - scripts/run_tank1_diagnostic.sh
  - scripts/run_tank2_diagnostic.sh

Execution:
  - execution/tank1_diagnostic_app.py
  - execution/tank2_diagnostic_app.py
```

### Feature 3: Virtual HVAC Technician (FREE, LOCAL)

**Dependencies:**
```
System:
  - Docker Desktop
  - Ollama with llama3.2:3b model

Python Packages:
  - CrewAI (in Docker container)

Subproject:
  - hvac-technician/

Execution:
  - hvac-technician/hvac_expert.py
```

### Feature 4: Multi-Agent Log Resolution

**Dependencies:**
```
System:
  - macOS (for log show command)
  - Python 3.8+

Python Packages:
  - None (stdlib only)

Scripts:
  - scripts/resolve_system_issues.sh

Execution:
  - execution/parse_macos_logs.py
  - execution/agent_debate.py
  - execution/agent_coordinator.py
```

### Feature 5: Reddit/RSS Processing (Optional)

**Dependencies:**
```
System:
  - Python 3.8+
  - Internet connection

Python Packages:
  - feedparser
  - google-generativeai
  - python-dotenv
  - beautifulsoup4
  - requests
  - scikit-learn
  - numpy
  - python-dateutil

Configuration:
  - .env with GOOGLE_API_KEY

Execution:
  - execution/fetch_rss.py
  - execution/clean_reddit_data.py
  - execution/evaluate_posts.py
  - execution/cluster_stories.py
  - execution/summarize_posts.py
  - execution/evaluate_clusters.py
  - execution/summarize_clusters.py
```

### Feature 6: PDF Generation

**Dependencies:**
```
System:
  - Python 3.8+

Python Packages:
  - reportlab

Execution:
  - execution/generate_tank1_diagnostic_pdf.py
  - execution/generate_troubleshooting_pdf.py
```

---

## 🚀 Quick Setup Guide by Feature

### Minimal Setup (Basic Diagnostics - FREE)
```bash
# No dependencies needed!
./scripts/run_tank1_diagnostic.sh
./scripts/run_tank2_diagnostic.sh
```

### AI Diagnostics Setup (Claude API - PAID)
```bash
# Install Python dependencies
pip install anthropic python-dotenv

# Create configuration
cp .env.diagnostic.example .env.diagnostic
# Edit .env.diagnostic and add your ANTHROPIC_API_KEY

# Run
./scripts/run_ai_diagnostic.sh
```

### Virtual HVAC Technician Setup (FREE, LOCAL)
```bash
# Install Ollama
# Download from https://ollama.ai

# Pull model
ollama pull llama3.2:3b

# Start Docker container (requires docker-compose setup)
docker compose up -d

# Run
docker compose exec crewai python /app/HVAC_ideas/hvac-technician/hvac_expert.py
```

### Full Setup (All Features)
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
pip install anthropic reportlab

# Configure API keys
cp .env.diagnostic.example .env.diagnostic
# Edit .env.diagnostic with ANTHROPIC_API_KEY

# Install Ollama and pull model
ollama pull llama3.2:3b

# Ready to use all features!
```

---

## 📋 Dependency Checklist

Use this checklist to verify your environment is properly configured:

### Core Dependencies
- [ ] Python 3.8+ installed
- [ ] Can run `python3 --version` successfully

### Optional: Virtual Environment
- [ ] Virtual environment created (`python3 -m venv venv`)
- [ ] Virtual environment activated (`source venv/bin/activate`)

### For AI Diagnostics (Claude API)
- [ ] `anthropic` library installed (`pip install anthropic`)
- [ ] `.env.diagnostic` file exists
- [ ] `ANTHROPIC_API_KEY` set in `.env.diagnostic`
- [ ] Internet connection available

### For Virtual HVAC Technician
- [ ] Docker Desktop installed and running
- [ ] Ollama installed and running
- [ ] `llama3.2:3b` model downloaded (`ollama pull llama3.2:3b`)
- [ ] CrewAI container built and running

### For Reddit/RSS Processing
- [ ] All packages from `requirements.txt` installed
- [ ] `.env` file with `GOOGLE_API_KEY` (if using Gemini)

### For macOS Log Resolution
- [ ] Running on macOS system
- [ ] `log show` command available

### For PDF Generation
- [ ] `reportlab` library installed (`pip install reportlab`)

---

## 🔍 Troubleshooting Dependencies

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'anthropic'`
```bash
# Solution:
pip install anthropic
```

**Issue:** `API key not found`
```bash
# Solution:
# 1. Check .env.diagnostic exists
ls -la .env.diagnostic

# 2. Verify ANTHROPIC_API_KEY is set
cat .env.diagnostic | grep ANTHROPIC_API_KEY

# 3. Create from template if missing
cp .env.diagnostic.example .env.diagnostic
# Then edit .env.diagnostic with your API key
```

**Issue:** `Cannot connect to Ollama`
```bash
# Solution:
# 1. Check Ollama is running
ollama list

# 2. Verify model is downloaded
ollama pull llama3.2:3b

# 3. Check Docker container networking
docker ps | grep crewai
```

**Issue:** `log show: command not found`
```bash
# Solution:
# This feature requires macOS
# Use on macOS system or skip multi-agent log resolution
```

---

## 📊 Dependency Summary

| Category | Count | Type |
|----------|-------|------|
| **System Dependencies** | 3 | OS, Docker, Ollama |
| **Python Packages (requirements.txt)** | 8 | External libraries |
| **Python Packages (additional)** | 2 | anthropic, reportlab |
| **Shell Scripts** | 5 | Launcher scripts |
| **Python Execution Scripts** | 16 | Core logic |
| **External APIs** | 2 | Anthropic, Google |
| **Configuration Files** | 3 | .env files |
| **Subprojects** | 1 | hvac-technician |

---

## 🔗 Related Documentation

- [Project Context](PROJECT_CONTEXT.md) - Complete project overview
- [Documentation Tracking](DOCUMENTATION_TRACKING.md) - Git workflow guide
- [LLM Switching Guide](LLM_SWITCHING_GUIDE.md) - How to switch between AI models
- [README.md](../../README.md) - Main project documentation

---

**Document Maintained By:** AI + Human collaboration
**Update Frequency:** As dependencies change
**Version Control:** Tracked in git with project
