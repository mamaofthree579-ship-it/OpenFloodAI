"""
OpenFloodAI — Forecast Runner
This script simulates multi-region daily forecasts.
"""

import json
from datetime import datetime
from flood_predictor_v2_blended import blended_flood_probability

# --- Define sample region inputs (would be loaded from data/regions in production) ---
regions = {
    "Sacramento": {
        "ENSO_bias": 0.5, "PDO_pos": True, "AR_cat": 3,
        "hydrologic_load": "HIGH", "IVT": 1200, "IVT_90pct": 1000,
        "radar_24h_accum": 30, "R24_thresh": 25,
        "tide_height": 1.8, "tide_thresh": 1.5,
        "ensemble_prob": 0.4, "seasonal_tilt": 0.1
    },
    "Ohio_Valley": {
        "ENSO_bias": 0.2, "PDO_pos": False, "AR_cat": 2,
        "hydrologic_load": "NORMAL", "IVT": 800, "IVT_90pct": 950,
        "radar_24h_accum": 20, "R24_thresh": 25,
        "tide_height": 0.0, "tide_thresh": 0.0,
        "ensemble_prob": 0.25, "seasonal_tilt": 0.05
    },
    "Mississippi": {
        "ENSO_bias": 0.35, "PDO_pos": True, "AR_cat": 3,
        "hydrologic_load": "HIGH", "IVT": 950, "IVT_90pct": 900,
        "radar_24h_accum": 40, "R24_thresh": 20,
        "tide_height": 0.5, "tide_thresh": 1.0,
        "ensemble_prob": 0.5, "seasonal_tilt": 0.08
    }
}

# --- Run forecasts ---
outputs = {}
for name, params in regions.items():
    outputs[name] = blended_flood_probability(params)

# --- Save results ---
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
data = {
    "timestamp": timestamp,
    "forecasts": outputs
}

output_path = "data/outputs/all_forecasts.json"
import os
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w") as f:
    json.dump(data, f, indent=2)

print(f"✅ Forecasts generated at {timestamp}")
for region, result in outputs.items():
    print(f"{region}: {result['tier']} (P={result['P_final']})")
