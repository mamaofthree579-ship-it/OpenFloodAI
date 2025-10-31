#!/usr/bin/env python3
"""
split_forecast_files.py - Split all_forecasts.json into per-region files.
Intended for backfill compatibility with older OpenFloodAI outputs.
"""
import json
from pathlib import Path

def main():
    base = Path(__file__).resolve().parents[1]
    all_path = base / "data" / "outputs" / "all_forecasts.json"
    if not all_path.exists():
        print("❌ No all_forecasts.json found.")
        return

    with open(all_path, "r") as f:
        data = json.load(f)

    if "forecasts" not in data:
        print("⚠️ Invalid format: missing 'forecasts' key.")
        return

    out_dir = base / "data" / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)

    for region, content in data["forecasts"].items():
        fname = f"forecast_{region.lower().replace(' ','_')}.json"
        region_data = {
            "region": region,
            "generated_utc": data.get("timestamp"),
            **content
        }
        with open(out_dir / fname, "w") as f:
            json.dump(region_data, f, indent=2)
        print(f"✅ Created {fname}")

    print("🎯 Split complete. All regions written to data/outputs/")

if __name__ == "__main__":
    main()
