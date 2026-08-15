"""
Delivery Agent.

Responsible for sending generated messages to end users via Telegram.
Credentials are loaded from environment variables — never hardcoded.
"""

import logging
from typing import Optional

import requests

from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)

TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"


class DeliveryAgent:
    """Delivers messages to users via the Telegram Bot API."""

    def __init__(self):
        if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
            logger.warning(
                "Telegram credentials not configured. "
                "Set TELEGRAM_TOKEN and TELEGRAM_CHAT_ID in your .env file."
            )

    def send(self, message: str) -> bool:
        """
        Sends a message via Telegram.

        Args:
            message: The text to send.

        Returns:
            True if sent successfully, False otherwise.
        """
        if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
            logger.warning("Skipping Telegram delivery — credentials not set")
            return False

        logger.info("Sending message via Telegram")

        url = TELEGRAM_API.format(token=TELEGRAM_TOKEN)
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Message delivered successfully")
            return True

        except requests.RequestException as e:
            logger.error("Telegram delivery failed: %s", e)
            return False