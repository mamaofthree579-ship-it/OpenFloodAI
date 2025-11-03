import os
import json
from datetime import datetime, timezone
from live_data_ingestor import get_live_environmental_data
from flood_predictor_v2_blended import blended_flood_probability

# 🌍 Define your country and region structure here
REGION_MAP = {
    "USA": ["Texas", "California", "Florida", "Louisiana"],
    "UK": ["England", "Scotland", "Wales"],
    "India": ["Delhi", "Mumbai", "Chennai", "Kolkata"],
    "Bangladesh": ["Dhaka", "Chittagong", "Khulna"],
    "Philippines": ["Manila", "Cebu", "Davao"],
    "Brazil": ["Amazonas", "Rio de Janeiro", "São Paulo"],
    "Nigeria": ["Lagos", "Abuja", "Kano"],
    "Australia": ["Queensland", "New South Wales", "Victoria"],
}

OUTPUT_DIR = "data/outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "all_forecasts.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_forecasts():
    forecasts = {}
    for country, regions in REGION_MAP.items():
        forecasts[country] = {}
        for region in regions:
            env_data = get_live_environmental_data(region)
            result = blended_flood_probability(env_data, region)
            forecasts[country][region] = result
    return forecasts

def main():
    print("🌊 Running OpenFloodAI forecast update...")

    forecasts = generate_forecasts()

    # Always update timestamp — even if no changes
    output = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "forecasts": forecasts
    }

    # Load old file to detect data changes
    old_data = None
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r") as f:
            try:
                old_data = json.load(f)
            except Exception:
                old_data = None

    # Save updated file (always refresh timestamp)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    # Compare to detect change
    if old_data and old_data.get("forecasts") == forecasts:
        print("✅ Forecasts unchanged — only timestamp updated.")
    else:
        print("✅ Forecasts updated successfully.")

    print(f"📁 Output saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
