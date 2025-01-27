import pandas as pd
from geopandas import GeoDataFrame, read_file
from shapely.geometry import Point
from shapely.ops import unary_union
from geopy.distance import geodesic
import folium
#This code selects the top 20 important bus stations with a straight-line distance of no more than 2000 meters as future subway stations, 
#selects routes based on the model, and calculates the coverage area within 2000 meters of the subway
bus_stops_path = 'Bus_Stops.csv'
bus_stops = pd.read_csv(bus_stops_path)
bus_stops_sorted = bus_stops.sort_values(by='Rider_Tota', ascending=False)
def is_far_enough(selected_stops, candidate, min_distance=2000):
    candidate_coords = (candidate['Y'], candidate['X'])
    for stop in selected_stops:
        stop_coords = (stop['Y'], stop['X'])
        if geodesic(candidate_coords, stop_coords).meters < min_distance:
            return False
    return True
selected_stops = []
for _, row in bus_stops_sorted.iterrows():
    if len(selected_stops) >= 20:
        break
    if is_far_enough(selected_stops, row):
        selected_stops.append(row)
selected_stops_df = pd.DataFrame(selected_stops)
selected_stops_df['geometry'] = selected_stops_df.apply(lambda row: Point(row['X'], row['Y']), axis=1)
selected_gdf = GeoDataFrame(selected_stops_df, geometry='geometry', crs="EPSG:4326")
boundary_path = 'baltimore_boundary.geojson'
baltimore_boundary = read_file(boundary_path)
projected_gdf = selected_gdf.to_crs("EPSG:3857")
projected_boundary = baltimore_boundary.to_crs("EPSG:3857")
projected_gdf['buffer_2000m'] = projected_gdf['geometry'].buffer(2000)
all_buffers = unary_union(projected_gdf['buffer_2000m'])
baltimore_boundary_union = unary_union(projected_boundary['geometry'])
clipped_buffers = all_buffers.intersection(baltimore_boundary_union)
buffer_area = clipped_buffers.area / 10**6
baltimore_area = baltimore_boundary_union.area / 10**6
coverage_rate = (buffer_area / baltimore_area) * 100
#Perhaps you have noticed the difference in size, 
#which is due to the use of different coordinate systems, 
#and the results can be studied solely through proportion
print(f"Expected subway coverage rate:{coverage_rate:.2f}%")
m = folium.Map(location=[39.2904, -76.6122], zoom_start=12)
clipped_buffers_geojson = GeoDataFrame(geometry=[clipped_buffers], crs="EPSG:3857").to_crs("EPSG:4326")
folium.GeoJson(clipped_buffers_geojson, style_function=lambda x: {'color': 'blue', 'weight': 1, 'fillOpacity': 0.3}).add_to(m)
for _, row in selected_gdf.iterrows():
    folium.Marker(
        location=[row['Y'], row['X']],
        popup=f"{row['stop_name']}<br>Riders: {row['Rider_Tota']}",
        tooltip=f"{row['stop_name']}"
    ).add_to(m)
ring_stations = [
    "ROGERS AVE METRO STATION BAY 1",
    "FALLS RD & WESTERN HIGH SCHOOL AND POLYTECHNIC INSTITUTE sb",
    "YORK RD & COLD SPRING LN nb",
    "BELAIR RD & FRANKFORD AVE nb",
    "PULASKI HWY & 62ND ST wb",
    "DUE KANE LOOP",
    "5501 HOLABIRD AVE eb",
]
line1_stations = [
    "NORTH AVE & BLOOMINGDALE RD eb",
    "NORTH AVE & PENNSYLVANIA AVE wb",
    "SAINT PAUL ST & NORTH AVE fs sb",
    "MADISON ST & BROADWAY fs wb",
    "HIGHLAND AVE & BALTIMORE ST fs nb",
    "5501 HOLABIRD AVE eb"
]
line2_stations = [
    "NORTHERN PKWY & MCCLEAN BLVD fs eb",
    "NORTHERN PKWY & YORK RD eb",
    "YORK RD & COLD SPRING LN nb",
    "SAINT PAUL ST & NORTH AVE fs sb",
    "BALTIMORE ST & CHARLES ST eb",
    "SOUTH BALTIMORE PARK & RIDE"
]
line3_stations = [
    "EDMONDSON AVE & ATHOL AVE eb",
    "WEST BALTIMORE MARC STATION BAY 2",
    "SAINT PAUL ST & NORTH AVE fs sb",
    "THE ALAMEDA & 32ND ST fs nb",
    "ERDMAN AVE & EDISON HWY eb",
    "BELAIR RD & FRANKFORD AVE nb"
]#The station name here is obtained after filtering
def add_polyline(stations, color):
    coordinates = []
    for station in stations:
        stop = bus_stops[bus_stops['stop_name'] == station]
        if not stop.empty:
            coordinates.append([stop.iloc[0]['Y'], stop.iloc[0]['X']])
    folium.PolyLine(locations=coordinates, color=color, weight=5).add_to(m)
add_polyline(ring_stations, 'red')
add_polyline(line1_stations, 'blue')
add_polyline(line2_stations, 'green')
add_polyline(line3_stations, 'purple')
m.save("Expected_Subway_Stops_And_Coverage_Rate.html")
print("Map has been saved as a html file.")
