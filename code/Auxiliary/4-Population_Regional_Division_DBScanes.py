import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import folium
#This code is the DBScan clustering of population and visualizes the centers of the clustering
file_path = 'Population_regional_division.csv'
data = pd.read_csv(file_path)
BALTIMORE_BOUNDARIES = {
    "lat_min": 39.19703,
    "lat_max": 39.37301,
    "lon_min": -76.71234,
    "lon_max": -76.44796
}
filtered_data = data[
    (data['INTPTLAT20'] >= BALTIMORE_BOUNDARIES['lat_min']) & 
    (data['INTPTLAT20'] <= BALTIMORE_BOUNDARIES['lat_max']) & 
    (data['INTPTLON20'] >= BALTIMORE_BOUNDARIES['lon_min']) & 
    (data['INTPTLON20'] <= BALTIMORE_BOUNDARIES['lon_max'])
]
X = filtered_data[['INTPTLAT20', 'INTPTLON20']].values
dbscan = DBSCAN(eps=0.01, min_samples=5)
filtered_data['cluster'] = dbscan.fit_predict(X)
num_noise_points = (filtered_data['cluster'] == -1).sum()
print(f"The number of Noise Point: {num_noise_points}")
cluster_sizes = filtered_data['cluster'].value_counts()
print(f"The size of each cluster: \n{cluster_sizes}")
cluster_populations = filtered_data.groupby('cluster')['population'].sum()
m = folium.Map(location=[39.29, -76.61], zoom_start=12)
for cluster_id in cluster_populations.index:
    if cluster_id != -1:
        cluster_data = filtered_data[filtered_data['cluster'] == cluster_id]
        center_lat = cluster_data['INTPTLAT20'].mean()
        center_lon = cluster_data['INTPTLON20'].mean()
        total_population = cluster_populations[cluster_id]
        folium.CircleMarker(
            location=[center_lat, center_lon],
            radius=12,
            color='darkred',
            fill=True,
            fill_color='darkred',
            popup=f'Cluster {cluster_id + 1}<br>Total Population: {total_population}'
        ).add_to(m)
noise_data = filtered_data[filtered_data['cluster'] == -1]
for _, row in noise_data.iterrows():
    folium.CircleMarker(
        location=[row['INTPTLAT20'], row['INTPTLON20']],
        radius=5,
        color='gray',
        fill=True,
        fill_color='gray',
        popup=f"Noise Point"
    ).add_to(m)
m.save('Population_Regional_Division_DBScanes.html')
print("Map has been saved as a html file.")
