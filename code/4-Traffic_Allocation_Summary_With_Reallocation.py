import pandas as pd
import geopandas as gpd
from math import radians, sin, cos, sqrt, atan2
#This code is designed to calculate the values assigned to the influence center by each traffic point, 
#and the generated 'Traffic_Allocation_Summary_With_Reallocation.csv' file shows the comparison before and after the bridge collapse
centers_file = 'Cluster_Centers_and_Populations.csv'
centers_data = pd.read_csv(centers_file)
centers_data = centers_data.rename(columns={
    "Center Latitude": "Center_Y",
    "Center Longitude": "Center_X",
    "Total Population": "Base_Weight"
})
adj_matrix_file = 'Normalized_Adjacency_Matrix.csv'
adj_matrix = pd.read_csv(adj_matrix_file, index_col=0)
centers_data['Adj_Weight'] = adj_matrix.sum(axis=1).values
centers_data['Total_Weight'] = centers_data['Adj_Weight']
traffic_file = 'MDOT_SHA_Annual_Average_Daily_Traffic_Baltimore.geojson'
traffic_data = gpd.read_file(traffic_file)
aadts = [col for col in traffic_data.columns if col.startswith('AADT_')]
traffic_data['Average_AADT'] = traffic_data[aadts].mean(axis=1)
traffic_data['Average_AADT'] = traffic_data['Average_AADT'].fillna(traffic_data['AADT'])
traffic_data['Lon'] = traffic_data.geometry.x
traffic_data['Lat'] = traffic_data.geometry.y
def haversine(lon1, lat1, lon2, lat2):
    R = 6371
    dlon = radians(lon2 - lon1)
    dlat = radians(lat2 - lat1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c
def allocate_traffic(centers_data, traffic_data):
    results = []
    for _, traffic_point in traffic_data.iterrows():
        traffic_lon, traffic_lat, traffic_aadt = traffic_point['Lon'], traffic_point['Lat'], traffic_point['Average_AADT']
        weights = []
        distances = []
        for _, center_row in centers_data.iterrows():
            center_lon, center_lat, total_weight = center_row['Center_X'], center_row['Center_Y'], center_row['Total_Weight']
            distance = haversine(traffic_lon, traffic_lat, center_lon, center_lat)
            distances.append(distance)
            weight = total_weight / (distance ** 2) if distance > 0 else 0
            weights.append(weight)
        weight_sum = sum(weights)
        normalized_weights = [w / weight_sum for w in weights] if weight_sum > 0 else [0] * len(weights)
        for center_id, normalized_weight in enumerate(normalized_weights):
            results.append({
                'Traffic_Point_ID': traffic_point.OBJECTID,
                'Center_ID': center_id,
                'Allocated_Volume': traffic_aadt * normalized_weight
            })
    return pd.DataFrame(results)
allocated_df = allocate_traffic(centers_data, traffic_data)
center_summary = allocated_df.groupby('Center_ID')['Allocated_Volume'].sum().reset_index()
center_summary.rename(columns={'Allocated_Volume': 'Total_Allocated_Volume'}, inplace=True)
total_volume = center_summary['Total_Allocated_Volume'].sum()
center_summary['Percentage_of_Total'] = (center_summary['Total_Allocated_Volume'] / total_volume) * 100
centers_data_filtered = centers_data[centers_data.index != 12].reset_index(drop=True)
reallocated_df = allocate_traffic(centers_data_filtered, traffic_data)
recenter_summary = reallocated_df.groupby('Center_ID')['Allocated_Volume'].sum().reset_index()
recenter_summary.rename(columns={'Allocated_Volume': 'Reallocated_Volume'}, inplace=True)
total_reallocated_volume = recenter_summary['Reallocated_Volume'].sum()
recenter_summary['Reallocated_Percentage'] = (recenter_summary['Reallocated_Volume'] / total_reallocated_volume) * 100
final_summary = center_summary.merge(
    recenter_summary, on='Center_ID', how='left'
).fillna(0)
final_summary['Volume_Change'] = final_summary['Reallocated_Volume'] - final_summary['Total_Allocated_Volume']
final_summary['Percentage_Change'] = final_summary['Reallocated_Percentage'] - final_summary['Percentage_of_Total']
final_summary['Percentage_of_Total'] = final_summary['Percentage_of_Total'].apply(lambda x: f"{x:.2f}%")
final_summary['Reallocated_Percentage'] = final_summary['Reallocated_Percentage'].apply(lambda x: f"{x:.2f}%")
final_summary['Percentage_Change'] = final_summary['Percentage_Change'].apply(lambda x: f"{x:.2f}%")
final_summary['Total_Allocated_Volume'] = pd.to_numeric(final_summary['Total_Allocated_Volume'], errors='coerce')
final_summary['Reallocated_Volume'] = pd.to_numeric(final_summary['Reallocated_Volume'], errors='coerce')
final_summary['Volume_Change_Percentage'] = (
    (final_summary['Reallocated_Volume'] - final_summary['Total_Allocated_Volume']) /
    final_summary['Total_Allocated_Volume']
) * 100
final_summary['Volume_Change_Percentage'] = final_summary['Volume_Change_Percentage'].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else '0.00%')
total_row = pd.DataFrame({
    'Center_ID': ['Total'],
    'Total_Allocated_Volume': [total_volume],
    'Percentage_of_Total': ['100.00%'],
    'Reallocated_Volume': [total_reallocated_volume],
    'Reallocated_Percentage': ['100.00%'],
    'Volume_Change': ['0'],
    'Percentage_Change': ['0.00%'],
    'Volume_Change_Percentage': ['0.00%']
})
final_summary = pd.concat([final_summary, total_row], ignore_index=True)
final_summary.to_csv('Traffic_Allocation_Summary_With_Reallocation.csv', index=False)
print("Data have been saved as a csv file.")
