import json, random
from datetime import datetime

# 🌎 Global region structure (continent → country → state/province → county/metro)
REGION_STRUCTURE = {
    "North America": {
        "United States": {
    "Alabama": ["Jefferson County", "Mobile County", "Madison County"],
    "Alaska": ["Anchorage Municipality", "Fairbanks North Star Borough", "Matanuska-Susitna Borough"],
    "Arizona": ["Maricopa County", "Pima County", "Pinal County"],
    "Arkansas": ["Pulaski County", "Benton County", "Washington County"],
    "California": ["Los Angeles County", "San Diego County", "Orange County", "Sacramento County", "San Francisco County"],
    "Colorado": ["Denver County", "El Paso County", "Arapahoe County"],
    "Connecticut": ["Fairfield County", "Hartford County", "New Haven County"],
    "Delaware": ["New Castle County", "Kent County", "Sussex County"],
    "Florida": ["Miami-Dade County", "Broward County", "Hillsborough County", "Orange County"],
    "Georgia": ["Fulton County", "Cobb County", "DeKalb County", "Gwinnett County"],
    "Hawaii": ["Honolulu County", "Maui County", "Hawaii County"],
    "Idaho": ["Ada County", "Canyon County", "Kootenai County"],
    "Illinois": ["Cook County", "DuPage County", "Lake County"],
    "Indiana": ["Marion County", "Lake County", "Allen County"],
    "Iowa": ["Polk County", "Linn County", "Scott County"],
    "Kansas": ["Johnson County", "Sedgwick County", "Wyandotte County"],
    "Kentucky": ["Jefferson County", "Fayette County", "Kenton County"],
    "Louisiana": ["Orleans Parish", "Jefferson Parish", "East Baton Rouge Parish"],
    "Maine": ["Cumberland County", "York County", "Penobscot County"],
    "Maryland": ["Baltimore County", "Montgomery County", "Prince George’s County"],
    "Massachusetts": ["Middlesex County", "Suffolk County", "Worcester County"],
    "Michigan": ["Wayne County", "Oakland County", "Macomb County"],
    "Minnesota": ["Hennepin County", "Ramsey County", "Dakota County"],
    "Mississippi": ["Hinds County", "Harrison County", "DeSoto County"],
    "Missouri": ["St. Louis County", "Jackson County", "Greene County"],
    "Montana": ["Yellowstone County", "Gallatin County", "Missoula County"],
    "Nebraska": ["Douglas County", "Lancaster County", "Sarpy County"],
    "Nevada": ["Clark County", "Washoe County", "Carson City"],
    "New Hampshire": ["Hillsborough County", "Rockingham County", "Merrimack County"],
    "New Jersey": ["Bergen County", "Middlesex County", "Essex County"],
    "New Mexico": ["Bernalillo County", "Doña Ana County", "Santa Fe County"],
    "New York": ["New York County", "Kings County", "Queens County", "Erie County", "Monroe County"],
    "North Carolina": ["Mecklenburg County", "Wake County", "Guilford County"],
    "North Dakota": ["Cass County", "Burleigh County", "Grand Forks County"],
    "Ohio": ["Cuyahoga County", "Franklin County", "Hamilton County"],
    "Oklahoma": ["Oklahoma County", "Tulsa County", "Cleveland County"],
    "Oregon": ["Multnomah County", "Washington County", "Lane County"],
    "Pennsylvania": ["Philadelphia County", "Allegheny County", "Montgomery County"],
    "Rhode Island": ["Providence County", "Kent County", "Washington County"],
    "South Carolina": ["Charleston County", "Greenville County", "Richland County"],
    "South Dakota": ["Minnehaha County", "Pennington County", "Lincoln County"],
    "Tennessee": ["Shelby County", "Davidson County", "Knox County"],
    "Texas": ["Harris County", "Dallas County", "Tarrant County", "Bexar County", "Travis County"],
    "Utah": ["Salt Lake County", "Utah County", "Davis County"],
    "Vermont": ["Chittenden County", "Rutland County", "Washington County"],
    "Virginia": ["Fairfax County", "Prince William County", "Loudoun County"],
    "Washington": ["King County", "Pierce County", "Snohomish County"],
    "West Virginia": ["Kanawha County", "Berkeley County", "Monongalia County"],
    "Wisconsin": ["Milwaukee County", "Dane County", "Waukesha County"],
    "Wyoming": ["Laramie County", "Natrona County", "Sweetwater County"]
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
