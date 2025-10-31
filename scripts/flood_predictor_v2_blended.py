#!/usr/bin/env python3
"""
flood_predictor_v2_blended.py
------------------------------------
Core flood probability model for OpenFloodAI.
Combines parametric and ensemble (blended) methods.

Enhancements:
• Integrates hydrologic and atmospheric indicators
• Includes soil moisture index (SMI)
• Uses 24-hour rainfall lag as intensity proxy
"""

def clamp(value, low, high):
    return max(low, min(high, value))

def lower_bound(prob):
    """Apply a probabilistic floor to avoid false negatives."""
    return prob * 0.75

def blended_flood_probability(inputs):
    """
    Compute both blended and parametric probabilities.
    Returns:
      blended_result, parametric_result
    """

    # --- Extract inputs ---
    ENSO_bias = inputs.get("ENSO_bias", 0.0)
    PDO_pos = inputs.get("PDO_pos", False)
    AR_cat = inputs.get("AR_cat", 1)
    hydrologic_load = inputs.get("hydrologic_load", "MEDIUM")
    IVT = inputs.get("IVT", 0)
    IVT_90pct = inputs.get("IVT_90pct", 0)
    radar_24h_accum = inputs.get("radar_24h_accum", 0)
    R24_thresh = inputs.get("R24_thresh", 0)
    tide_height = inputs.get("tide_height", 0)
    tide_thresh = inputs.get("tide_thresh", 0)
    smi = inputs.get("smi", 0.3)
    rainfall_lag_24h = inputs.get("rainfall_lag_24h", 0.0)

    # --- Base probability ---
    ensemble_prob = 0.35

    # --- Seasonal tilt adjustment ---
    seasonal_tilt = 0.0
    if ENSO_bias >= 0.4 and PDO_pos and AR_cat >= 3 and hydrologic_load.upper() == "HIGH":
        seasonal_tilt += 0.15

    # --- Coastal enhancement ---
    if IVT > IVT_90pct and radar_24h_accum > R24_thresh and tide_height > tide_thresh:
        coastal_multiplier = 1.4
    else:
        coastal_multiplier = 1.0

    # --- Rainfall lag response (24h) ---
    # Heavier recent rainfall increases short-term risk
    rain_factor = min(1.5, 1 + (rainfall_lag_24h / 50.0))

    # --- Soil moisture multiplier ---
    smi_mult = 1.0 + (smi - 0.3) * 0.8  # Dampens or amplifies by ~±40%

    # --- Combine all modifiers ---
    P_final = clamp(
        ensemble_prob * (1 + seasonal_tilt) * coastal_multiplier * rain_factor * smi_mult,
        0, 1
    )

    # --- Determine tier ---
    if P_final >= 0.60 and lower_bound(P_final) >= 0.40:
        tier = "RED"
    elif P_final >= 0.30 and lower_bound(P_final) >= 0.15:
        tier = "AMBER"
    else:
        tier = "GREEN"

    # --- Parametric baseline (for comparison) ---
    parametric_prob = clamp(
        0.25 + 0.1 * AR_cat + 0.2 * smi + (rainfall_lag_24h / 100.0),
        0, 1
    )
    if parametric_prob >= 0.6:
        parametric_tier = "RED"
    elif parametric_prob >= 0.3:
        parametric_tier = "AMBER"
    else:
        parametric_tier = "GREEN"

    blended_result = {"P_final": P_final, "tier": tier}
    parametric_result = {"P_final": parametric_prob, "tier": parametric_tier}

    return blended_result, parametric_result
