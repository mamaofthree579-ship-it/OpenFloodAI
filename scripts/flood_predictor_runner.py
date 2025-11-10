import json, random
from datetime import datetime

# 🌎 Global region structure (continent → country → state/province → county/metro)
REGION_STRUCTURE = {
    "North America": {
        "United States": {
            "California": ["Los Angeles County", "San Diego County", "Sacramento County"],
            "Texas": ["Harris County", "Travis County", "Dallas County"],
            "Florida": ["Miami-Dade County", "Orange County", "Hillsborough County"],
            "New York": ["New York County", "Erie County", "Monroe County"]
        },
        "Canada": {
            "Ontario": ["Toronto", "Ottawa"],
            "British Columbia": ["Vancouver", "Victoria"],
            "Quebec": ["Montreal", "Quebec City"]
        },
        "Mexico": {
            "Jalisco": ["Guadalajara", "Puerto Vallarta"],
            "Nuevo León": ["Monterrey", "San Nicolás de los Garza"]
        }
    },
    "South America": {
        "Brazil": {
            "São Paulo": ["São Paulo City", "Campinas"],
            "Rio de Janeiro": ["Rio de Janeiro City", "Niterói"]
        },
        "Argentina": {
            "Buenos Aires": ["Buenos Aires City", "La Plata"],
            "Córdoba": ["Córdoba City", "Villa Carlos Paz"]
        },
        "Chile": {
            "Santiago Metropolitan": ["Santiago", "Puente Alto"],
            "Valparaíso": ["Valparaíso", "Viña del Mar"]
        }
    },
    "Europe": {
        "United Kingdom": {
            "England": ["London", "Manchester"],
            "Scotland": ["Edinburgh", "Glasgow"],
            "Wales": ["Cardiff", "Swansea"]
        },
        "France": {
            "Île-de-France": ["Paris", "Versailles"],
            "Provence-Alpes-Côte d'Azur": ["Marseille", "Nice"]
        },
        "Germany": {
            "Bavaria": ["Munich", "Nuremberg"],
            "North Rhine-Westphalia": ["Cologne", "Düsseldorf"]
        },
        "Italy": {
            "Lazio": ["Rome", "Viterbo"],
            "Lombardy": ["Milan", "Bergamo"]
        }
    },
    "Africa": {
        "Nigeria": {
            "Lagos": ["Lagos Mainland", "Ikeja"],
            "Kano": ["Kano City", "Gwale"]
        },
        "Kenya": {
            "Nairobi": ["Westlands", "Kasarani"],
            "Mombasa": ["Mvita", "Changamwe"]
        },
        "South Africa": {
            "Gauteng": ["Johannesburg", "Pretoria"],
            "Western Cape": ["Cape Town", "Stellenbosch"]
        },
        "Egypt": {
            "Cairo Governorate": ["Cairo", "Helwan"],
            "Alexandria": ["Alexandria City", "Montaza"]
        }
    },
    "Asia": {
        "India": {
            "Maharashtra": ["Mumbai", "Pune"],
            "Tamil Nadu": ["Chennai", "Madurai"],
            "West Bengal": ["Kolkata", "Howrah"]
        },
        "China": {
            "Guangdong": ["Guangzhou", "Shenzhen"],
            "Beijing": ["Dongcheng", "Haidian"]
        },
        "Japan": {
            "Tokyo": ["Chiyoda", "Shinjuku"],
            "Osaka": ["Kita", "Naniwa"]
        },
        "Philippines": {
            "Metro Manila": ["Quezon City", "Manila"],
            "Cebu": ["Cebu City", "Mandaue"]
        }
    },
    "Oceania": {
        "Australia": {
            "New South Wales": ["Sydney", "Newcastle"],
            "Victoria": ["Melbourne", "Geelong"],
            "Queensland": ["Brisbane", "Cairns"]
        },
        "New Zealand": {
            "Auckland Region": ["Auckland City", "Manukau"],
            "Canterbury": ["Christchurch", "Ashburton"]
        },
        "Fiji": {
            "Central Division": ["Suva", "Nausori"],
            "Western Division": ["Lautoka", "Nadi"]
        }
    },
    "Antarctica": {
        "Research Stations": {
            "Ross Ice Shelf": ["McMurdo Station", "Scott Base"],
            "Queen Maud Land": ["Troll Station", "Neumayer Station III"]
        }
    }
}

# 🌊 Flood tier logic
def determine_tier(probability):
    if probability > 0.75:
        return "RED"
    elif probability > 0.45:
        return "AMBER"
    else:
        return "GREEN"

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
    output_path = "data/outputs/all_forecasts.json"

    with open(output_path, "w") as f:
        json.dump(forecast_data, f, indent=2)

    print("✅ Forecast generation complete:", forecast_data["timestamp"])
