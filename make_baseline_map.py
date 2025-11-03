#!/usr/bin/env python3
"""
make_baseline_map.py
Generates a baseline environmental map centered on the Sacramento–Verona USGS gauge.

Features:
 - Auto-fetch catchment basin geometry from USGS NLDI API (live open data)
 - Reads DEM, land cover, streams, and roads
 - Creates GeoPackage + PNG map outputs
"""

import os
import geopandas as gpd
import pandas as pd
import requests
import rasterio
from rasterio.plot import show as rshow
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon

# -----------------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------------
GAUGE_ID = "11425500"  # USGS gauge for Sacramento–Verona
OUT_DIR = "outputs"
os.makedirs(OUT_DIR, exist_ok=True)

gauge_csv = "data/raw/usgs_11425500_meta.csv"   # optional
dem_tif = "data/raw/dem_sacramento_10m.tif"
nlcd_tif = "data/raw/nlcd_2019_ca_clip.tif"
smap_tif = "data/raw/smap_sacramento_anom.tif"  # optional
streams_shp = "data/raw/nhd_streams.shp"
roads_shp = "data/raw/roads.shp"

out_gpkg = os.path.join(OUT_DIR, "sacramento_baseline.gpkg")
out_png = os.path.join(OUT_DIR, "sacramento_baseline_map.png")

# -----------------------------------------------------------------------------
# LOAD / FETCH CATCHMENT
# -----------------------------------------------------------------------------
nldi_url = f"https://labs.waterdata.usgs.gov/api/nldi/linked-data/nwissite/USGS-{GAUGE_ID}/basin"

print("Fetching catchment from:", nldi_url)
try:
    catch = gpd.read_file(nldi_url).to_crs("EPSG:3857")
    print("✅ Retrieved catchment from USGS NLDI API")
except Exception as e:
    print(f"⚠️ Failed to load catchment from NLDI ({e}). Using fallback polygon.")
    poly = Polygon([
        (-121.7, 38.6),
        (-121.5, 38.6),
        (-121.5, 38.8),
        (-121.7, 38.8),
        (-121.7, 38.6)
    ])
    catch = gpd.GeoDataFrame({"name": ["fallback_catchment"]},
                              geometry=[poly],
                              crs="EPSG:4326").to_crs("EPSG:3857")

# -----------------------------------------------------------------------------
# LOAD VECTOR LAYERS (if they exist)
# -----------------------------------------------------------------------------
def safe_read_vector(path):
    if os.path.exists(path):
        print(f"Loading {path}")
        return gpd.read_file(path).to_crs("EPSG:3857")
    else:
        print(f"⚠️ Missing vector file: {path}")
        return gpd.GeoDataFrame(geometry=[], crs="EPSG:3857")

streams = safe_read_vector(streams_shp)
roads = safe_read_vector(roads_shp)

# -----------------------------------------------------------------------------
# LOAD GAUGE POINT
# -----------------------------------------------------------------------------
if os.path.exists(gauge_csv):
    print(f"Loading gauge metadata: {gauge_csv}")
    g = pd.read_csv(gauge_csv)
    gauge_gdf = gpd.GeoDataFrame(
        g,
        geometry=gpd.points_from_xy(g.longitude, g.latitude),
        crs="EPSG:4326"
    ).to_crs("EPSG:3857")
else:
    print("Using default gauge coordinates.")
    gauge_gdf = gpd.GeoDataFrame(
        {"id": [GAUGE_ID]},
        geometry=gpd.points_from_xy([-121.59722], [38.77444]),
        crs="EPSG:4326"
    ).to_crs("EPSG:3857")

# -----------------------------------------------------------------------------
# SAVE GEOPACKAGE
# -----------------------------------------------------------------------------
print("Writing GeoPackage:", out_gpkg)
catch.to_file(out_gpkg, layer="catchment", driver="GPKG")
if not streams.empty:
    streams.to_file(out_gpkg, layer="streams", driver="GPKG")
if not roads.empty:
    roads.to_file(out_gpkg, layer="roads", driver="GPKG")
gauge_gdf.to_file(out_gpkg, layer="gauge", driver="GPKG")

# -----------------------------------------------------------------------------
# DEM + HILLSHADE
# -----------------------------------------------------------------------------
if os.path.exists(dem_tif):
    print("Reading DEM:", dem_tif)
    with rasterio.open(dem_tif) as dem:
        dem_data = dem.read(1)
        dem_affine = dem.transform
        dem_crs = dem.crs

    x, y = np.gradient(dem_data.astype(float), 1, 1)
    slope = np.pi/2.0 - np.arctan(np.sqrt(x*x + y*y))
    aspect = np.arctan2(-x, y)
    azimuth = 315.0
    altitude = 45.0
    az_rad = np.deg2rad(azimuth)
    alt_rad = np.deg2rad(altitude)
    hs = np.sin(alt_rad)*np.sin(slope) + np.cos(alt_rad)*np.cos(slope)*np.cos(az_rad - aspect)
    hs = (hs - hs.min()) / (hs.max() - hs.min())
else:
    print(f"⚠️ DEM file missing: {dem_tif}")
    hs, dem_affine = None, None

# -----------------------------------------------------------------------------
# PLOTTING
# -----------------------------------------------------------------------------
print("Generating map...")
fig, ax = plt.subplots(1, 1, figsize=(11, 11))

if hs is not None:
    rshow(hs, transform=dem_affine, ax=ax, cmap='Greys', alpha=0.7)

# Overlay land cover if present
if os.path.exists(nlcd_tif):
    with rasterio.open(nlcd_tif) as nl:
        nl_data = nl.read(1)
        rshow(nl_data, transform=nl.transform, ax=ax, cmap='tab20', alpha=0.4)

# Plot vector layers
if not streams.empty:
    streams.plot(ax=ax, linewidth=0.6, color='blue', label="Streams")
if not roads.empty:
    roads.plot(ax=ax, linewidth=0.4, color='grey', label="Roads")

catch.boundary.plot(ax=ax, color='black', linewidth=1.2, label="Catchment")
gauge_gdf.plot(ax=ax, color='red', markersize=50, label=f'USGS Gauge {GAUGE_ID}')

ax.set_title("Sacramento–Verona Baseline Environmental Map", fontsize=14)
ax.axis('off')
plt.legend()
plt.savefig(out_png, dpi=300, bbox_inches='tight')
plt.close()

print(f"✅ Map and data written to:\n  {out_gpkg}\n  {out_png}")
