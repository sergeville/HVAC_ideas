#!/usr/bin/env python3
"""
AI-Powered Tank #2 Diagnostic Assistant
Uses Claude API to provide intelligent, adaptive troubleshooting guidance.
"""

import os
import sys
import json
from datetime import datetime
from typing import List, Dict
from pathlib import Path

try:
    from anthropic import Anthropic
except ImportError:
    print("Error: anthropic library not installed.")
    print("Install with: pip install anthropic")
    sys.exit(1)

class AITank2Diagnostic:
    def __init__(self):
        self.output_dir = "/Users/sergevilleneuve/Documents/MyExperiments/HVAC_ideas/.tmp"
        self.session_time = datetime.now()
        self.session_id = self.session_time.strftime("%Y%m%d_%H%M%S")
        self.conversation_history: List[Dict] = []

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

        # Load API key from .env.diagnostic file
        api_key = self._load_api_key()
        if not api_key:
            print("Error: ANTHROPIC_API_KEY not found.")
            print("\nPlease create a .env.diagnostic file with:")
            print("  ANTHROPIC_API_KEY=your-api-key-here")
            print("\nGet your API key from: https://console.anthropic.com/")
            sys.exit(1)

        self.client = Anthropic(api_key=api_key)
        # Use Claude 3 Haiku - fast, affordable, widely available
        self.model = "claude-3-haiku-20240307"

        # System prompt that defines the AI's role
        self.system_prompt = self._create_system_prompt()

    def _load_api_key(self) -> str:
        """Load API key from .env.diagnostic file."""
        # Look for .env.diagnostic in project root
        project_root = Path(__file__).parent.parent
        env_file = project_root / ".env.diagnostic"

        if not env_file.exists():
            # Also check current directory
            env_file = Path(".env.diagnostic")
            if not env_file.exists():
                return None

        # Read and parse .env.diagnostic file
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue
                    # Parse KEY=value format
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        if key == 'ANTHROPIC_API_KEY':
                            return value
        except Exception as e:
            print(f"Error reading .env.diagnostic: {e}")
            return None

        return None

    def _create_system_prompt(self) -> str:
        """Create the system prompt that defines the AI's role and knowledge."""
        return """You are an expert HVAC diagnostic assistant specializing in troubleshooting the Oil Tank Transfer Box system (Program #3201) controlled by a Schneider Electric Zelio Logic SR3B261FU PLC.

CURRENT PROBLEM: Tank #2 does not fill automatically (but may work in manual mode).

YOUR ROLE:
- Guide the technician through systematic diagnostic troubleshooting
- Ask clear, specific questions to gather information
- Analyze responses intelligently and adapt your questioning
- Provide technical explanations when needed
- Make recommendations based on findings
- Be conversational and helpful, not robotic

SYSTEM KNOWLEDGE:

Hardware:
- PLC: Schneider Electric Zelio Logic SR3B261FU (100-240V AC)
- Expansion: SR3XT141FU (XT2)
- Cycle Time: 20ms
- Input Filtering: 3ms "Slow" filter

Critical Inputs:
- IL: System Ready (master gate for ALL operations)
- ID: Tank A direction (controls relay M4)
- IE: Tank B direction (controls relay M5)

Critical Outputs:
- Q1, Q2: Transfer pumps
- Q6, Q7, Q8: Solenoid valves

Important Relays:
- M1: System Ready Gate (must be ON for pumps to run)
- M2: Transfer Demand (must be ON when transfer requested)
- M3: Safety Interlock (must be ON, blocked if valves stuck)
- M4: Direction A latch
- M5: Direction B latch
- M6: Stop command (must be OFF)

Timers:
- T9 & TA: Set to 1.5 seconds (valves must open within this window)

TANK #2 SPECIFIC INFORMATION:
- Tank #2 typically corresponds to Tank B (Input IE, Relay M5)
- However, verify with technician as labeling can vary by facility
- If Tank #2 = Tank B: Check Input IE and relay M5
- If Tank #2 = Tank A: Check Input ID and relay M4

DIAGNOSTIC APPROACH:
1. First determine if Tank #2 = Tank A (Input ID) or Tank B (Input IE)
2. Test in Manual mode to isolate AUTO vs physical problems
3. Check level sensor/float switch for Tank #2
4. Verify sensor signal reaches PLC terminal
5. Check System Ready relay M1 and Input IL
6. Verify all safety interlocks (M2, M3, M6)
7. Test valve timing (1.5s window)

COMMON FAILURE PATTERNS:
- Manual works, Auto fails → Sensor or input wiring problem (70% of cases)
- Input IL missing → M1 stays OFF, blocks everything
- Timer timeouts → Valves too slow (>1.5s)
- M3 blocked → Valves stuck or conflicting outputs

CONVERSATION GUIDELINES:
- Start by gathering basic info (technician name, what they've observed)
- Ask ONE clear question at a time
- If technician seems confused, rephrase or provide context
- After each answer, briefly acknowledge and explain significance
- Provide step-by-step instructions for tests when needed
- Adapt follow-up questions based on previous answers
- Skip irrelevant steps intelligently
- Summarize findings periodically
- At the end, provide clear root cause analysis and recommendations

IMPORTANT:
- Be conversational and friendly, but professional
- Explain technical terms when first mentioned
- Provide safety reminders (LOTO, 240V AC warning)
- If technician says "I don't know" or "not sure", suggest ways to find out
- Track all findings mentally to make final diagnosis

When the diagnostic session is complete and you've identified the root cause, end with:
"DIAGNOSTIC COMPLETE - Would you like me to generate the final report?"
"""

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('clear' if os.name == 'posix' else 'cls')

    def print_header(self):
        """Print application header."""
        print("\n" + "=" * 80)
        print("  AI-POWERED TANK #2 DIAGNOSTIC ASSISTANT")
        print("=" * 80)
        print(f"  System: Oil Tank Transfer Box (Program #3201)")
        print(f"  Session ID: {self.session_id}")
        print(f"  Powered by: Claude AI (Anthropic)")
        print("=" * 80 + "\n")

    def chat(self, user_message: str) -> str:
        """Send message to AI and get response."""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Get AI response
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=self.system_prompt,
            messages=self.conversation_history
        )

        # Extract assistant's message
        assistant_message = response.content[0].text

        # Add to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def run_diagnostic(self):
        """Main diagnostic conversation loop."""
        self.clear_screen()
        self.print_header()

        print("⚠️  SAFETY WARNING: Follow all LOTO procedures. System operates at 240V AC.")
        print("\n" + "=" * 80)
        print("\nWelcome! I'm your AI diagnostic assistant.")
        print("I'll guide you through troubleshooting Tank #2's auto-fill problem.")
        print("\nTips:")
        print("  • Answer naturally - I'll understand context")
        print("  • Say 'clarify' or 'explain' if you need more info")
        print("  • Type 'skip' if you can't answer a question")
        print("  • Type 'quit' to end session (I'll save everything)")
        print("\nLet's begin!\n")
        print("=" * 80 + "\n")

        # Initial prompt to start conversation
        initial_prompt = (
            "I'm starting a diagnostic session for Tank #2 auto-fill failure. "
            "Begin by introducing yourself and asking for the technician's name and "
            "a brief description of what they've observed with the system."
        )

        ai_response = self.chat(initial_prompt)
        print(f"AI: {ai_response}\n")

        # Main conversation loop
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                # Check for quit command
                if user_input.lower() in ['quit', 'exit', 'done']:
                    print("\n" + "=" * 80)
                    print("Ending diagnostic session...")

                    # Ask AI for final summary
                    summary_request = (
                        "The technician is ending the session. Based on our conversation, "
                        "provide a brief summary of what we found and any recommendations. "
                        "Keep it concise (3-5 sentences)."
                    )
                    final_summary = self.chat(summary_request)
                    print(f"\nAI: {final_summary}\n")
                    break

                # Send to AI and get response
                ai_response = self.chat(user_input)
                print(f"\nAI: {ai_response}\n")

                # Check if diagnostic is complete
                if "DIAGNOSTIC COMPLETE" in ai_response:
                    generate = input("\nGenerate final report? (Y/N): ").strip().upper()
                    if generate in ['Y', 'YES']:
                        self._generate_final_report()
                    break

            except KeyboardInterrupt:
                print("\n\n" + "=" * 80)
                print("Session interrupted by user.")
                save = input("Save conversation? (Y/N): ").strip().upper()
                if save in ['Y', 'YES']:
                    self._save_conversation()
                break
            except Exception as e:
                print(f"\nError: {e}")
                print("Attempting to save conversation...")
                self._save_conversation()
                break

        # Save conversation
        self._save_conversation()
        print("\n" + "=" * 80)
        print("Session saved. Thank you!")
        print("=" * 80 + "\n")

    def _generate_final_report(self):
        """Ask AI to generate structured final report."""
        print("\n" + "=" * 80)
        print("Generating final diagnostic report...")
        print("=" * 80 + "\n")

        report_request = """Based on our entire diagnostic conversation, generate a structured final report with these sections:

1. TECHNICIAN INFORMATION
2. PROBLEM DESCRIPTION
3. TESTS PERFORMED (list all tests/measurements done)
4. KEY FINDINGS (critical discoveries)
5. ROOT CAUSE ANALYSIS
6. RECOMMENDATIONS (specific corrective actions)
7. SYSTEM STATUS (working / not working / partially working)

Format each section clearly with headers. Be specific and reference actual measurements/observations from our conversation."""

        report = self.chat(report_request)
        print(f"{report}\n")

        # Save report to separate file
        report_file = os.path.join(
            self.output_dir,
            f"Tank2_AI_Diagnostic_Report_{self.session_id}.txt"
        )

        with open(report_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("AI-POWERED DIAGNOSTIC REPORT - TANK #2 AUTO-FILL FAILURE\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"System: Oil Tank Transfer Box (Program #3201)\n")
            f.write(f"PLC: Schneider Electric Zelio Logic SR3B261FU\n\n")
            f.write("=" * 80 + "\n\n")
            f.write(report)
            f.write("\n\n" + "=" * 80 + "\n")
            f.write("END OF REPORT\n")
            f.write("=" * 80 + "\n")

        print(f"\n✓ Final report saved to: {report_file}")

    def _save_conversation(self):
        """Save full conversation history to file."""
        filename = f"Tank2_AI_Conversation_{self.session_id}.txt"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("AI DIAGNOSTIC CONVERSATION LOG - TANK #2\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Started: {self.session_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"System: Oil Tank Transfer Box (Program #3201)\n\n")
            f.write("=" * 80 + "\n\n")

            for msg in self.conversation_history:
                role = msg['role'].upper()
                content = msg['content']

                if role == "USER":
                    f.write(f"TECHNICIAN: {content}\n\n")
                else:
                    f.write(f"AI ASSISTANT: {content}\n\n")
                f.write("-" * 80 + "\n\n")

            f.write("=" * 80 + "\n")
            f.write("END OF CONVERSATION\n")
            f.write("=" * 80 + "\n")

        print(f"✓ Conversation saved to: {filepath}")

        # Also save as JSON for potential future analysis
        json_file = os.path.join(self.output_dir, f"Tank2_AI_Conversation_{self.session_id}.json")
        with open(json_file, 'w') as f:
            json.dump({
                'session_id': self.session_id,
                'tank': 2,
                'started': self.session_time.isoformat(),
                'ended': datetime.now().isoformat(),
                'conversation': self.conversation_history
            }, f, indent=2)

        print(f"✓ JSON data saved to: {json_file}")
        return filepath


def main():
    """Main entry point."""
    try:
        app = AITank2Diagnostic()
        app.run_diagnostic()
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
