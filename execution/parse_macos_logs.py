#!/usr/bin/env python3
"""
Parse and analyze macOS system logs for the multi-agent resolution framework.

This script implements Layer 3 (Execution) for log analysis:
- Parses macOS unified log format
- Categorizes by severity (Fault, Error, Warning, Default/Info)
- Groups by process, subsystem, and category
- Identifies error chains and dependencies
- Outputs structured data for Agent Alpha (The Investigator)
"""

import re
import sys
from collections import defaultdict, Counter
from datetime import datetime
from typing import Dict, List, Tuple


class LogEntry:
    """Represents a single log entry from macOS unified logging."""

    def __init__(self, raw_line: str):
        self.raw = raw_line
        self.timestamp = None
        self.thread_id = None
        self.level = "Default"
        self.process_id = None
        self.process_name = None
        self.subsystem = None
        self.category = None
        self.message = None
        self._parse()

    def _parse(self):
        """Parse macOS log format: TIMESTAMP THREAD LEVEL FLAGS PID SEQ PROCESS: (SUBSYSTEM) [CATEGORY] MESSAGE"""
        # Example: 2026-01-08 11:45:23.123456-0500 0x1a2b3c Error 0x0 1234 0 kernel: (AppleACPIPlatform) Message
        pattern = r'^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d+[+-]\d{4})\s+(\w+)\s+(Default|Info|Debug|Error|Fault|Warning)\s+\S+\s+(\d+)\s+\d+\s+([^:]+):\s+(?:\(([^)]+)\))?\s*(?:\[([^\]]+)\])?\s*(.*)$'

        match = re.match(pattern, self.raw.strip())
        if match:
            self.timestamp = match.group(1)
            self.thread_id = match.group(2)
            self.level = match.group(3)
            self.process_id = match.group(4)
            self.process_name = match.group(5).strip()
            self.subsystem = match.group(6) or "Unknown"
            self.category = match.group(7) or "General"
            self.message = match.group(8).strip()

    def is_error(self) -> bool:
        """Check if this entry represents an error condition."""
        return self.level in ['Error', 'Fault']

    def is_warning(self) -> bool:
        """Check if this entry is a warning."""
        return self.level == 'Warning'

    def category_type(self) -> str:
        """Categorize the log source into System, User, or Apps."""
        system_processes = ['kernel', 'launchd', 'WindowServer', 'com.apple.xpc.launchd',
                          'systemd', 'CoreServicesUIAgent', 'loginwindow']

        if self.process_name in system_processes or self.process_name.startswith('com.apple'):
            return "System"
        elif self.process_name in ['Safari', 'Mail', 'Photos', 'Music', 'Notes']:
            return "Apple Apps"
        else:
            return "Third-Party Apps"


class LogAnalyzer:
    """Analyzes parsed logs and generates reports for the multi-agent system."""

    def __init__(self):
        self.entries: List[LogEntry] = []
        self.errors: List[LogEntry] = []
        self.warnings: List[LogEntry] = []

    def add_log_line(self, line: str):
        """Parse and add a log line."""
        entry = LogEntry(line)
        if entry.message:  # Valid parse
            self.entries.append(entry)
            if entry.is_error():
                self.errors.append(entry)
            elif entry.is_warning():
                self.warnings.append(entry)

    def generate_distribution_graph(self) -> str:
        """Generate a text-based distribution of errors by category and severity."""
        if not self.errors and not self.warnings:
            return "No errors or warnings found in logs."

        report = []
        report.append("\n" + "="*80)
        report.append("ERROR DISTRIBUTION GRAPH")
        report.append("="*80 + "\n")

        # Group by category type
        category_counts = defaultdict(lambda: {'Error': 0, 'Fault': 0, 'Warning': 0})

        for entry in self.errors + self.warnings:
            cat_type = entry.category_type()
            category_counts[cat_type][entry.level] += 1

        # Display distribution
        for cat_type in ['System', 'Apple Apps', 'Third-Party Apps']:
            if cat_type in category_counts:
                counts = category_counts[cat_type]
                total = sum(counts.values())
                report.append(f"{cat_type}: {total} issues")
                for level in ['Fault', 'Error', 'Warning']:
                    if counts[level] > 0:
                        bar = '█' * counts[level]
                        report.append(f"  {level:10} [{counts[level]:2}] {bar}")
                report.append("")

        return "\n".join(report)

    def map_error_flow(self) -> str:
        """Map the flow of errors to identify causality chains."""
        if not self.errors:
            return "No errors to map."

        report = []
        report.append("\n" + "="*80)
        report.append("ERROR FLOW ANALYSIS (Chronological)")
        report.append("="*80 + "\n")

        for i, entry in enumerate(self.errors, 1):
            arrow = "→" if i < len(self.errors) else "✗"
            report.append(f"{arrow} [{entry.level}] {entry.category_type()} | {entry.process_name}")
            report.append(f"  Time: {entry.timestamp}")
            report.append(f"  Subsystem: {entry.subsystem}")
            report.append(f"  Message: {entry.message}")
            report.append("")

        return "\n".join(report)

    def identify_root_causes(self) -> str:
        """Identify potential root causes based on error patterns."""
        if not self.errors:
            return "No errors to analyze."

        report = []
        report.append("\n" + "="*80)
        report.append("POTENTIAL ROOT CAUSES")
        report.append("="*80 + "\n")

        # Group by process
        process_errors = defaultdict(list)
        for entry in self.errors:
            process_errors[entry.process_name].append(entry)

        # Find processes with multiple errors (likely culprits)
        sorted_processes = sorted(process_errors.items(), key=lambda x: len(x[1]), reverse=True)

        for process, errors in sorted_processes[:5]:  # Top 5
            report.append(f"Process: {process} ({len(errors)} errors)")
            # Group by message pattern
            messages = Counter([e.message for e in errors])
            for msg, count in messages.most_common(3):
                report.append(f"  [{count}x] {msg[:80]}...")
            report.append("")

        return "\n".join(report)

    def generate_full_report(self) -> str:
        """Generate complete diagnostic report for Agent Alpha."""
        report = []
        report.append("="*80)
        report.append("MULTI-AGENT LOG ANALYSIS REPORT")
        report.append("Phase 1: DIAGNOSTIC (Agent Alpha - The Investigator)")
        report.append("="*80)
        report.append(f"\nTotal Log Entries: {len(self.entries)}")
        report.append(f"Errors (Error + Fault): {len(self.errors)}")
        report.append(f"Warnings: {len(self.warnings)}")
        report.append(f"Info/Debug: {len(self.entries) - len(self.errors) - len(self.warnings)}")

        report.append(self.generate_distribution_graph())
        report.append(self.map_error_flow())
        report.append(self.identify_root_causes())

        return "\n".join(report)


def main():
    """Main entry point for log analysis."""
    if len(sys.argv) < 2:
        print("Usage: python parse_macos_logs.py <log_file>")
        print("Or pipe logs: log show --last 1h | python parse_macos_logs.py -")
        sys.exit(1)

    analyzer = LogAnalyzer()

    # Read from file or stdin
    if sys.argv[1] == '-':
        for line in sys.stdin:
            analyzer.add_log_line(line)
    else:
        with open(sys.argv[1], 'r') as f:
            for line in f:
                analyzer.add_log_line(line)

    # Generate and print report
    print(analyzer.generate_full_report())


if __name__ == '__main__':
    main()
