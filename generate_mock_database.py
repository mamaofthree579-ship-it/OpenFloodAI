# file: generate_mock_database.py
import json
import os
import random
from datetime import datetime

# Initialize deep 4-tier structural lookup dictionary
mock_db = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "forecasts": {
        "North America": {
            "United States": {
                "Maryland": {
                    "Baltimore County": {"rainfall_intensity": 0.82, "river_level": 0.65, "soil_saturation": 0.88, "rainfall_last_24h": 0.75},
                    "Howard County": {"rainfall_intensity": 0.45, "river_level": 0.40, "soil_saturation": 0.60, "rainfall_last_24h": 0.35},
                    "Montgomery County": {"rainfall_intensity": 0.15, "river_level": 0.22, "soil_saturation": 0.30, "rainfall_last_24h": 0.10}
                },
                "Texas": {
                    "Harris County (Coast)": {"rainfall_intensity": 0.90, "river_level": 0.75, "soil_saturation": 0.95, "rainfall_last_24h": 0.85},
                    "Travis County (Valley)": {"rainfall_intensity": 0.50, "river_level": 0.55, "soil_saturation": 0.40, "rainfall_last_24h": 0.60},
                    "El Paso County (Desert)": {"rainfall_intensity": 0.05, "river_level": 0.10, "soil_saturation": 0.08, "rainfall_last_24h": 0.02}
                }
            }
        },
        "Asia": {
            "Bangladesh": {
                "Dhaka Division": {
                    "Dhaka Central (Delta)": {"rainfall_intensity": 0.88, "river_level": 0.85, "soil_saturation": 0.90, "rainfall_last_24h": 0.92}
                }
            }
        }
    }
}

# Ensure directory structure exists safely
target_dir = os.path.join("data", "outputs")
os.makedirs(target_dir, exist_ok=True)

# Output compiled database file
with open(os.path.join(target_dir, "all_forecasts.json"), "w") as f:
    json.dump(mock_db, f, indent=2)

print("✅ Success: Main JSON Database generated successfully at data/outputs/all_forecasts.json")
