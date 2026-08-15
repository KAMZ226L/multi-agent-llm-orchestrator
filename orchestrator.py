"""
Orchestrator module.

Coordinates the multi-agent pipeline:
1. LLM analyzes the user query and decides which API endpoint to call
2. Data agent fetches the data from the external API
3. LLM agent generates a human-readable response
4. Delivery agent sends the response via Telegram
"""

import json
import logging
from typing import Optional

from agents.data_agent import DataAgent
from agents.llm_agent import LLMAgent
from agents.delivery_agent import DeliveryAgent
from config import ENDPOINTS, OLLAMA_URL, OLLAMA_MODEL

import requests

logger = logging.getLogger(__name__)


class Orchestrator:
    """Coordinates the flow between agents to process user queries."""

    def __init__(self):
        self.data_agent = DataAgent()
        self.llm_agent = LLMAgent()
        self.delivery_agent = DeliveryAgent()

    def analyze_query(self, query: str) -> Optional[dict]:
        """Uses the LLM to interpret the user query and decide which endpoint to call."""
        logger.info("Analyzing query: '%s'", query)

        available_endpoints = ", ".join(ENDPOINTS.keys())

        payload = {
            "model": OLLAMA_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": f"""You are a query analyzer for the One Piece API.
                    Available endpoint types: {available_endpoints}.
                    Analyze the user message and return ONLY a JSON object:
                    {{"type": "<endpoint_type>", "name": "character name if applicable, otherwise null"}}
                    Do not write anything else, only the JSON."""
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            "stream": False
        }

        try:
            response = requests.post(OLLAMA_URL, json=payload, timeout=30)
            response.raise_for_status()

            text = response.json()["message"]["content"]
            text = text.strip().replace("```json", "").replace("```", "").strip()

            result = json.loads(text)
            logger.info("Query analyzed — endpoint: %s, name: %s", result.get("type"), result.get("name"))
            return result

        except requests.RequestException as e:
            logger.error("Failed to connect to Ollama: %s", e)
            return None
        except (json.JSONDecodeError, KeyError) as e:
            logger.error("Failed to parse LLM response: %s", e)
            return None

    def build_url(self, analysis: dict) -> str:
        """Builds the correct API URL based on the LLM analysis."""
        endpoint_type = analysis.get("type", "characters_all")
        name = analysis.get("name")

        if endpoint_type == "character_search" and name:
            return ENDPOINTS["character_search"].format(name=name)

        return ENDPOINTS.get(endpoint_type, ENDPOINTS["characters_all"])

    def run(self, query: str) -> None:
        """Executes the full orchestration pipeline."""
        logger.info("Starting pipeline")

        # Step 1: Analyze query
        analysis = self.analyze_query(query)
        if not analysis:
            print("Could not understand the query. Please try again.")
            return

        # Step 2: Fetch data
        url = self.build_url(analysis)
        logger.info("Built URL: %s", url)

        data = self.data_agent.fetch(url)
        if not data:
            print("No data found for that query.")
            return

        # Step 3: Generate response
        message = self.llm_agent.generate(data, query)
        if not message:
            print("Could not generate a response.")
            return

        print(f"\n{message}")

        # Step 4: Deliver via Telegram
        self.delivery_agent.send(message)

        logger.info("Pipeline completed")