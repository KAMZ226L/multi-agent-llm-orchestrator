"""
LLM Agent.

Responsible for generating human-readable responses from raw API data
using a local LLM served by Ollama.
"""

import json
import logging
from typing import Optional, Union

import requests

from config import OLLAMA_URL, OLLAMA_MODEL

logger = logging.getLogger(__name__)

MAX_ITEMS = 5  # Limit list data to avoid exceeding context window


class LLMAgent:
    """Generates natural language responses from structured data using a local LLM."""

    def generate(self, data: Union[dict, list], original_query: str) -> Optional[str]:
        """
        Sends raw API data to the LLM and returns a formatted response.

        Args:
            data: The raw data from the API (dict or list).
            original_query: The user's original question for context.

        Returns:
            A human-readable message string, or None on failure.
        """
        logger.info("Generating response with LLM")

        # Truncate large lists to stay within context limits
        if isinstance(data, list) and len(data) > MAX_ITEMS:
            logger.info("Truncating data from %d to %d items", len(data), MAX_ITEMS)
            data = data[:MAX_ITEMS]

        payload = {
            "model": OLLAMA_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an expert assistant on One Piece. "
                        "You receive JSON data and the user's original question. "
                        "Generate a clear, well-structured, and engaging response. "
                        "Use markdown formatting for readability."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Original question: '{original_query}'\n"
                        f"Data: {json.dumps(data, ensure_ascii=False)}"
                    )
                }
            ],
            "stream": False
        }

        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=60)
            response.raise_for_status()

            message = response.json()["message"]["content"]
            logger.info("Response generated (%d chars)", len(message))
            return message

        except requests.Timeout:
            logger.error("LLM request timed out")
            return None
        except requests.RequestException as e:
            logger.error("Failed to connect to Ollama: %s", e)
            return None
        except (KeyError, ValueError) as e:
            logger.error("Failed to parse LLM response: %s", e)
            return None