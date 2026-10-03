import random

# ==========================================
# 1. OPTIMIZED LIVE DATA FETCHER
# ==========================================
def get_live_environmental_data(region: str):
    """
    Returns realistic, normalized input values for a given region.
    Simulates real sensor or satellite data.
    """
    # Seed data remains normalized (0 to 1)
    data = {
        "rainfall_intensity": random.uniform(0.1, 0.9),
        "river_level": random.uniform(0.1, 0.9),
        "soil_saturation": random.uniform(0.2, 1.0),    # Primed baselines
        "rainfall_last_24h": random.uniform(0.2, 1.0),  # Historic lag
    }

    region_lower = region.lower()
    
    # Apply baseline environmental sensitivities
    if "coast" in region_lower or "bay" in region_lower:
        data["river_level"] *= 0.8  
        data["rainfall_intensity"] *= 1.1
    elif "mountain" in region_lower or "valley" in region_lower:
        data["river_level"] *= 1.2
        data["soil_saturation"] *= 1.1

    # Clamp values safely to [0, 1]
    for k, v in data.items():
        data[k] = max(0.0, min(1.0, v))

    return data


# ==========================================
# 2. CORRECTED 24-HOUR BLENDED PREDICTOR
# ==========================================
def blended_flood_probability(env_data, region):
    """
    Calculates a realistic 24-hour predictive flood probability.
    Weights are realigned to reflect cumulative daily storage thresholds.
    """
    rain = env_data.get("rainfall_intensity", 0)
    river = env_data.get("river_level", 0)
    soil = env_data.get("soil_saturation", 0)
    lag = env_data.get("rainfall_last_24h", 0)

    # FIXED: Realigned 24-hour predictive matrix weights.
    # Prior 24h lag and soil saturation are highly weighted as core catalysts.
    base_prob = (
        0.15 * rain +
        0.30 * river +
        0.25 * soil +
        0.30 * lag
    )

    # FIXED: Additive regional risk compounding instead of destructive overwrites
    region_factor = 1.0
    region_lower = region.lower()

    # Feature-based adjustments
    if "coast" in region_lower or "bay" in region_lower:
        region_factor += 0.20
    if "valley" in region_lower or "delta" in region_lower:
        region_factor += 0.10
    if "mountain" in region_lower or "plateau" in region_lower:
        region_factor -= 0.10
    if "desert" in region_lower or "dry" in region_lower:
        region_factor -= 0.40
    if "river" in region_lower or "basin" in region_lower:
        region_factor += 0.30

    # Territory-based adjustments 
    if any(state in region for state in ["Texas", "Florida", "Louisiana", "Bangladesh", "Philippines"]):
        region_factor += 0.25
    if any(state in region for state in ["California", "Spain", "Morocco", "Chile"]):
        region_factor -= 0.15

    # Apply cumulative math adjustments 
    P_final = base_prob * region_factor
    P_final = max(0.0, min(1.0, P_final))

    if P_final >= 0.75:
        tier = "RED"
    elif P_final >= 0.40:
        tier = "AMBER"
    else:
        tier = "GREEN"

    return {
        "P_final": round(P_final, 3),
        "tier": tier,
        "details": {
            "base_probability": round(base_prob, 3),
            "region_factor": round(region_factor, 2),
            "inputs": {
                "rainfall_intensity": round(rain, 3),
                "river_level": round(river, 3),
                "soil_saturation": round(soil, 3),
                "rainfall_last_24h": round(lag, 3)
            }
        }
    }


# ==========================================
# 3. VERIFICATION UNIT TEST
# ==========================================
if __name__ == "__main__":
    # Test Location string triggering compound conditions (Coast + Texas)
    test_zone = "South Texas Coast"
    
    print(f"📡 Initializing pipeline simulation for: '{test_zone}'...")
    simulated_live_feed = get_live_environmental_data(test_zone)
    prediction_output = blended_flood_probability(simulated_live_feed, test_zone)
    
    import pprint
    pprint.pprint(prediction_output)
"""
flood_predictor_v2_blended.py
Calculates blended flood probability using environmental data and regional bias factors.
"""

import math

def blended_flood_probability(env_data, region):
    """
    Calculates a realistic blended flood probability based on:
    - rainfall_intensity
    - river_level
    - soil_saturation
    - rainfall_last_24h
    plus region-specific adjustments.
    """

    rain = env_data.get("rainfall_intensity", 0)
    river = env_data.get("river_level", 0)
    soil = env_data.get("soil_saturation", 0)
    lag = env_data.get("rainfall_last_24h", 0)

    # Core blended probability model
    base_prob = (
        0.45 * rain +
        0.35 * river +
        0.15 * soil +
        0.05 * lag
    )

    # --- Regional adjustments (the “basin tuning”) ---
    region_factor = 1.0

    region_lower = region.lower()
    if "coast" in region_lower or "bay" in region_lower:
        region_factor = 1.2      # coastal areas more flood-prone
    elif "valley" in region_lower or "delta" in region_lower:
        region_factor = 1.1
    elif "mountain" in region_lower or "plateau" in region_lower:
        region_factor = 0.9
    elif "desert" in region_lower or "dry" in region_lower:
        region_factor = 0.6
    elif "river" in region_lower or "basin" in region_lower:
        region_factor = 1.3
    elif region in ["Texas", "Florida", "Louisiana", "Bangladesh", "Philippines"]:
        region_factor = 1.25
    elif region in ["California", "Spain", "Morocco", "Chile"]:
        region_factor = 0.85

    # Adjusted final probability
    P_final = base_prob * region_factor

    # Clamp to [0, 1]
    P_final = max(0.0, min(1.0, P_final))

    # --- Tier classification ---
    if P_final >= 0.75:
        tier = "RED"
    elif P_final >= 0.4:
        tier = "AMBER"
    else:
        tier = "GREEN"

    return {
        "P_final": round(P_final, 3),
        "tier": tier,
        "details": {
            "rainfall_intensity": round(rain, 3),
            "river_level": round(river, 3),
            "soil_saturation": round(soil, 3),
            "rainfall_last_24h": round(lag, 3),
            "region_factor": region_factor
        }
    }
