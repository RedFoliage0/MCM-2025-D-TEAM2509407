import numpy as np
import pandas as pd
from geopandas import GeoDataFrame, read_file
from shapely.geometry import Point
from shapely.ops import unary_union
import folium
#This code is designed to display the coverage area of the bus and the conceptual coverage area after adding the ring route, 
#and will output the percentage of coverage before and after and the percentage of increase
bus_stops_path = 'Bus_Stops.csv'
bus_stops = pd.read_csv(bus_stops_path)
bus_stops['geometry'] = bus_stops.apply(lambda row: Point(row['X'], row['Y']), axis=1)
bus_stops_gdf = GeoDataFrame(bus_stops, geometry='geometry', crs="EPSG:4326")
bus_stops_gdf['buffer_300m'] = bus_stops_gdf['geometry'].buffer(0.003)
boundary_path = 'baltimore_boundary.geojson'
baltimore_boundary = read_file(boundary_path)
baltimore_boundary = baltimore_boundary.to_crs(bus_stops_gdf.crs)
baltimore_boundary_union = unary_union(baltimore_boundary['geometry'])
all_buffers = unary_union(bus_stops_gdf['buffer_300m'])
clipped_buffers = all_buffers.intersection(baltimore_boundary_union)
original_area = clipped_buffers.area * 111 * 111
baltimore_area = baltimore_boundary_union.area * 111 * 111
original_coverage_rate = (original_area / baltimore_area) * 100
#Perhaps you have noticed the difference in size, 
#which is due to the use of different coordinate systems, 
#and the results can be studied solely through proportion
print(f"Original coverage rate: {original_coverage_rate:.2f}%")
def generate_circle_points(center, radius, num_points=360):
    points = []
    for angle in np.linspace(0, 360, num_points):
        angle_rad = np.radians(angle)
        lat = center[0] + (radius / 111000) * np.cos(angle_rad)
        lon = center[1] + (radius / (111000 * np.cos(np.radians(center[0])))) * np.sin(angle_rad)
        points.append(Point(lon, lat))
    return points
city_center = [39.2904, -76.6122]
circle_radii = [4000, 7000, 8500]
buffer_distance = 300 
circle_points = []
for radius in circle_radii:
    circle_points.extend(generate_circle_points(city_center, radius))
circle_points_gdf = GeoDataFrame(geometry=circle_points, crs="EPSG:4326")
circle_points_gdf['buffer'] = circle_points_gdf['geometry'].buffer(buffer_distance / 111000)
circle_buffers_union = unary_union(circle_points_gdf['buffer']).intersection(baltimore_boundary_union)
overall_union = unary_union([clipped_buffers, circle_buffers_union])
overall_area = overall_union.area * 111 * 111
overall_coverage_rate = (overall_area / baltimore_area) * 100
added_area = overall_area - original_area
added_coverage_rate = (added_area / baltimore_area) * 100
increase_rate = ((overall_area - original_area) / original_area) * 100
print(f"Overall coverage rate: {overall_coverage_rate:.2f}%")
print(f"Added coverage rate: {added_coverage_rate:.2f}%")
print(f"Increase rate: {increase_rate:.2f}%")
m = folium.Map(location=city_center, zoom_start=12)
folium.GeoJson(clipped_buffers, style_function=lambda x: {'color': 'blue', 'weight': 1, 'fillOpacity': 0.3}).add_to(m)
folium.GeoJson(circle_buffers_union, style_function=lambda x: {'color': 'orange', 'weight': 1, 'fillOpacity': 0.7}).add_to(m)
for _, row in bus_stops.iterrows():
    folium.CircleMarker(location=[row['Y'], row['X']], radius=3, color='green', fill=True).add_to(m)
for radius in circle_radii:
    folium.Circle(
        location=city_center,
        radius=radius,
        color='red',
        fill=False,
        weight=2
    ).add_to(m)
m.save("Bus_Stops_Coverage_Full.html")
print("Map has been saved as a html file.")