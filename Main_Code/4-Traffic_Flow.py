import folium
import json
from collections import defaultdict
import numpy as np
#This code is designed to visually display the distribution of traffic flow in the city and the characteristics of bus routes within a limited range
BALTIMORE_BOUNDARIES = {
    "lat_min": 39.19703,
    "lat_max": 39.37301,
    "lon_min": -76.71234,
    "lon_max": -76.44796
}
geojson_file_path = 'MDOT_SHA_Annual_Average_Daily_Traffic_Baltimore.geojson'
with open(geojson_file_path) as f:
    geojson_data = json.load(f)
def is_within_baltimore(lat, lon):
    return (BALTIMORE_BOUNDARIES["lat_min"] <= lat <= BALTIMORE_BOUNDARIES["lat_max"] and
            BALTIMORE_BOUNDARIES["lon_min"] <= lon <= BALTIMORE_BOUNDARIES["lon_max"])
def aggregate_traffic_points(features):
    lat_lon_clusters = defaultdict(list)
    for feature in features:
        geometry = feature['geometry']
        if geometry['type'] == 'Point':
            lat, lon = geometry['coordinates'][1], geometry['coordinates'][0]
            if is_within_baltimore(lat, lon):
                traffic_volume = feature['properties'].get('AADT', 0)
                lat_lon_clusters[(lat, lon)].append(traffic_volume)
    average_traffic = []
    for (lat, lon), volumes in lat_lon_clusters.items():
        avg_volume = np.mean(volumes)
        average_traffic.append((lat, lon, avg_volume))
    return average_traffic
traffic_data = aggregate_traffic_points(geojson_data['features'])
m = folium.Map(location=[39.2904, -76.6122], zoom_start=12)
def style_function(traffic_volume):
    if traffic_volume > 20000:
        fill_color = 'red'
        radius = 10
    elif traffic_volume > 10000:
        fill_color = 'orange'
        radius = 8
    elif traffic_volume > 5000:
        fill_color = 'yellow'
        radius = 6
    else:
        fill_color = 'green'
        radius = 4
    return fill_color, radius
for lat, lon, avg_volume in traffic_data:
    fill_color, radius = style_function(avg_volume)
    folium.CircleMarker(
        location=[lat, lon],
        radius=radius,
        color='black',
        weight=1,
        fill=True,
        fill_color=fill_color,
        fill_opacity=0.6
    ).add_to(m)
m.save('Traffic_Flow.html')
print("Map has been saved as a html file.")

