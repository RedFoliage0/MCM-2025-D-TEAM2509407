import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
from sklearn.cluster import KMeans
import networkx as nx
from scipy.spatial import distance_matrix
import numpy as np
from pyproj import CRS, Transformer
#This code is designed to calculate the average number of possible sites that each site may reach after moving three times after planning the path, 
#and save it in 'Bus_Station_Connectivity_Average_Count.csv' file
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
average_connectivity_per_cluster = []
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
    adjacency_matrix = nx.to_numpy_array(mst)
    reach_matrix = adjacency_matrix + np.linalg.matrix_power(adjacency_matrix, 2) + np.linalg.matrix_power(adjacency_matrix, 3)
    reach_matrix[reach_matrix > 0] = 1
    node_connectivity = np.sum(reach_matrix, axis=1) - 1 
    average_connectivity = np.mean(node_connectivity)
    average_connectivity_per_cluster.append({
        "Cluster": cluster_id,
        "Average Connectivity": average_connectivity
    })
average_connectivity_df = pd.DataFrame(average_connectivity_per_cluster)
average_connectivity_df.to_csv('Bus_Station_Connectivity_Average_Count.csv', index=False)
print("Data have been saved as a csv file.")
