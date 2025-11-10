import json
import random
from datetime import datetime
from pathlib import Path

# === REGION STRUCTURE ===
REGION_STRUCTURE = {
    "North America": {
        "United States": ["California", "Florida", "Texas", "New York"],
        "Canada": ["Ontario", "Quebec", "British Columbia"],
        "Mexico": ["Yucatán", "Chiapas", "Baja California"]
    },
    "South America": {
        "Brazil": ["São Paulo", "Amazonas", "Bahia"],
        "Argentina": ["Buenos Aires", "Cordoba"],
        "Chile": ["Santiago", "Valparaíso"]
    },
    "Europe": {
        "United Kingdom": ["England", "Scotland", "Wales"],
        "France": ["Île-de-France", "Normandy", "Provence"],
        "Germany": ["Bavaria", "Saxony", "Berlin"],
        "Italy": ["Lombardy", "Tuscany", "Sicily"],
        "Spain": ["Madrid", "Catalonia", "Andalusia"]
    },
    "Africa": {
        "Nigeria": ["Lagos", "Abuja", "Kano"],
        "South Africa": ["Gauteng", "Western Cape", "KwaZulu-Natal"],
        "Kenya": ["Nairobi", "Mombasa"],
        "Egypt": ["Cairo", "Alexandria"]
    },
    "Asia": {
        "India": ["Maharashtra", "Tamil Nadu", "Kerala"],
        "China": ["Beijing", "Guangdong", "Sichuan"],
        "Japan": ["Tokyo", "Osaka"],
        "Indonesia": ["Jakarta", "Bali"],
        "Philippines": ["Luzon", "Visayas", "Mindanao"]
    },
    "Oceania": {
        "Australia": ["New South Wales", "Queensland", "Victoria"],
        "New Zealand": ["Auckland", "Wellington", "Canterbury"]
    }
}

# === SIMPLE SIMULATION FUNCTION ===
def blended_flood_probability(region_name):
    # Simulate rainfall, river flow, tide, and runoff conditions
    rainfall = random.uniform(0, 1)
    river_flow = random.uniform(0, 1)
    tide_effect = random.uniform(0, 1)
    soil_saturation = random.uniform(0, 1)

    # Weighted blending formula (adjustable later)
    P_final = (0.4 * rainfall + 0.3 * river_flow + 0.2 * tide_effect + 0.1 * soil_saturation)
    tier = "RED" if P_final > 0.66 else "AMBER" if P_final > 0.33 else "GREEN"

    return {"P_final": round(P_final, 3), "tier": tier}


# === MAIN FORECAST GENERATION ===
def generate_forecast():
    print("🔄 Generating multi-region forecasts...")
    data = {"forecasts": {}, "timestamp": datetime.utcnow().isoformat() + "Z"}

    for continent, countries in REGION_STRUCTURE.items():
        for country, regions in countries.items():
            data["forecasts"].setdefault(country, {})
            for region in regions:
                data["forecasts"][country][region] = blended_flood_probability(region)

    print("✅ Forecast generation complete.")
    return data


# === WRITE TO FILE ===
def save_forecast(data, output_path="data/outputs/all_forecasts.json"):
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
    print(f"💾 Forecast written to {output_file.resolve()}")


if __name__ == "__main__":
    forecast_data = generate_forecast()
    save_forecast(forecast_data)
