# Complete Diagnostic Applications Guide

You have **4 diagnostic applications** available for troubleshooting the Oil Tank Transfer Box system.

## Quick Reference Table

| Tank | Type | Command | Cost | Requires Internet |
|------|------|---------|------|-------------------|
| **Tank #1** | Basic | `./run_tank1_diagnostic.sh` | FREE | NO |
| **Tank #1** | AI-Powered | `./run_ai_diagnostic.sh` | ~$0.10-$1.50/session | YES |
| **Tank #2** | Basic | `./run_tank2_diagnostic.sh` | FREE | NO |
| **Tank #2** | AI-Powered | `./run_ai_tank2_diagnostic.sh` | ~$0.10-$1.50/session | YES |

---

## Tank #1 Applications

### 1. Tank #1 Basic App (FREE)

**Command:**
```bash
./run_tank1_diagnostic.sh
```

**Features:**
- ✅ Completely FREE
- ✅ Works offline (no internet needed)
- ✅ No API key required
- ✅ Structured question flow
- ✅ Saves all answers to text file
- ✅ Covers all diagnostic steps

**Limitations:**
- ❌ Fixed questions (no adaptation)
- ❌ No natural conversation
- ❌ No clarifications or explanations
- ❌ Cannot handle unusual situations

**Output Files:**
- `.tmp/Tank1_Diagnostic_Session_YYYYMMDD_HHMMSS.txt`

**Best For:**
- Field work without internet
- Quick structured diagnostics
- Training new technicians
- When budget is $0

---

### 2. Tank #1 AI-Powered App

**Command:**
```bash
./run_ai_diagnostic.sh
```

**Features:**
- ✅ Natural conversation with AI
- ✅ Adapts to your answers
- ✅ Explains technical concepts
- ✅ Handles unusual situations
- ✅ Comprehensive analysis reports
- ✅ Can clarify confusing questions

**Requirements:**
- ❌ Anthropic API key (from console.anthropic.com)
- ❌ Internet connection
- ❌ API credits (~$0.10-$1.50 per session)

**Output Files:**
- `.tmp/Tank1_AI_Conversation_YYYYMMDD_HHMMSS.txt` (full conversation)
- `.tmp/Tank1_AI_Diagnostic_Report_YYYYMMDD_HHMMSS.txt` (structured report)
- `.tmp/Tank1_AI_Conversation_YYYYMMDD_HHMMSS.json` (machine-readable)

**Best For:**
- Complex problems
- Need expert guidance
- Want detailed analysis
- Building knowledge base

---

## Tank #2 Applications

### 3. Tank #2 Basic App (FREE)

**Command:**
```bash
./run_tank2_diagnostic.sh
```

**Features:**
- ✅ Completely FREE
- ✅ Works offline (no internet needed)
- ✅ No API key required
- ✅ Structured question flow
- ✅ Saves all answers to text file
- ✅ Covers all Tank #2 diagnostic steps

**Limitations:**
- ❌ Fixed questions (no adaptation)
- ❌ No natural conversation
- ❌ No clarifications or explanations
- ❌ Cannot handle unusual situations

**Output Files:**
- `.tmp/Tank2_Diagnostic_Session_YYYYMMDD_HHMMSS.txt`

**Best For:**
- Field work without internet
- Quick structured diagnostics
- Training new technicians
- When budget is $0

---

### 4. Tank #2 AI-Powered App

**Command:**
```bash
./run_ai_tank2_diagnostic.sh
```

**Features:**
- ✅ Natural conversation with AI
- ✅ Adapts to your answers
- ✅ Explains technical concepts
- ✅ Handles unusual situations
- ✅ Comprehensive analysis reports
- ✅ Can clarify confusing questions

**Requirements:**
- ❌ Anthropic API key (from console.anthropic.com)
- ❌ Internet connection
- ❌ API credits (~$0.10-$1.50 per session)

**Output Files:**
- `.tmp/Tank2_AI_Conversation_YYYYMMDD_HHMMSS.txt` (full conversation)
- `.tmp/Tank2_AI_Diagnostic_Report_YYYYMMDD_HHMMSS.txt` (structured report)
- `.tmp/Tank2_AI_Conversation_YYYYMMDD_HHMMSS.json` (machine-readable)

**Best For:**
- Complex problems
- Need expert guidance
- Want detailed analysis
- Building knowledge base

---

## Feature Comparison

| Feature | Basic Apps | AI-Powered Apps |
|---------|------------|-----------------|
| **Cost** | FREE | ~$0.10-$1.50/session |
| **Setup Time** | 0 minutes | 5 minutes (API key) |
| **Internet** | Not required | Required |
| **Conversation Style** | Fixed questions | Natural dialogue |
| **Adaptability** | None | Intelligent routing |
| **Explanations** | None | On demand |
| **Clarifications** | None | Anytime |
| **Report Quality** | Q&A list | Structured analysis |
| **Unusual Situations** | Cannot handle | Handles well |
| **Technical Training** | No | Yes (explains concepts) |

---

## When to Use Each App

### Use Basic Apps When:
- ✓ No internet connection available
- ✓ Zero budget
- ✓ Problem is straightforward
- ✓ Just need to document findings
- ✓ Training with structured flow

### Use AI Apps When:
- ✓ Complex or unusual problem
- ✓ Need guidance and explanations
- ✓ Want comprehensive analysis
- ✓ Building diagnostic knowledge base
- ✓ Internet and budget available

---

## Setup Instructions

### Basic Apps (Tank #1 & #2)

**No setup required!** Just run:

```bash
# Tank 1
./run_tank1_diagnostic.sh

# Tank 2
./run_tank2_diagnostic.sh
```

### AI Apps (Tank #1 & #2)

**One-time setup (5 minutes):**

1. **Get API Key:**
   - Visit: https://console.anthropic.com/
   - Sign up and create API key

2. **Configure `.env.diagnostic`:**
   ```bash
   # File will be created automatically, or create manually:
   echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" > .env.diagnostic
   ```

3. **Add Credits:**
   - Go to: https://console.anthropic.com/settings/plans
   - Add minimum $5 credits

4. **Run:**
   ```bash
   # Tank 1
   ./run_ai_diagnostic.sh

   # Tank 2
   ./run_ai_tank2_diagnostic.sh
   ```

**Note:** Both AI apps share the same `.env.diagnostic` file and API credits.

---

## File Structure

```
HVAC_ideas/
├── execution/
│   ├── tank1_diagnostic_app.py       # Tank 1 Basic
│   ├── ai_tank1_diagnostic.py        # Tank 1 AI
│   ├── tank2_diagnostic_app.py       # Tank 2 Basic
│   └── ai_tank2_diagnostic.py        # Tank 2 AI
├── .tmp/
│   ├── Tank1_Diagnostic_Session_*.txt
│   ├── Tank1_AI_Conversation_*.txt
│   ├── Tank1_AI_Diagnostic_Report_*.txt
│   ├── Tank2_Diagnostic_Session_*.txt
│   ├── Tank2_AI_Conversation_*.txt
│   └── Tank2_AI_Diagnostic_Report_*.txt
├── .env.diagnostic                   # API key (for AI apps)
├── run_tank1_diagnostic.sh           # Tank 1 Basic launcher
├── run_ai_diagnostic.sh              # Tank 1 AI launcher
├── run_tank2_diagnostic.sh           # Tank 2 Basic launcher
├── run_ai_tank2_diagnostic.sh        # Tank 2 AI launcher
└── ALL_DIAGNOSTIC_APPS.md            # This file
```

---

## Example: Basic App Session

```
=======================================================================
  TANK #1 AUTO-FILL DIAGNOSTIC APPLICATION
=======================================================================

[Q1.1] Which input controls Tank #1?

  1. Tank A (Input ID)
  2. Tank B (Input IE)
  3. Not Sure

Enter choice number: 1

[Q2.1] What happened when you tested in Manual mode?

  1. Tank #1 filled successfully
  2. Tank #1 did NOT fill
  3. Pump started but stopped after 1-2 seconds
  4. Unable to test

Enter choice number: 1

ℹ️  Pumps and valves work. Problem is AUTO sensing. Continue to STEP 3.

...
```

---

## Example: AI App Session

```
================================================================================
  AI-POWERED TANK #1 DIAGNOSTIC ASSISTANT
================================================================================

AI: Hello! I'm your diagnostic assistant for Tank #1 auto-fill issues.
    What's your name and what have you observed?

You: I'm Mike. Tank 1 won't fill automatically but manual works.

AI: Thanks Mike! Since manual works, your pumps and valves are functioning.
    The problem is in the automatic sensing system.

    Is Tank #1 the same as "Tank A" or "Tank B" in your facility?

You: Tank A

AI: Perfect. So we'll focus on Input ID and relay M4. Let's start by
    checking the float switch. Can you locate it and tell me if it
    moves freely?

You: yes it moves ok

AI: Good. Now let's test electrically. Do you have a multimeter?

...
```

---

## Troubleshooting

### Basic Apps Not Working

**"python3: command not found"**
- Install Python 3: `brew install python3` (Mac) or apt/yum (Linux)

**"Permission denied"**
```bash
chmod +x run_tank1_diagnostic.sh
chmod +x run_tank2_diagnostic.sh
```

### AI Apps Not Working

**"ANTHROPIC_API_KEY not found"**
- Create `.env.diagnostic` file with your API key
- Format: `ANTHROPIC_API_KEY=sk-ant-your-key`

**"Your credit balance is too low"**
- Add credits: https://console.anthropic.com/settings/plans
- Minimum $5 required

**"anthropic library not installed"**
```bash
source venv/bin/activate
pip install anthropic
```

---

## Cost Analysis

### Basic Apps
- **Per session:** $0.00
- **Annual (100 sessions):** $0.00
- **ROI:** N/A (free)

### AI Apps
- **Per session:** $0.10 - $1.50
- **Average session:** $0.40
- **Annual (100 sessions):** ~$40
- **ROI:** Pays for itself if saves 1-2 minutes labor per session

---

## Recommendation Matrix

| Scenario | Recommended App |
|----------|-----------------|
| Field work, no internet | Basic |
| Zero budget | Basic |
| Simple problem | Basic |
| Training new technicians | Basic |
| Complex problem | AI |
| Need explanations | AI |
| Building knowledge base | AI |
| Unusual situation | AI |
| Want detailed analysis | AI |
| Internet + budget available | AI |

---

## All Available Commands

**Quick reference for all 4 apps:**

```bash
# TANK #1
./run_tank1_diagnostic.sh          # Basic (FREE)
./run_ai_diagnostic.sh             # AI-Powered (requires credits)

# TANK #2
./run_tank2_diagnostic.sh          # Basic (FREE)
./run_ai_tank2_diagnostic.sh       # AI-Powered (requires credits)
```

---

## Safety Reminder

⚠️ **All apps require following LOTO procedures**
- Lock out and tag out before working
- System operates at 240V AC
- Qualified personnel only
- Verify de-energized before touching terminals

---

## Support

**Application Issues:**
- Check this guide
- Review error messages
- Verify permissions

**PLC/System Issues:**
- Refer to Program #3201 documentation
- Contact Schneider Electric
- Consult qualified technician

**API/Billing (AI apps only):**
- Visit: https://console.anthropic.com/

---

**Last Updated:** January 10, 2026
**Total Applications:** 4 (2 Basic + 2 AI)
**System:** Oil Tank Transfer Box (Program #3201)
