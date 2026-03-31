# main.py
"""
Trading Agent — CLI entry point.

Run:
    python main.py

Or test a single query:
    python main.py "NIFTY 18000 CE, 2 lots, buy 200, sell 280, SL 160"
"""

import sys
from agent.trading_agent import ask_agent

BANNER = """
╔══════════════════════════════════════════════════════╗
║         📈  Options Trading AI Agent  📈             ║
║   Powered by Ollama (llama3.1) + LangChain           ║
║   Type 'exit' or 'quit' to stop                      ║
╚══════════════════════════════════════════════════════╝
"""

EXAMPLE_QUERIES = [
    "NIFTY 18000 CE, 2 lots, buy at 200, sell at 280, stop loss 160",
    "Calculate BANKNIFTY 44000 PE trade: 1 lot, entry 350, target 500, SL 280",
    "What is the break-even for NIFTY 19500 CE if I buy at 120?",
]


def run_cli():
    print(BANNER)
    print("💡 Example queries:")
    for i, q in enumerate(EXAMPLE_QUERIES, 1):
        print(f"   {i}. {q}")
    print()

    session_id = "cli_session"

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit", "bye"):
            print("👋 Goodbye!")
            break

        print("\nAgent: ", end="", flush=True)
        response = ask_agent(user_input, session_id=session_id)
        print(response)
        print()


def run_single(query: str):
    """Run a single query and print result (useful for testing)."""
    print(f"\n🔍 Query: {query}\n")
    response = ask_agent(query, session_id="test")
    print(f"✅ Response:\n{response}\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Single query mode: python main.py "your query here"
        run_single(" ".join(sys.argv[1:]))
    else:
        # Interactive CLI mode
        run_cli()
