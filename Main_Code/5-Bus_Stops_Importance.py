import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
#This code is designed to draw a histogram of bus stops after distinguishing their importance and to display bus stops without the folio 
boundary_path = 'baltimore_boundary.geojson'
baltimore_boundary = gpd.read_file(boundary_path)
bus_data_path = 'Bus_Stops.csv'
bus_stops_data = pd.read_csv(bus_data_path)
bus_stops_data['Stop_Rider'] = pd.to_numeric(bus_stops_data['Stop_Rider'], errors='coerce')
bus_stops_data = bus_stops_data[bus_stops_data['Stop_Rider'] >= 0]
geometry = [Point(xy) for xy in zip(bus_stops_data['X'], bus_stops_data['Y'])]
bus_stops_gdf = gpd.GeoDataFrame(bus_stops_data, geometry=geometry, crs="EPSG:4326")
bins = [-1, 500, 1500, 2500, 3500, bus_stops_data['Stop_Rider'].max()]
labels = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
bus_stops_gdf['Category'] = pd.cut(bus_stops_gdf['Stop_Rider'], bins=bins, labels=labels)
category_colors = {
    'Very Low': '#ade1f5', 
    'Low': '#64c4ec',      
    'Medium': '#1f98d0',   
    'High': '#005a9c',     
    'Very High': '#002d62' 
}
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
baltimore_boundary.plot(ax=ax, color='none', edgecolor='black', linewidth=1)
for category, color in category_colors.items():
    subset = bus_stops_gdf[bus_stops_gdf['Category'] == category]
    subset.plot(ax=ax, markersize=10, color=color, label=f'{category}')
legend_labels = [
    f'Very Low (0-{bins[1]})',
    f'Low ({bins[1]}-{bins[2]})',
    f'Medium ({bins[2]}-{bins[3]})',
    f'High ({bins[3]}-{bins[4]})',
    f'Very High (>{bins[4]})'
]
legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10)
                  for color in category_colors.values()]
ax.legend(legend_handles, legend_labels, title='Stop Rider Range', fontsize=10, title_fontsize=12, loc='upper right')
plt.xlabel('Longitude', fontsize=12)
plt.ylabel('Latitude', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig('Bus_Stops_Importance_Histogram.png', dpi=300)
print("Pictrue has been saved as png a file.")
plt.show()
category_counts = bus_stops_gdf['Category'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
ax = category_counts.plot(kind='bar', color=[category_colors[label] for label in labels], edgecolor='black')
plt.legend(legend_handles, legend_labels, title='Stop Rider Range', fontsize=10, title_fontsize=12, loc='upper right')
plt.xlabel('Category', fontsize=14)
plt.ylabel('Number of Stops', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('Bus_Stops_Importance_Scatter_Plot.png', dpi=300)
print("Pictrue has been saved as png a file.")
plt.show()
