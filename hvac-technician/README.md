# 🔧 Virtual HVAC Technician

An AI-powered HVAC expert assistant that answers all kinds of questions about heating, ventilation, and air conditioning systems.

**🏠 100% LOCAL** - Runs entirely on your machine using Ollama (no internet, no API costs, completely free and private)

## Prerequisites

Before using this project, you need:

1. **Docker Desktop** - Running on your machine
2. **Ollama** - Running locally with the `llama3.2:3b` model
   ```bash
   # Install Ollama from https://ollama.ai
   # Pull the model:
   ollama pull llama3.2:3b
   ```
3. **CrewAI Container** - Built from the provided Docker setup (see Setup section)

## Features

✅ **Expert HVAC Knowledge**
- Residential & commercial systems
- Heating, cooling, and ventilation
- Troubleshooting and diagnostics
- Installation and maintenance
- Energy efficiency tips
- Safety guidelines

✅ **Two Specialized Agents**
1. **Master HVAC Technician** - General HVAC questions
2. **Diagnostics Specialist** - Troubleshooting and repairs

✅ **Interactive or Single-Question Mode**
- Chat continuously with the AI expert
- Or ask a single question and get an answer

## Setup

This project requires a Docker container with CrewAI and a connection to your local Ollama instance.

### Step 1: Install and Start Ollama

```bash
# Install Ollama from https://ollama.ai
# Or if you have it in Docker:
docker start ollama

# Pull the required model:
ollama pull llama3.2:3b

# Verify it's running:
ollama list
```

### Step 2: Build the CrewAI Container

Navigate to the parent directory containing `docker-compose.yml` and `Dockerfile`:

```bash
cd /path/to/opencode  # Or wherever your docker-compose.yml is located
docker compose build
docker compose up -d
```

This creates a container that:
- Has CrewAI, LangChain, and LiteLLM installed
- Can communicate with your local Ollama instance
- Mounts this hvac-technician folder for access to the scripts

### Step 3: Verify Setup

```bash
# Check containers are running:
docker ps

# You should see:
# - ollama container (if using Docker for Ollama)
# - crewai-agent container
```

## Quick Start

**Note:** These commands assume you're in the directory containing `docker-compose.yml` (e.g., `/path/to/opencode/`).
If the compose file is in a different location, add `-f /path/to/docker-compose.yml` to the commands.

### Interactive Mode (Recommended)

```bash
docker compose exec crewai python /app/HVAC_ideas/hvac-technician/hvac_expert.py
```

Then ask questions like:
```
❓ Your question: How do I change my HVAC filter?
❓ Your question: My AC is not cooling properly, what should I check?
❓ Your question: What's the difference between a heat pump and a furnace?
```

Type `quit` to exit.

### Single Question Mode

```bash
docker compose exec crewai python /app/HVAC_ideas/hvac-technician/hvac_expert.py "How often should I replace my HVAC filter?"
```

### Using the Shell Command (If Configured)

If you've set up the `hvac` shell function in your `~/.zshrc`:

```bash
# Single question with animated spinner
hvac "How often should I change my HVAC filter?"

# Interactive mode
hvac
```

This provides a cleaner interface with automatic error filtering and progress indication.

## Example Questions

### General HVAC Questions

```
- What is SEER rating and why does it matter?
- How does a heat pump work?
- What size AC unit do I need for a 2000 sq ft home?
- What's the difference between central air and mini-split?
- How can I improve my home's air quality?
- What temperature should I set my thermostat?
- How much does it cost to install central air?
```

### Troubleshooting Questions

```
- My AC is running but not cooling
- Furnace keeps shutting off
- Thermostat not responding
- Strange smell coming from vents
- Ice buildup on AC unit
- Uneven heating in different rooms
- Loud noise from HVAC system
```

### Maintenance Questions

```
- How often should I service my HVAC?
- What maintenance can I do myself?
- How do I clean my AC coils?
- When should I replace my system?
- How to prepare HVAC for winter/summer?
- Signs my HVAC needs repair
```

### Installation Questions

```
- Can I install a thermostat myself?
- What tools do I need for HVAC maintenance?
- How to size a new HVAC system?
- Ductless vs ducted systems
- Best HVAC brands?
```

## How It Works

The system automatically detects if your question is about:
- **General Information** → Uses Master HVAC Technician
- **Troubleshooting** → Uses Diagnostics Specialist

**Troubleshooting keywords detected:**
- "not working", "broken", "problem", "issue"
- "fix", "repair", "troubleshoot", "diagnose"
- "won't", "doesn't"

## Safety First! ⚠️

The AI will remind you about:
- Electrical safety
- Gas line safety
- When to call a professional
- Proper tool usage
- Code compliance

**Always prioritize safety and call a licensed technician for complex repairs!**

## Customization

### Change the AI Model

Edit `hvac_expert.py`:
```python
llm = LLM(
    model="ollama/llama3.2:3b",  # Change this to a larger model
    base_url=ollama_host
)
```

### Add More Agents

You could add:
- **Energy Efficiency Expert** - Optimization tips
- **Installation Specialist** - Step-by-step install guides
- **Safety Inspector** - Code compliance checker

### Adjust Expertise Level

Modify the agent's `backstory` to:
- Focus on specific HVAC types (residential vs commercial)
- Specialize in certain brands
- Target DIY users vs professionals

## Example Session

```
🔧 Virtual HVAC Technician
============================================================
Your AI-powered HVAC expert is ready to help!
Ask me anything about heating, ventilation, air conditioning,
troubleshooting, maintenance, installation, and more.
============================================================

💬 Interactive Mode
Type your HVAC questions (or 'quit' to exit)
------------------------------------------------------------

❓ Your question: My furnace is making a loud banging noise

🔧 HVAC Expert:
------------------------------------------------------------
A loud banging noise from your furnace can indicate several issues.
Here's a step-by-step troubleshooting guide:

**Possible Causes:**
1. Delayed ignition (gas buildup)
2. Dirty burners
3. Expanding/contracting ductwork
4. Loose blower wheel
5. Cracked heat exchanger (serious!)

**Diagnostic Steps:**
1. Turn off the furnace immediately
2. Listen to when the noise occurs (startup, during operation, shutdown)
3. Check air filter - replace if dirty
4. Inspect visible ducts for loose connections
5. Look for any visible damage or debris

**Solutions:**
[Detailed solutions based on diagnosis]

**Safety Warnings:**
⚠️ Do NOT operate if you smell gas
⚠️ Cracked heat exchanger can leak carbon monoxide
⚠️ Turn off gas supply if you suspect gas leak

**Call a Professional If:**
- You smell gas or carbon monoxide
- Noise is very loud or getting worse
- You see cracks in the heat exchanger
- You're not comfortable with DIY inspection

------------------------------------------------------------
```

## Tips for Best Results

1. **Be Specific** - "AC not cooling" vs "AC making 60Hz humming noise"
2. **Include Details** - System type, age, recent changes
3. **Ask Follow-ups** - The AI remembers context in interactive mode
4. **Safety First** - Always follow safety recommendations

## Technical Stack

- **CrewAI** - Multi-agent AI framework for coordinating specialized agents
- **Ollama** - Local LLM runtime (runs llama3.2:3b model on your machine)
- **Docker** - Container orchestration for easy deployment
- **Python 3.11** - Application runtime environment

## Why Local AI?

✅ **100% Free** - No API costs, no subscriptions, no usage limits
✅ **Private** - All data stays on your machine, no external servers
✅ **No Internet Required** - Works completely offline once setup
✅ **Fast** - Direct communication between containers
✅ **Customizable** - Full control over models and agents

**Cost Comparison:**
- This setup: $0.00
- Cloud AI APIs: $0.01-0.10+ per question

## 🔗 Related Tools in This Repository

This Virtual HVAC Technician is part of a larger collection of HVAC diagnostic tools. You may also be interested in:

### Oil Tank & Fuel Pump Diagnostics ⛽

If you're troubleshooting oil heating systems, fuel pumps, or tank transfer issues, check out these specialized diagnostic scripts in the parent directory:

**Tank 1 Auto-Fill Diagnostics:**
- `run_tank1_diagnostic.sh` - Interactive diagnostic for automatic fill systems
- Helps troubleshoot float switches, control boxes, and fill automation

**Tank 2 Transfer Pump Diagnostics:**
- `run_tank2_diagnostic.sh` - Standard Tank 2 transfer pump diagnostic
- `run_ai_tank2_diagnostic.sh` - AI-enhanced diagnostics for fuel transfer systems
- Troubleshoots relay issues, electrical problems, and pump failures

**General Oil Tank AI Assistant:**
- `run_ai_diagnostic.sh` - General purpose oil tank diagnostic assistant
- Interactive troubleshooting for fuel pump systems
- Root cause analysis and solution recommendations

**Documentation:**
- [Tank Diagnostics Guide](../TANK_DIAGNOSTICS_GUIDE.md)
- [AI Diagnostic README](../AI_DIAGNOSTIC_README.md)
- [All Diagnostic Apps Overview](../ALL_DIAGNOSTIC_APPS.md)
- [Tank 1 Auto Fill Guide (PDF)](../Tank1_Auto_Fill_Diagnostic_Guide.pdf)
- [Oil Tank Transfer Troubleshooting (PDF)](../Oil_Tank_Transfer_Troubleshooting_Guide.pdf)

### How to Access These Tools

From the repository root (`/path/to/HVAC_ideas/`):

```bash
# Run Tank 1 diagnostics
./run_tank1_diagnostic.sh

# Run AI-enhanced Tank 2 diagnostics
./run_ai_tank2_diagnostic.sh

# General AI diagnostic assistant
./run_ai_diagnostic.sh
```

**Note:** These tools use the same local AI setup (Ollama + CrewAI) so you don't need any additional configuration!

---

**Need HVAC help? Your virtual technician is ready! 🔧**

**Questions or issues?** Make sure Ollama is running locally with `llama3.2:3b` model installed.
