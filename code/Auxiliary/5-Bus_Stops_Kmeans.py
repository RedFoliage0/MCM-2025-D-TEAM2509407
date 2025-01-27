import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.model_selection import KFold
from sklearn.metrics import silhouette_score
import folium
#This code is the Kmeans clustering of bus stops and visualizes the centers of the clustering within a limited range
file_path_new = 'Bus_Stops.csv'
new_data = pd.read_csv(file_path_new)
BALTIMORE_BOUNDARIES = {
    "lat_min": 39.19703,
    "lat_max": 39.37301,
    "lon_min": -76.71234,
    "lon_max": -76.44796
}
filtered_data = new_data[
    (new_data['Y'] >= BALTIMORE_BOUNDARIES['lat_min']) & 
    (new_data['Y'] <= BALTIMORE_BOUNDARIES['lat_max']) & 
    (new_data['X'] >= BALTIMORE_BOUNDARIES['lon_min']) & 
    (new_data['X'] <= BALTIMORE_BOUNDARIES['lon_max'])
]
X = filtered_data[['Y', 'X']].values
def get_silhouette_score(k_range, X, n_splits=5):
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=42)
    scores = []
    for k in k_range:
        avg_score = 0
        for train_index, test_index in kf.split(X):
            X_train, X_test = X[train_index], X[test_index]
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(X_train)
            score = silhouette_score(X_test, kmeans.predict(X_test))
            avg_score += score
        scores.append(avg_score / n_splits)
    return scores
k_range = range(2, 101)
silhouette_scores = get_silhouette_score(k_range, X)
best_k = k_range[np.argmax(silhouette_scores)]
print(f"The best k: {best_k}")
kmeans = KMeans(n_clusters=best_k, random_state=42)
kmeans.fit(X)
filtered_data['cluster'] = kmeans.labels_
cluster_centers = kmeans.cluster_centers_
cluster_populations = filtered_data.groupby('cluster')['Stop_Rider'].sum()
m = folium.Map(location=[39.29, -76.61], zoom_start=12)
for i, center in enumerate(cluster_centers):
    center_lat = center[0]
    center_lon = center[1]
    total_population = cluster_populations[i]
    folium.CircleMarker(
        location=[center_lat, center_lon],
        radius=12,
        color='darkred',
        fill=True,
        fill_color='darkred',
        popup=f'Cluster {i + 1}<br>Total Riders: {total_population}'
    ).add_to(m)
m.save('Bus_Stops_Kmeans.html')
print("Map has been saved as a html file.")