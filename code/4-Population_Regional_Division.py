import pandas as pd
import folium
from folium.plugins import MarkerCluster
#This code is designed to generate visualizations of population distribution
file_path = 'Population_Regional_Division.csv'
data = pd.read_csv(file_path)
baltimore_coords = [39.2904, -76.6122]
Populationmap = folium.Map(location=baltimore_coords, zoom_start=12)
marker_cluster = MarkerCluster().add_to(Populationmap)
for index, row in data.iterrows():
    lat = row['INTPTLAT20']
    lon = row['INTPTLON20']
    population = row['population']
    size = population / 100
    color = f"#{int(min(population * 2, 255)):02x}{int(max(255 - population // 10, 0)):02x}00"
    folium.CircleMarker(
        location=[lat, lon],
        radius=size,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
        popup=f"population: {population}"
    ).add_to(marker_cluster)
Populationmap.save('Population_Regional_Division.html')
print("Map has been saved as a html file.")