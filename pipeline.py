# pipeline.py

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import ANTHROPIC_KEY, USE_MOCK
from agent.extractor      import extract_locations
from agent.explainer       import explain_route, summarize_route
from services.mock_data    import get_mock_locations, get_mock_matrix
from services.bigquery_logger import log_route
from algorithms.nearest_neighbour import (
    nearest_neighbor_route,
    two_opt_improve,
)


def run_pipeline(user_message: str) -> dict:
    """
    Full end-to-end logistics pipeline.

    1. Extract locations from user message using Claude
    2. Build distance matrix (mock or live Google Maps)
    3. Optimize route using Nearest Neighbor + 2-opt
    4. Generate driver briefing using Claude
    5. Log result to BigQuery
    6. Return full result dict

    Args:
        user_message: plain English e.g.
                      "deliver to Saket, Rohini and Dwarka today"

    Returns:
        {
            "route":          [...],
            "total_distance": float,
            "briefing":       str,
            "summary":        str,
            "logged":         bool,
        }
    """

    print(f"\n[Pipeline] Starting for: '{user_message}'")

    # ── Step 1: Extract locations ─────────────────────────────────
    print("[Pipeline] Step 1 — Extracting locations...")
    extracted = extract_locations(user_message, ANTHROPIC_KEY)
    print(f"[Pipeline] Extracted: {extracted}")

    # ── Step 2: Build distance matrix ────────────────────────────
    print("[Pipeline] Step 2 — Building distance matrix...")
    mock_locs   = get_mock_locations()
    mock_matrix = get_mock_matrix()
    all_labels  = [l["address"] for l in mock_locs]

    # Match extracted locations to mock data keys
    matched = []
    for loc in extracted:
        for key in all_labels:
            if any(
                word.lower() in key.lower()
                for word in loc.split()
                if len(word) > 3
            ):
                if key not in matched:
                    matched.append(key)
                break

    # Fall back to all mock locations if none matched
    if len(matched) < 2:
        print("[Pipeline] Not enough matches — using all mock locations")
        matched = all_labels

    print(f"[Pipeline] Matched stops: {matched}")

    # ── Step 3: Optimize route ────────────────────────────────────
    print("[Pipeline] Step 3 — Optimizing route...")
    route, _    = nearest_neighbor_route(mock_matrix, matched[0], matched)
    best, km    = two_opt_improve(route, mock_matrix)
    print(f"[Pipeline] Optimized: {best}")
    print(f"[Pipeline] Distance:  {round(km, 1)} km")

    # ── Step 4: Generate AI explanations ─────────────────────────
    print("[Pipeline] Step 4 — Generating AI briefing...")
    briefing = summary = ""
    if ANTHROPIC_KEY and ANTHROPIC_KEY != "your_real_anthropic_key_here":
        try:
            briefing = explain_route(best, km, ANTHROPIC_KEY)
            summary  = summarize_route(
                best, km, "Nearest Neighbor + 2-opt", ANTHROPIC_KEY
            )
        except Exception as e:
            print(f"[Pipeline] AI explanation failed: {e}")
            briefing = f"Route: {' → '.join(best)}. Total: {round(km,1)} km."
            summary  = briefing
    else:
        briefing = f"Route: {' → '.join(best)}. Total: {round(km,1)} km."
        summary  = briefing

    # ── Step 5: Log to BigQuery ───────────────────────────────────
    print("[Pipeline] Step 5 — Logging to BigQuery...")
    logged = False
    try:
        logged = log_route(
            route=          best,
            total_distance= km,
            algorithm=      "Nearest Neighbor + 2-opt",
            user_message=   user_message,
            briefing=       briefing,
        )
    except Exception as e:
        print(f"[Pipeline] BigQuery logging failed: {e}")

    # ── Return full result ────────────────────────────────────────
    result = {
        "route":           best,
        "route_readable":  " → ".join([s.split(",")[0] for s in best]),
        "total_distance":  round(km, 1),
        "num_stops":       len(best) - 2,
        "briefing":        briefing,
        "summary":         summary,
        "logged":          logged,
        "user_message":    user_message,
    }

    print(f"[Pipeline] Done! {result['route_readable']} — {result['total_distance']} km")
    return result