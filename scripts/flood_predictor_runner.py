#!/#!/usr/bin/env python3
"""
OpenFloodAI — Automated Flood Forecast Runner (Multi-Region v3)
---------------------------------------------------------------
Generates a hierarchical JSON structure:
{
  "timestamp": "...",
  "forecasts": {
    "USA": {
      "Florida": {"P_final": 0.82, "tier": "RED"},
      "Texas": {"P_final": 0.44, "tier": "AMBER"}
    },
    "India": {
      "Kerala": {"P_final": 0.73, "tier": "RED"}
    }
  }
}
"""

import json
import os
import random
from datetime import datetime
from pathlib import Path

# Try to import the probability model
try:
    from scripts.flood_predictor_v2_blended import blended_flood_probability
except ImportError:
    # Fallback (for local / GitHub Action runs)
    from flood_predictor_v2_blended import blended_flood_probability


# ----------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------
OUTPUT_DIR = Path("data/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Define monitored countries and regions
REGIONS = {
    "USA": ["Florida", "Texas", "California", "Maine"],
    "India": ["Kerala", "Gujarat", "Assam"],
    "UK": ["London", "Manchester", "Liverpool"],
    "Australia": ["Queensland", "Victoria", "New South Wales"]
}

# Probability → Tier mapping
def tier_from_prob(p):
    if p >= 0.6:
        return "RED"
    elif p >= 0.3:
        return "AMBER"
    else:
        return "GREEN"


# ----------------------------------------------------------
# MAIN FORECAST LOGIC
# ----------------------------------------------------------
def generate_forecast_for_region(country: str, region: str):
    """
    Generate a synthetic forecast entry.
    Replace randoms with real sensor data when available.
    """
    # Example synthetic parameters
    ensemble_prob = random.uniform(0.05, 0.95)
    enso_bias = random.uniform(-1.0, 1.0)
    pdo_pos = random.choice([True, False])
    ar_cat = random.randint(1, 5)
    hydrologic_load = random.choice(["LOW", "MEDIUM", "HIGH"])
    ivt = random.uniform(100, 500)
    radar_24h_accum = random.uniform(0, 200)
    tide_height = random.uniform(0, 2.5)

    # Compute blended probability
    p_final = blended_flood_probability(
        ensemble_prob=ensemble_prob,
        ENSO_bias=enso_bias,
        PDO_pos=pdo_pos,
        AR_cat=ar_cat,
        hydrologic_load=hydrologic_load,
        IVT=ivt,
        radar_24h_accum=radar_24h_accum,
        tide_height=tide_height
    )

    return {
        "P_final": round(p_final, 3),
        "tier": tier_from_prob(p_final)
    }


def main():
    print("🌊 Running multi-region forecast generator...")

    all_forecasts = {}
    for country, subregions in REGIONS.items():
        all_forecasts[country] = {}
        for region in subregions:
            all_forecasts[country][region] = generate_forecast_for_region(country, region)

    result = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "forecasts": all_forecasts
    }

    output_path = OUTPUT_DIR / "all_forecasts.json"
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"✅ Forecast updated: {output_path}")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
