#!/usr/bin/env python3
"""
Multi-Agent Debate Script - Phase 2: Deliberation

This script simulates the debate between:
- Agent Alpha (The Investigator): Proposes immediate fixes
- Agent Beta (The Architect): Critiques based on system/app impact

The agents debate until consensus is reached on the best solution.
"""

import sys
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class ErrorPattern:
    """Represents an identified error pattern from Phase 1."""
    process: str
    subsystem: str
    category: str  # System, Apple Apps, Third-Party Apps
    error_count: int
    messages: List[str]
    severity: str  # Fault, Error, Warning


@dataclass
class ProposedFix:
    """A solution proposed by Agent Alpha."""
    fix_id: int
    title: str
    description: str
    commands: List[str]
    targets: List[str]  # Affected processes/systems
    risk_level: str  # Low, Medium, High
    estimated_impact: str


@dataclass
class Critique:
    """Agent Beta's critique of a proposed fix."""
    fix_id: int
    concerns: List[str]
    benefits: List[str]
    system_impact: str
    app_impact: str
    recommendation: str  # Approve, Modify, Reject


@dataclass
class DebateRound:
    """A single round of debate between agents."""
    round_num: int
    alpha_statement: str
    beta_response: str
    resolution: str  # Continue, Modify, Accept


class AgentAlpha:
    """The Investigator - Proposes immediate fixes based on error patterns."""

    def __init__(self):
        self.name = "Agent Alpha (The Investigator)"

    def analyze_patterns(self, errors: List[ErrorPattern]) -> List[ProposedFix]:
        """Analyze error patterns and propose fixes."""
        fixes = []

        # Group errors by category
        system_errors = [e for e in errors if e.category == "System"]
        app_errors = [e for e in errors if e.category in ["Apple Apps", "Third-Party Apps"]]

        # Generate fixes based on patterns
        fix_id = 1

        # Check for kernel/system errors
        kernel_errors = [e for e in system_errors if e.process == "kernel"]
        if kernel_errors:
            fixes.append(self._propose_kernel_fix(fix_id, kernel_errors))
            fix_id += 1

        # Check for framework/library issues
        framework_errors = [e for e in errors if "framework" in str(e.messages).lower() or "library" in str(e.messages).lower()]
        if framework_errors:
            fixes.append(self._propose_framework_fix(fix_id, framework_errors))
            fix_id += 1

        # Check for resource exhaustion
        resource_errors = [e for e in errors if any(keyword in str(e.messages).lower() for keyword in ["memory", "out of", "allocation"])]
        if resource_errors:
            fixes.append(self._propose_resource_fix(fix_id, resource_errors))
            fix_id += 1

        # Check for service/daemon issues
        service_errors = [e for e in system_errors if "launchd" in e.process or "service" in str(e.messages).lower()]
        if service_errors:
            fixes.append(self._propose_service_fix(fix_id, service_errors))
            fix_id += 1

        return fixes[:3]  # Return top 3 fixes

    def _propose_kernel_fix(self, fix_id: int, errors: List[ErrorPattern]) -> ProposedFix:
        """Propose fix for kernel-related errors."""
        return ProposedFix(
            fix_id=fix_id,
            title="Reset NVRAM and SMC",
            description="Kernel ACPI and hardware enumeration errors suggest corrupted NVRAM or SMC state. Reset both to restore default hardware configuration.",
            commands=[
                "sudo nvram -c",
                "# Then restart Mac and hold: Option + Command + P + R (NVRAM reset)",
                "# For SMC: Shut down, press Shift + Control + Option + Power for 10s"
            ],
            targets=["kernel", "ACPI", "IOKit drivers"],
            risk_level="Medium",
            estimated_impact="May reset system preferences, but resolves hardware initialization issues"
        )

    def _propose_framework_fix(self, fix_id: int, errors: List[ErrorPattern]) -> ProposedFix:
        """Propose fix for framework loading issues."""
        return ProposedFix(
            fix_id=fix_id,
            title="Repair System Frameworks and Permissions",
            description="Missing framework errors indicate corrupted system files or permission issues. Rebuild framework cache and repair permissions.",
            commands=[
                "sudo update_dyld_shared_cache -force",
                "sudo /System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user",
                "sudo diskutil repairPermissions /"
            ],
            targets=["SpringBoard", "LaunchServices", "System Frameworks"],
            risk_level="Low",
            estimated_impact="Safe operation, rebuilds framework cache without data loss"
        )

    def _propose_resource_fix(self, fix_id: int, errors: List[ErrorPattern]) -> ProposedFix:
        """Propose fix for resource exhaustion issues."""
        return ProposedFix(
            fix_id=fix_id,
            title="Clear Caches and Free Memory",
            description="Memory allocation failures suggest insufficient resources. Clear system caches, restart memory-hungry processes.",
            commands=[
                "sudo purge",
                "sudo rm -rf /Library/Caches/*",
                "sudo rm -rf ~/Library/Caches/*",
                "killall -9 Safari  # Restart affected apps"
            ],
            targets=["Safari", "WebKit", "System Memory"],
            risk_level="Low",
            estimated_impact="Temporary performance impact during cache rebuild, but resolves memory pressure"
        )

    def _propose_service_fix(self, fix_id: int, errors: List[ErrorPattern]) -> ProposedFix:
        """Propose fix for service/daemon issues."""
        return ProposedFix(
            fix_id=fix_id,
            title="Reload Launch Services",
            description="Service initialization failures indicate corrupted launch daemons. Reload launchd configuration and restart services.",
            commands=[
                "sudo launchctl list | grep com.apple | awk '{print $3}' | xargs -I {} sudo launchctl kickstart -k system/{}",
                "killall Dock",
                "killall Finder"
            ],
            targets=["launchd", "com.apple.xpc.launchd", "System Services"],
            risk_level="Medium",
            estimated_impact="Temporary UI disruption as Finder/Dock restart, but resolves service issues"
        )


class AgentBeta:
    """The Architect - Evaluates solutions for long-term stability."""

    def __init__(self):
        self.name = "Agent Beta (The Architect)"

    def critique_fix(self, fix: ProposedFix, errors: List[ErrorPattern]) -> Critique:
        """Critique a proposed fix based on system/app impact."""
        concerns = []
        benefits = []
        system_impact = ""
        app_impact = ""
        recommendation = ""

        # Analyze by fix type
        if "NVRAM" in fix.title or "SMC" in fix.title:
            concerns = [
                "Requires physical restart and manual key combinations",
                "Resets system preferences (time zone, startup disk, etc.)",
                "May not address software-level issues"
            ]
            benefits = [
                "Resolves deep hardware initialization problems",
                "No data loss or software reinstallation required",
                "Eliminates ACPI and power management errors"
            ]
            system_impact = "HIGH - Resets firmware-level configuration, requires manual intervention"
            app_impact = "LOW - Apps unaffected, but system preferences reset"
            recommendation = "MODIFY - Only use if software fixes fail, document preference backup first"

        elif "Framework" in fix.title or "Permission" in fix.title:
            concerns = [
                "Rebuilding cache may take 5-10 minutes",
                "Requires sudo privileges"
            ]
            benefits = [
                "Safe, non-destructive operation",
                "Fixes framework loading and permission issues",
                "Standard macOS maintenance procedure"
            ]
            system_impact = "LOW - Standard system maintenance, no configuration changes"
            app_impact = "LOW - May require app relaunches, but no data loss"
            recommendation = "APPROVE - Safe first-line fix for framework issues"

        elif "Cache" in fix.title or "Memory" in fix.title:
            concerns = [
                "Killing Safari loses unsaved work",
                "Cache clearing may temporarily slow performance",
                "Doesn't address root cause of memory leaks"
            ]
            benefits = [
                "Immediate relief from memory pressure",
                "Quick to execute",
                "No system-level changes"
            ]
            system_impact = "MINIMAL - Temporary performance impact during cache rebuild"
            app_impact = "MEDIUM - Active applications may need restart, potential data loss"
            recommendation = "MODIFY - Warn user to save work first, investigate memory leak source"

        elif "Launch" in fix.title or "Service" in fix.title:
            concerns = [
                "Restarting all Apple services may cause brief system instability",
                "Dock/Finder restart interrupts workflow",
                "May not fix underlying service corruption"
            ]
            benefits = [
                "Reloads damaged service configurations",
                "Quick recovery without full reboot",
                "Fixes XPC service communication issues"
            ]
            system_impact = "MEDIUM - Brief UI disruption, services restart"
            app_impact = "MEDIUM - Running apps may lose connection to system services"
            recommendation = "APPROVE - Good middle-ground fix, less disruptive than full reboot"

        return Critique(
            fix_id=fix.fix_id,
            concerns=concerns,
            benefits=benefits,
            system_impact=system_impact,
            app_impact=app_impact,
            recommendation=recommendation
        )


class DebateFacilitator:
    """Facilitates the debate between Alpha and Beta."""

    def __init__(self, alpha: AgentAlpha, beta: AgentBeta):
        self.alpha = alpha
        self.beta = beta
        self.debate_log: List[DebateRound] = []

    def conduct_debate(self, errors: List[ErrorPattern]) -> Tuple[ProposedFix, Critique, List[DebateRound]]:
        """Conduct debate until consensus is reached."""
        print(f"\n{'='*80}")
        print("PHASE 2: DELIBERATION (Agent Alpha & Agent Beta)")
        print(f"{'='*80}\n")

        # Alpha proposes fixes
        print(f"[{self.alpha.name}]")
        print("Analyzing error patterns and proposing solutions...\n")
        proposed_fixes = self.alpha.analyze_patterns(errors)

        print(f"I propose {len(proposed_fixes)} immediate fixes:\n")
        for fix in proposed_fixes:
            print(f"Fix #{fix.fix_id}: {fix.title}")
            print(f"  Description: {fix.description}")
            print(f"  Risk Level: {fix.risk_level}")
            print(f"  Targets: {', '.join(fix.targets)}")
            print()

        # Beta critiques each fix
        print(f"\n[{self.beta.name}]")
        print("Evaluating proposed solutions for system stability...\n")

        critiques = []
        for fix in proposed_fixes:
            critique = self.beta.critique_fix(fix, errors)
            critiques.append(critique)

            print(f"Fix #{fix.fix_id} Analysis:")
            print(f"  System Impact: {critique.system_impact}")
            print(f"  App Impact: {critique.app_impact}")
            print(f"  Recommendation: {critique.recommendation}")
            print(f"  Benefits: {', '.join(critique.benefits[:2])}")
            print(f"  Concerns: {', '.join(critique.concerns[:2])}")
            print()

        # Find consensus
        best_fix, best_critique = self._reach_consensus(proposed_fixes, critiques)

        # Debate rounds
        self._debate_round_1(best_fix, best_critique)
        self._debate_round_2(best_fix, best_critique)

        return best_fix, best_critique, self.debate_log

    def _reach_consensus(self, fixes: List[ProposedFix], critiques: List[Critique]) -> Tuple[ProposedFix, Critique]:
        """Determine the best fix based on recommendations."""
        # Prioritize: APPROVE > MODIFY > REJECT
        approved = [(f, c) for f, c in zip(fixes, critiques) if "APPROVE" in c.recommendation]
        modified = [(f, c) for f, c in zip(fixes, critiques) if "MODIFY" in c.recommendation]

        if approved:
            return approved[0]
        elif modified:
            return modified[0]
        else:
            return fixes[0], critiques[0]

    def _debate_round_1(self, fix: ProposedFix, critique: Critique):
        """First round of debate."""
        alpha_statement = f"Fix #{fix.fix_id} directly addresses the root cause with {fix.risk_level.lower()} risk. The commands are standard macOS maintenance procedures."
        beta_response = f"Agreed, but {critique.system_impact.split('-')[0].strip()} system impact requires user awareness. I recommend proceeding with user notification."

        self.debate_log.append(DebateRound(
            round_num=1,
            alpha_statement=alpha_statement,
            beta_response=beta_response,
            resolution="Continue"
        ))

        print(f"\n{'='*80}")
        print("DEBATE - Round 1")
        print(f"{'='*80}")
        print(f"[Alpha]: {alpha_statement}")
        print(f"[Beta]: {beta_response}\n")

    def _debate_round_2(self, fix: ProposedFix, critique: Critique):
        """Second round - reach consensus."""
        alpha_statement = f"Acknowledged. I'll include verification steps to confirm the fix resolves: {', '.join(fix.targets[:2])}."
        beta_response = f"Consensus reached. Fix #{fix.fix_id} is the optimal solution. Recommendation: {critique.recommendation}."

        self.debate_log.append(DebateRound(
            round_num=2,
            alpha_statement=alpha_statement,
            beta_response=beta_response,
            resolution="Accept"
        ))

        print(f"{'='*80}")
        print("DEBATE - Round 2 (Consensus)")
        print(f"{'='*80}")
        print(f"[Alpha]: {alpha_statement}")
        print(f"[Beta]: {beta_response}\n")


def parse_phase1_output(text: str) -> List[ErrorPattern]:
    """Parse the output from parse_macos_logs.py to extract error patterns."""
    errors = []

    # Look for "Process: X (N errors)" pattern in POTENTIAL ROOT CAUSES section
    in_root_causes = False
    current_process = None
    current_messages = []

    for line in text.split('\n'):
        if "POTENTIAL ROOT CAUSES" in line:
            in_root_causes = True
            continue

        if in_root_causes:
            if line.startswith("Process:"):
                # Save previous process if exists
                if current_process:
                    errors.append(current_process)

                # Parse new process line: "Process: kernel (3 errors)"
                parts = line.split("(")
                if len(parts) >= 2:
                    process_name = parts[0].replace("Process:", "").strip()
                    error_count = int(parts[1].split()[0])

                    # Determine category
                    system_processes = ["kernel", "launchd", "WindowServer", "com.apple.xpc.launchd", "CoreServicesUIAgent"]
                    if process_name in system_processes:
                        category = "System"
                    elif process_name in ["Safari", "Mail", "Photos"]:
                        category = "Apple Apps"
                    else:
                        category = "Third-Party Apps"

                    current_process = ErrorPattern(
                        process=process_name,
                        subsystem="Unknown",
                        category=category,
                        error_count=error_count,
                        messages=[],
                        severity="Error"
                    )
                    current_messages = []

            elif line.strip().startswith("[") and current_process:
                # Parse message line: "  [1x] Message..."
                msg = line.strip().split("] ", 1)[-1]
                current_messages.append(msg)
                current_process.messages = current_messages

    # Add last process
    if current_process:
        errors.append(current_process)

    return errors


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python agent_debate.py <phase1_output.txt>")
        print("Or pipe: python parse_macos_logs.py logs.txt | python agent_debate.py -")
        sys.exit(1)

    # Read Phase 1 output
    if sys.argv[1] == '-':
        phase1_text = sys.stdin.read()
    else:
        with open(sys.argv[1], 'r') as f:
            phase1_text = f.read()

    # Parse errors
    errors = parse_phase1_output(phase1_text)

    if not errors:
        print("No errors found in Phase 1 output. Cannot proceed with debate.")
        sys.exit(1)

    # Initialize agents
    alpha = AgentAlpha()
    beta = AgentBeta()
    facilitator = DebateFacilitator(alpha, beta)

    # Conduct debate
    best_fix, best_critique, debate_log = facilitator.conduct_debate(errors)

    # Output consensus
    print(f"\n{'='*80}")
    print("CONSENSUS REACHED")
    print(f"{'='*80}\n")
    print(f"Selected Fix: #{best_fix.fix_id} - {best_fix.title}")
    print(f"Recommendation: {best_critique.recommendation}")
    print(f"\nThis decision will be passed to Agent Gamma (The Coordinator) for execution planning.")


if __name__ == '__main__':
    main()
