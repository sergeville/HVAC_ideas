#!/usr/bin/env python3
"""
Agent Gamma (The Coordinator) - Phase 3: Master Plan Generation

This script:
- Takes output from Phase 1 (diagnostics) and Phase 2 (debate consensus)
- Generates a structured execution plan in markdown format
- Includes root cause analysis, consensus rationale, implementation steps, and verification
"""

import sys
import re
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ConsensusDecision:
    """The consensus reached by Alpha and Beta."""
    fix_id: int
    title: str
    description: str
    commands: List[str]
    risk_level: str
    targets: List[str]
    recommendation: str
    system_impact: str
    app_impact: str
    benefits: List[str]
    concerns: List[str]


@dataclass
class RootCauseAnalysis:
    """Root cause identified from Phase 1."""
    primary_issue: str
    affected_processes: List[str]
    error_count: int
    category: str
    evidence: List[str]


class AgentGamma:
    """The Coordinator - Generates final execution plan."""

    def __init__(self):
        self.name = "Agent Gamma (The Coordinator)"

    def parse_phase1_output(self, text: str) -> RootCauseAnalysis:
        """Extract root cause from Phase 1 diagnostic output."""
        lines = text.split('\n')

        # Find error distribution
        in_distribution = False
        error_categories = {}
        total_errors = 0

        for line in lines:
            if "Total Log Entries:" in line:
                continue
            if "Errors (Error + Fault):" in line:
                total_errors = int(line.split(':')[1].strip())
            if "ERROR DISTRIBUTION GRAPH" in line:
                in_distribution = True
                continue
            if in_distribution and ":" in line and "issues" in line:
                parts = line.split(":")
                if len(parts) >= 2:
                    category = parts[0].strip()
                    count = int(parts[1].split()[0])
                    error_categories[category] = count

        # Find primary root cause (first process in root causes section)
        in_root_causes = False
        primary_process = None
        primary_error_count = 0
        evidence = []

        for i, line in enumerate(lines):
            if "POTENTIAL ROOT CAUSES" in line:
                in_root_causes = True
                continue

            if in_root_causes:
                if line.startswith("Process:"):
                    if not primary_process:  # First process is primary cause
                        parts = line.split("(")
                        if len(parts) >= 2:
                            primary_process = parts[0].replace("Process:", "").strip()
                            primary_error_count = int(parts[1].split()[0])
                    else:
                        break  # Stop after first process
                elif line.strip().startswith("[") and primary_process:
                    evidence.append(line.strip().split("] ", 1)[-1][:80])

        # Determine primary issue type
        evidence_text = " ".join(evidence).lower()
        if "framework" in evidence_text or "library" in evidence_text:
            primary_issue = "Missing or corrupted system frameworks"
        elif "memory" in evidence_text or "allocation" in evidence_text:
            primary_issue = "Memory exhaustion and resource pressure"
        elif "acpi" in evidence_text or "hardware" in evidence_text:
            primary_issue = "Hardware initialization and ACPI errors"
        elif "service" in evidence_text or "launchd" in evidence_text:
            primary_issue = "System service initialization failures"
        else:
            primary_issue = "System instability and error cascades"

        category = max(error_categories, key=error_categories.get) if error_categories else "System"

        return RootCauseAnalysis(
            primary_issue=primary_issue,
            affected_processes=[primary_process] if primary_process else [],
            error_count=primary_error_count or total_errors,
            category=category,
            evidence=evidence[:3]  # Top 3 evidence points
        )

    def parse_phase2_output(self, text: str) -> ConsensusDecision:
        """Extract consensus decision from Phase 2 debate output."""
        lines = text.split('\n')

        # Parse the selected fix from "CONSENSUS REACHED" section
        in_consensus = False
        fix_id = None
        title = None
        recommendation = None

        for line in lines:
            if "CONSENSUS REACHED" in line:
                in_consensus = True
                continue

            if in_consensus:
                if "Selected Fix:" in line:
                    # Parse: "Selected Fix: #2 - Repair System Frameworks and Permissions"
                    parts = line.split(":")[-1].strip()
                    fix_id = int(parts.split("#")[1].split("-")[0].strip())
                    title = "-".join(parts.split("-")[1:]).strip()
                elif "Recommendation:" in line:
                    recommendation = line.split(":", 1)[1].strip()

        # Now find the full details of this fix from earlier in the output
        description = ""
        commands = []
        risk_level = ""
        targets = []
        system_impact = ""
        app_impact = ""
        benefits = []
        concerns = []

        current_fix_id = None
        in_fix_section = False
        in_analysis_section = False

        for i, line in enumerate(lines):
            # Find the fix proposal section
            if f"Fix #{fix_id}:" in line and "I propose" not in line:
                current_fix_id = fix_id
                in_fix_section = True
                continue

            if in_fix_section and current_fix_id == fix_id:
                if "Description:" in line:
                    description = line.split(":", 1)[1].strip()
                elif "Risk Level:" in line:
                    risk_level = line.split(":", 1)[1].strip()
                elif "Targets:" in line:
                    targets = [t.strip() for t in line.split(":", 1)[1].split(",")]
                elif line.strip() == "":
                    in_fix_section = False

            # Find the analysis section for this fix
            if f"Fix #{fix_id} Analysis:" in line:
                in_analysis_section = True
                continue

            if in_analysis_section:
                if "System Impact:" in line:
                    system_impact = line.split(":", 1)[1].strip()
                elif "App Impact:" in line:
                    app_impact = line.split(":", 1)[1].strip()
                elif "Benefits:" in line:
                    benefits = [b.strip() for b in line.split(":", 1)[1].split(",")]
                elif "Concerns:" in line:
                    concerns = [c.strip() for c in line.split(":", 1)[1].split(",")]
                elif line.strip() == "":
                    in_analysis_section = False

        return ConsensusDecision(
            fix_id=fix_id or 0,
            title=title or "Unknown Fix",
            description=description,
            commands=commands,  # Will be populated from known fixes
            risk_level=risk_level,
            targets=targets,
            recommendation=recommendation or "",
            system_impact=system_impact,
            app_impact=app_impact,
            benefits=benefits,
            concerns=concerns
        )

    def get_implementation_steps(self, decision: ConsensusDecision) -> List[str]:
        """Generate detailed implementation steps based on the fix."""
        # Map fix titles to their implementation steps
        implementations = {
            "Reset NVRAM and SMC": [
                "**Back up system preferences:**",
                "   - Document current startup disk, time zone, display settings",
                "   - Take screenshots of System Preferences if needed",
                "",
                "**Reset NVRAM:**",
                "   1. Shut down the Mac completely",
                "   2. Turn it on and immediately hold: `Option + Command + P + R`",
                "   3. Keep holding for about 20 seconds (until you hear startup sound twice)",
                "   4. Release the keys and allow Mac to boot normally",
                "",
                "**Reset SMC:**",
                "   1. Shut down the Mac",
                "   2. For laptops with non-removable battery:",
                "      - Hold `Shift + Control + Option + Power` for 10 seconds",
                "      - Release all keys, then press Power to start",
                "   3. For desktops:",
                "      - Unplug power cord, wait 15 seconds, plug back in",
                "      - Wait 5 seconds, then press Power button",
                "",
                "**Restore preferences:**",
                "   - Reset startup disk in System Preferences > Startup Disk",
                "   - Reconfigure time zone, display settings, etc.",
            ],

            "Repair System Frameworks and Permissions": [
                "**Prepare the system:**",
                "   - Ensure you have admin privileges",
                "   - Close all running applications",
                "   - Have at least 5-10 minutes available (process cannot be interrupted)",
                "",
                "**Step 1: Rebuild dyld shared cache**",
                "```bash",
                "sudo update_dyld_shared_cache -force",
                "```",
                "   - This rebuilds the system framework cache",
                "   - Takes 3-5 minutes depending on Mac speed",
                "   - Do NOT interrupt this process",
                "",
                "**Step 2: Reset Launch Services database**",
                "```bash",
                "sudo /System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user",
                "```",
                "   - Rebuilds framework registration",
                "   - Fixes application launch issues",
                "",
                "**Step 3: Repair disk permissions (if needed)**",
                "```bash",
                "sudo diskutil repairPermissions /",
                "```",
                "   - Note: On macOS 10.11+, this may not be necessary",
                "   - System auto-repairs permissions on updates",
                "",
                "**Step 4: Restart the system**",
                "```bash",
                "sudo shutdown -r now",
                "```",
            ],

            "Clear Caches and Free Memory": [
                "**Important: Save all work first!**",
                "   - This process will close applications and may cause data loss",
                "   - Save documents in Safari, TextEdit, and other apps",
                "",
                "**Step 1: Purge system memory**",
                "```bash",
                "sudo purge",
                "```",
                "   - Forces system to clear inactive memory",
                "   - Takes 10-30 seconds",
                "",
                "**Step 2: Clear system caches**",
                "```bash",
                "# Clear system-level caches (requires sudo)",
                "sudo rm -rf /Library/Caches/*",
                "",
                "# Clear user-level caches",
                "rm -rf ~/Library/Caches/*",
                "```",
                "   - Removes temporary cache files",
                "   - Apps will rebuild caches on next launch",
                "",
                "**Step 3: Restart memory-intensive applications**",
                "```bash",
                "# Graceful quit Safari",
                "osascript -e 'quit app \"Safari\"'",
                "",
                "# Or force quit if not responding",
                "killall -9 Safari",
                "```",
                "",
                "**Step 4: Monitor memory usage**",
                "```bash",
                "# Check current memory pressure",
                "vm_stat",
                "",
                "# Or use Activity Monitor",
                "open -a 'Activity Monitor'",
                "```",
            ],

            "Reload Launch Services": [
                "**Important: This will restart Dock and Finder**",
                "   - Save all work in open applications",
                "   - This process takes 30-60 seconds",
                "",
                "**Step 1: Reload system launch services**",
                "```bash",
                "# List and kickstart all Apple services",
                "sudo launchctl list | grep com.apple | awk '{print $3}' | xargs -I {} sudo launchctl kickstart -k system/{}",
                "```",
                "   - Restarts all com.apple.* services",
                "   - May take 30-45 seconds",
                "",
                "**Step 2: Restart Dock**",
                "```bash",
                "killall Dock",
                "```",
                "   - Dock will automatically restart",
                "   - Takes 2-3 seconds",
                "",
                "**Step 3: Restart Finder**",
                "```bash",
                "killall Finder",
                "```",
                "   - Finder will automatically restart",
                "   - Desktop will briefly flash",
                "",
                "**Step 4: Verify service status**",
                "```bash",
                "# Check if services are running",
                "sudo launchctl list | grep com.apple | head -10",
                "```",
            ]
        }

        # Find matching implementation
        for key in implementations:
            if key in decision.title:
                return implementations[key]

        # Default generic steps
        return [
            "1. Review the fix description and commands",
            "2. Execute commands in order",
            "3. Monitor for errors during execution",
            "4. Restart system if required",
            "5. Verify resolution"
        ]

    def get_verification_steps(self, decision: ConsensusDecision, root_cause: RootCauseAnalysis) -> List[str]:
        """Generate verification steps to confirm the fix worked."""
        steps = [
            "**Immediate Verification:**",
            "",
            "1. **Check for new errors in logs:**",
            "   ```bash",
            "   # Check last 5 minutes for errors",
            "   log show --last 5m --level error",
            "   ```",
            "   Expected: No new errors related to the original issue",
            "",
            "2. **Verify affected processes are stable:**",
        ]

        # Add process-specific checks
        for process in decision.targets[:3]:
            if "kernel" in process.lower():
                steps.append(f"   - Check kernel status: `sysctl kern.osversion`")
            elif "safari" in process.lower():
                steps.append(f"   - Launch Safari and verify it starts without errors")
            elif "launchd" in process.lower() or "service" in process.lower():
                steps.append(f"   - Verify services: `sudo launchctl list | grep com.apple`")
            elif "framework" in process.lower():
                steps.append(f"   - Test framework loading: Launch System Preferences")
            else:
                steps.append(f"   - Monitor {process} in Activity Monitor")

        steps.extend([
            "",
            "3. **Run diagnostic again:**",
            "   ```bash",
            "   # Capture logs for 1 hour and analyze",
            "   log show --last 1h --level error > post_fix_logs.txt",
            "   python3 execution/parse_macos_logs.py post_fix_logs.txt",
            "   ```",
            "   Expected: Significant reduction in error count",
            "",
            "**Long-term Monitoring (24-48 hours):**",
            "",
            "4. **Monitor system stability:**",
            "   - Watch for crash reports in Console.app",
            "   - Check `/Library/Logs/DiagnosticReports/` for new crashes",
            "   - Verify applications launch and run normally",
            "",
            "5. **Performance check:**",
            "   - Open Activity Monitor and check CPU/Memory usage",
            "   - Verify no processes are stuck or consuming excessive resources",
            "",
            "6. **If errors persist:**",
            "   - Capture new logs and run through the multi-agent system again",
            "   - The issue may require escalation to Apple Support",
            "   - Consider the next-best fix from Phase 2 debate",
        ])

        return steps

    def generate_master_plan(self, phase1_text: str, phase2_text: str) -> str:
        """Generate the complete master plan markdown document."""
        # Parse inputs
        root_cause = self.parse_phase1_output(phase1_text)
        decision = self.parse_phase2_output(phase2_text)

        # Generate plan sections
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        plan = []
        plan.append("# SYSTEM RESOLUTION MASTER PLAN")
        plan.append(f"*Generated by Multi-Agent Log Resolution System*")
        plan.append(f"*Timestamp: {timestamp}*")
        plan.append("")
        plan.append("---")
        plan.append("")

        # Section 1: Root Cause Analysis
        plan.append("## 1. ROOT CAUSE ANALYSIS")
        plan.append("")
        plan.append(f"**Primary Issue:** {root_cause.primary_issue}")
        plan.append("")
        plan.append(f"**Category:** {root_cause.category}")
        plan.append("")
        plan.append(f"**Affected Processes:**")
        for proc in root_cause.affected_processes[:5]:
            plan.append(f"- {proc}")
        plan.append("")
        plan.append(f"**Error Count:** {root_cause.error_count} errors detected")
        plan.append("")
        plan.append("**Evidence:**")
        for i, evidence in enumerate(root_cause.evidence, 1):
            plan.append(f"{i}. {evidence}")
        plan.append("")
        plan.append("---")
        plan.append("")

        # Section 2: Consensus Decision
        plan.append("## 2. CONSENSUS DECISION")
        plan.append("")
        plan.append(f"**Selected Fix:** #{decision.fix_id} - {decision.title}")
        plan.append("")
        plan.append(f"**Recommendation:** {decision.recommendation}")
        plan.append("")
        plan.append(f"**Risk Level:** {decision.risk_level}")
        plan.append("")
        plan.append("**Why This Fix Was Chosen:**")
        plan.append("")
        plan.append(f"*{decision.description}*")
        plan.append("")
        plan.append("**Benefits:**")
        for benefit in decision.benefits:
            plan.append(f"- {benefit}")
        plan.append("")
        plan.append("**Considerations:**")
        for concern in decision.concerns:
            plan.append(f"- {concern}")
        plan.append("")
        plan.append("**Impact Assessment:**")
        plan.append(f"- System Impact: {decision.system_impact}")
        plan.append(f"- Application Impact: {decision.app_impact}")
        plan.append("")
        plan.append("---")
        plan.append("")

        # Section 3: Implementation Steps
        plan.append("## 3. IMPLEMENTATION STEPS")
        plan.append("")
        implementation_steps = self.get_implementation_steps(decision)
        plan.extend(implementation_steps)
        plan.append("")
        plan.append("---")
        plan.append("")

        # Section 4: Verification Steps
        plan.append("## 4. VERIFICATION STEPS")
        plan.append("")
        verification_steps = self.get_verification_steps(decision, root_cause)
        plan.extend(verification_steps)
        plan.append("")
        plan.append("---")
        plan.append("")

        # Footer
        plan.append("## NOTES")
        plan.append("")
        plan.append("- This plan was generated through multi-agent consensus")
        plan.append("- Agent Alpha (Investigator) proposed the fix based on diagnostic data")
        plan.append("- Agent Beta (Architect) evaluated system/app impact")
        plan.append("- Agent Gamma (Coordinator) structured this execution plan")
        plan.append("")
        plan.append("**Before proceeding:**")
        plan.append("1. Back up important data")
        plan.append("2. Ensure you have admin privileges")
        plan.append("3. Set aside adequate time for implementation")
        plan.append("4. Document any deviations from this plan")
        plan.append("")
        plan.append("**If this fix does not resolve the issue:**")
        plan.append("Run the diagnostic again and the system will propose alternative solutions.")
        plan.append("")

        return "\n".join(plan)


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python agent_coordinator.py <phase1_output.txt> <phase2_output.txt>")
        print("Or pipe both: python parse_macos_logs.py logs.txt > p1.txt && python agent_debate.py p1.txt > p2.txt && python agent_coordinator.py p1.txt p2.txt")
        sys.exit(1)

    # Read Phase 1 and Phase 2 outputs
    with open(sys.argv[1], 'r') as f:
        phase1_text = f.read()

    with open(sys.argv[2], 'r') as f:
        phase2_text = f.read()

    # Initialize coordinator
    gamma = AgentGamma()

    # Generate master plan
    print(gamma.generate_master_plan(phase1_text, phase2_text))


if __name__ == '__main__':
    main()
