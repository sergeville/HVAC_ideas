# Directive: Resolve macOS System Logs

## Goal
Analyze macOS system logs to identify errors, determine root causes, and generate actionable resolution plans through multi-agent consensus.

## Inputs
- macOS system logs (captured via `log show` or `log stream`)
- Time range (typically last 1-24 hours)
- Error level filter (Error, Fault, Warning)

## Tools/Scripts to Use

### Primary Tool (Recommended)
- **Script:** `execution/resolve_system_issues.sh`
- **Purpose:** All-in-one wrapper that orchestrates the complete 3-phase analysis

### Individual Phase Tools
If running phases separately:
1. **Phase 1:** `execution/parse_macos_logs.py` - Diagnostic analysis
2. **Phase 2:** `execution/agent_debate.py` - Agent debate and consensus
3. **Phase 3:** `execution/agent_coordinator.py` - Master plan generation

## Outputs
- **Primary:** Master plan markdown document (`.tmp/master_plan_<timestamp>.md`)
- **Intermediate:** Phase 1 diagnostic report, Phase 2 debate transcript
- **Format:** Structured markdown with:
  - Root cause analysis
  - Consensus decision rationale
  - Step-by-step implementation instructions
  - Verification procedures

## Process Flow

### 1. Capture Logs
```bash
# Option A: Last hour of errors
log show --last 1h --level error > logs.txt

# Option B: Last 24 hours
log show --last 24h --level error > logs.txt

# Option C: Live stream (Ctrl+C to stop)
log stream --level error
```

### 2. Run Analysis
```bash
# Quick method (recommended)
./execution/resolve_system_issues.sh logs.txt

# Or for live capture
./execution/resolve_system_issues.sh --live
```

### 3. Review Master Plan
The system generates a comprehensive plan that includes:
- **What's wrong:** Root cause identification
- **What to do:** Specific fix with commands
- **Why this fix:** Consensus reasoning from agent debate
- **How to verify:** Post-fix validation steps

### 4. Execute Fix
Follow the implementation steps in the master plan exactly as written. The system provides:
- Preparation checklist
- Step-by-step commands
- Timing expectations
- Risk warnings

### 5. Verify Resolution
Run the verification steps from the master plan:
```bash
# Check for new errors
log show --last 5m --level error

# Re-run diagnostic
log show --last 1h --level error > post_fix_logs.txt
python3 execution/parse_macos_logs.py post_fix_logs.txt
```

Compare error counts before/after. Expect significant reduction (>70%).

## Edge Cases & Constraints

### No Errors Found
If log analysis finds no errors:
- System reports "No errors or warnings found"
- No action needed
- Consider expanding time range if issues are intermittent

### Multiple Critical Issues
If >10 errors from different sources:
- System prioritizes by frequency and severity
- Focus on the top 3-5 issues first
- Re-run analysis after applying initial fixes

### Unknown Process/Subsystem
If logs contain unfamiliar processes:
- System categorizes as "Third-Party Apps"
- Proposed fixes focus on standard system maintenance
- May require app-specific troubleshooting

### Fix Doesn't Resolve Issue
If errors persist after applying fix:
1. Capture new logs (post-fix)
2. Re-run the complete analysis pipeline
3. System will propose alternative solutions from Phase 2 debate
4. Consider escalation to Apple Support if all fixes fail

### Permission Requirements
Most fixes require `sudo` access:
- Ensure admin privileges before starting
- System warns about permission requirements in master plan
- Never run commands you don't understand

## Success Criteria
- Error count reduced by >70% after fix application
- Affected processes stable for 24-48 hours
- No new crashes or hangs
- System performance returns to normal

## Timing Expectations
- **Log capture:** 10-60 seconds
- **Phase 1 analysis:** 1-2 seconds
- **Phase 2 debate:** 2-3 seconds
- **Phase 3 plan:** 1 second
- **Total analysis time:** <10 seconds
- **Fix implementation:** 5-30 minutes (varies by fix type)

## Known Limitations
- System focuses on macOS unified logging format only
- Cannot analyze binary crash dumps (use Console.app for those)
- Proposed fixes are standard macOS maintenance procedures
- Deep hardware issues may require professional service
- Does not automatically execute fixes (requires manual approval)

## Updates & Improvements
When you discover:
- New error patterns → Add to Phase 1 parser
- Better fix procedures → Update Phase 2 proposals
- Verification gaps → Enhance Phase 3 templates

The 3-layer architecture allows updating execution scripts without changing the directive.

## Related Directives
- (Future) `analyze_crash_reports.md` - For binary crash dumps
- (Future) `monitor_system_health.md` - Proactive monitoring
- (Future) `performance_optimization.md` - Speed/resource issues
