# file: run_accuracy_audit.py
import json
import os
import pandas as pd


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
    if any(
        s in region_string
        for s in ["Texas", "Florida", "Louisiana", "Bangladesh", "Philippines"]
    ):
        region_factor += 0.25
    if any(
        s in region_string for s in ["California", "Spain", "Morocco", "Chile"]
    ):
        region_factor -= 0.15

    P_final = max(0.0, min(1.0, base_prob * region_factor))
    tier = (
        "RED" if P_final >= 0.75 else ("AMBER" if P_final >= 0.40 else "GREEN")
    )
    return {"P_final": round(P_final, 3), "tier": tier}


# Load database target
with open(os.path.join("data", "outputs", "all_forecasts.json"), "r") as f:
    db = json.load(f)

# Real 24hr observed outcomes to verify calibration accuracy
ground_truth_observations = {
    "Baltimore County": "RED",
    "Howard County": "GREEN",  # Model predicts AMBER (False Alarm Risk check)
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
                location_str = f"{county} ({state}, {country})"

                # Pass node variables through updated calculations
                prediction = evaluate_engine_logic(metrics, location_str)

                observed = ground_truth_observations.get(county, "UNKNOWN")
                is_accurate = prediction["tier"] == observed

                if is_accurate:
                    correct_predictions += 1
                    status = "✅ PASS"
                else:
                    status = (
                        "❌ FALSE ALARM"
                        if prediction["tier"] == "RED" or prediction["tier"] == "AMBER"
                        else "❌ MISS"
                    )

                audit_log.append(
                    {
                        "Location": county,
                        "Model Prob": f"{prediction['P_final']*100:.1f}%",
                        "Predicted Tier": prediction["tier"],
                        "Observed Event": observed,
                        "Audit Status": status,
                    }
                )

# Compute exact Model Performance Rating
confidence_score = (correct_predictions / total_nodes) * 100

# Present audit metrics
print("\n=== 🔍 24-HOUR BLENDED PREDICTION ENGINE AUDIT LOG ===")
df = pd.DataFrame(audit_log)
print(df.to_markdown(index=False))
print("\n" + "=" * 55)
print(
    f"🏆 SYSTEM PERFORMANCE RATING: {confidence_score:.1f}% ACCURACY"
)
print("=" * 55 + "\n")

# Streamlit dashboard UI area
st.markdown("### 🔍 24-Hour Blended Prediction Engine Audit Log")
st.dataframe(df, use_container_width=True)
st.metric("System Performance Rating", f"{confidence_score:.1f}% Accuracy")

