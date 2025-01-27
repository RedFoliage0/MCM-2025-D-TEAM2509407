import geopandas as gpd
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.model_selection import KFold
from sklearn.metrics import silhouette_score
import folium
#This code is the Kmeans clustering of traffic flow and visualizes the centers of the clustering within a limited range
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
best_k = 2
best_score = -1
kf = KFold(n_splits=5, shuffle=True, random_state=42)
for k in range(2, 101):
    scores = []
    for train_index, test_index in kf.split(X):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(X[train_index])
        score = silhouette_score(X[test_index], kmeans.predict(X[test_index]))
        scores.append(score)
    avg_score = np.mean(scores)
    if avg_score > best_score:
        best_score = avg_score
        best_k = k
kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
gdf['cluster'] = kmeans.fit_predict(X)
cluster_centers = pd.DataFrame(kmeans.cluster_centers_, columns=['lat', 'lon'])
cluster_centers['avg_traffic'] = gdf.groupby('cluster')['avg_traffic'].mean().values
baltimore_map = folium.Map(location=[39.2904, -76.6122], zoom_start=12)
for _, row in cluster_centers.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=row['avg_traffic'] / 1000,
        color="red",
        fill=True,
        fill_color="darkred",
        fill_opacity=0.7,
        popup=f"Traffic: {row['avg_traffic']:.0f}"
    ).add_to(baltimore_map)
baltimore_map.save("Traffic_Flow_Kmeans.html")
print("Map has been saved as a html file.")

