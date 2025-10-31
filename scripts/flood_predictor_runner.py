#!/usr/bin/env python3
"""
flood_predictor_runner.py - Main daily forecast runner for OpenFloodAI
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# --- Fix import path for GitHub Actions and local runs ---
BASE = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE / "scripts"))

# ✅ Correct import (no "scripts." prefix)
from flood_predictor_v2_blended import blended_flood_probability
from datetime import datetime
from pathlib import Path

# Import the model function
from scripts.flood_predictor_v2_blended import blended_flood_probability

# --- Paths ---
BASE = Path(__file__).resolve().parents[1]
CONFIG_PATH = BASE / "config" / "region_parameters.json"
LIVE_INPUT_PATH = BASE / "data" / "inputs" / "live_conditions.json"
OUTPUT_DIR = BASE / "data" / "outputs"

# --- Helpers ---
def load_json(path, fallback=None):
    """Load a JSON file safely."""
    if not path.exists():
        print(f"⚠️  Missing file: {path}")
        return fallback or {}
    with open(path, "r") as f:
        return json.load(f)

def save_json(data, path):
    """Save a dictionary to JSON with indentation."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def timestamp_utc():
    """Return current UTC timestamp string."""
    return datetime.utcnow().isoformat() + "Z"

# --- Main execution ---
def main():
    print("🌊 Running OpenFloodAI forecast runner...")

    # Load static configuration
    regions = load_json(CONFIG_PATH, fallback={})
    if not regions:
        print("❌ No region configuration found. Exiting.")
        return

    # Load live conditions
    live_data = load_json(LIVE_INPUT_PATH, fallback={}).get("regions", {})

    # Prepare output container
    all_forecasts = {
        "timestamp": timestamp_utc(),
        "forecasts": {}
    }

    for region_name, params in regions.items():
        print(f"📍 Processing region: {region_name}")

        # Pull live conditions if available
        live = live_data.get(region_name, {})
        inputs = {
            "ENSO_bias": params.get("ENSO_bias", 0.0),
            "PDO_pos": params.get("PDO_pos", False),
            "AR_cat": params.get("AR_cat", 1),
            "hydrologic_load": params.get("hydrologic_load", "MEDIUM"),
            "IVT": params.get("IVT", 0),
            "IVT_90pct": params.get("IVT_90pct", 0),
            "radar_24h_accum": params.get("radar_24h_accum", 0),
            "R24_thresh": params.get("R24_thresh", 0),
            "tide_height": params.get("tide_height", 0),
            "tide_thresh": params.get("tide_thresh", 0),
            # Live updates (optional)
            "smi": live.get("smi", params.get("default_smi", 0.3)),
            "rainfall_lag_48h": live.get("rainfall_lag_48h", 0.0)
        }

        # Run the forecast model
        blended, parametric = blended_flood_probability(inputs)

        # Store outputs
        region_output = {
            "P_final": round(blended["P_final"], 3),
            "tier": blended["tier"],
            "parametric_prob": round(parametric["P_final"], 3),
            "parametric_tier": parametric["tier"],
            "inputs_used": inputs
        }

        all_forecasts["forecasts"][region_name] = region_output

        # Save per-region forecast
        region_fname = f"forecast_{region_name.lower().replace(' ', '_')}.json"
        region_path = OUTPUT_DIR / region_fname
        save_json(region_output, region_path)
        print(f"✅ Saved forecast for {region_name} → {region_fname}")

    # Save the combined forecast
    all_path = OUTPUT_DIR / "all_forecasts.json"
    save_json(all_forecasts, all_path)
    print(f"🌐 Combined forecasts written to {all_path}")
    print("🏁 Forecast run complete.")

if __name__ == "__main__":
    main()
