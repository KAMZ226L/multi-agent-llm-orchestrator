"""
Configuration module.

Loads settings from environment variables with sensible defaults.
Sensitive values (API tokens) are never hardcoded — use a .env file.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Ollama (local LLM)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/chat")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# API Endpoints
API_BASE = "https://api.api-onepiece.com/v2"

ENDPOINTS = {
    "characters_all": f"{API_BASE}/characters/en",
    "character_search": f"{API_BASE}/characters/en/search?name={{name}}",
    "fruits": f"{API_BASE}/fruits/en",
    "sagas": f"{API_BASE}/sagas/en",
    "crews": f"{API_BASE}/crews/en",
}