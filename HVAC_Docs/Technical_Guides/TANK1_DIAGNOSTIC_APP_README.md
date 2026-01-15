# Tank #1 Diagnostic Application

## Overview

This interactive command-line application guides technicians through systematic troubleshooting of Tank #1 auto-fill failures in the Oil Tank Transfer Box system (Program #3201).

## Features

- **Step-by-step guided diagnostics** - Walks through 7 diagnostic steps
- **Interactive Q&A interface** - Asks questions and waits for responses
- **Automatic report generation** - Saves all responses to a text file
- **Session tracking** - Each diagnostic session gets a unique ID
- **Smart routing** - Skips irrelevant steps based on previous answers
- **Error recovery** - Saves partial results if interrupted

## System Requirements

- Python 3.6 or higher
- Terminal/Command line access
- No additional libraries required (uses only Python standard library)

## How to Run

### Option 1: Using the launcher script (Recommended)

```bash
./run_tank1_diagnostic.sh
```

### Option 2: Direct Python execution

```bash
python3 execution/tank1_diagnostic_app.py
```

### Option 3: With virtual environment

```bash
source venv/bin/activate
python execution/tank1_diagnostic_app.py
```

## What the Application Does

### Diagnostic Flow

1. **Initial Information** - Collects technician name, date/time, problem description
2. **Step 1: Tank Direction** - Identifies which PLC input controls Tank #1 (ID or IE)
3. **Step 2: Manual Mode Test** - Quick test to isolate AUTO vs physical problems
4. **Step 3: Level Sensor Check** - Visual and electrical testing of float switch
5. **Step 4: PLC Input Signal** - Verifies sensor signal reaches PLC terminal
6. **Step 5: System Ready (M1)** - Checks master gate relay and Input IL
7. **Step 6: Safety Interlocks** - Verifies M1, M2, M3, M6 relay states
8. **Step 7: Timer & Valves** - Tests 1.5-second valve timing window
9. **Summary** - Documents root cause and corrective actions

### Question Types

The app supports different question types:

- **Text input** - Free-form text answers
- **Yes/No** - Simple Y/N questions
- **Multiple choice** - Numbered options (enter choice number)
- **Numeric input** - Measurements (voltage, time, etc.)

## Output Files

All diagnostic sessions are saved to `.tmp/` directory:

**Filename format:** `Tank1_Diagnostic_Session_YYYYMMDD_HHMMSS.txt`

**Example:** `Tank1_Diagnostic_Session_20260110_115230.txt`

### Report Contents

The generated text file includes:

- Session ID and timestamp
- System information (PLC model, program number)
- All questions and answers grouped by diagnostic step
- Timestamps for each response
- Root cause analysis
- Corrective actions taken

## Usage Example

```
=======================================================================
  TANK #1 AUTO-FILL DIAGNOSTIC APPLICATION
=======================================================================
  System: Oil Tank Transfer Box (Program #3201)
  PLC: Schneider Electric Zelio Logic SR3B261FU
  Session ID: 20260110_115230

  This application will guide you through systematic troubleshooting
  of Tank #1 auto-fill failure. All responses will be saved.

  ⚠️  WARNING: Follow all LOTO procedures. System operates at 240V AC.

Press ENTER to continue...

=======================================================================
  INITIAL INFORMATION
=======================================================================

[Q0.1] Technician name:

Your answer: John Smith

[Q0.2] Date/Time of diagnosis:

Your answer: 2026-01-10 11:52 AM

...
```

## Tips for Technicians

1. **Have equipment ready before starting:**
   - Digital multimeter
   - Laptop with Zelio Soft (if available)
   - PLC cable
   - System documentation

2. **Follow LOTO procedures** - Ensure system is safe before testing

3. **Answer accurately** - Responses are saved for documentation

4. **Skip irrelevant questions** - App will route based on your answers

5. **Interrupt if needed** - Press Ctrl+C to stop; app will offer to save partial results

## Viewing Results

After completing the diagnostic session:

1. Navigate to `.tmp/` directory
2. Open the text file with your session ID
3. Review all questions and answers
4. Share with supervisors or use for maintenance records

**View on command line:**
```bash
cat .tmp/Tank1_Diagnostic_Session_*.txt
```

**View most recent:**
```bash
ls -t .tmp/Tank1_Diagnostic_Session_*.txt | head -1 | xargs cat
```

## Troubleshooting the App

### App won't start

**Error:** `python: command not found`
- Solution: Use `python3` instead

**Error:** `Permission denied`
- Solution: `chmod +x run_tank1_diagnostic.sh`

### Cannot save results

**Error:** `.tmp/ directory not found`
- Solution: App creates this automatically, but check write permissions

### Screen formatting issues

- Try maximizing terminal window
- Use a modern terminal emulator

## Integration with PDF Guide

This application complements the static PDF guide:

- **PDF:** Reference documentation for offline use
- **App:** Interactive guided diagnostics with automatic recording

You can use both together:
1. Review PDF to understand overall diagnostic approach
2. Run app during actual troubleshooting
3. App saves all findings automatically

## Support

For issues with:
- **The diagnostic app** - Check this README
- **The Oil Tank Transfer Box system** - Refer to Program #3201 documentation
- **PLC programming** - Contact Schneider Electric support or qualified technician

## File Locations

```
HVAC_ideas/
├── execution/
│   └── tank1_diagnostic_app.py          # Main application
├── .tmp/
│   └── Tank1_Diagnostic_Session_*.txt   # Saved diagnostic reports
├── run_tank1_diagnostic.sh              # Launcher script
├── TANK1_DIAGNOSTIC_APP_README.md       # This file
└── Tank1_Auto_Fill_Diagnostic_Guide.pdf # PDF reference guide
```

## Version History

- **v1.0** (2026-01-10) - Initial release
  - 7-step diagnostic workflow
  - Text report generation
  - Multiple question types
  - Session tracking

---

**Safety Reminder:** This application is for qualified personnel only. Always follow lockout/tagout (LOTO) procedures when working on electrical systems operating at 240V AC.
