import json
import os
from datetime import datetime
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="OpenFloodAI — Global Forecasts",
    page_icon="🌊",
    layout="centered",
)

# 2. Inject CSS Styles to Match the New HTML Spec
st.markdown(
    """
    <style>
    .stApp { background-color: #eef6ff; }
    h1, h2, h3, p, label { color: #333333 !important; }
    
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
    .custom-header h1 { color: white !important; margin: 0; font-size: 1.6em; }
    .custom-header div { font-size: 0.9em; }
    
    /* Table Styling mimicking HTML structure */
    .forecast-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        background: white;
        border-radius: 6px;
        overflow: hidden;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .forecast-table th, .forecast-table td {
        border-bottom: 1px solid #ddd;
        text-align: center;
        padding: 12px;
        color: #333;
    }
    .forecast-table th { background-color: #0077cc; color: white !important; }
    
    /* Risk Tier Row Background Colors */
    .RED { background-color: #ffb3b3; }
    .AMBER { background-color: #fff2b3; }
    .GREEN { background-color: #c6f6c3; }
    
    /* Probability Bar Layout */
    .bar-container {
        width: 100%;
        background-color: #e6e6e6;
        border-radius: 4px;
        overflow: hidden;
        height: 12px;
        margin-top: 4px;
    }
    .bar { height: 12px; }
    .bar.RED { background-color: #ff4d4d; }
    .bar.AMBER { background-color: #ffc107; }
    .bar.GREEN { background-color: #28a745; }
    
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
    unsafe_allow_html=True,
)

# 3. Data Loading Function
@st.cache_data(ttl=60)
def load_forecast_data():
    data_path = os.path.join("data", "outputs", "all_forecasts.json")
    try:
        with open(data_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

data = load_forecast_data()

# 4. Render Dynamic Header Timestamp
if data and "timestamp" in data:
    try:
        formatted_time = datetime.fromisoformat(
            data["timestamp"].replace("Z", "+00:00")
        ).strftime("%m/%d/%Y, %I:%M:%S %p")
        header_time = f"Updated: {formatted_time}"
    except Exception:
        header_time = f"Updated: {data['timestamp']}"
else:
    header_time = "⚠️ Could not load forecast data."

st.markdown(
    f"""
    <div class="custom-header">
        <h1>🌊 OpenFloodAI — Global Forecasts</h1>
        <div>{header_time}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# 5. Cascading Deep Dropdowns Architecture
if data and "forecasts" in data:
    forecasts = data["forecasts"]

    # --- 1. CONTINENT ---
    continents = ["-- Choose Continent --"] + sorted(list(forecasts.keys()))
    sel_continent = st.selectbox("🌎 Continent:", options=continents)

    # --- 2. COUNTRY ---
    if sel_continent != "-- Choose Continent --" and sel_continent in forecasts:
        countries = ["-- Choose Country --"] + sorted(list(forecasts[sel_continent].keys()))
        sel_country = st.selectbox("🌍 Country:", options=countries)
    else:
        st.selectbox("🌍 Country:", options=["-- Choose Country --"], disabled=True)
        sel_country = "-- Choose Country --"

    # --- 3. STATE / REGION ---
    if sel_country != "-- Choose Country --" and sel_country in forecasts.get(sel_continent, {}):
        states = ["-- Choose State/Region --"] + sorted(list(forecasts[sel_continent][sel_country].keys()))
        sel_state = st.selectbox("🏙️ State/Region:", options=states)
    else:
        st.selectbox("🏙️ State/Region:", options=["-- Choose State/Region --"], disabled=True)
        sel_state = "-- Choose State/Region --"

    # --- 4. COUNTY ---
    if sel_state != "-- Choose State/Region --" and sel_state in forecasts.get(sel_continent, {}).get(sel_country, {}):
        counties = ["-- Choose County --"] + sorted(list(forecasts[sel_continent][sel_country][sel_state].keys()))
        sel_county = st.selectbox("📍 County:", options=counties)
    else:
        st.selectbox("📍 County:", options=["-- Choose County --"], disabled=True)
        sel_county = "-- Choose County --"

    # 6. Render the Interactive Dynamic Forecast Table Row
    if (
        sel_continent != "-- Choose Continent --"
        and sel_country != "-- Choose Country --"
        and sel_state != "-- Choose State/Region --"
        and sel_county != "-- Choose County --"
    ):
        # Fetching nested leaf values safely
        try:
            values = forecasts[sel_continent][sel_country][sel_state][sel_county]
            tier = str(values.get("tier", "GREEN")).upper()
            p_final = values.get("P_final", 0.0)
            probability = p_final * 100

            # Generate identical design layout structure using HTML table mapping
            st.markdown(
                f"""
                <table class="forecast-table">
                    <thead>
                        <tr>
                            <th>Location</th>
                            <th>Flood Probability</th>
                            <th>Tier</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="{tier}">
                            <td><strong>{sel_county}</strong></td>
                            <td>
                                {probability:.1f}%
                                <div class="bar-container">
                                    <div class="bar {tier}" style="width:{probability}%"></div>
                                </div>
                            </td>
                            <td><strong>{tier}</strong></td>
                        </tr>
                    </tbody>
                </table>
                """,
                unsafe_allow_html=True,
            )
        except KeyError:
            st.error("⚠️ Data mismatch encountered mapping this specific path branch sequence.")
else:
    st.error("No valid multi-tier nesting parameters found in `all_forecasts.json` structure.")

# 7. Layout Footer
st.markdown(
    """
    <div class="custom-footer">
        🌍 OpenFloodAI — Open & Community Flood Forecasting
    </div>
    """,
    unsafe_allow_html=True,
)
