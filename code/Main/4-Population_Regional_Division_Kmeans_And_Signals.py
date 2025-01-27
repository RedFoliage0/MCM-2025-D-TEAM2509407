import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.model_selection import KFold
from sklearn.metrics import silhouette_score
import folium
#This code uses Kmeans to find population clustering centers and adds three selected scenic spots, visualizes them, 
#and generates 'Cluster_Centers_and_Populations.csv' files for statistical analysis
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
kmeans = KMeans(n_clusters=10, random_state=42)
kmeans.fit(X)
filtered_data['cluster'] = kmeans.labels_
cluster_centers = kmeans.cluster_centers_
filtered_data['population'] = filtered_data['population'].fillna(0)
cluster_populations = filtered_data.groupby('cluster')['population'].sum()
output_data = pd.DataFrame({
    'Cluster': range(10),
    'Center Latitude': cluster_centers[:, 0],
    'Center Longitude': cluster_centers[:, 1],
    'Total Population': cluster_populations.values,
    'category': 'community'
})
scenic_spots = [
    {
        'Cluster': 10,
        'Center Latitude': 39.29131,
        'Center Longitude': -76.61185,
        'Total Population': None,
        'category': 'scenicspot'
    },
    {
        'Cluster': 11,
        'Center Latitude': 39.32333,
        'Center Longitude': -76.64944,
        'Total Population': None,
        'category': 'scenicspot'
    },
    {
        'Cluster': 12,
        'Center Latitude': 39.18805,
        'Center Longitude': -76.54638,
        'Total Population': None,
        'category': 'scenicspot'
    }
]#The Serial Number in the csv is the Serial Number in the html minus one
scenic_spots_df = pd.DataFrame(scenic_spots)
output_data = pd.concat([output_data, scenic_spots_df], ignore_index=True)
output_data.to_csv('Cluster_Centers_and_Populations.csv', index=False)
print("Data have been saved as a csv file.")
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
        popup=f'Cluster {i + 1}<br>Total Population: {total_population}'
    ).add_to(m)
folium.CircleMarker(
        location=[39.29131, -76.61185],
        radius=12,
        color='darkred',
        fill=True,
        fill_color='darkred',
        popup=f'Cluster {11}<br>scenic spot: {5000000}'
    ).add_to(m)
folium.CircleMarker(
        location=[39.32333, -76.64944],
        radius=12,
        color='darkred',
        fill=True,
        fill_color='darkred',
        popup=f'Cluster {12}<br>scenic spot: {5000000}'
    ).add_to(m)
folium.CircleMarker(
        location=[39.18805, -76.54638],
        radius=12,
        color='darkred',
        fill=True,
        fill_color='darkred',
        popup=f'Cluster {13}<br>scenic spot: {5000000}'
    ).add_to(m)
m.save('Population_Regional_Division_Kmeans_And_Scenic_Spot.html')
print("Map has been saved as a html file.")