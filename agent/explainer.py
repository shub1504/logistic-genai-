# agent/explainer.py

import requests
from agent.prompts import ROUTE_EXPLAINER_PROMPT, ROUTE_SUMMARY_PROMPT


CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"


def _call_claude(prompt: str, api_key: str, max_tokens: int = 300) -> str:
    headers = {
        "x-api-key":         api_key,
        "anthropic-version": "2023-06-01",
        "content-type":      "application/json",
    }
    payload = {
        "model":      "claude-sonnet-4-20250514",
        "max_tokens": max_tokens,
        "messages":   [{"role": "user", "content": prompt}],
    }
    try:
        response = requests.post(
            CLAUDE_API_URL, headers=headers, json=payload
        )
        response.raise_for_status()
        return response.json()["content"][0]["text"].strip()
    except Exception as e:
        print(f"[Explainer] API error: {e}")
        return "Route explanation unavailable."


def explain_route(
    route: list[str],
    total_distance: float,
    api_key: str
) -> str:
    """Generate a friendly driver briefing for a given route."""
    prompt = ROUTE_EXPLAINER_PROMPT.format(
        route=          " → ".join(route),
        total_distance= round(total_distance, 1),
        num_stops=      len(route) - 2,
    )
    return _call_claude(prompt, api_key)


def summarize_route(
    route: list[str],
    total_distance: float,
    algorithm: str,
    api_key: str
) -> str:
    """Generate a concise operational summary for a manager dashboard."""
    prompt = ROUTE_SUMMARY_PROMPT.format(
        route=          " → ".join(route),
        total_distance= round(total_distance, 1),
        algorithm=      algorithm,
        num_stops=      len(route) - 2,
    )
    return _call_claude(prompt, api_key, max_tokens=200)