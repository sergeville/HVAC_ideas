# AI-Powered Tank Diagnostic Applications

Complete guide for troubleshooting Tank #1 and Tank #2 auto-fill failures using AI-powered diagnostic assistants.

## Quick Reference

| Tank | Command | Output Files |
|------|---------|--------------|
| **Tank #1** | `./run_ai_diagnostic.sh` | `Tank1_AI_Conversation_*.txt`<br>`Tank1_AI_Diagnostic_Report_*.txt` |
| **Tank #2** | `./run_ai_tank2_diagnostic.sh` | `Tank2_AI_Conversation_*.txt`<br>`Tank2_AI_Diagnostic_Report_*.txt` |

## System Information

**Oil Tank Transfer Box System**
- Program: #3201
- PLC: Schneider Electric Zelio Logic SR3B261FU
- Expansion: SR3XT141FU (XT2)
- Voltage: 100-240V AC
- Cycle Time: 20ms

## Tank Assignments

### Tank #1
- **Typical Assignment:** Tank A
- **PLC Input:** ID
- **Relay:** M4
- **Solenoid:** Q6 (typical)
- **Pump:** Q1 (typical)
- **Timer:** T9 (1.5 seconds)

### Tank #2
- **Typical Assignment:** Tank B
- **PLC Input:** IE
- **Relay:** M5
- **Solenoid:** Q7 (typical)
- **Pump:** Q2 (typical)
- **Timer:** TA (1.5 seconds)

**Note:** Tank assignments can vary by facility. The AI will help verify which is which.

## Setup (One-Time)

### 1. Get Anthropic API Key

1. Visit: https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create new API key
5. Copy the key (starts with `sk-ant-`)

### 2. Configure API Key

The `.env.diagnostic` file is shared by both Tank #1 and Tank #2 apps.

**Edit existing file:**
```bash
nano .env.diagnostic
```

**Or create new:**
```bash
cat > .env.diagnostic << 'EOF'
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
EOF
```

**Important:** Replace `sk-ant-your-actual-key-here` with your real API key.

### 3. Add Credits

Go to: https://console.anthropic.com/settings/plans
- Add minimum $5 credits
- Or upgrade to paid plan

## Using Tank #1 Diagnostic App

### Start Tank #1 Session

```bash
./run_ai_diagnostic.sh
```

### Example Session

```
AI: Hello! I'm your diagnostic assistant for Tank #1 auto-fill issues.
    Before we start, what's your name and what have you observed so far?

You: Hi, I'm Mike. Tank 1 won't fill on its own but manual works.

AI: Thanks Mike. Since manual works, the pumps and valves are functioning.
    The problem is likely in the automatic sensing system.

    First, is Tank #1 the same as "Tank A" or "Tank B" in your system?

You: Tank A

AI: Perfect. So we'll focus on Input ID and relay M4.
    Let's start by checking the float switch sensor...
```

### Commands During Session

- Type normally to answer questions
- `clarify` - Ask AI to explain or rephrase
- `skip` - Skip a question you can't answer
- `quit` - End session and save

## Using Tank #2 Diagnostic App

### Start Tank #2 Session

```bash
./run_ai_tank2_diagnostic.sh
```

### Example Session

```
AI: Hello! I'm your diagnostic assistant for Tank #2 auto-fill issues.
    What's your name and what's happening with Tank #2?

You: I'm Sarah. Tank 2 stopped filling automatically yesterday.

AI: Thanks Sarah. Let me start by asking: does Tank #2 work in manual mode?

You: Yes, manual is fine

AI: Good! That tells me the physical components (pumps, valves) are working.
    Is Tank #2 the same as "Tank A" or "Tank B" in your documentation?

You: Tank B

AI: Excellent. So Tank #2 = Tank B, which uses Input IE and relay M5.
    Let's check the level sensor first...
```

## Output Files

All diagnostic sessions save to `.tmp/` directory.

### For Each Tank

**Conversation Log** (Full transcript)
```
.tmp/Tank1_AI_Conversation_20260110_143022.txt
.tmp/Tank2_AI_Conversation_20260110_145530.txt
```

**Diagnostic Report** (Structured analysis)
```
.tmp/Tank1_AI_Diagnostic_Report_20260110_143022.txt
.tmp/Tank2_AI_Diagnostic_Report_20260110_145530.txt
```

**JSON Data** (Machine-readable)
```
.tmp/Tank1_AI_Conversation_20260110_143022.json
.tmp/Tank2_AI_Conversation_20260110_145530.json
```

### Sample Report Structure

```
================================================================================
AI-POWERED DIAGNOSTIC REPORT - TANK #2 AUTO-FILL FAILURE
================================================================================

1. TECHNICIAN INFORMATION
   - Name: Sarah Johnson
   - Date: January 10, 2026

2. PROBLEM DESCRIPTION
   - Tank #2 fails to fill automatically
   - Manual mode works correctly

3. TESTS PERFORMED
   - Manual mode test: PASSED
   - Input IE voltage: 0.3V (FAILED - should be 12-24V)
   - Float switch continuity: OPEN (no contact closure)

4. KEY FINDINGS
   - Tank #2 = Tank B (Input IE, Relay M5)
   - Float switch mechanically stuck
   - No signal to Input IE

5. ROOT CAUSE ANALYSIS
   Float switch for Tank #2 is mechanically binding due to debris
   accumulation. Switch cannot close contacts to trigger "low level" signal.

6. RECOMMENDATIONS
   IMMEDIATE:
   - Clean float switch assembly
   - Remove debris from tank
   - Test full range of motion
   - Verify Input IE receives 24V when tank is low

   PREVENTIVE:
   - Quarterly float switch inspections
   - Install debris filter

7. SYSTEM STATUS
   NOT WORKING - Awaiting sensor cleaning/replacement
```

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
- Check `.env.diagnostic` exists
- Verify format: `ANTHROPIC_API_KEY=sk-ant-...`
- No quotes needed

### "Your credit balance is too low"
- Add credits: https://console.anthropic.com/settings/plans
- Minimum $5 required

### "anthropic library not installed"
```bash
source venv/bin/activate
pip install anthropic
```

### Wrong tank diagnosis?
- AI will ask which tank = A or B
- Check your facility documentation
- Verify PLC terminal labeling

## Cost Information

**Per Session:**
- Short diagnostic (15 min): ~$0.10 - $0.30
- Average diagnostic (30 min): ~$0.30 - $0.80
- Long diagnostic (60 min): ~$0.80 - $1.50

**$5 Credits = 5-50 diagnostic sessions**

## Diagnostic Approach

Both apps follow the same systematic approach:

### Phase 1: Initial Assessment
1. Identify tank assignment (A or B)
2. Test manual mode
3. Determine if problem is AUTO sensing vs physical

### Phase 2: Sensor Verification
1. Visual inspection of float switch
2. Mechanical operation test
3. Electrical continuity test
4. Terminal voltage measurement

### Phase 3: PLC Logic Check
1. Verify Input IL (System Ready)
2. Check directional input (ID or IE)
3. Monitor relays (M1, M2, M3, M4/M5, M6)
4. Verify no safety interlocks active

### Phase 4: Timing & Sequencing
1. Test solenoid valve operation
2. Measure valve actuation time
3. Check 1.5-second timer window
4. Verify pump start sequence

### Phase 5: Root Cause & Recommendations
1. AI analyzes all findings
2. Identifies root cause
3. Provides specific corrective actions
4. Suggests preventive maintenance

## Key Differences: Tank #1 vs Tank #2

| Aspect | Tank #1 | Tank #2 |
|--------|---------|---------|
| **Typical Assignment** | Tank A | Tank B |
| **Input** | ID | IE |
| **Relay** | M4 | M5 |
| **Timer** | T9 | TA |
| **Common Solenoid** | Q6 | Q7 |
| **Common Pump** | Q1 | Q2 |

**Both tanks share:**
- System Ready: Input IL, Relay M1
- Safety Interlock: Relay M3
- Stop Command: Relay M6
- Transfer Demand: Relay M2

## Tips for Best Results

### Preparation
- ✅ Have multimeter ready
- ✅ Access to PLC terminals
- ✅ Zelio Soft software (optional but helpful)
- ✅ LOTO procedures completed
- ✅ System documentation nearby

### During Diagnosis
- ✅ Answer naturally
- ✅ Provide specific measurements
- ✅ Ask for clarification if confused
- ✅ Take notes as you go
- ✅ Safety first - follow LOTO

### After Diagnosis
- ✅ Review AI report
- ✅ Implement recommendations
- ✅ Test system after repair
- ✅ Save reports for records

## Common Issues & Solutions

### Both Tanks Not Filling

**Check:**
1. Input IL (System Ready)
2. Relay M1 status
3. E-Stop or safety devices
4. Power supply to PLC

**This affects ALL operations, not just one tank.**

### One Tank Works, Other Doesn't

**Tank #1 works, Tank #2 fails:**
- Check Input IE
- Check Relay M5
- Check Tank #2 float switch

**Tank #2 works, Tank #1 fails:**
- Check Input ID
- Check Relay M4
- Check Tank #1 float switch

### Manual Works, Auto Fails (Either Tank)

**Most likely (70% of cases):**
- Float switch sensor failed
- Input wiring broken
- 3ms filter rejecting signal

**Less likely:**
- Wrong tank assignment
- Relay not latching
- Timer configuration

### Pump Starts Then Stops (Either Tank)

**Timer timeout fault:**
- Solenoid valve too slow (>1.5s)
- Valve mechanically binding
- Insufficient valve voltage
- Timer setting too short

## Safety Reminders

⚠️ **CRITICAL SAFETY WARNINGS:**

1. **LOTO Required** - Lock out and tag out before any work
2. **High Voltage** - System operates at 240V AC
3. **Qualified Personnel Only** - Electrical work requires certification
4. **No Live Work** - De-energize before touching terminals
5. **Verify De-energized** - Test with multimeter before proceeding

## File Locations

```
HVAC_ideas/
├── execution/
│   ├── ai_tank1_diagnostic.py       # Tank 1 app
│   └── ai_tank2_diagnostic.py       # Tank 2 app
├── .tmp/
│   ├── Tank1_AI_Conversation_*.txt
│   ├── Tank1_AI_Diagnostic_Report_*.txt
│   ├── Tank2_AI_Conversation_*.txt
│   └── Tank2_AI_Diagnostic_Report_*.txt
├── .env.diagnostic                  # API key (shared by both)
├── run_ai_diagnostic.sh             # Tank 1 launcher
├── run_ai_tank2_diagnostic.sh       # Tank 2 launcher
└── TANK_DIAGNOSTICS_GUIDE.md        # This file
```

## Quick Start Guide

### Tank #1 Issue

```bash
# 1. Ensure API key is configured
cat .env.diagnostic

# 2. Run Tank 1 diagnostic
./run_ai_diagnostic.sh

# 3. Answer AI questions naturally
# 4. Review report in .tmp/ folder
```

### Tank #2 Issue

```bash
# 1. Ensure API key is configured
cat .env.diagnostic

# 2. Run Tank 2 diagnostic
./run_ai_tank2_diagnostic.sh

# 3. Answer AI questions naturally
# 4. Review report in .tmp/ folder
```

### Both Tanks Issue

```bash
# Run diagnostics separately
./run_ai_diagnostic.sh       # Tank 1 first
./run_ai_tank2_diagnostic.sh # Tank 2 second

# Compare reports to find common cause
# (likely Input IL or Relay M1 if both fail)
```

## Support

**For Application Issues:**
- Check this guide
- Verify API key and credits
- Review error messages

**For PLC/System Issues:**
- Refer to Program #3201 documentation
- Contact Schneider Electric support
- Consult qualified PLC technician

**For API/Billing:**
- Visit: https://console.anthropic.com/

---

**Last Updated:** January 10, 2026
**Version:** 1.0
