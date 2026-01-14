# 🔧 Virtual HVAC Technician

An AI-powered HVAC expert assistant that answers all kinds of questions about heating, ventilation, and air conditioning systems.

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

## Quick Start

### Interactive Mode (Recommended)

```bash
docker compose exec crewai python hvac_expert.py
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
docker compose exec crewai python hvac_expert.py "How often should I replace my HVAC filter?"
```

### Use with olla (Simpler, No Container)

```bash
olla "You are an HVAC expert. How do I troubleshoot a furnace that won't turn on?"
```

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

## Powered By

- **CrewAI** - Multi-agent AI framework
- **Ollama** - Local AI (llama3.2:3b)
- **20+ years** of virtual HVAC expertise!

---

**Need HVAC help? Your virtual technician is ready! 🔧**
