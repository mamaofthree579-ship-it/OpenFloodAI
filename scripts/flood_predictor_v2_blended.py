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


# Optional quick test
if __name__ == "__main__":
    from live_data_fetcher import get_live_environmental_data
    region = "Texas"
    sample = get_live_environmental_data(region)
    result = blended_flood_probability(sample, region)
    print(f"Sample forecast for {region}:\n", result)
