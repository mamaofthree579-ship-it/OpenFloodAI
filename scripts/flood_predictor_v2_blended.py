#!/usr/bin/env python3
"""
flood_predictor_v2_blended.py - v1.0.1 Smart Basins update

Adds:
 - Soil Moisture Index (SMI) multiplier
 - Rainfall lag response (48h) multiplier
 - Regional parameter support (loaded externally)
"""
from typing import Dict, Any

def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))

def compute_local_multiplier(smi: float, rainfall_lag_48h: float, params: Dict[str, Any]) -> float:
    """
    Simple local multiplier based on soil moisture and recent rainfall.
    - smi: 0..1 (1 = saturated)
    - rainfall_lag_48h: mm (rain in last 48h)
    - params: region-specific thresholds
    """
    mult = 1.0
    smi_thresh = params.get("smi_threshold", 0.75)
    rain_thresh = params.get("rain_lag_threshold_mm", 20.0)
    if smi >= smi_thresh and rainfall_lag_48h > rain_thresh:
        mult += params.get("smi_rain_multiplier", 0.25)
    return mult

def blended_flood_probability(inputs: Dict[str, Any], region_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    inputs: dictionary with keys such as:
      ENSO_bias, PDO_pos, AR_cat, hydrologic_load, IVT, IVT_90pct,
      radar_24h_accum, R24_thresh, tide_height, tide_thresh,
      ensemble_prob, seasonal_tilt, smi, rainfall_lag_48h
    region_params: region-specific thresholds and multipliers
    returns: dict with P_final, tier, and diagnostics
    """
    ENSO_bias = float(inputs.get("ENSO_bias", 0.0))
    PDO_pos = bool(inputs.get("PDO_pos", False))
    AR_cat = int(inputs.get("AR_cat", 1))
    hydrologic_load = str(inputs.get("hydrologic_load", "NORMAL")).upper()
    IVT = float(inputs.get("IVT", 0.0))
    IVT_90pct = float(inputs.get("IVT_90pct", region_params.get("IVT_90pct", 850.0)))
    radar_24h_accum = float(inputs.get("radar_24h_accum", 0.0))
    R24_thresh = float(region_params.get("R24_thresh", 75.0))
    tide_height = float(inputs.get("tide_height", 0.0))
    tide_thresh = float(region_params.get("tide_thresh", 0.0))
    ensemble_prob = float(inputs.get("ensemble_prob", region_params.get("base_ensemble_prob", 0.35)))
    seasonal_tilt = float(inputs.get("seasonal_tilt", region_params.get("seasonal_tilt", 0.0)))
    smi = float(inputs.get("smi", region_params.get("default_smi", 0.25)))
    rainfall_lag_48h = float(inputs.get("rainfall_lag_48h", 0.0))

    # Seasonal escalation
    if ENSO_bias >= region_params.get("ENSO_threshold", 0.4) and PDO_pos and AR_cat >= region_params.get("AR_cat_thresh", 3) and hydrologic_load == "HIGH":
        seasonal_tilt += region_params.get("seasonal_escalation", 0.15)

    # Coastal multiplier
    coastal_multiplier = 1.4 if (IVT > IVT_90pct and radar_24h_accum > R24_thresh and tide_height > tide_thresh) else 1.0

    # Local basin multiplier (SMI + rainfall lag)
    local_multiplier = compute_local_multiplier(smi, rainfall_lag_48h, region_params)

    # Combine all multipliers
    P_raw = ensemble_prob * (1.0 + seasonal_tilt) * coastal_multiplier * local_multiplier
    P_final = clamp(P_raw, 0.0, 1.0)

    # Tier mapping (using region thresholds if provided)
    amber_thr = region_params.get("amber_threshold", 0.30)
    red_thr = region_params.get("red_threshold", 0.60)

    if P_final >= red_thr:
        tier = "RED"
    elif P_final >= amber_thr:
        tier = "AMBER"
    else:
        tier = "GREEN"

    diagnostics = {
        "ensemble_prob": ensemble_prob,
        "seasonal_tilt": round(seasonal_tilt, 3),
        "coastal_multiplier": coastal_multiplier,
        "local_multiplier": local_multiplier,
        "P_raw": round(P_raw, 4)
    }

    return {"P_final": round(P_final, 3), "tier": tier, "diagnostics": diagnostics}
