# MCM-2025-D-TEAM2509407
This repository contains all the code used for our MCM 2025 submission for Question D. See attached PDF for the paper.

All the code we used for our MCM 2025 question D submission. See attached PDF for the paper.

For the dataset provided in the question, we mainly use the following:
nodes_drive.csv, edges_drive.csv, Bus_Stops.csv, Bus_Routes.csv, Edge_Names_With_Nodes.csv, MDOT_SHA_Annual_Average_Daily_Traffic_Baltimore.csv, DataDictionary.csv

We also collected data from the website

1. merged_bus_data.csv: Determine the approximate correspondence between bus stops and bus routes through Google Maps and OpenStreetMap
googlemap: https://www.google.com.hk/maps/@39.2664084,-76.6100485,11.27z/data=!5m1!1e1?entry=ttu&g_ep=EgoyMDI1MDEyMi4wIKXMDSoASAFQAw%3D%3D
OpenStreetMap: https://www.openstreetmap.org/#map=12/39.2999/-76.6037
2. Population_regional_division.csv: To know the population size within the region, from https://statisticalatlas.com/place/Maryland/Baltimore/Population#data-map/block-group
3. MDOT_SHA_Annual_Average_Daily_Traffic_Baltimore.geojson: as the supplement of MDOT_SHA_Annual_Average_Daily_Traffic_Baltimore.csv, from https://data.imap.maryland.gov/datasets/maryland::mdot-sha-annual-average-daily-traffic-aadt-locations/explore
4.baltimore_boundary.geojson: To understand the administrative divisions of Baltimore, form https://overpass-turbo.eu/

The remaining dataset was derived through modeling

1. Total_Scenic_Change_Influence_Data.xlsx and Sensitivity_Analysis_Data_Table.csv, these are tables calculated for sensitivity
2. Sensitivity_Analysis_Data_Table.csv, These are tables calculated for sensitivity, it is the correlation matrix of attraction points
3. Cluster_Centers_and_Populations.csv, used to record information about attraction points
4. Traffic_Allocation_Summary_With_Reallocation.csv, it is used to record the changes in data before and after the collapse of the bridge
5. Bus_Station_Connectivity_Average_Count.csv, It is used to record the average number of reachable bus stops within the three bus stops after clustering

The tags before the code are used to facilitate distinguishing the corresponding scope and increase readability, but not all code is described in the paper
