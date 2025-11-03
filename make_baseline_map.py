import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString
import pandas as pd
import requests, json, os

# -----------------------------
# Streamlit page setup
# -----------------------------
st.set_page_config(page_title="Sacramento – Verona Baseline Map", layout="wide")
st.title("🗺️ Sacramento – Verona Baseline Map (Hybrid Online/Offline)")

# -----------------------------
# Try to fetch live NLDI basin
# -----------------------------
@st.cache_data(show_spinner=False)
def fetch_nldi_feature(gauge_id, feature_type):
    """
    Fetch GeoJSON from USGS NLDI using the current API base.
    feature_type: 'basin' or 'navigate/UM/flowlines'
    """
    base = "https://labs.waterdata.usgs.gov/api/nldi/nwissite"
    url = f"{base}/USGS-{gauge_id}/{feature_type}"
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        return gpd.read_file(json.dumps(r.json()))
    except Exception as e:
        st.warning(f"⚠️ Live NLDI data unavailable ({e})")
        return None

gauge_id = "11425500"

st.info("Attempting to load live USGS NLDI basin and flowlines...")

catch = fetch_nldi_feature(gauge_id, "basin")
streams = fetch_nldi_feature(gauge_id, "navigate/UM/flowlines")

# -----------------------------
# Offline fallback if needed
# -----------------------------
if catch is None or streams is None:
    st.write("🔁 Using offline synthetic data instead (no internet or USGS API down).")

    catch_poly = Polygon([
        (-121.7, 38.6), (-121.5, 38.6),
        (-121.5, 38.8), (-121.7, 38.8),
        (-121.7, 38.6)
    ])
    catch = gpd.GeoDataFrame({"id": [1]}, geometry=[catch_poly], crs="EPSG:4326")

    streams = gpd.GeoDataFrame(
        {"name": ["stream1", "stream2"]},
        geometry=[
            LineString([(-121.68, 38.6), (-121.68, 38.8)]),
            LineString([(-121.55, 38.6), (-121.55, 38.8)]),
        ],
        crs="EPSG:4326"
    )

catch = catch.to_crs("EPSG:3857")
streams = streams.to_crs("EPSG:3857")

roads = gpd.GeoDataFrame(
    {"name": ["road1"]},
    geometry=[LineString([(-121.7, 38.7), (-121.5, 38.7)])],
    crs="EPSG:4326"
).to_crs("EPSG:3857")

gauge_gdf = gpd.GeoDataFrame(
    {"id": [11425500]},
    geometry=gpd.points_from_xy([-121.59722], [38.77444]),
    crs="EPSG:4326"
).to_crs("EPSG:3857")

# -----------------------------
# Plot map
# -----------------------------
fig, ax = plt.subplots(figsize=(10, 10))

catch.boundary.plot(ax=ax, color="black", linewidth=1.2, label="Catchment")
streams.plot(ax=ax, color="blue", linewidth=0.8, label="Streams")
roads.plot(ax=ax, color="grey", linewidth=0.4, label="Roads")
gauge_gdf.plot(ax=ax, color="red", markersize=50, label="USGS Gauge 11425500")

ax.set_title("Sacramento – Verona Baseline Map (Hybrid Mode)")
ax.axis("off")
ax.legend()

st.pyplot(fig)

# -----------------------------
# Footer
# -----------------------------
st.caption("🛰️ Displays live USGS NLDI data when available; otherwise uses offline synthetic geometry.")
