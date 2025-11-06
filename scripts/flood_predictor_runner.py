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

# ✅ Flood tiers by probability threshold
def classify_tier(prob):
    if prob >= 0.6:
        return "RED"
    elif prob >= 0.3:
        return "AMBER"
    else:
        return "GREEN"

# ✅ Generate mock forecasts
def generate_forecast():
    data = {"forecasts": {}, "timestamp": datetime.utcnow().isoformat() + "Z"}  # ✅ Fixed here

    for country, regions in REGION_STRUCTURE.items('option'):
        data["forecasts"][country] = {}
        for region in regions:
            # Slightly different probability each run
            p_final = round(random.uniform(0.05, 0.95), 3)
            data["forecasts"][country][region] = {
                "P_final": p_final,
                "tier": classify_tier(p_final)
            }

    return data

# ✅ Save to JSON
def save_forecast(data):
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅ Forecasts saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    forecast_data = generate_forecast()
    save_forecast(forecast_data)
    print("✅ New forecast generated at:", forecast_data["timestamp"])
