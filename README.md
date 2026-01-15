# HVAC Ideas & AI-Powered Tools

A comprehensive collection of HVAC (Heating, Ventilation, and Air Conditioning) AI-powered diagnostic tools, technical documentation, and troubleshooting guides.

**⚡ Two AI Systems Available:**
- **System 1:** Virtual HVAC Technician - 🟢 FREE (Local Ollama + CrewAI)
- **System 2:** Oil Tank Diagnostics - 🔵 PAID (Claude API, cloud-based)

## 🚀 AI-Powered Tools

### 1. Virtual HVAC Technician 🔧 🟢 FREE & LOCAL
**Location:** `hvac-technician/`
**AI System:** CrewAI + Ollama (llama3.2:3b) running in Docker
**Cost:** $0.00 - Completely free, runs 100% locally
**Privacy:** All data stays on your machine, no cloud, no internet required

An AI expert assistant with 20+ years of virtual HVAC knowledge. Ask any question about heating, cooling, ventilation, installation, maintenance, or troubleshooting.

**Features:**
- Two specialized AI agents (Master Technician + Diagnostics Specialist)
- Interactive chat mode or single-question mode
- Auto-detects troubleshooting questions
- Covers residential & commercial systems
- Safety-first approach
- **No API keys needed** - everything runs locally

**Quick Start:**
```bash
# Using the hvac command (if configured)
hvac "How often should I change my HVAC filter?"

# Or directly via Docker
docker compose exec crewai python /app/HVAC_ideas/hvac-technician/hvac_expert.py
```

📖 [Virtual HVAC Technician Full Documentation](hvac-technician/README.md)

### 2. Oil Tank Diagnostic Tools ⛽ 🔵 PAID (Claude API)
**AI System:** Claude API (Anthropic, cloud-based)
**Cost:** Paid API - Requires Anthropic API key (~$0.01-0.05 per diagnostic session)
**Privacy:** Data sent to Anthropic's servers for processing
**Setup Required:** ANTHROPIC_API_KEY in `.env.diagnostic` file

AI-powered troubleshooting scripts for oil heating systems, specifically focused on fuel pump and tank transfer issues.

**⚠️ Important:** These scripts use the Claude API (not local). You need:
1. An Anthropic API account at https://console.anthropic.com/
2. A paid API key configured in `.env.diagnostic`
3. Internet connection for API calls

**Available Scripts:**

#### Tank 1 Diagnostics
- **`run_tank1_diagnostic.sh`** - Tank 1 auto-fill diagnostic questionnaire
- Troubleshoots automatic fill systems, float switches, and control boxes

#### Tank 2 Diagnostics
- **`run_tank2_diagnostic.sh`** - Tank 2 transfer pump diagnostic
- **`run_ai_tank2_diagnostic.sh`** - AI-enhanced Tank 2 diagnostics
- Troubleshoots fuel transfer pumps, relay issues, and electrical problems

#### General AI Diagnostics
- **`run_ai_diagnostic.sh`** - General oil tank AI diagnostic assistant
- Interactive troubleshooting for fuel pump systems
- Helps identify root causes and recommend solutions

**Quick Start:**
```bash
# Run Tank 1 diagnostics
./run_tank1_diagnostic.sh

# Run Tank 2 AI-enhanced diagnostics
./run_ai_tank2_diagnostic.sh

# General AI diagnostic assistant
./run_ai_diagnostic.sh
```

**Documentation:**
- 📖 [Tank Diagnostics Guide](HVAC_Docs/Technical_Guides/TANK_DIAGNOSTICS_GUIDE.md)
- 📖 [Tank 1 Diagnostic App README](HVAC_Docs/Technical_Guides/TANK1_DIAGNOSTIC_APP_README.md)
- 📖 [AI Diagnostic README](HVAC_Docs/Technical_Guides/AI_DIAGNOSTIC_README.md)
- 📖 [All Diagnostic Apps Overview](HVAC_Docs/Technical_Guides/ALL_DIAGNOSTIC_APPS.md)
- 📖 [Diagnostic Apps Comparison](HVAC_Docs/Technical_Guides/DIAGNOSTIC_APPS_COMPARISON.md)
- 📄 [Tank 1 Auto Fill Guide (PDF)](HVAC_Docs/Technical_Guides/Tank1_Auto_Fill_Diagnostic_Guide.pdf)
- 📄 [Oil Tank Transfer Troubleshooting (PDF)](HVAC_Docs/Technical_Guides/Oil_Tank_Transfer_Troubleshooting_Guide.pdf)

## 📚 Project Contents

### Documentation

All technical documentation has been organized in the **HVAC_Docs/** directory:

- **[HVAC_Docs/](HVAC_Docs/)** - Complete documentation hub
  - **Technical_Guides/** - Diagnostic guides, troubleshooting PDFs, HVAC diagrams
  - **Procedures/** - Step-by-step verification procedures and checklists
  - **Development_Docs/** - Project context, standards, and improvement logs
  - **Prompts_and_Guides/** - AI prompt guides and HVAC AR glasses documentation

See the [HVAC Documentation Index](HVAC_Docs/README.md) for a complete navigation guide.

### Code & Architecture

This project follows a **3-layer architecture** for maximum reliability:

1. **Layer 1: Directives** (`directives/`) - SOPs and instructions in Markdown
2. **Layer 2: Orchestration** (AI agents) - Intelligent routing and decision-making
3. **Layer 3: Execution** (`execution/`) - Deterministic Python scripts

**Key Files:**
- **main.py** - Python utilities for HVAC analysis
- **requirements.txt** - Python package dependencies
- **.tmp/** - Temporary/intermediate processing files (not committed)

See [CLAUDE.md](CLAUDE.md) for complete architecture documentation.

## Key Components Reference

The documentation covers these primary HVAC components:

- **COMP** - Compressor
- **OFM** - Outdoor Fan Motor
- **CB** - Control Board
- **CONT** - Contactor
- **CAP** - Dual Capacitor
- **TRAN** - Transformer
- **CCH** - Crankcase Heater
- **RVS** - Reversing Valve

## 🛠️ Prerequisites

### For Virtual HVAC Technician (Local/Free)

1. **Docker Desktop** - Running on your machine
2. **Ollama** - Local LLM runtime with `llama3.2:3b` model
   ```bash
   # Install Ollama from https://ollama.ai
   # Pull the model:
   ollama pull llama3.2:3b
   ```
3. **CrewAI Container** - Docker container with CrewAI framework
   ```bash
   # Navigate to the directory with docker-compose.yml
   cd /path/to/opencode
   docker compose build
   docker compose up -d
   ```

For detailed setup instructions, see the [Virtual HVAC Technician README](hvac-technician/README.md).

### For Oil Tank Diagnostics (Claude API/Paid)

1. **Anthropic API Account** - Sign up at https://console.anthropic.com/
2. **API Key** - Generate a paid API key from your account
3. **Configuration File** - Create `.env.diagnostic` with:
   ```bash
   ANTHROPIC_API_KEY=your-api-key-here
   ```
4. **Internet Connection** - Required for API calls to Anthropic servers

**Estimated Costs:**
- ~$0.01-0.05 per diagnostic session
- Pay-as-you-go billing through Anthropic

For detailed information, see the diagnostic tool documentation files listed above.

## 📖 Additional Documentation

### Core AI Instructions (Root)
- **[AGENTS.md](AGENTS.md)** - Multi-agent system architecture and instructions
- **[CLAUDE.md](CLAUDE.md)** - Claude AI configuration and prompts
- **[GEMINI.md](GEMINI.md)** - Gemini AI configuration and prompts

### Technical Procedures
- **[Oil Tank Transfer Box Verification](HVAC_Docs/Procedures/Oil%20Tank%20Transfer%20Box%20Verification%20Procedure.md)** - Step-by-step verification guide
- **[PLC Fault Code Guide](HVAC_Docs/Procedures/PLC%20Fault%20Code%20Guide.md)** - PLC error codes and solutions
- **[Technical Verification Checklist](HVAC_Docs/Procedures/checklist.md)** - System verification steps

### Development Documentation
- **[Project Context](HVAC_Docs/Development_Docs/PROJECT_CONTEXT.md)** - Comprehensive project overview for AI assistants
- **[Documentation Standards](HVAC_Docs/Development_Docs/DOCUMENTATION_STANDARDS.md)** - Documentation best practices
- **[Model Fix Guide](HVAC_Docs/Development_Docs/MODEL_FIX_README.md)** - AI model configuration fixes
- **[Multi-Agent Log Resolution](HVAC_Docs/Development_Docs/multi-agents-log-resolution.md)** - Agent collaboration workflows
- **[Improvements Summary](HVAC_Docs/Development_Docs/IMPROVEMENTS_SUMMARY.md)** - System enhancements and changes

## 🐍 Python Environment (For Non-AI Tools)

If you plan to use the traditional Python tools:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 💡 Use Cases

This repository is useful for:
- **HVAC Technicians** - AI-powered troubleshooting and diagnostics
- **Oil Heating Specialists** - Fuel pump and tank transfer diagnostics
- **Field Technicians** - Real-time AR-assisted diagnostics
- **Students** - Learning HVAC electrical systems and diagnostics
- **DIY Homeowners** - Understanding their HVAC systems safely
- **System Integrators** - Multi-agent diagnostic workflows

## 🎯 Why This Repository?

### Virtual HVAC Technician (Local/Free)
✅ **100% Free** - No API costs, all local using Ollama
✅ **Privacy** - All diagnostics run on your machine, no cloud
✅ **Offline** - Works without internet once set up
✅ **Unlimited Usage** - Ask as many questions as you want

### Oil Tank Diagnostics (Claude API/Paid)
🔵 **Specialized Knowledge** - Deep expertise in oil heating systems
🔵 **Highly Accurate** - Uses Claude's advanced reasoning
🔵 **Structured Diagnostics** - Step-by-step troubleshooting workflows
🔵 **Cost-Effective** - Only ~$0.01-0.05 per diagnostic session

### Both Systems
✅ **Safety First** - All tools emphasize safety and when to call professionals
✅ **Multiple Approaches** - General questions, specific troubleshooting, step-by-step guides
✅ **Professional Quality** - Built with real-world HVAC expertise

## 📄 License

This is a personal project for educational and professional reference purposes.

## 🤝 Contributing

This is an experimental repository. Feel free to learn from it and adapt the AI diagnostic approaches for your own projects!
