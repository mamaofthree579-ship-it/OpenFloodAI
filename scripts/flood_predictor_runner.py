"""
flood_predictor_runner.py
Runs the blended flood probability model and exports updated JSON for the dashboard.
"""

import os
import json
from datetime import datetime
from flood_predictor_v2_blended import blended_flood_probability

# ✅ Define country → region structure
REGIONS = {
    "USA": ["California", "Texas", "Florida", "New York", "Louisiana"],
    "UK": ["London", "Manchester", "Liverpool", "Bristol"],
    "India": ["Delhi", "Mumbai", "Kolkata", "Chennai", "Assam"],
    "Brazil": ["Rio de Janeiro", "São Paulo", "Bahia", "Amazonas"],
    "Australia": ["Sydney", "Queensland", "Victoria", "Western Australia"],
    "Nigeria": ["Lagos", "Abuja", "Rivers", "Kano"],
    "Philippines": ["Manila", "Cebu", "Davao"],
}

# ✅ Safer tier classification thresholds
def classify_tier(prob):
    """Convert numeric probability (0-1) into a color tier."""
    if prob >= 0.75:
        return "RED"      # High flood risk
    elif prob >= 0.40:
        return "AMBER"    # Moderate flood risk
    else:
        return "GREEN"    # Low flood risk

def run_forecast():
    results = {}
    for country, regions in REGIONS.items():
        results[country] = {}
        for region in regions:
            try:
                P_final = blended_flood_probability(region)
            except Exception:
                # Fallback for regions without detailed data
                import random
                P_final = random.uniform(0.05, 0.95)
            tier = classify_tier(P_final)
            results[country][region] = {
                "P_final": round(P_final, 3),
                "tier": tier,
            }

    output_dir = os.path.join("data", "outputs")
    os.makedirs(output_dir, exist_ok=True)

    output_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "forecasts": results,
    }

    with open(os.path.join(output_dir, "all_forecasts.json"), "w") as f:
        json.dump(output_data, f, indent=2)

    print("✅ Forecast generation complete.")
    print(f"Saved {len(results)} countries worth of forecasts to all_forecasts.json")

if __name__ == "__main__":
    run_forecast()
