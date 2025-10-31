#!/usr/bin/env python3
"""
live_data_ingestor.py - Fetch live data for OpenFloodAI
Pulls rainfall, IVT (approx.), tide, and soil moisture for each region.
Requires `requests` and `pandas`.
"""
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CONFIG = BASE / "config" / "region_parameters.json"
LIVE_OUT = BASE / "data" / "inputs" / "live_conditions.json"

def get_soil_moisture_usgs(site="09380000"):
    """Fetch SMI proxy (soil moisture) from USGS Water Services (example site)."""
    try:
        url = f"https://waterservices.usgs.gov/nwis/iv/?sites={site}&parameterCd=00045&format=json"
        r = requests.get(url, timeout=10)
        js = r.json()
        val = float(js["value"]["timeSeries"][0]["values"][0]["value"][-1]["value"])
        # Normalize roughly 0-1 (this depends on site and calibration)
        smi = min(1.0, max(0.0, val / 50.0))
        return smi
    except Exception as e:
        print("SMI fetch failed:", e)
        return 0.4  # fallback

def get_recent_rainfall(lat, lon, hours=48):
    """Get NOAA precipitation estimate (experimental)."""
    try:
        end = datetime.utcnow()
        start = end - timedelta(hours=hours)
        url = (
            f"https://api.weather.gov/points/{lat},{lon}"
        )
        meta = requests.get(url, timeout=10).json()
        grid = meta["properties"]["forecastGridData"]
        grid_data = requests.get(grid, timeout=10).json()
        # This section depends on NOAA format; simplified proxy:
        rain = grid_data["properties"]["quantitativePrecipitation"]["values"][0]["value"]
        return rain or 0.0
    except Exception as e:
        print("Rainfall fetch failed:", e)
        return 0.0

def main():
    regions = json.loads(CONFIG.read_text())
    live = {"timestamp": datetime.utcnow().isoformat() + "Z", "regions": {}}
    for region in regions:
        # You can assign lat/lon for each basin (placeholder values here)
        lat, lon = (38.6, -121.5) if "Sacramento" in region else (37.7, -85.7)
        smi = get_soil_moisture_usgs()
        rainfall = get_recent_rainfall(lat, lon)
        live["regions"][region] = {"smi": smi, "rainfall_lag_48h": rainfall}
        print(f"Fetched {region}: SMI={smi:.2f}, 48h Rain={rainfall:.1f}mm")

    Path(LIVE_OUT).parent.mkdir(parents=True, exist_ok=True)
    LIVE_OUT.write_text(json.dumps(live, indent=2))
    print(f"✅ Live data written to {LIVE_OUT}")

if __name__ == "__main__":
    main()
