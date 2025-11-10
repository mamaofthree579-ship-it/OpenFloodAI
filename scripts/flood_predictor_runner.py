import json
import random
from datetime import datetime
from pathlib import Path

# --------------------------------------------------------
# 🌍 Define the regions by country for multi-region forecast
# --------------------------------------------------------
REGION_STRUCTURE = {
    # 🌎 North America
    "USA": [
        "California", "Texas", "Florida", "New York",
        "Louisiana", "Illinois", "Pennsylvania", "Washington"
    ],
    "Canada": [
        "British Columbia", "Ontario", "Quebec",
        "Alberta", "Nova Scotia", "Manitoba"
    ],
    "Mexico": [
        "Jalisco", "Chiapas", "Veracruz", "Nuevo León",
        "Yucatán", "Puebla"
    ],

    # 🌍 Europe
    "UK": ["England", "Scotland", "Wales", "Northern Ireland"],
    "France": ["Île-de-France", "Occitanie", "Provence-Alpes-Côte d’Azur", "Brittany", "Normandy"],
    "Germany": ["Bavaria", "North Rhine-Westphalia", "Berlin", "Hamburg", "Saxony"],

    # 🌏 Asia
    "India": ["Maharashtra", "Kerala", "Assam", "Tamil Nadu", "West Bengal", "Gujarat"],
    "China": ["Guangdong", "Sichuan", "Beijing", "Shanghai", "Yunnan", "Hunan"],
    "Philippines": ["Luzon", "Visayas", "Mindanao", "Metro Manila"],
    "Japan": ["Tokyo", "Osaka", "Kyoto", "Hokkaido", "Okinawa"],

    # 🌍 Africa
    "Nigeria": ["Lagos", "Rivers", "Anambra", "Kano", "Ogun"],
    "South Africa": ["Gauteng", "KwaZulu-Natal", "Western Cape", "Eastern Cape", "Limpopo"],

    # 🌏 Oceania
    "Australia": ["New South Wales", "Queensland", "Victoria", "Western Australia", "Tasmania"],

    # 🌎 South America
    "Brazil": ["São Paulo", "Rio de Janeiro", "Bahia", "Amazonas", "Paraná"],
    "Argentina": ["Buenos Aires", "Córdoba", "Santa Fe", "Mendoza", "Salta"]
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
    output_path = "data/outputs/all_forecasts.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w") as f:
    json.dump(data, f, indent=2)

    print(f"✅ Forecast data written to {output_path}")

    print("Writing forecasts for", len(REGION_STRUCTURE), "countries...")
for country, regions in REGION_STRUCTURE.items():
    print("  ", country, ":", len(regions), "regions")
    
# --------------------------------------------------------
# 🚀 Main runner
# --------------------------------------------------------
if __name__ == "__main__":
    forecast_data = generate_forecast()
    save_forecast_to_file(forecast_data)
    print(f"Forecast generated at {forecast_data['timestamp']}")
