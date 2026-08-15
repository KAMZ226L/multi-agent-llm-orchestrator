"""
Multi-Agent LLM Orchestrator

A multi-agent system that uses a local LLM (Ollama) to interpret user queries,
fetch data from external APIs, generate natural language responses, and deliver
them via Telegram.
"""

import logging
from orchestrator import Orchestrator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S"
)

def main():
    orchestrator = Orchestrator()

    print("\n=== Multi-Agent LLM Orchestrator ===")
    print("Ask anything about One Piece (type 'exit' to quit)\n")

    while True:
        query = input("You: ").strip()

        if not query:
            continue
        if query.lower() in ("exit", "quit", "q"):
            print("Goodbye!")
            break

        orchestrator.run(query)
        print()


if __name__ == "__main__":
    main()