#!/usr/bin/env python3
"""
OpenFloodAI — Blended Flood Probability Model (v2 Multi-Region)
---------------------------------------------------------------
Combines seasonal signals, atmospheric rivers, and local hydrology
to produce a unified exceedance probability (P_final).
"""

import math
import random


# --------------------------------------------------------------------
# Helper Functions
# --------------------------------------------------------------------

def clamp(value, min_val, max_val):
    """Ensure value stays between given bounds."""
    return max(min_val, min(value, max_val))


def lower_bound(prob):
    """Provides a conservative lower bound for uncertainty estimation."""
    return max(0, prob - 0.15)


# --------------------------------------------------------------------
# Core Probability Model
# --------------------------------------------------------------------

def blended_flood_probability(
    ensemble_prob: float,
    ENSO_bias: float,
    PDO_pos: bool,
    AR_cat: int,
    hydrologic_load: str,
    IVT: float,
    radar_24h_accum: float,
    tide_height: float
) -> float:
    """
    Combine global climate signals and local hydrometeorology into
    a blended flood exceedance probability (0–1).
    """

    # --- Seasonal (climate-scale) adjustment ---
    seasonal_tilt = 0.0

    # ENSO and PDO influence
    if ENSO_bias >= 0.4 and PDO_pos and AR_cat >= 3 and hydrologic_load.upper() == "HIGH":
        seasonal_tilt += 0.15  # +15% enhancement
    elif ENSO_bias <= -0.4 and not PDO_pos:
        seasonal_tilt -= 0.1   # -10% suppression (La Niña + neg PDO)

    # --- Local forcing multiplier ---
    IVT_90pct = 350.0   # typical strong moisture flux threshold
    R24_thresh = 100.0  # heavy rain threshold (mm)
    tide_thresh = 1.5   # coastal surge threshold (m)

    if IVT > IVT_90pct and radar_24h_accum > R24_thresh and tide_height > tide_thresh:
        coastal_multiplier = 1.4
    elif radar_24h_accum > R24_thresh:
        coastal_multiplier = 1.2
    else:
        coastal_multiplier = 1.0

    # --- Final combination ---
    P_final = clamp(ensemble_prob * (1 + seasonal_tilt) * coastal_multiplier, 0, 1)

    # --- Tier gating ---
    if P_final >= 0.60 and lower_bound(P_final) >= 0.40:
        tier = "RED"
    elif P_final >= 0.30 and lower_bound(P_final) >= 0.15:
        tier = "AMBER"
    else:
        tier = "GREEN"

    return P_final


# --------------------------------------------------------------------
# Example test (manual validation)
# --------------------------------------------------------------------
if __name__ == "__main__":
    print("🌧️ Running sample forecast test...\n")

    sample = blended_flood_probability(
        ensemble_prob=0.45,
        ENSO_bias=0.6,
        PDO_pos=True,
        AR_cat=4,
        hydrologic_load="HIGH",
        IVT=400,
        radar_24h_accum=120,
        tide_height=1.8
    )

    print(f"Sample blended probability: {sample:.2f}")
