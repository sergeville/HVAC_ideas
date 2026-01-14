# HVAC Ideas & AI-Powered Tools

A comprehensive collection of HVAC (Heating, Ventilation, and Air Conditioning) AI-powered diagnostic tools, technical documentation, and troubleshooting guides.

**🤖 Powered by Local AI** - All AI tools run locally using Ollama (no cloud, no API costs, completely free and private)

## 🚀 AI-Powered Tools

### 1. Virtual HVAC Technician 🔧
**Location:** `hvac-technician/`

An AI expert assistant with 20+ years of virtual HVAC knowledge. Ask any question about heating, cooling, ventilation, installation, maintenance, or troubleshooting.

**Features:**
- Two specialized AI agents (Master Technician + Diagnostics Specialist)
- Interactive chat mode or single-question mode
- Auto-detects troubleshooting questions
- Covers residential & commercial systems
- Safety-first approach

**Quick Start:**
```bash
# Using the hvac command (if configured)
hvac "How often should I change my HVAC filter?"

# Or directly via Docker
docker compose exec crewai python /app/HVAC_ideas/hvac-technician/hvac_expert.py
```

📖 [Full Documentation](hvac-technician/README.md)

### 2. Oil Tank Diagnostic Tools ⛽

AI-powered troubleshooting scripts for oil heating systems, specifically focused on fuel pump and tank transfer issues.

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
- 📖 [Tank Diagnostics Guide](TANK_DIAGNOSTICS_GUIDE.md)
- 📖 [Tank 1 Diagnostic App README](TANK1_DIAGNOSTIC_APP_README.md)
- 📖 [AI Diagnostic README](AI_DIAGNOSTIC_README.md)
- 📖 [All Diagnostic Apps Overview](ALL_DIAGNOSTIC_APPS.md)
- 📖 [Diagnostic Apps Comparison](DIAGNOSTIC_APPS_COMPARISON.md)
- 📄 [Tank 1 Auto Fill Guide (PDF)](Tank1_Auto_Fill_Diagnostic_Guide.pdf)
- 📄 [Oil Tank Transfer Troubleshooting (PDF)](Oil_Tank_Transfer_Troubleshooting_Guide.pdf)

## 📚 Project Contents

### Documentation

- **HVAC.md** - Comprehensive technical analysis of outdoor heat pump unit electrical wiring
  - Component abbreviations and functions
  - System logic and power flow diagrams
  - Safety switches and sensors reference
  - Standard wire color guide

- **AI-Prompt-Guide-for-HVAC-AR-Glasses.md** - Guide for using AI-powered AR glasses in HVAC fieldwork
  - Optimized prompts for real-time diagnostics
  - Best practices for using AR glasses with HVAC systems
  - Hardware limitations and workarounds

### Diagrams & References

- **hvac.jpeg** - HVAC system diagram
- **can help me understand this hvac diagram.pdf** - Technical schematic reference document

### Code

- **main.py** - Python utilities for HVAC analysis
- **requirements.txt** - Python package dependencies

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

## 🛠️ Prerequisites (For AI Tools)

To use the AI-powered tools, you need:

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

## 📖 Additional Documentation

### Technical Guides
- **[Oil Tank Transfer Box Verification Procedure](Oil%20Tank%20Transfer%20Box%20Verification%20Procedure.md)** - Step-by-step verification guide
- **[PLC Fault Code Guide](PLC%20Fault%20Code%20Guide.md)** - PLC error codes and solutions
- **[Model Fix README](MODEL_FIX_README.md)** - AI model configuration fixes

### Multi-Agent Systems
- **[AGENTS.md](AGENTS.md)** - Multi-agent system documentation
- **[Multi-Agent Log Resolution](multi-agents-log-resolution.md)** - Agent collaboration for log analysis
- **[Log Resolution README](README_LOG_RESOLUTION.md)** - Detailed log analysis guide

### AI Prompts & Guides
- **[CLAUDE.md](CLAUDE.md)** - Claude AI configuration and prompts
- **[GEMINI.md](GEMINI.md)** - Gemini AI configuration and prompts
- **[AI Co-authorship Legal Implications](AI%20Co-authorship%20and%20Legal%20Implications.md)** - Legal considerations for AI-generated content

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

✅ **Free AI Tools** - No API costs, all local using Ollama
✅ **Privacy** - All diagnostics run on your machine
✅ **Specialized Knowledge** - 20+ years of virtual HVAC expertise
✅ **Multiple Diagnostic Approaches** - General questions, specific troubleshooting, step-by-step guides
✅ **Safety First** - All tools emphasize safety and when to call professionals

## 📄 License

This is a personal project for educational and professional reference purposes.

## 🤝 Contributing

This is an experimental repository. Feel free to learn from it and adapt the AI diagnostic approaches for your own projects!
