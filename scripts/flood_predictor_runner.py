import json, random
from datetime import datetime

# 🌎 Global region structure (continent → country → state/province → county/metro)
REGION_STRUCTURE = {
    "North America": {
        "United States": {
    "Alabama": ["Jefferson County", "Mobile County", "Madison County", "Autauga County", "Baldwin County", "Barbour County", "Bibb County", "Blount County", "Bullock County", "Butler County", "Calhoun County", "Chambers Count", "Cherokee County", "Chilton County", "Choctaw County", "Clarke County", "Clay County", "Cleburne County", "Coffee County", "Colbert County", "Conecuh County", "Coosa County", "Covington County", "Crenshaw County", "Cullman County", "Dale County", "Dallas County", "DeKalb County", "Elmore County", "Escambia County", "Etowah County", "Fayette County", "Franklin County", "Geneva Count", "Greene County", "Hale County", "Henry County", "Houston County", "Jackson County", "Lamar County", "Lauderdale County", "Lawrence County", "Lee County", "Limestone County", "Lowndes County", "Macon County", "Marengo County", "Marion County", "Marshall County", "Monroe County", "Montgomery County", "Morgan County", "Perry County", "Pickens County", "Pike County", "Randolph County", "Russell County", "St. Clair County", "Shelby County", "Sumter County", "Talladega County", "Tallapoosa County", "Tuscaloosa County", "Walker County", "Washington County", "Wilcox County", "Winston County"],
    "Alaska": ["Anchorage Municipality", "Fairbanks North Star Borough", "Matanuska-Susitna Borough", "Aleutians East", "Aleutians West", "Bethel Borough", "Bristol Bay", "Chugach", "Copper River", "Denali", "Dillingham", "Hoonah-Angoon", "Kusilvak", "Bristol Bay Borough", "Denali Borough", "Haines Borough", "City and Borough of Juneau", "Kenai Peninsula", "Ketchikan Gateway", "Kodiak Island", "Lake and Peninsula", "Nome", "North Slope", "Northwest Arctic", "Prince of Wales-Hyder", "Southeast Fairbanks", "Skagway", "Valdez-Cordova Borough", "Wrangell City and Borough", "Yukon-Koyukuk Borough"],
    "Arizona": ["Maricopa County", "Pima County", "Pinal County", "Apache County", "Cochise County", "Coconino County", "Gila County", "Graham County", "Greenlee County", "La Paz County", "Mohave County", "Navajo County", "Santa Cruz County", "Yavapai County", "Yuma County"],
    "Arkansas": ["Pulaski County", "Benton County", "Washington County", "Arkansas County", "Ashley County", "Baxter County", "Boone County", "Bradley County", "Calhoun County", "Carroll County", "Chicot County", "Clark County", "Clay County", "Cleburne County", "Cleveland County", "Columbia County", "Conway County", "Craighead County", "Crawford County", "Crittenden County", "Cross County", "Dallas County", "Desha County", "Drew County", "Faulkner County", "Franklin County", "Fulton County", "Garland County", "Grant County", "Greene County", "Hempstead County", "Hot Spring County", "Howard County", "Independence County", "Izard County", "Jackson County", "Jefferson County", "Johnson County", "Lafayette County", "Lawrence County", "Lee County", "Lincoln County", "Little River County", "Logan County", "Lonoke County", "Madison County", "Marion County", "Miller County", "Mississippi County", "Monroe County", "Montgomery County", "Nevada County", "Newton County", "Ouachita County", "Perry County", "Phillips County", "Pike County", "Poinsett County", "Polk County", "Pope County", "Prairie County", "Randolph County", "Saint Francis County", "Saline County", "Scott County", "Searcy County", "Sebastian County", "Sevier County", "Sharp County", "Stone County", "Union County", "Van Buren County", "White County", "Woodruff County", "Yell County"],
    "California": ["Los Angeles County", "San Diego County", "Orange County", "Sacramento County", "San Francisco County", "Alameda County", "Alpine County", "Amador County", "Butte County", "Calaveras County", "Colusa County", "Contra Costa County", "Del Norte County", "El Dorado County", "Fresno County", "Glenn County", "Humboldt County", "Imperial County", "Inyo County", "Kern County", "Kings County", "Lake County", "Lassen County", "Madera County", "Marin County", "Mariposa County", "Mendocino County", "Merced County", "Modoc County", "Mono County", "Monterey County", "Napa County", "Nevada County", "Placer County", "Plumas County", "Riverside County", "San Benito County", "San Bernardino County", "San Diego County", "San Joaquin County", "San Luis Obispo County", "San Mateo County", "Santa Barbara County", "Santa Clara County", "Santa Cruz County", "Shasta County", "Sierra County", "Siskiyou County", "Solano County", "Sonoma County", "Stanislaus County", "Sutter County", "Tehama County", "Trinity County", "Tulare County", "Tuolumne County", "Ventura County", "Yolo County", "Yuba County"],
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
    "Virginia": ["Fairfax County", "Prince William County", "Loudoun County", "Clarke County"],
    "Washington": ["King County", "Pierce County", "Snohomish County", "Adams County", "Asotin County", "Benton County", "Chelan Count", "Clallam County", "Clark County", "Columbia County", "Cowlitz County", "Douglas County", "Ferry County", "Franklin County", "Garfield County", "Grant County", "Grays Harbor County", "Island County", "Jefferson County", "Kitsap County", "Kittitas County", "Klickitat County", "Lewis County", "Lincoln County", "Mason County", "Okanogan County", "Pacific County", "Pend Oreille County", "San Juan County", "Skagit County", "Skamania County", "Spokane County", "Stevens County", "Thurston County", "Wahkiakum County", "Walla Walla County", "Whatcom County", "Whitman County", "Yakima County"],
    "West Virginia": ["Kanawha County", "Berkeley County", "Monongalia County", "Jefferson County", "Barbour County", "Boone County", "Braxton County", "Brooke County", "Cabell County", "Calhoun County", "Clay County", "Doddridge County", "Fayette County", "Gilmer County", "Grant County", "Greenbrier County", "Hampshire County", "Hancock County", "Hardy County", "Harrison County", "Jackson County", "Lewis County", "Lincoln County", "Logan County", "McDowell County", "Marion County", "Marshall County", "Mason County", "Mercer County", "Mineral County", "Mingo County", "Monroe County", "Morgan County", "Nicholas County", "Ohio County", "Pendleton County", "Pleasants County", "Pocahontas County", "Preston County", "Putnam County", "Raleigh County", "Randolph County", "Ritchie County", "Roane County", "Summers County", "Taylor County", "Tucker County", "Tyler County", "Upshur County", "Wayne County", "Webster County", "Wetzel County", "Wirt County", "Wood County", "Wyoming County"],
    "Wisconsin": ["Milwaukee County", "Dane County", "Waukesha County", "Adams County", "Ashland County", "Barron County", "Bayfield County", "Brown County", "Buffalo County", "Burnett County", "Calumet County", "Chippewa County", "Clark County", "Columbia County", "Crawford County", "Dodge County", "Door County", "Douglas County", "Dunn County", "Eau Claire County", "Florence County", "Fond du Lac County", "Forest County", "Grant County", "Green County", "Green Lake County", "Iowa County", "Iron County", "Jackson County", "Jefferson County", "Juneau County", "Kenosha County", "Kewaunee County", "La Crosse County", "Lafayette County", "Langlade County", "Lincoln County", "Manitowoc County", "Marathon County", "Marinette County", "Marquette County", "Menominee County", "Monroe County", "Oconto County", "Oneida County", "Outagamie County", "Ozaukee County", "Pepin County", "Pierce County", "Polk County", "Portage County", "Price County", "Racine County", "Richland County", "Rock County", "Rusk County", "St. Croix County", "Sauk County", "Sawyer County", "Shawano County", "Sheboygan County", "Taylor County", "Trempealeau County", "Vernon County", "Vilas County", "Walworth County", "Washburn County", "Washington County", "Waupaca County", "Waushara County", "Winnebago County", "Wood County"],
    "Wyoming": ["Laramie County", "Natrona County", "Sweetwater County", "Albany County", "Big Horn County", "Campbell County", "Carbon County", "Converse County", "Crook County", "Fremont County", "Goshen County", "Hot Springs County", "Johnson County", "Lincoln County", "Niobrara County", "Park County", "Platte County", "Sheridan County", "Sublette County", "Teton County", "Uinta County", "Washakie County", "Weston County"],
    "District of Columbia": ["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5", "Ward 6", "Ward 7", "Ward 8"]         
        },
        "Canada": {
    "Alberta": ["Calgary", "Edmonton", "Red Deer"],
    "British Columbia": ["Vancouver", "Victoria", "Kelowna", "Prince George"],
    "Manitoba": ["Winnipeg", "Brandon", "Steinbach"],
    "New Brunswick": ["Fredericton", "Saint John", "Moncton"],
    "Newfoundland and Labrador": ["St. John's", "Corner Brook", "Gander"],
    "Nova Scotia": ["Halifax", "Sydney", "Truro"],
    "Ontario": ["Toronto", "Ottawa", "Hamilton", "London"],
    "Prince Edward Island": ["Charlottetown", "Summerside"],
    "Quebec": ["Montreal", "Quebec City", "Sherbrooke", "Gatineau"],
    "Saskatchewan": ["Saskatoon", "Regina", "Prince Albert"],
    "Northwest Territories": ["Yellowknife", "Inuvik"],
    "Nunavut": ["Iqaluit", "Rankin Inlet"],
    "Yukon": ["Whitehorse", "Dawson City"]
    },
        "Mexico": {
    "Aguascalientes": ["Aguascalientes City", "Jesús María", "Calvillo"],
    "Baja California": ["Tijuana", "Mexicali", "Ensenada"],
    "Baja California Sur": ["La Paz", "Los Cabos", "Comondú"],
    "Campeche": ["Campeche City", "Ciudad del Carmen"],
    "Chiapas": ["Tuxtla Gutiérrez", "San Cristóbal de las Casas", "Tapachula"],
    "Chihuahua": ["Chihuahua City", "Ciudad Juárez", "Delicias"],
    "Coahuila": ["Saltillo", "Torreón", "Piedras Negras"],
    "Colima": ["Colima City", "Manzanillo", "Tecomán"],
    "Durango": ["Durango City", "Gómez Palacio", "Lerdo"],
    "Guanajuato": ["León", "Irapuato", "Celaya", "Guanajuato City"],
    "Guerrero": ["Acapulco", "Chilpancingo", "Iguala"],
    "Hidalgo": ["Pachuca", "Tula de Allende", "Tulancingo"],
    "Jalisco": ["Guadalajara", "Puerto Vallarta", "Zapopan", "Tepatitlán"],
    "Mexico City": ["Álvaro Obregón", "Iztapalapa", "Benito Juárez", "Coyoacán"],
    "Mexico State": ["Toluca", "Naucalpan", "Ecatepec"],
    "Michoacán": ["Morelia", "Uruapan", "Lázaro Cárdenas"],
    "Morelos": ["Cuernavaca", "Temixco", "Jiutepec"],
    "Nayarit": ["Tepic", "Bahía de Banderas", "Compostela"],
    "Nuevo León": ["Monterrey", "Guadalupe", "San Nicolás de los Garza"],
    "Oaxaca": ["Oaxaca de Juárez", "Salina Cruz", "Juchitán"],
    "Puebla": ["Puebla City", "Tehuacán", "Atlixco"],
    "Querétaro": ["Querétaro City", "San Juan del Río", "El Marqués"],
    "Quintana Roo": ["Cancún", "Chetumal", "Playa del Carmen", "Tulum"],
    "San Luis Potosí": ["San Luis Potosí City", "Soledad", "Ciudad Valles"],
    "Sinaloa": ["Culiacán", "Mazatlán", "Los Mochis"],
    "Sonora": ["Hermosillo", "Ciudad Obregón", "Nogales"],
    "Tabasco": ["Villahermosa", "Cárdenas", "Comalcalco"],
    "Tamaulipas": ["Reynosa", "Matamoros", "Tampico"],
    "Tlaxcala": ["Tlaxcala City", "Apizaco", "Huamantla"],
    "Veracruz": ["Veracruz City", "Xalapa", "Coatzacoalcos", "Poza Rica"],
    "Yucatán": ["Mérida", "Valladolid", "Tizimín"],
    "Zacatecas": ["Zacatecas City", "Guadalupe", "Fresnillo"]
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
