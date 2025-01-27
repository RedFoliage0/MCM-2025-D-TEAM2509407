import pandas as pd
import folium
#This code is to draw all points and edges within a limited range
BALTIMORE_BOUNDARIES = {
    "lat_min": 39.19703,
    "lat_max": 39.37301,
    "lon_min": -76.71234,
    "lon_max": -76.44796
}
nodes_drive_df = pd.read_csv('nodes_drive.csv')
edges_drive_df = pd.read_csv('edges_drive.csv')
def create_map(center=[39.2904, -76.6122], zoom_start=12):
    return folium.Map(location=center, zoom_start=zoom_start)
def filter_baltimore_nodes(nodes_df, boundaries):
    return nodes_df[(nodes_df['y'] >= boundaries['lat_min']) &
                    (nodes_df['y'] <= boundaries['lat_max']) &
                    (nodes_df['x'] >= boundaries['lon_min']) &
                    (nodes_df['x'] <= boundaries['lon_max'])]
def filter_baltimore_edges(edges_df, nodes_df, boundaries):
    baltimore_nodes = filter_baltimore_nodes(nodes_df, boundaries)
    baltimore_node_ids = baltimore_nodes['osmid'].values
    filtered_edges = edges_df[edges_df['u'].isin(baltimore_node_ids) & edges_df['v'].isin(baltimore_node_ids)]
    return filtered_edges
def plot_road_nodes_and_edges(nodes_drive_df, edges_drive_df):
    m = create_map()
    for _, node in nodes_drive_df.iterrows():
        popup = folium.Popup(f"Lat: {node['y']}, Lon: {node['x']}", max_width=200)
        folium.CircleMarker([node['y'], node['x']], radius=5, color='black', fill=True, fill_opacity=1,popup=popup).add_to(m)
    for _, edge in edges_drive_df.iterrows():
        u_node = nodes_drive_df[nodes_drive_df['osmid'] == edge['u']].iloc[0]
        v_node = nodes_drive_df[nodes_drive_df['osmid'] == edge['v']].iloc[0]
        folium.PolyLine([(u_node['y'], u_node['x']), (v_node['y'], v_node['x'])], color="brown", weight=5, opacity=0.5).add_to(m)
    m.save('Drive_Nodes_And_Edges.html')
baltimore_nodes_df = filter_baltimore_nodes(nodes_drive_df, BALTIMORE_BOUNDARIES)
baltimore_edges_df = filter_baltimore_edges(edges_drive_df, baltimore_nodes_df, BALTIMORE_BOUNDARIES)
plot_road_nodes_and_edges(baltimore_nodes_df, baltimore_edges_df)
print("Map has been saved as a html file.")
