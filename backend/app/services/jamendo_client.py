import logging
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

JAMENDO_CLIENT_ID = os.getenv("JAMENDO_CLIENT_ID")
BASE_URL = "https://api.jamendo.com/v3.0/"

logger = logging.getLogger(__name__)

if JAMENDO_CLIENT_ID:
    logger.info("Jamendo Client ID loaded successfully for client.")
else:
    logger.error("Jamendo Client ID is not set for client.")

class JamendoClient:
    def __init__(self, client_id: str):
        if not client_id:
            raise ValueError("Jamendo client ID is required.")
        self.client_id = client_id

    def search_tracks(self, query: str, limit: int = 20):
        endpoint = "tracks/"
        params = {
            "client_id": self.client_id,
            "format": "json",
            "namesearch": query,
            "limit": limit,
            "order": "popularity_total",
        }
        
        logger.info(f"Searching Jamendo with query: {query}")
        logger.info(f"Request params: {params}")

        try:
            response = requests.get(f"{BASE_URL}{endpoint}", params=params)
            logger.info(f"Jamendo API response status code: {response.status_code}")
            response.raise_for_status()

            try:
                data = response.json()
                logger.info("Successfully decoded JSON from Jamendo API response.")
                # logger.debug(f"Jamendo API response data: {data}")
            except json.JSONDecodeError:
                logger.error("Failed to decode JSON from Jamendo API response.")
                logger.error(f"Response text: {response.text}")
                return None, "Failed to decode response from Jamendo API."

            if data.get("headers", {}).get("status") == "success":
                return data.get("results", []), None
            else:
                error_message = data.get("headers", {}).get("error_message", "Unknown error")
                logger.error(f"Jamendo API error: {error_message}")
                return None, f"Jamendo API error: {error_message}"

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to Jamendo API: {e}")
            return None, f"Failed to connect to Jamendo API: {e}"

jamendo_client = JamendoClient(client_id=JAMENDO_CLIENT_ID)
