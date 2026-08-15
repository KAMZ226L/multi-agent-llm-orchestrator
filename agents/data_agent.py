"""
Data Agent.

Responsible for fetching data from external APIs.
Handles timeouts, HTTP errors, and malformed responses.
"""

import logging
from typing import Optional, Union

import requests

logger = logging.getLogger(__name__)


class DataAgent:
    """Fetches and validates data from external REST APIs."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def fetch(self, url: str) -> Optional[Union[dict, list]]:
        """
        Fetches JSON data from the given URL.

        Args:
            url: The API endpoint to query.

        Returns:
            Parsed JSON as dict or list, or None if the request fails.
        """
        logger.info("Fetching data from: %s", url)

        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()

            if not data:
                logger.warning("API returned empty data")
                return None

            record_count = len(data) if isinstance(data, list) else 1
            logger.info("Received %d record(s)", record_count)
            return data

        except requests.Timeout:
            logger.error("Request timed out after %ds", self.timeout)
            return None
        except requests.HTTPError as e:
            logger.error("HTTP error: %s", e)
            return None
        except requests.RequestException as e:
            logger.error("Request failed: %s", e)
            return None
        except ValueError:
            logger.error("Response is not valid JSON")
            return None