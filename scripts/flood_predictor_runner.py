import os
import json
import random
from datetime import datetime

# ✅ Ensure output directory exists
OUTPUT_DIR = os.path.join("data", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------------------------------
# 🔧 Helper functions
# -----------------------------------------------------

def classify_tier(prob):
    """Assign tier based on flood probability."""
    if prob >= 0.60:
        return "RED"
    elif prob >= 0.30:
        return "AMBER"
    else:
        return "GREEN"

def generate_region_data(regions):
    """Generate simulated forecast data for a list of regions."""
    return {
        region: {
            "P_final": round(random.uniform(0.05, 0.85), 2),
            "tier": classify_tier(random.uniform(0.05, 0.85))
        }
        for region in regions
    }

# -----------------------------------------------------
# 🌎 Define countries and regions
# -----------------------------------------------------

REGIONAL_STRUCTURE = {
    "USA": ["California", "Texas", "Florida", "New York", "Louisiana", "Colorado"],
    "Canada": ["British Columbia", "Ontario", "Quebec", "Alberta"],
    "United Kingdom": ["England", "Scotland", "Wales", "Northern Ireland"],
    "India": ["Maharashtra", "Kerala", "Assam", "Tamil Nadu", "Gujarat"],
    "Australia": ["Queensland", "New South Wales", "Victoria", "Western Australia"],
    "Brazil": ["Amazonas", "São Paulo", "Bahia", "Rio de Janeiro"],
    "Philippines": ["Luzon", "Visayas", "Mindanao"],
    "Kenya": ["Nairobi", "Kisumu", "Mombasa"],
    "Japan": ["Tokyo", "Osaka", "Hokkaido", "Kyushu"],
    "Italy": ["Lombardy", "Sicily", "Veneto", "Tuscany"]
}

# -----------------------------------------------------
# 🧮 Generate all forecasts
# -----------------------------------------------------

def build_forecast():
    print("🌊 Generating multi-region forecast data...")
    forecasts = {}
    for country, regions in REGIONAL_STRUCTURE.items():
        forecasts[country] = generate_region_data(regions)
    return forecasts

# -----------------------------------------------------
# 💾 Write output JSON
# -----------------------------------------------------

def main():
    data = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "forecasts": build_forecast()
    }

    output_path = os.path.join(OUTPUT_DIR, "all_forecasts.json")
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Forecast data written to {output_path}")

if __name__ == "__main__":
    main()
