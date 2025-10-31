#!/usr/bin/env python3
"""
live_data_ingestor.py
------------------------------------
Generates or fetches live data inputs for OpenFloodAI model.
Currently uses simulated (pseudo-random) data for development.
"""

import random

def fetch_live_data(lat, lon):
    """
    Simulates live meteorological + hydrological readings for a given lat/lon.
    Replace later with real API integrations (e.g., NOAA, ECMWF, NASA).
    """

    print(f"   ↳ Generating simulated data for lat={lat}, lon={lon}")

    ENSO_bias = random.uniform(-0.5, 1.2)
    PDO_pos = random.choice([True, False])
    AR_cat = random.randint(1, 5)
    hydrologic_load = random.choice(["LOW", "MEDIUM", "HIGH"])
    IVT = random.uniform(250, 700)
    IVT_90pct = 500
    radar_24h_accum = random.uniform(5, 100)
    R24_thresh = 30
    tide_height = random.uniform(0.5, 2.5)
    tide_thresh = 1.5
    smi = random.uniform(0.2, 0.8)
    rainfall_lag_24h = random.uniform(0, 75)

    return {
        "ENSO_bias": ENSO_bias,
        "PDO_pos": PDO_pos,
        "AR_cat": AR_cat,
        "hydrologic_load": hydrologic_load,
        "IVT": IVT,
        "IVT_90pct": IVT_90pct,
        "radar_24h_accum": radar_24h_accum,
        "R24_thresh": R24_thresh,
        "tide_height": tide_height,
        "tide_thresh": tide_thresh,
        "smi": smi,
        "rainfall_lag_24h": rainfall_lag_24h
    }
