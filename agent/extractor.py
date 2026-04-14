# agent/extractor.py

import json
import re
import requests
from agent.prompts import LOCATION_EXTRACTOR_PROMPT


CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"


def extract_locations(user_message: str, api_key: str) -> list[str]:
    """
    Use Claude to extract delivery locations from a natural language message.
    Returns list of location strings.
    """
    if not api_key or api_key == "your_real_anthropic_key_here":
        # Fallback: simple keyword extraction without AI
        keywords = ["Saket", "Rohini", "Dwarka", "Connaught", "Lajpat"]
        return [
            k + ", New Delhi"
            for k in keywords
            if k.lower() in user_message.lower()
        ]

    prompt = LOCATION_EXTRACTOR_PROMPT.format(user_message=user_message)

    headers = {
        "x-api-key":         api_key,
        "anthropic-version": "2023-06-01",
        "content-type":      "application/json",
    }
    payload = {
        "model":    "claude-sonnet-4-20250514",
        "max_tokens": 512,
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        response = requests.post(
            CLAUDE_API_URL, headers=headers, json=payload
        )
        response.raise_for_status()
        raw = response.json()["content"][0]["text"].strip()
        raw = re.sub(r"```(?:json)?", "", raw).strip().strip("`")
        locations = json.loads(raw)
        if isinstance(locations, list):
            return locations
    except Exception as e:
        print(f"[Extractor] Error: {e}")

    return []