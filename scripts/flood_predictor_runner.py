#!/usr/bin/env python3
"""
🌊 OpenFloodAI — Automated Flood Forecast Runner (v2)
----------------------------------------------------
This script generates daily regional flood probability forecasts and saves them
to data/outputs/all_forecasts.json for the dashboard.

It uses blended ensemble logic combining:
- Seasonal indicators (ENSO, PDO, etc.)
- Atmospheric river (AR) category
- Hydrologic load factors
- Coastal and IVT multipliers

By default, it runs with simulated data but can easily be extended to real feeds.
"""

import os
import json
import random
from datetime import datetime

# ---------------------------------------------------------------------------
# Simulated Region Data (You can expand these or connect to real feeds)
# ---------------------------------------------------------------------------

REGIONS = {
    "Sacramento Basin": {"lat": 38.58, "lon": -121.49},
    "Ohio Valley": {"lat": 38.0, "lon": -84.5},
    "Mississippi Tributaries": {"lat": 34.7, "lon": -90.2},
    "Pacific Northwest": {"lat": 45.5, "lon": -122.6},
    "Gulf Coast": {"lat": 29.9, "lon": -90.1},
    "Northeast Corridor": {"lat": 40.7, "lon": -74.0},
    "Central Plains": {"lat": 39.1, "lon": -96.6},
    "Florida Peninsula": {"lat": 27.9, "lon": -82.5}
}

# ---------------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------------

def clamp(value, minv=0, maxv=1):
    return max(min(value, maxv), minv)

def blended_flood_probability(region_name):
    """
    Generate a blended flood probability for a given region.
    This uses pseudo-random logic mimicking an ensemble forecast.
    """
    # Core factors (these could be replaced with real hydrologic data)
    ENSO_bias = random.uniform(-0.5, 0.8)
    PDO_pos = random.choice([True, False])
    AR_cat = random.randint(1, 5)
    hydrologic_load = random.choice(["LOW", "MODERATE", "HIGH"])
    IVT = random.uniform(200, 900)  # Integrated Vapor Transport
    IVT_90pct = 750
    radar_24h_accum = random.uniform(0, 150)  # mm
    R24_thresh = 100
    tide_height = random.uniform(0.2, 2.0)
    tide_thresh = 1.5

    # Seasonal tilt
    seasonal_tilt = 0.0
    if ENSO_bias >= 0.4 and PDO_pos and AR_cat >= 3 and hydrologic_load == "HIGH":
        seasonal_tilt += 0.15

    # Coastal multiplier
    coastal_multiplier = 1.4 if (IVT > IVT_90pct and radar_24h_accum > R24_thresh and tide_height > tide_thresh) else 1.0

    # Base ensemble probability
    ensemble_prob = random.uniform(0.15, 0.75)

    # Final probability
    P_final = clamp(ensemble_prob * (1 + seasonal_tilt) * coastal_multiplier)

    # Tier mapping
    if P_final >= 0.60:
        tier = "RED"
    elif P_final >= 0.30:
        tier = "AMBER"
    else:
        tier = "GREEN"

    return {
        "P_final": round(P_final, 2),
        "tier": tier
    }

# ---------------------------------------------------------------------------
# Main Forecast Generation
# ---------------------------------------------------------------------------

def main():
    print("🌊 Running OpenFloodAI forecast runner...")
    results = {}

    for region, coords in REGIONS.items():
        values = blended_flood_probability(region)
        results[region] = {
            **values,
            "lat": coords["lat"],
            "lon": coords["lon"]
        }
        print(f"✅ {region}: {values['tier']} ({values['P_final']})")

    # Output directory
    output_dir = os.path.join("data", "outputs")
    os.makedirs(output_dir, exist_ok=True)

    # Save JSON
    output_path = os.path.join(output_dir, "all_forecasts.json")
    output_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "forecasts": results
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    print(f"\n📁 Saved forecast results → {output_path}")
    print("🏁 Forecast run complete.\n")

# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()
