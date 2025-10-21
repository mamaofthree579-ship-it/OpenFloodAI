"""
OpenFloodAI v2 — Blended Flood Probability Core
Copyright (C) 2025  mamaofthree579-ship-it
License: GNU AGPL v3.0

This script calculates blended flood probabilities by combining
seasonal climate signals, hydrologic indicators, and coastal amplifiers.
"""

import math

def clamp(value, low=0.0, high=1.0):
    """Clamp a value within a valid probability range."""
    return max(low, min(high, value))

def lower_bound(p):
    """Lower bound of uncertainty window."""
    return max(0.0, p - 0.15)

def blended_flood_probability(inputs: dict) -> dict:
    """
    Combine seasonal, ensemble, and coastal influences into one probability.
    inputs keys:
        ENSO_bias, PDO_pos, AR_cat, hydrologic_load, IVT,
        IVT_90pct, radar_24h_accum, R24_thresh, tide_height,
        tide_thresh, ensemble_prob, seasonal_tilt
    """
    ENSO_bias = inputs.get("ENSO_bias", 0)
    PDO_pos = inputs.get("PDO_pos", False)
    AR_cat = inputs.get("AR_cat", 1)
    hydrologic_load = inputs.get("hydrologic_load", "NORMAL")
    IVT = inputs.get("IVT", 0)
    IVT_90pct = inputs.get("IVT_90pct", 1000)
    radar_24h_accum = inputs.get("radar_24h_accum", 0)
    R24_thresh = inputs.get("R24_thresh", 25)
    tide_height = inputs.get("tide_height", 0)
    tide_thresh = inputs.get("tide_thresh", 1.5)
    ensemble_prob = inputs.get("ensemble_prob", 0.2)
    seasonal_tilt = inputs.get("seasonal_tilt", 0.0)

    # --- Escalate seasonal tilt ---
    if ENSO_bias >= 0.4 and PDO_pos and AR_cat >= 3 and hydrologic_load.upper() == "HIGH":
        seasonal_tilt += 0.15

    # --- Coastal multiplier ---
    if IVT > IVT_90pct and radar_24h_accum > R24_thresh and tide_height > tide_thresh:
        coastal_multiplier = 1.4
    else:
        coastal_multiplier = 1.0

    # --- Combine ---
    P_final = clamp(ensemble_prob * (1 + seasonal_tilt) * coastal_multiplier, 0, 1)

    # --- Tier mapping ---
    if P_final >= 0.60 and lower_bound(P_final) >= 0.40:
        tier = "RED"
    elif P_final >= 0.30 and lower_bound(P_final) >= 0.15:
        tier = "AMBER"
    else:
        tier = "GREEN"

    return {
        "P_final": round(P_final, 3),
        "tier": tier,
        "coastal_multiplier": coastal_multiplier,
        "seasonal_tilt": round(seasonal_tilt, 3)
    }
