# MCM-2025-D-TEAM2509407
This repository contains all the code used for our MCM 2025 submission for Question D. See attached PDF for the paper.

For the dataset provided in the question, we mainly use the following: nodes_drive.csv, edges_drive.csv, Bus_Stops.csv, Bus_Routes.csv, Edge_Names_With_Nodes.csv, MDOT_SHA_Annual_Average_Daily_Traffic_Baltimore.csv, DataDictionary.csv

We also collected data from the website

merged_bus_data.csv: Determine the approximate correspondence between bus stops and bus routes through Google Maps
Population_regional_division.csv: To know the population size within the region, from https://statisticalatlas.com/place/Maryland/Baltimore/Population#data-map/block-group
MDOT_SHA_Annual_Average_Daily_Traffic_Baltimore.geojson: as the supplement of MDOT_SHA_Annual_Average_Daily_Traffic_Baltimore.csv, from https://data.imap.maryland.gov/datasets/maryland::mdot-sha-annual-average-daily-traffic-aadt-locations/explore
baltimore_boundary.geojson: To understand the administrative divisions of Baltimore, form https://overpass-turbo.eu/
The remaining dataset was derived through modeling

Total_Scenic_Change_Influence_Data.xlsx and Sensitivity_Analysis_Data_Table.csv, these are tables calculated for sensitivity
These are tables calculated for sensitivity, it is the correlation matrix of attraction points
Cluster_Centers_and_Populations.csv, used to record information about attraction points
Traffic_Allocation_Summary_With_Reallocation.csv, it is used to record the changes in data before and after the collapse of the bridge
Bus_Station_Connectivity_Average_Count.csv, It is used to record the average number of reachable bus stops within the three bus stops after clustering
The tags before the code are used to facilitate distinguishing the corresponding scope and increase readability, but not all code is described in the paper, and the same applies to maps and pictures
Traffic_Allocation_Summary_With_Reallocation.csv
Details changes in traffic data before and after a bridge collapse.
Bus_Station_Connectivity_Average_Count.csv
Average number of bus stops accessible from three clustered bus stops.

Code Structure
To enhance readability and usability, we have included descriptive tags at the beginning of the code files to clarify their corresponding scope. Note that not all code sections are explicitly referenced in the paper.
