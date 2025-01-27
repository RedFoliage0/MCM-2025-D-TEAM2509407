import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import Polygon
from pyproj import CRS, Transformer
from sklearn.cluster import KMeans
import networkx as nx
from scipy.spatial import distance_matrix
#This code is designed to visualize the process of removing low bus stops before clustering
boundary_path = 'baltimore_boundary.geojson'
baltimore_boundary = gpd.read_file(boundary_path)
bus_data_path = 'Bus_Stops.csv'
bus_stops_data = pd.read_csv(bus_data_path)
bus_stops_data['Stop_Rider'] = pd.to_numeric(bus_stops_data['Stop_Rider'], errors='coerce')
bus_stops_data = bus_stops_data[bus_stops_data['Stop_Rider'] >= 0]
geometry = [Point(xy) for xy in zip(bus_stops_data['X'], bus_stops_data['Y'])]
bus_stops_gdf = gpd.GeoDataFrame(bus_stops_data, geometry=geometry, crs="EPSG:4326")
utm_crs = CRS("EPSG:32618")
bus_stops_gdf = bus_stops_gdf.to_crs(utm_crs)
baltimore_boundary = baltimore_boundary.to_crs(utm_crs)
bins = [-1, 500, 1500, 2500, 3500, bus_stops_data['Stop_Rider'].max()]
labels = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
bus_stops_gdf['Category'] = pd.cut(bus_stops_gdf['Stop_Rider'], bins=bins, labels=labels)
filtered_gdf = bus_stops_gdf[~bus_stops_gdf['Category'].isin(['Very Low'])]
coordinates = filtered_gdf.geometry.apply(lambda p: (p.x, p.y)).tolist()
kmeans = KMeans(n_clusters=10, random_state=42)
filtered_gdf['Cluster'] = kmeans.fit_predict(coordinates)
center_lat = 39.2904
center_lon = -76.6122
transformer = Transformer.from_crs("EPSG:4326", utm_crs, always_xy=True)
center_x, center_y = transformer.transform(center_lon, center_lat)
radii = [4000, 7000, 8500]
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
baltimore_boundary.plot(ax=ax, color='none', edgecolor='black', linewidth=1)
for radius in radii:
    circle = Point(center_x, center_y).buffer(radius)
    circle_gdf = gpd.GeoDataFrame(geometry=[circle], crs=utm_crs)
    circle_gdf.plot(ax=ax, edgecolor='red', facecolor='none', linestyle='--', linewidth=1.5, alpha=0.7, label=f'{radius} meters')
for cluster_id in range(10):
    cluster_points = filtered_gdf[filtered_gdf['Cluster'] == cluster_id]
    cluster_coords = cluster_points.geometry.apply(lambda p: (p.x, p.y)).tolist()
    dist_matrix = distance_matrix(cluster_coords, cluster_coords)
    G = nx.Graph()
    for i, coord1 in enumerate(cluster_coords):
        for j, coord2 in enumerate(cluster_coords):
            if i != j:
                G.add_edge(i, j, weight=dist_matrix[i][j])
    mst = nx.minimum_spanning_tree(G)
    cluster_points.plot(ax=ax, markersize=15, label=f'Cluster {cluster_id}')
    for edge in mst.edges:
        x1, y1 = cluster_coords[edge[0]]
        x2, y2 = cluster_coords[edge[1]]
        plt.plot([x1, x2], [y1, y2], color='gray', linewidth=1)
plt.legend(title='Clusters', fontsize=10, loc='lower left')
plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig('Accurate_Clustered_Bus_Stops_MST_with_Circles.png', dpi=300)
print("Pictrue has been saved as a png file.")
plt.show()
