#!/usr/bin/env python3
"""
Virtual HVAC Technician - AI-powered HVAC expert assistant
Answers all kinds of questions about heating, ventilation, and air conditioning

Supports two LLM backends:
- ollama (default, FREE): Local Ollama with llama3.2:3b
- claude (PAID): Claude API via Anthropic (requires ANTHROPIC_API_KEY)

Usage:
  python hvac_expert.py "your question"                    # Uses Ollama (free)
  python hvac_expert.py --llm=claude "your question"       # Uses Claude API (paid)
  python hvac_expert.py --llm ollama "your question"       # Explicit Ollama
"""

from crewai import Agent, Task, Crew, LLM
import os
import sys
import argparse
from dotenv import load_dotenv

# Parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(
        description='Virtual HVAC Technician - AI-powered HVAC expert',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "How often should I change my filter?"              # Free (Ollama)
  %(prog)s --llm=claude "How often should I change my filter?" # Paid (Claude API)
  %(prog)s --llm claude "Troubleshoot AC issue"                # Paid (Claude API)
  %(prog)s                                                      # Interactive mode
        """
    )
    parser.add_argument(
        '--llm',
        choices=['ollama', 'claude'],
        default='ollama',
        help='LLM backend to use (default: ollama=FREE, claude=PAID)'
    )
    parser.add_argument(
        'question',
        nargs='*',
        help='Your HVAC question (if not provided, enters interactive mode)'
    )
    return parser.parse_args()

# Configure LLM based on choice
def configure_llm(llm_choice):
    if llm_choice == 'claude':
        # Load API key from .env.diagnostic
        env_path = os.path.join(os.path.dirname(__file__), '..', '.env.diagnostic')
        if os.path.exists(env_path):
            load_dotenv(env_path)

        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("❌ Error: ANTHROPIC_API_KEY not found!")
            print()
            print("To use Claude API, you need:")
            print("1. An Anthropic API account from https://console.anthropic.com/")
            print("2. Create .env.diagnostic in the parent directory with:")
            print("   ANTHROPIC_API_KEY=your-api-key-here")
            print()
            print("Cost: ~$0.01-0.05 per session")
            print()
            print("Falling back to free Ollama...")
            return configure_llm('ollama'), 'ollama'

        print("🔵 Using Claude API (PAID - ~$0.01-0.05 per session)")
        # Note: Change model name if needed. Common options:
        # - claude-3-5-haiku-20241022 (cheaper, faster)
        # - claude-3-5-sonnet-20241022 (balanced)
        # - claude-3-opus-20240229 (most capable)
        return LLM(
            model="claude-3-5-haiku-20241022",
            api_key=api_key
        ), 'claude'
    else:
        # Default: Ollama (free)
        ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        print("🟢 Using Ollama (FREE - Local)")
        return LLM(
            model="ollama/llama3.2:3b",
            base_url=ollama_host
        ), 'ollama'

# Global LLM instance (will be set in main)
llm = None
llm_name = None

# Function to create agents with the configured LLM
def create_agents(llm_instance):
    hvac_expert = Agent(
        role='Master HVAC Technician',
        goal='Provide expert advice on all HVAC-related questions',
        backstory="""You are a highly experienced HVAC technician with 20+ years
        in the field. You have expertise in:
        - Residential and commercial HVAC systems
        - Heating systems (furnaces, boilers, heat pumps)
        - Air conditioning (central AC, mini-splits, window units)
        - Ventilation and air quality
        - Refrigeration cycles and components
        - Troubleshooting and diagnostics
        - Installation and maintenance
        - Energy efficiency and optimization
        - HVAC codes and safety standards
        - Tools and equipment

        You explain technical concepts clearly, provide step-by-step guidance,
        and always prioritize safety. You're patient, thorough, and helpful.""",
        verbose=True,
        allow_delegation=False,
        llm=llm_instance
    )

    diagnostics_expert = Agent(
        role='HVAC Diagnostics Specialist',
        goal='Help troubleshoot HVAC problems and provide solutions',
        backstory="""You are a specialist in HVAC diagnostics and problem-solving.
        You excel at:
        - Identifying symptoms and root causes
        - Using diagnostic tools and techniques
        - Creating step-by-step troubleshooting guides
        - Explaining repair procedures
        - Recommending preventive maintenance
        - Estimating repair costs
        - Knowing when to call a professional

        You ask clarifying questions to narrow down issues and provide
        safe, practical solutions.""",
        verbose=True,
        allow_delegation=False,
        llm=llm_instance
    )

    return hvac_expert, diagnostics_expert

def ask_question(question, use_diagnostics=False, hvac_expert=None, diagnostics_expert=None):
    """Ask a question to the HVAC expert"""

    if use_diagnostics:
        # For troubleshooting questions, use diagnostics specialist
        task = Task(
            description=f"""User question: {question}

            Provide a detailed, step-by-step troubleshooting guide.
            Include:
            1. Possible causes
            2. Diagnostic steps
            3. Solutions
            4. Safety warnings
            5. When to call a professional

            Be specific and practical.""",
            agent=diagnostics_expert,
            expected_output="Detailed troubleshooting guide with step-by-step instructions"
        )
        agent = diagnostics_expert
    else:
        # For general questions, use main HVAC expert
        task = Task(
            description=f"""User question: {question}

            Provide a clear, comprehensive answer.
            Include relevant details, examples, and practical advice.
            If it's a safety concern, emphasize safety precautions.
            If it involves complex repairs, mention when to call a professional.""",
            agent=hvac_expert,
            expected_output="Clear, comprehensive answer to the HVAC question"
        )
        agent = hvac_expert

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False  # Less verbose for cleaner output
    )

    result = crew.kickoff()

    # Return just the answer text, clean
    return str(result)

def interactive_mode():
    """Run in interactive Q&A mode"""
    # Show header in interactive mode
    print("\n🔧 Virtual HVAC Technician")
    print("=" * 60)
    print("Your AI-powered HVAC expert is ready to help!")
    print("Ask me anything about heating, ventilation, air conditioning,")
    print("troubleshooting, maintenance, installation, and more.")
    print("=" * 60)
    print("\n💬 Interactive Mode")
    print("Type your HVAC questions (or 'quit' to exit)")
    print("-" * 60)

    while True:
        print("\n❓ Your question: ", end="")
        question = input().strip()

        if question.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Thanks for using Virtual HVAC Technician!")
            break

        if not question:
            continue

        # Check if it's a troubleshooting question
        troubleshoot_keywords = [
            'not working', 'broken', 'problem', 'issue', 'fix',
            'repair', 'troubleshoot', 'diagnose', 'won\'t', 'doesn\'t'
        ]
        use_diagnostics = any(keyword in question.lower() for keyword in troubleshoot_keywords)

        print("\n🔧 HVAC Expert:")
        print("-" * 60)

        try:
            answer = ask_question(question, use_diagnostics)
            print(answer)
        except Exception as e:
            print(f"Error: {e}")
            print("Please try rephrasing your question.")

        print("-" * 60)

def single_question_mode(question):
    """Answer a single question and exit"""
    # Check if it's troubleshooting
    troubleshoot_keywords = [
        'not working', 'broken', 'problem', 'issue', 'fix',
        'repair', 'troubleshoot', 'diagnose', 'won\'t', 'doesn\'t'
    ]
    use_diagnostics = any(keyword in question.lower() for keyword in troubleshoot_keywords)

    answer = ask_question(question, use_diagnostics)

    # Print clean output only
    print("\n" + "=" * 60)
    print(answer)
    print("=" * 60 + "\n")

# Main execution
if __name__ == "__main__":
    # Parse arguments
    args = parse_args()

    # Configure LLM
    llm, llm_name = configure_llm(args.llm)

    # Create agents with the configured LLM
    hvac_expert, diagnostics_expert = create_agents(llm)

    # Determine mode
    if args.question:
        # Single question mode
        question = " ".join(args.question)

        # Check if it's troubleshooting
        troubleshoot_keywords = [
            'not working', 'broken', 'problem', 'issue', 'fix',
            'repair', 'troubleshoot', 'diagnose', 'won\'t', 'doesn\'t'
        ]
        use_diagnostics = any(keyword in question.lower() for keyword in troubleshoot_keywords)

        answer = ask_question(question, use_diagnostics, hvac_expert, diagnostics_expert)

        # Print clean output only
        print("\n" + "=" * 60)
        print(answer)
        print("=" * 60 + "\n")
    else:
        # Interactive mode
        print("\n🔧 Virtual HVAC Technician")
        print("=" * 60)
        print("Your AI-powered HVAC expert is ready to help!")
        print("Ask me anything about heating, ventilation, air conditioning,")
        print("troubleshooting, maintenance, installation, and more.")
        print("=" * 60)
        print("\n💬 Interactive Mode")
        print("Type your HVAC questions (or 'quit' to exit)")
        print("-" * 60)

        while True:
            print("\n❓ Your question: ", end="")
            question = input().strip()

            if question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thanks for using Virtual HVAC Technician!")
                break

            if not question:
                continue

            # Check if it's a troubleshooting question
            troubleshoot_keywords = [
                'not working', 'broken', 'problem', 'issue', 'fix',
                'repair', 'troubleshoot', 'diagnose', 'won\'t', 'doesn\'t'
            ]
            use_diagnostics = any(keyword in question.lower() for keyword in troubleshoot_keywords)

            print("\n🔧 HVAC Expert:")
            print("-" * 60)

            try:
                answer = ask_question(question, use_diagnostics, hvac_expert, diagnostics_expert)
                print(answer)
            except Exception as e:
                print(f"Error: {e}")
                print("Please try rephrasing your question.")

            print("-" * 60)
