import pandas as pd
import folium
import random
#This code is for drawing all bus stops
bus_data_file_path = 'merged_bus_data.csv'
bus_data_df = pd.read_csv(bus_data_file_path)
group_by_route = bus_data_df.groupby('Route_Name')
map_center = [39.2904, -76.6122]
m = folium.Map(location=map_center, zoom_start=12)
def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))
for route_name, group in group_by_route:
    route_coords = group[['Y', 'X']].values.tolist()
    route_color = random_color()
    for coord in route_coords:
        folium.CircleMarker(
            location=[coord[0], coord[1]],
            radius=5,
            color=route_color,
            fill=True,
            fill_color=route_color,
            fill_opacity=0.8,
        ).add_to(m)
m.save("Bus_Stops.html")
print("Map has been saved as a html file.")