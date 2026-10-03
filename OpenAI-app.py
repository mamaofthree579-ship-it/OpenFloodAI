import json
import os
from datetime import datetime
import streamlit as st

# 1. Page Configuration & Custom Theme Styling
st.set_page_config(
    page_title="OpenFloodAI — Global Flood Forecasts",
    page_icon="🌊",
    layout="centered",
)

# Inject custom CSS to match your original UI styling
st.markdown(
    """
    <style>
    /* Global Styles */
    .stApp {
        background-color: #eef6ff;
    }
    h1, h2, h3, p, label {
        color: #333333 !important;
    }
    
    /* Header Container */
    .custom-header {
        background-color: #0077cc;
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 25px;
    }
    .custom-header h1 {
        color: white !important;
        margin: 0;
        font-size: 1.6em;
    }
    .custom-header div {
        font-size: 0.9em;
    }
    
    /* Risk Tier Badges & Row Backgrounds */
    .tier-card {
        padding: 15px;
        border-radius: 6px;
        margin-top: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .RED { background-color: #ffb3b3; color: #b30000; }
    .AMBER { background-color: #fff2b3; color: #8a6d3b; }
    .GREEN { background-color: #c6f6c3; color: #1e5a1e; }
    
    /* Progress Bar Layout */
    .bar-container {
        width: 100%;
        background-color: #e6e6e6;
        border-radius: 4px;
        overflow: hidden;
        height: 12px;
        margin-top: 6px;
    }
    .bar { height: 12px; }
    .bar.RED { background-color: #ff4d4d; }
    .bar.AMBER { background-color: #ffc107; }
    .bar.GREEN { background-color: #28a745; }
    
    /* Diagnostic Box */
    pre {
        background-color: #f8f9fa;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
        color: #333;
    }
    
    /* Footer */
    .custom-footer {
        background-color: #0077cc;
        color: white !important;
        padding: 10px;
        text-align: center;
        border-radius: 8px;
        margin-top: 40px;
        font-size: 0.9em;
    }
    </style>
    """,
    unsafe_html=True,
)


# 2. Data Loading Function
@st.cache_data(ttl=60)  # Caches data for 60 seconds, acting like your cache-buster (?cb=)
def load_forecast_data():
    data_path = os.path.join("data", "outputs", "all_forecasts.json")
    try:
        with open(data_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


# Load JSON Data
data = load_forecast_data()

# 3. Render Header
if data and "timestamp" in data:
    # Format timestamp similarly to JavaScript's toLocaleString()
    formatted_time = datetime.fromisoformat(
        data["timestamp"].replace("Z", "+00:00")
    ).strftime("%m/%d/%Y, %I:%M:%S %p")
    header_time_html = f"Updated: {formatted_time}"
else:
    header_time_html = "⚠️ Could not load forecast data."

st.markdown(
    f"""
    <div class="custom-header">
        <h1>🌊 OpenFloodAI — Global Dashboard</h1>
        <div>{header_time_html}</div>
    </div>
    """,
    unsafe_html=True,
)

# 4. Application Logic / Dropdowns
if data and "forecasts" in data:
    forecasts = data["forecasts"]

    # Country Selector
    countries = ["-- Choose a Country --"] + sorted(list(forecasts.keys()))
    selected_country = st.selectbox("🌍 Select Country:", options=countries)

    # Region Selector (depends on selected country)
    if selected_country != "-- Choose a Country --":
        regions = ["-- Choose a Region --"] + sorted(
            list(forecasts[selected_country].keys())
        )
        selected_region = st.selectbox("🏙️ Select Region:", options=regions)
    else:
        st.selectbox("🏙️ Select Region:", options=["-- Choose a Region --"], disabled=True)
        selected_region = "-- Choose a Region --"

    # 5. Render Forecast Details & Table Metrics
    if (
        selected_country != "-- Choose a Country --"
        and selected_region != "-- Choose a Region --"
    ):
        entry = forecasts[selected_country][selected_region]

        # Extract values
        tier = entry.get("tier", "GREEN").upper()
        p_final = entry.get("P_final", 0.0)
        probability = p_final * 100
        generated_utc = entry.get("generated_utc", data["timestamp"])

        # Display Forecast Metrics Table Row alternative styled in HTML
        st.markdown("### 📊 Active Forecast Overview")
        st.markdown(
            f"""
            <div class="tier-card {tier}">
                <h3><strong>Region:</strong> {selected_region}</h3>
                <p><strong>Risk Tier:</strong> <span style="font-weight:bold;">{tier}</span></p>
                <p><strong>Flood Probability:</strong> {probability:.1f}%</p>
                <div class="bar-container">
                    <div class="bar {tier}" style="width:{probability}%"></div>
                </div>
            </div>
            """,
            unsafe_html=True,
        )

        # Extended Metadata & Diagnostics (from your second JS block script)
        st.markdown("---")
        st.markdown(f"**Model v1.0.1** • Generated: `{generated_utc}`")

        # Diagnostics section
        if "diagnostics" in entry:
            st.markdown("#### Diagnostics JSON:")
            st.json(entry["diagnostics"])

else:
    st.error(
        "No forecast data available. Please ensure your `data/outputs/all_forecasts.json` file exists."
    )

# 6. Render Footer
st.markdown(
    """
    <div class="custom-footer">
        🌍 OpenFloodAI — Open & Community Flood Forecasting
    </div>
    """,
    unsafe_html=True,
)
