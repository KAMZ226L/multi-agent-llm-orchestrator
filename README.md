# Multi-Agent LLM Orchestrator

A multi-agent system that uses a local LLM (Ollama) to interpret natural language queries, fetch data from external APIs, generate human-readable responses, and deliver them via Telegram — all coordinated by a central orchestrator.

## Architecture

```
User Query
    │
    ▼
┌──────────────┐
│ Orchestrator │ ← Coordinates the full pipeline
└──────┬───────┘
       │
       ├──→ LLM (Ollama) analyzes the query
       │         → Decides which API endpoint to call
       │
       ├──→ Data Agent fetches from external API
       │         → Handles errors, timeouts, validation
       │
       ├──→ LLM Agent generates a response
       │         → Converts raw JSON into readable text
       │
       └──→ Delivery Agent sends via Telegram
                 → Bot API with markdown formatting
```

## How it works

1. **Query Analysis** — The orchestrator sends the user's natural language query to a local LLM (Qwen 3 8B via Ollama). The LLM decides which API endpoint to call and extracts any relevant parameters (e.g., a character name).

2. **Data Fetching** — The Data Agent calls the selected API endpoint, handles errors and timeouts, and returns the raw JSON data.

3. **Response Generation** — The LLM Agent receives the raw data plus the original query and generates a well-formatted, context-aware response.

4. **Delivery** — The Delivery Agent sends the final response to the user via the Telegram Bot API.

Each agent is independent and can be extended or replaced without affecting the others.

## Tech Stack

- **Python 3.10+**
- **Ollama** — local LLM inference (Qwen 3 8B)
- **Telegram Bot API** — message delivery
- **python-dotenv** — environment variable management
- **Logging** — structured logging throughout the pipeline

## Setup

### Prerequisites

- [Ollama](https://ollama.ai) installed and running
- A Telegram bot token (get one from [@BotFather](https://t.me/botfather))

### Installation

```bash
# Clone the repo
git clone https://github.com/KAMZ226L/multi-agent-llm-orchestrator.git
cd multi-agent-llm-orchestrator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Pull the LLM model
ollama pull qwen3:8b

# Configure environment variables
cp .env.example .env
# Edit .env with your Telegram credentials
```

### Run

```bash
python main.py
```

## Project Structure

```
multi-agent-llm-orchestrator/
├── main.py                  # Entry point (interactive CLI)
├── orchestrator.py          # Pipeline coordinator
├── config.py                # Environment & API configuration
├── agents/
│   ├── data_agent.py        # Fetches data from external APIs
│   ├── llm_agent.py         # Generates responses using Ollama
│   └── delivery_agent.py    # Sends messages via Telegram
├── .env.example             # Template for environment variables
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
```

## Extending

The system is designed to be easily extensible:

- **Add a new API**: Add endpoints in `config.py` and update the system prompt in `orchestrator.py`
- **Swap the LLM**: Change `OLLAMA_MODEL` in your `.env` to any Ollama-supported model
- **Add a delivery channel**: Create a new agent in `agents/` following the same interface
- **Switch to a remote LLM**: Modify `llm_agent.py` to call OpenAI, Anthropic, or any other provider

## License

MIT
