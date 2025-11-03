# make_baseline_map.py
import geopandas as gpd

catchment_shp = "/path/to/your/catchment.shp"
print("Reading:", catchment_shp)
catch = gpd.read_file(catchment_shp)
print(catch.head())
print(catch.crs)
catch = catch.to_crs("EPSG:3857")

import rasterio
from rasterio.plot import show as rshow
import matplotlib.pyplot as plt
import numpy as np
import os
print(os.path.exists(catchment_shp))
print(catchment_shp)

# CONFIG - edit filepaths as needed
gauge_csv = "data/raw/usgs_11425500_meta.csv"   # optional
catchment_shp = "data/static/sacramento_verona_catchment.shp"
dem_tif = "data/raw/dem_sacramento_10m.tif"
nlcd_tif = "data/raw/nlcd_2019_ca_clip.tif"
smap_tif = "data/raw/smap_sacramento_anom.tif"  # optional
streams_shp = "data/raw/nhd_streams.shp"
roads_shp = "data/raw/roads.shp"

out_gpkg = "outputs/sacramento_baseline.gpkg"
out_png = "outputs/sacramento_baseline_map.png"

os.makedirs("outputs", exist_ok=True)

# load vector layers
catch = gpd.read_file(catchment_shp).to_crs("EPSG:3857")
streams = gpd.read_file(streams_shp).to_crs("EPSG:3857")
roads = gpd.read_file(roads_shp).to_crs("EPSG:3857")

# quick gauge point if available
if os.path.exists(gauge_csv):
    import pandas as pd
    g = pd.read_csv(gauge_csv)
    gauge_gdf = gpd.GeoDataFrame(g, geometry=gpd.points_from_xy(g.longitude, g.latitude), crs="EPSG:4326").to_crs("EPSG:3857")
else:
    # fallback coords from USGS site: lat 38.77444, lon -121.59722 (example)
    gauge_gdf = gpd.GeoDataFrame({"id":[11425500]}, geometry=gpd.points_from_xy([-121.59722],[38.77444]), crs="EPSG:4326").to_crs("EPSG:3857")

# create GeoPackage with layers
catch.to_file(out_gpkg, layer="catchment", driver="GPKG")
streams.to_file(out_gpkg, layer="streams", driver="GPKG")
roads.to_file(out_gpkg, layer="roads", driver="GPKG")
gauge_gdf.to_file(out_gpkg, layer="gauge", driver="GPKG")

# Read DEM for visualization
with rasterio.open(dem_tif) as dem:
    dem_data = dem.read(1)
    dem_affine = dem.transform
    dem_crs = dem.crs

# Compute hillshade
x, y = np.gradient(dem_data.astype(float), 1, 1)
slope = np.pi/2.0 - np.arctan(np.sqrt(x*x + y*y))
aspect = np.arctan2(-x, y)
azimuth = 315.0 # degrees
altitude = 45.0
az_rad = np.deg2rad(azimuth)
alt_rad = np.deg2rad(altitude)
hs = np.sin(alt_rad)*np.sin(slope) + np.cos(alt_rad)*np.cos(slope)*np.cos(az_rad - aspect)
hs = (hs - hs.min()) / (hs.max() - hs.min())

# Start plot
fig, ax = plt.subplots(1,1, figsize=(11,11))
# show hillshade
rshow(hs, transform=dem_affine, ax=ax, cmap='Greys', alpha=0.7)

# overlay nlcd if available
if os.path.exists(nlcd_tif):
    with rasterio.open(nlcd_tif) as nl:
        nl_data = nl.read(1)
        # simple mask to catchment bounding box
        rshow(nl_data, transform=nl.transform, ax=ax, cmap='tab20', alpha=0.5)

# plot vectors
streams.plot(ax=ax, linewidth=0.6, color='blue')
roads.plot(ax=ax, linewidth=0.4, color='grey')
catch.boundary.plot(ax=ax, color='black', linewidth=1.2)
gauge_gdf.plot(ax=ax, color='red', markersize=50, label='USGS Gauge 11425500')

ax.set_title("Sacramento - Verona Baseline Environmental Map")
ax.axis('off')
plt.legend()
plt.savefig(out_png, dpi=300, bbox_inches='tight')
print("Wrote:", out_gpkg, out_png)
