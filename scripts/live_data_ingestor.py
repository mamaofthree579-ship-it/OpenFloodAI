"""
live_data_fetcher.py
Fetches or simulates live environmental data for multiple regions.
This file ensures normalized (0–1) input values for correct flood probability classification.
"""

import random

def get_live_environmental_data(region: str):
    """
    Returns realistic, normalized input values for a given region.
    Simulates real sensor or satellite data.
    """

    # Each parameter is normalized (0–1)
    data = {
        "rainfall_intensity": random.uniform(0, 1),      # 0 = dry, 1 = extreme rain
        "river_level": random.uniform(0, 1),             # 0 = low, 1 = flood stage
        "soil_saturation": random.uniform(0, 1),         # 0 = dry, 1 = saturated
        "rainfall_last_24h": random.uniform(0, 1),       # rainfall lag effect
    }

    # Introduce region-based biases for realism
    region_lower = region.lower()
    if "coast" in region_lower or "bay" in region_lower:
        data["river_level"] *= 0.9  # slightly lower sensitivity to inland flooding
        data["rainfall_intensity"] *= 1.1
    elif "mountain" in region_lower or "valley" in region_lower:
        data["river_level"] *= 1.1
        data["soil_saturation"] *= 1.2

    # Clamp values to stay within [0, 1]
    for k, v in data.items():
        data[k] = max(0.0, min(1.0, v))

    return data


# Optional quick test
if __name__ == "__main__":
    from pprint import pprint
    print("🌦 Live data sample for 'California':")
    pprint(get_live_environmental_data("California"))
