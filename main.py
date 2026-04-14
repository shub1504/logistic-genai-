# main.py

"""
Main entry point for the Logistics Optimizer.
Runs as a CLI tool or launches the ADK web interface.

Usage:
    python main.py
    python main.py --web        (launches ADK web UI)
    python main.py --message "deliver to Saket and Rohini"
"""

import os
import sys
import argparse
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipeline import run_pipeline


def print_result(result: dict):
    """Pretty print a pipeline result to the terminal."""
    print("\n" + "="*60)
    print("  LOGISTICS OPTIMIZER — RESULT")
    print("="*60)
    print(f"  Route:     {result['route_readable']}")
    print(f"  Distance:  {result['total_distance']} km")
    print(f"  Stops:     {result['num_stops']}")
    print(f"  Logged:    {'✅ Yes' if result['logged'] else '❌ No'}")
    print("-"*60)
    print("  DRIVER BRIEFING:")
    print(f"  {result['briefing']}")
    print("-"*60)
    print("  MANAGER SUMMARY:")
    print(f"  {result['summary']}")
    print("="*60 + "\n")


def run_interactive():
    """Interactive CLI loop — keep asking for deliveries."""
    print("\n" + "="*60)
    print("  DELHI LOGISTICS OPTIMIZER")
    print("  Powered by Dijkstra + Gemini + BigQuery")
    print("="*60)
    print("  Type your delivery request in plain English.")
    print("  Example: 'deliver to Saket, Rohini and Dwarka'")
    print("  Type 'quit' to exit.\n")

    while True:
        try:
            user_input = input("  You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "q"):
                print("  Goodbye!")
                break

            result = run_pipeline(user_input)
            print_result(result)

        except KeyboardInterrupt:
            print("\n  Goodbye!")
            break
        except Exception as e:
            print(f"  [Error] {e}")


def run_adk_web():
    """Launch the ADK web interface."""
    print("[Main] Launching ADK web interface...")
    try:
        import subprocess
        subprocess.run(
            ["adk", "web", "logistics_agent_app/"],
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
    except FileNotFoundError:
        print("[Main] ADK not found. Install with: pip install google-adk")
        print("[Main] Falling back to interactive CLI...")
        run_interactive()


def main():
    parser = argparse.ArgumentParser(
        description="Delhi Logistics Optimizer"
    )
    parser.add_argument(
        "--web",
        action="store_true",
        help="Launch ADK web interface"
    )
    parser.add_argument(
        "--message",
        type=str,
        help="Run a single delivery message and exit"
    )
    args = parser.parse_args()

    if args.web:
        run_adk_web()
    elif args.message:
        result = run_pipeline(args.message)
        print_result(result)
    else:
        run_interactive()


if __name__ == "__main__":
    main()