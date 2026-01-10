#!/usr/bin/env python3
"""
Interactive Tank #1 Diagnostic Application
Guides technician through troubleshooting steps and records all responses.
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple

class Tank1DiagnosticApp:
    def __init__(self):
        self.responses = {}
        self.output_dir = "/Users/sergevilleneuve/Documents/MyExperiments/HVAC_ideas/.tmp"
        self.session_time = datetime.now()
        self.session_id = self.session_time.strftime("%Y%m%d_%H%M%S")

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('clear' if os.name == 'posix' else 'cls')

    def print_header(self, title):
        """Print a formatted section header."""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70 + "\n")

    def print_separator(self):
        """Print a simple separator line."""
        print("-" * 70)

    def ask_question(self, question_id: str, question_text: str,
                     options: List[str] = None, input_type: str = "text") -> str:
        """
        Ask a question and get user response.

        Args:
            question_id: Unique identifier for the question
            question_text: The question to display
            options: List of options for multiple choice
            input_type: Type of input expected (text, choice, yesno, number)

        Returns:
            User's response
        """
        print(f"\n[Q{question_id}] {question_text}\n")

        if options and input_type == "choice":
            for i, option in enumerate(options, 1):
                print(f"  {i}. {option}")
            print()

            while True:
                try:
                    response = input("Enter choice number: ").strip()
                    choice_num = int(response)
                    if 1 <= choice_num <= len(options):
                        answer = options[choice_num - 1]
                        self.responses[question_id] = {
                            'question': question_text,
                            'answer': answer,
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        return answer
                    else:
                        print(f"Please enter a number between 1 and {len(options)}")
                except ValueError:
                    print("Please enter a valid number")

        elif input_type == "yesno":
            while True:
                response = input("Enter (Y/N): ").strip().upper()
                if response in ['Y', 'YES', 'N', 'NO']:
                    answer = 'YES' if response in ['Y', 'YES'] else 'NO'
                    self.responses[question_id] = {
                        'question': question_text,
                        'answer': answer,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    return answer
                print("Please enter Y or N")

        elif input_type == "number":
            while True:
                response = input("Enter value: ").strip()
                if response:
                    self.responses[question_id] = {
                        'question': question_text,
                        'answer': response,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    return response
                print("Please enter a value")

        else:  # text input
            response = input("Your answer: ").strip()
            if not response:
                response = "(No response)"
            self.responses[question_id] = {
                'question': question_text,
                'answer': response,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            return response

    def show_info(self, message: str):
        """Display informational message."""
        print(f"\nℹ️  {message}\n")

    def show_warning(self, message: str):
        """Display warning message."""
        print(f"\n⚠️  WARNING: {message}\n")

    def show_recommendation(self, message: str):
        """Display recommendation."""
        print(f"\n✓ RECOMMENDATION: {message}\n")

    def pause(self):
        """Pause for user to continue."""
        input("\nPress ENTER to continue...")

    def run_diagnostic(self):
        """Main diagnostic workflow."""
        self.clear_screen()

        # Welcome screen
        self.print_header("TANK #1 AUTO-FILL DIAGNOSTIC APPLICATION")
        print("  System: Oil Tank Transfer Box (Program #3201)")
        print("  PLC: Schneider Electric Zelio Logic SR3B261FU")
        print(f"  Session ID: {self.session_id}")
        print()
        print("  This application will guide you through systematic troubleshooting")
        print("  of Tank #1 auto-fill failure. All responses will be saved.")
        print()
        self.show_warning("Follow all LOTO procedures. System operates at 240V AC.")
        self.pause()

        # Initial information
        self.clear_screen()
        self.print_header("INITIAL INFORMATION")

        self.ask_question("0.1", "Technician name:", input_type="text")
        self.ask_question("0.2", "Date/Time of diagnosis:", input_type="text")
        self.ask_question("0.3", "Problem description (in your own words):", input_type="text")

        # STEP 1: Identify Tank Direction
        self.clear_screen()
        self.print_header("STEP 1: IDENTIFY TANK #1 DIRECTION")

        self.show_info("The PLC uses two inputs to control tank direction:")
        print("  • Input ID → Tank A (Direction 1) → Controls Relay M4")
        print("  • Input IE → Tank B (Direction 2) → Controls Relay M5")

        tank_direction = self.ask_question(
            "1.1",
            "Which input controls Tank #1?",
            options=["Tank A (Input ID)", "Tank B (Input IE)", "Not Sure"],
            input_type="choice"
        )

        if "Not Sure" in tank_direction:
            self.show_recommendation(
                "Check system documentation or consult with facility manager to identify Tank #1."
            )

        self.pause()

        # STEP 2: Manual Mode Test
        self.clear_screen()
        self.print_header("STEP 2: MANUAL MODE TEST")

        self.show_info(
            "This test determines if the problem is automatic sensing or physical pump/valve failure."
        )
        print("Procedure:")
        print("  1. Switch control selector to MANUAL mode")
        print("  2. Manually activate transfer to Tank #1")
        print("  3. Observe what happens\n")

        manual_result = self.ask_question(
            "2.1",
            "What happened when you tested in Manual mode?",
            options=[
                "Tank #1 filled successfully",
                "Tank #1 did NOT fill",
                "Pump started but stopped after 1-2 seconds",
                "Unable to test"
            ],
            input_type="choice"
        )

        # Provide guidance based on manual test
        if "filled successfully" in manual_result:
            self.show_info("Pumps and valves work. Problem is AUTO sensing. Continue to STEP 3.")
            skip_physical = True
        elif "did NOT fill" in manual_result:
            self.show_info("Physical problem with pump, valves, or wiring. Jump to STEP 5.")
            skip_physical = False
        elif "stopped after" in manual_result:
            self.show_info("Timer timeout fault. Valve may be too slow. Jump to STEP 7.")
            skip_physical = False
        else:
            skip_physical = False

        self.pause()

        # STEP 3: Check Level Sensor
        self.clear_screen()
        self.print_header("STEP 3: CHECK TANK #1 LEVEL SENSOR")

        self.show_info("Checking the float switch or level sensor that triggers Tank #1 fill.")

        self.ask_question(
            "3.1",
            "Visual inspection - Does the float/sensor move freely without binding?",
            input_type="yesno"
        )

        self.ask_question(
            "3.2",
            "Is there visible damage, corrosion, or debris on the sensor?",
            input_type="yesno"
        )

        sensor_continuity = self.ask_question(
            "3.3",
            "Electrical continuity test - Does sensor make/break contact when moved?",
            input_type="yesno"
        )

        if sensor_continuity == "NO":
            self.show_recommendation("Sensor is failed. Replace sensor and retest system.")
            self.ask_question("3.4", "Was sensor replaced?", input_type="yesno")

        self.pause()

        # STEP 4: Verify PLC Input Signal
        self.clear_screen()
        self.print_header("STEP 4: VERIFY PLC INPUT SIGNAL")

        self.show_info("Testing if sensor signal reaches the PLC terminal.")

        if "Tank A" in self.responses.get("1.1", {}).get('answer', ''):
            input_to_check = "ID"
        elif "Tank B" in self.responses.get("1.1", {}).get('answer', ''):
            input_to_check = "IE"
        else:
            input_to_check = self.ask_question(
                "4.0",
                "Which input should we check?",
                options=["ID", "IE"],
                input_type="choice"
            )

        self.show_info(f"Testing Input {input_to_check}")
        print("Procedure:")
        print(f"  1. Connect multimeter to terminal {input_to_check} and common ground")
        print("  2. Trigger low-level condition for Tank #1")
        print("  3. Measure DC voltage (expect 12-24V when activated)\n")

        voltage = self.ask_question(
            "4.1",
            f"What voltage did you measure at Input {input_to_check}? (in VDC)",
            input_type="number"
        )

        try:
            v = float(voltage)
            if v < 5:
                self.show_warning(
                    f"Low voltage ({v}V). Check wiring between sensor and PLC terminal {input_to_check}."
                )
        except ValueError:
            pass

        has_zelio = self.ask_question(
            "4.2",
            "Do you have access to Zelio Soft software or PLC display?",
            input_type="yesno"
        )

        if has_zelio == "YES":
            relay_to_check = "M4" if input_to_check == "ID" else "M5"
            relay_status = self.ask_question(
                "4.3",
                f"When sensor is triggered, does relay {relay_to_check} turn ON?",
                input_type="yesno"
            )

            if relay_status == "NO":
                self.show_warning(
                    "Relay not activating. Possible input filtering or PLC configuration issue."
                )

        self.pause()

        # STEP 5: System Ready Relay (M1)
        self.clear_screen()
        self.print_header("STEP 5: SYSTEM READY RELAY CHECK (M1)")

        self.show_info(
            "Relay M1 is the master 'System Ready' gate. If M1 is OFF, NO pumps can run."
        )

        if has_zelio == "YES":
            m1_status = self.ask_question(
                "5.1",
                "Check PLC display/Zelio Soft - Is relay M1 active (ON)?",
                input_type="yesno"
            )

            if m1_status == "NO":
                self.show_warning("M1 is OFF - This blocks all pump operation!")
                print("\nMost common cause: Input IL is open or missing signal")
        else:
            m1_status = "UNKNOWN"
            self.show_info("Cannot check M1 without PLC access. Checking Input IL instead.")

        il_voltage = self.ask_question(
            "5.2",
            "Measure voltage at terminal IL (System Ready input) in VDC:",
            input_type="number"
        )

        try:
            v = float(il_voltage)
            if v < 5:
                self.show_warning(
                    f"Input IL has low/no voltage ({v}V). This is likely the main problem!"
                )
                self.show_recommendation(
                    "Check 'System Ready' sensor wiring to IL terminal. Verify safety devices are closed."
                )
        except ValueError:
            pass

        self.pause()

        # STEP 6: Safety Interlocks
        self.clear_screen()
        self.print_header("STEP 6: SAFETY INTERLOCK CHECK")

        if has_zelio == "YES":
            self.show_info("Checking all safety relay states via PLC display/software.")

            relays_to_check = [
                ("M1", "System Ready Gate", "ON"),
                ("M2", "Transfer Demand", "ON"),
                ("M3", "Safety Interlock", "ON"),
                ("M6", "Stop Command", "OFF"),
            ]

            for relay_name, relay_function, expected in relays_to_check:
                status = self.ask_question(
                    f"6.{relay_name}",
                    f"Relay {relay_name} ({relay_function}) - Current state?",
                    options=["ON", "OFF"],
                    input_type="choice"
                )

                if status != expected:
                    self.show_warning(
                        f"Relay {relay_name} is {status} but should be {expected}!"
                    )
        else:
            self.show_info("Skipping relay check - no PLC access available.")

        self.pause()

        # STEP 7: Timer & Valve Check
        self.clear_screen()
        self.print_header("STEP 7: TIMER & VALVE SEQUENCING")

        self.show_info("Checking if valves open within the 1.5-second timer window.")

        test_timer = self.ask_question(
            "7.1",
            "Do you want to test valve actuation timing?",
            input_type="yesno"
        )

        if test_timer == "YES":
            print("\nProcedure:")
            print("  1. Trigger Tank #1 fill in Auto mode")
            print("  2. Watch solenoid valve (Q6 or Q7)")
            print("  3. Measure time from valve activation to full open")
            print("  4. Observe if pump starts\n")

            valve_time = self.ask_question(
                "7.2",
                "How long did the valve take to fully open? (in seconds)",
                input_type="number"
            )

            try:
                t = float(valve_time)
                if t > 1.5:
                    self.show_warning(
                        f"Valve takes {t}s to open - exceeds 1.5s timer limit!"
                    )
                    self.show_recommendation(
                        "Check valve for mechanical binding or increase timer setting in PLC program."
                    )
            except ValueError:
                pass

            pump_start = self.ask_question(
                "7.3",
                "Did the pump start after valve opened?",
                input_type="yesno"
            )

            if pump_start == "NO":
                self.show_warning("Timer timeout fault - valve took too long to open.")

        self.pause()

        # Final Analysis
        self.clear_screen()
        self.print_header("DIAGNOSTIC SUMMARY")

        self.ask_question(
            "8.1",
            "Based on your findings, what is the root cause?",
            input_type="text"
        )

        self.ask_question(
            "8.2",
            "What corrective action did you take (or will take)?",
            input_type="text"
        )

        system_working = self.ask_question(
            "8.3",
            "After repairs, is the system tested and working?",
            options=["YES - Tank #1 fills automatically", "NO - Still not working", "Not tested yet"],
            input_type="choice"
        )

        if "Still not working" in system_working:
            self.ask_question(
                "8.4",
                "What additional help is needed?",
                input_type="text"
            )

        # Save results
        self.clear_screen()
        self.print_header("SAVING DIAGNOSTIC REPORT")

        text_file = self.save_text_report()
        print(f"✓ Text report saved: {text_file}")

        print("\nDiagnostic session complete. Thank you!")
        print()

    def save_text_report(self) -> str:
        """Save diagnostic responses to a text file."""
        filename = f"Tank1_Diagnostic_Session_{self.session_id}.txt"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("TANK #1 AUTO-FILL DIAGNOSTIC REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Session ID: {self.session_id}\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"System: Oil Tank Transfer Box (Program #3201)\n")
            f.write(f"PLC: Schneider Electric Zelio Logic SR3B261FU\n")
            f.write("\n" + "=" * 80 + "\n\n")

            # Group responses by step
            current_step = ""
            for qid in sorted(self.responses.keys(), key=lambda x: (float(x.split('.')[0]), float(x.split('.')[1]))):
                response = self.responses[qid]
                step_num = qid.split('.')[0]

                # Print step header
                if step_num != current_step:
                    current_step = step_num
                    step_names = {
                        '0': 'INITIAL INFORMATION',
                        '1': 'STEP 1: IDENTIFY TANK DIRECTION',
                        '2': 'STEP 2: MANUAL MODE TEST',
                        '3': 'STEP 3: LEVEL SENSOR CHECK',
                        '4': 'STEP 4: PLC INPUT SIGNAL',
                        '5': 'STEP 5: SYSTEM READY RELAY (M1)',
                        '6': 'STEP 6: SAFETY INTERLOCKS',
                        '7': 'STEP 7: TIMER & VALVE SEQUENCING',
                        '8': 'DIAGNOSTIC SUMMARY'
                    }
                    f.write("\n" + "-" * 80 + "\n")
                    f.write(f"{step_names.get(step_num, 'STEP ' + step_num)}\n")
                    f.write("-" * 80 + "\n\n")

                f.write(f"[Q{qid}] {response['question']}\n")
                f.write(f"Answer: {response['answer']}\n")
                f.write(f"Time: {response['timestamp']}\n\n")

            f.write("\n" + "=" * 80 + "\n")
            f.write("END OF DIAGNOSTIC REPORT\n")
            f.write("=" * 80 + "\n")

        return filepath


def main():
    """Main entry point."""
    app = Tank1DiagnosticApp()

    try:
        app.run_diagnostic()
    except KeyboardInterrupt:
        print("\n\nDiagnostic interrupted by user.")
        save = input("Save partial results? (Y/N): ").strip().upper()
        if save in ['Y', 'YES']:
            filepath = app.save_text_report()
            print(f"Partial results saved to: {filepath}")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError occurred: {e}")
        print("Attempting to save partial results...")
        try:
            filepath = app.save_text_report()
            print(f"Partial results saved to: {filepath}")
        except:
            print("Could not save results.")
        sys.exit(1)


if __name__ == "__main__":
    main()
