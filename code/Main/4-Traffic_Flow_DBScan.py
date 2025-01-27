import geopandas as gpd
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import folium
#This code is the DBScan clustering of traffic flow and visualizes the centers of the clustering within a limited range
file_path = "MDOT_SHA_Annual_Average_Daily_Traffic_Baltimore.geojson"
gdf = gpd.read_file(file_path)
BALTIMORE_BOUNDARIES = {
    "lat_min": 39.19703,
    "lat_max": 39.37301,
    "lon_min": -76.71234,
    "lon_max": -76.44796
}
gdf = gdf.dropna(subset=['geometry'])
gdf['lat'] = gdf.geometry.y
gdf['lon'] = gdf.geometry.x
gdf = gdf[(gdf['lat'] >= BALTIMORE_BOUNDARIES['lat_min']) & 
          (gdf['lat'] <= BALTIMORE_BOUNDARIES['lat_max']) &
          (gdf['lon'] >= BALTIMORE_BOUNDARIES['lon_min']) & 
          (gdf['lon'] <= BALTIMORE_BOUNDARIES['lon_max'])]
traffic_cols = [col for col in gdf.columns if 'AADT' in col]
gdf['avg_traffic'] = gdf[traffic_cols].astype(float).mean(axis=1, skipna=True)
X = gdf[['lat', 'lon']].values
dbscan = DBSCAN(eps=0.005, min_samples=10)
gdf['cluster'] = dbscan.fit_predict(X)
cluster_centers = gdf.groupby('cluster').agg({'lat': 'mean', 'lon': 'mean', 'avg_traffic': 'mean'}).reset_index()
baltimore_map = folium.Map(location=[39.2904, -76.6122], zoom_start=12)
for _, row in cluster_centers.iterrows():
    if row['cluster'] != -1:
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=row['avg_traffic'] / 1000,
            color="blue",
            fill=True,
            fill_color="darkblue",
            fill_opacity=0.7,
            popup=f"Traffic: {row['avg_traffic']:.0f}"
        ).add_to(baltimore_map)
baltimore_map.save("Traffic_Flow_DBSCAN.html")
print("Map has been saved as a html file.")