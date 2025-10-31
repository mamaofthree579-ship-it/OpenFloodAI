#!/usr/bin/env python3
"""
flood_predictor_runner.py
------------------------------------
Runs the blended flood forecast model for multiple regions
and exports results to JSON for the dashboard.
"""

import json
from datetime import datetime
from pathlib import Path
from flood_predictor_v2_blended import blended_flood_probability
from live_data_ingestor import fetch_live_data

# --- Output path setup ---
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "all_forecasts.json"

# --- Define target regions ---
REGIONS = {
    "Pacific Northwest": {"lat": 47.6, "lon": -122.3},
    "California Coast": {"lat": 36.8, "lon": -121.9},
    "Midwest": {"lat": 41.9, "lon": -87.6},
    "Gulf States": {"lat": 29.9, "lon": -90.1},
    "Northeast": {"lat": 42.4, "lon": -71.1}
}

def run_forecast():
    all_results = {}
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    print("🌍 Running OpenFloodAI blended flood forecast...\n")

    for region, coords in REGIONS.items():
        print(f"→ Fetching data for {region}...")

        # Live data ingestion (mocked with random if offline)
        live = fetch_live_data(coords["lat"], coords["lon"])

        inputs = {
            "ENSO_bias": live.get("ENSO_bias", 0.2),
            "PDO_pos": live.get("PDO_pos", True),
            "AR_cat": live.get("AR_cat", 2),
            "hydrologic_load": live.get("hydrologic_load", "MEDIUM"),
            "IVT": live.get("IVT", 400),
            "IVT_90pct": live.get("IVT_90pct", 500),
            "radar_24h_accum": live.get("radar_24h_accum", 30),
            "R24_thresh": live.get("R24_thresh", 25),
            "tide_height": live.get("tide_height", 1.2),
            "tide_thresh": live.get("tide_thresh", 1.5),
            "smi": live.get("smi", 0.4),
            "rainfall_lag_24h": live.get("rainfall_lag_24h", 15.0)
        }

        blended, parametric = blended_flood_probability(inputs)

        all_results[region] = {
            "inputs": inputs,
            "blended": blended,
            "parametric": parametric
        }

        print(f"   ✅ {region} — {blended['tier']} ({blended['P_final']:.2f})")

    # Save outputs
    result_payload = {
        "timestamp": timestamp,
        "forecasts": {
            region: data["blended"] for region, data in all_results.items()
        }
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(result_payload, f, indent=2)

    print(f"\n📦 Forecasts saved to: {OUTPUT_FILE}")
    print(f"🕒 Timestamp: {timestamp}\n")

if __name__ == "__main__":
    run_forecast()
