import json
import random
from datetime import datetime
from pathlib import Path

# --------------------------------------------------------
# 🌍 Define the regions by country for multi-region forecast
# --------------------------------------------------------
REGION_STRUCTURE = {
    "USA": ["California", "Texas", "Florida", "New York", "Louisiana"],
    "UK": ["England", "Scotland", "Wales"],
    "India": ["Maharashtra", "Kerala", "Assam", "West Bengal"],
    "Philippines": ["Luzon", "Visayas", "Mindanao"],
    "Nigeria": ["Lagos", "Rivers", "Anambra", "Kano"],
    "Australia": ["New South Wales", "Queensland", "Victoria"],
}

# --------------------------------------------------------
# 🚨 Simple tier logic
# --------------------------------------------------------
def determine_tier(prob):
    if prob > 0.7:
        return "RED"
    elif prob > 0.4:
        return "AMBER"
    else:
        return "GREEN"

# --------------------------------------------------------
# 🧠 Simulated forecast generation
# --------------------------------------------------------
def generate_forecast():
    data = {"forecasts": {}, "timestamp": datetime.utcnow().isoformat() + "Z"}

    for country, regions in REGION_STRUCTURE.items():
        data["forecasts"][country] = {}
        for region in regions:
            # Random probability generation (simulate model output)
            prob = round(random.uniform(0.05, 0.95), 3)
            tier = determine_tier(prob)
            data["forecasts"][country][region] = {
                "P_final": prob,
                "tier": tier
            }

    return data

# --------------------------------------------------------
# 💾 Write forecast output
# --------------------------------------------------------
def save_forecast_to_file(forecast_data):
    output_dir = Path("data/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "all_forecasts.json"

    with open(output_path, "w") as f:
        json.dump(forecast_data, f, indent=2)

    print(f"✅ Forecast written to {output_path}")

# --------------------------------------------------------
# 🚀 Main runner
# --------------------------------------------------------
if __name__ == "__main__":
    forecast_data = generate_forecast()
    save_forecast_to_file(forecast_data)
    print(f"Forecast generated at {forecast_data['timestamp']}")
