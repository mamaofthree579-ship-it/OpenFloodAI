import json, random
from datetime import datetime

# 🌍 Hierarchical geographic structure
REGION_STRUCTURE = {
    "North America": {
        "United States": {
            "California": ["Los Angeles County", "San Diego County", "Sacramento County"],
            "Texas": ["Harris County", "Travis County", "Dallas County"],
            "Florida": ["Miami-Dade County", "Orange County", "Hillsborough County"]
        },
        "Canada": {
            "Ontario": ["Toronto", "Ottawa"],
            "British Columbia": ["Vancouver", "Victoria"]
        }
    },
    "Europe": {
        "United Kingdom": {
            "England": ["London", "Manchester"],
            "Scotland": ["Edinburgh", "Glasgow"]
        },
        "France": {
            "Île-de-France": ["Paris", "Versailles"],
            "Provence-Alpes-Côte d'Azur": ["Marseille", "Nice"]
        }
    },
    "Asia": {
        "Japan": {
            "Tokyo": ["Chiyoda", "Shinjuku"],
            "Osaka": ["Kita", "Naniwa"]
        },
        "India": {
            "Maharashtra": ["Mumbai", "Pune"],
            "Tamil Nadu": ["Chennai", "Madurai"]
        }
    }
}

# 🎯 Tier calculation based on flood probability
def determine_tier(p):
    if p > 0.65:
        return "RED"
    elif p > 0.35:
        return "AMBER"
    else:
        return "GREEN"

# 💧 Generate hierarchical forecast data
def generate_forecast():
    data = {"forecasts": {}, "timestamp": datetime.utcnow().isoformat() + "Z"}

    for continent, countries in REGION_STRUCTURE.items():
        data["forecasts"][continent] = {}
        for country, states in countries.items():
            data["forecasts"][continent][country] = {}
            for state, counties in states.items():
                data["forecasts"][continent][country][state] = {}
                for county in counties:
                    p_val = round(random.uniform(0.05, 0.95), 2)
                    tier = determine_tier(p_val)
                    data["forecasts"][continent][country][state][county] = {
                        "P_final": p_val,
                        "tier": tier
                    }
    return data

if __name__ == "__main__":
    forecast_data = generate_forecast()
    with open("data/outputs/all_forecasts.json", "w") as f:
        json.dump(forecast_data, f, indent=2)
    print("✅ Forecast generation complete:", forecast_data["timestamp"])
