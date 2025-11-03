# # make_baseline_map_streamlit.py
import streamlit as st
import geopandas as gpd
from shapely.geometry import Polygon, LineString
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

st.set_page_config(page_title="Offline Sacramento Baseline Map", layout="wide")
st.title("🗺️ Sacramento – Verona Offline Baseline Map")

# -----------------------------------
# OFFLINE SYNTHETIC VECTOR LAYERS
# -----------------------------------
catch_poly = Polygon([
    (-121.7, 38.6), (-121.5, 38.6), (-121.5, 38.8),
    (-121.7, 38.8), (-121.7, 38.6)
])
catch = gpd.GeoDataFrame({"id": [1]}, geometry=[catch_poly], crs="EPSG:4326").to_crs("EPSG:3857")

stream_lines = [
    LineString([(-121.68, 38.6), (-121.68, 38.8)]),
    LineString([(-121.55, 38.6), (-121.55, 38.8)]),
]
streams = gpd.GeoDataFrame({"name": ["stream1", "stream2"]},
                           geometry=stream_lines, crs="EPSG:4326").to_crs("EPSG:3857")

roads = gpd.GeoDataFrame({"name": ["road1"]},
                         geometry=[LineString([(-121.7, 38.7), (-121.5, 38.7)])],
                         crs="EPSG:4326").to_crs("EPSG:3857")

# Gauge point
gauge_gdf = gpd.GeoDataFrame(
    {"id": [11425500]},
    geometry=gpd.points_from_xy([-121.59722], [38.77444]),
    crs="EPSG:4326"
).to_crs("EPSG:3857")

# -----------------------------------
# PLOT
# -----------------------------------
fig, ax = plt.subplots(figsize=(11, 11))

catch.boundary.plot(ax=ax, color="black", linewidth=1.2)
streams.plot(ax=ax, linewidth=0.6, color="blue")
roads.plot(ax=ax, linewidth=0.4, color="grey")
gauge_gdf.plot(ax=ax, color="red", markersize=50, label="USGS Gauge 11425500")

ax.set_title("Sacramento - Verona Baseline Environmental Map (Offline)")
ax.axis("off")
plt.legend()

# ✅ Show map in Streamlit
st.pyplot(fig)
