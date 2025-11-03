# make_baseline_map_offline.py
import geopandas as gpd
from shapely.geometry import Polygon, LineString
import rasterio
from rasterio.plot import show as rshow
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

# ------------------------------
# CONFIG - adjust paths as needed
# ------------------------------
gauge_csv = "data/raw/usgs_11425500_meta.csv"   # optional
dem_tif = "data/raw/dem_sacramento_10m.tif"    # optional
nlcd_tif = "data/raw/nlcd_2019_ca_clip.tif"    # optional
roads_shp = "data/raw/roads.shp"               # optional

out_gpkg = "outputs/sacramento_baseline.gpkg"
out_png = "outputs/sacramento_baseline_map.png"

os.makedirs("outputs", exist_ok=True)

# ------------------------------
# OFFLINE SYNTHETIC VECTOR LAYERS
# ------------------------------
# Synthetic catchment polygon
catch_poly = Polygon([
    (-121.7, 38.6),
    (-121.5, 38.6),
    (-121.5, 38.8),
    (-121.7, 38.8),
    (-121.7, 38.6)
])
catch = gpd.GeoDataFrame({"id":[1]}, geometry=[catch_poly], crs="EPSG:4326").to_crs("EPSG:3857")

# Synthetic streams
stream_lines = [
    LineString([(-121.68, 38.6), (-121.68, 38.8)]),
    LineString([(-121.55, 38.6), (-121.55, 38.8)]),
]
streams = gpd.GeoDataFrame({"name": ["stream1", "stream2"]},
                           geometry=stream_lines, crs="EPSG:4326").to_crs("EPSG:3857")

# Synthetic roads (optional, very simple)
road_lines = [
    LineString([(-121.7, 38.7), (-121.5, 38.7)]),
]
roads = gpd.GeoDataFrame({"name": ["road1"]}, geometry=road_lines, crs="EPSG:4326").to_crs("EPSG:3857")

# ------------------------------
# GAUGE POINT
# ------------------------------
if os.path.exists(gauge_csv):
    g = pd.read_csv(gauge_csv)
    gauge_gdf = gpd.GeoDataFrame(
        g, geometry=gpd.points_from_xy(g.longitude, g.latitude), crs="EPSG:4326"
    ).to_crs("EPSG:3857")
else:
    gauge_gdf = gpd.GeoDataFrame(
        {"id":[11425500]},
        geometry=gpd.points_from_xy([-121.59722],[38.77444]),
        crs="EPSG:4326"
    ).to_crs("EPSG:3857")

# ------------------------------
# SAVE TO GeoPackage
# ------------------------------
catch.to_file(out_gpkg, layer="catchment", driver="GPKG")
streams.to_file(out_gpkg, layer="streams", driver="GPKG")
roads.to_file(out_gpkg, layer="roads", driver="GPKG")
gauge_gdf.to_file(out_gpkg, layer="gauge", driver="GPKG")

# ------------------------------
# READ DEM IF AVAILABLE
# ------------------------------
if os.path.exists(dem_tif):
    with rasterio.open(dem_tif) as dem:
        dem_data = dem.read(1)
        dem_affine = dem.transform
        dem_crs = dem.crs

    # Compute hillshade
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
    dem_data = None
    hs = None

# ------------------------------
# PLOT
# ------------------------------
fig, ax = plt.subplots(1,1, figsize=(11,11))

# hillshade background
if hs is not None:
    rshow(hs, transform=dem_affine, ax=ax, cmap='Greys', alpha=0.7)

# overlay NLCD if available
if os.path.exists(nlcd_tif):
    with rasterio.open(nlcd_tif) as nl:
        nl_data = nl.read(1)
        rshow(nl_data, transform=nl.transform, ax=ax, cmap='tab20', alpha=0.5)

# plot vectors
catch.boundary.plot(ax=ax, color='black', linewidth=1.2)
streams.plot(ax=ax, linewidth=0.6, color='blue')
roads.plot(ax=ax, linewidth=0.4, color='grey')
gauge_gdf.plot(ax=ax, color='red', markersize=50, label='USGS Gauge 11425500')

ax.set_title("Sacramento - Verona Baseline Environmental Map (Offline)")
ax.axis('off')
plt.legend()

# save and show
plt.savefig(out_png, dpi=300, bbox_inches='tight')
plt.show()
print("✅ Offline map complete. Saved:", out_gpkg, out_png)
