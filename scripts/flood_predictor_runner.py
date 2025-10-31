#!/usr/bin/env python3
"""
Updated runner for v1.0.1 - loads region parameters and computes forecasts with SMI & lag.
Writes per-region JSONs and combined all_forecasts.json
"""
import json, os
from datetime import datetime
from pathlib import Path
from scripts.flood_predictor_v2_blended import blended_flood_probability

BASE = Path(__file__).resolve().parents[0]
REGION_CFG = BASE.parent / "config" / "region_parameters.json"

def load_region_config():
    if not REGION_CFG.exists():
        return {}
    return json.loads(REGION_CFG.read_text())

def main():
    regions = load_region_config()
    out_dir = BASE.parent / "data" / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    all_forecasts = {"timestamp": datetime.utcnow().isoformat() + "Z", "forecasts": {}}

    for region_name, params in regions.items():
        # Example inputs - in production these should come from live data sources
        inputs = {
            "ENSO_bias": params.get("ENSO_bias", 0.4),
            "PDO_pos": params.get("PDO_pos", True),
            "AR_cat": params.get("AR_cat", 3),
            "hydrologic_load": params.get("hydrologic_load", "HIGH"),
            "IVT": params.get("IVT_90pct", params.get("IVT_90pct", 850)),
            "IVT_90pct": params.get("IVT_90pct", 850),
            "radar_24h_accum": params.get("radar_24h_accum", 0),
            "R24_thresh": params.get("R24_thresh", 75),
            "tide_height": params.get("tide_height", 0),
            "tide_thresh": params.get("tide_thresh", 0),
            "ensemble_prob": params.get("base_ensemble_prob", 0.35),
            "seasonal_tilt": params.get("seasonal_tilt", 0.0),
            "smi": params.get("default_smi", 0.3),
            "rainfall_lag_48h": params.get("default_rain_lag_mm", 0.0)
        }
        res = blended_flood_probability(inputs, params)
        # write per-region file
        fname = f"forecast_{region_name.lower().replace(' ','_')}.json"
        with open(out_dir / fname, "w") as f:
            json.dump({"region": region_name, "generated_utc": all_forecasts["timestamp"], **res}, f, indent=2)
        all_forecasts["forecasts"][region_name] = res
        print("Wrote", fname)

    with open(out_dir / "all_forecasts.json", "w") as f:
        json.dump(all_forecasts, f, indent=2)
    print("All forecasts written to", out_dir / "all_forecasts.json")

if __name__ == "__main__":
    main()
