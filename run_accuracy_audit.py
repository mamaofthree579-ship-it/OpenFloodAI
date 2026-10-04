# file: run_accuracy_audit.py
import json
import os
import pandas as pd
import streamlit as st

def evaluate_engine_logic(env_data, region_string):
    """Execution clone of v2.1.0 core blended predictive engine."""
    rain = env_data.get("rainfall_intensity", 0.0)
    river = env_data.get("river_level", 0.0)
    soil = env_data.get("soil_saturation", 0.0)
    lag = env_data.get("rainfall_last_24h", 0.0)

    # Realigned 24-hour matrix predictive weights
    base_prob = (0.15 * rain) + (0.30 * river) + (0.25 * soil) + (0.30 * lag)

    region_factor = 1.0
    region_lower = region_string.lower()

    # Features
    if "coast" in region_lower or "bay" in region_lower:
        region_factor += 0.20
    if "valley" in region_lower or "delta" in region_lower:
        region_factor += 0.10
    if "mountain" in region_lower or "plateau" in region_lower:
        region_factor -= 0.10
    if "desert" in region_lower or "dry" in region_lower:
        region_factor -= 0.40
    if "river" in region_lower or "basin" in region_lower:
        region_factor += 0.30

    # Territories
    if any(s in region_string for s in ["Texas", "Florida", "Louisiana", "Bangladesh", "Philippines"]):
        region_factor += 0.25
    if any(s in region_string for s in ["California", "Spain", "Morocco", "Chile"]):
        region_factor -= 0.15

    P_final = max(0.0, min(1.0, base_prob * region_factor))
    tier = "RED" if P_final >= 0.75 else ("AMBER" if P_final >= 0.40 else "GREEN")
    return {"P_final": round(P_final, 3), "tier": tier}

# Load database target
data_path = os.path.join("data", "outputs", "all_forecasts.json")
try:
    with open(data_path, "r") as f:
        db = json.load(f)
except FileNotFoundError:
    st.error("⚠️ Could not find data/outputs/all_forecasts.json. Please ensure the app has run at least once to generate the database.")
    st.stop()

# FIXED: Standardized dictionary keys to match county names precisely
ground_truth_observations = {
    "Baltimore County": "RED",
    "Howard County": "GREEN",  
    "Montgomery County": "GREEN",
    "Harris County (Coast)": "RED",
    "Travis County (Valley)": "AMBER",
    "El Paso County (Desert)": "GREEN",
    "Dhaka Central (Delta)": "RED",
}

audit_log = []
total_nodes = 0
correct_predictions = 0

# Flatten hierarchy leaves to process validation matrix loops
for continent, countries in db["forecasts"].items():
    for country, states in countries.items():
        for state, counties in states.items():
            for county, metrics in counties.items():
                total_nodes += 1
                
                # This is the string evaluated by the algorithm for regional factors
                location_str = f"{county} ({state}, {country})"

                # Pass node variables through updated calculations
                prediction = evaluate_engine_logic(metrics, location_str)

                # FIXED: Look up using just the raw 'county' string key to match ground_truth dict
                observed = ground_truth_observations.get(county, "UNKNOWN")
                
                # Safety fallback check in case of key matching variations
                if observed == "UNKNOWN":
                    is_accurate = False
                    status = "❓ UNKNOWN BASELINE"
                else:
                    is_accurate = prediction["tier"] == observed
                    if is_accurate:
                        correct_predictions += 1
                        status = "✅ PASS"
                    else:
                        status = "❌ FALSE ALARM" if prediction["tier"] in ["RED", "AMBER"] else "❌ MISS"

                audit_log.append({
                    "Location": county,
                    "Model Prob": f"{prediction['P_final']*100:.1f}%",
                    "Predicted Tier": prediction["tier"],
                    "Observed Event": observed,
                    "Audit Status": status,
                })

# Compute exact Model Performance Rating
if total_nodes > 0:
    confidence_score = (correct_predictions / total_nodes) * 100
else:
    confidence_score = 0.0

# ==============================================================================
# 📊 NATIVE STREAMLIT INTERFACE RENDER 
# ==============================================================================
st.markdown("### 🔍 24-Hour Blended Prediction Engine Audit Log")

# Render metrics summary cards side-by-side
col1, col2 = st.columns(2)
with col1:
    st.metric("System Performance Rating", f"{confidence_score:.1f}% Accuracy")
with col2:
    st.metric("Total Monitored Leaf Nodes", f"{total_nodes}")

# Display the evaluation dataset in an interactive web spreadsheet grid
df = pd.DataFrame(audit_log)
st.dataframe(df, use_container_width=True)
