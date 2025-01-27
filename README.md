# MCM-2025-D-TEAM2509407
This repository contains all the code used for our MCM 2025 submission for Question D. See attached PDF for the paper.

Dataset Overview
Provided Datasets
We primarily utilized the following datasets provided in the question:

nodes_drive.csv
edges_drive.csv
Bus_Stops.csv
Bus_Routes.csv
Edge_Names_With_Nodes.csv
MDOT_SHA_Annual_Average_Daily_Traffic_Baltimore.csv
DataDictionary.csv
Additional Collected Datasets
We also gathered the following datasets from external sources to supplement our analysis:

merged_bus_data.csv
Mapped approximate correspondences between bus stops and bus routes using Google Maps.
Population_regional_division.csv
Population data within the region, sourced from Statistical Atlas.
MDOT_SHA_Annual_Average_Daily_Traffic_Baltimore.geojson
Supplementary data for traffic, sourced from Maryland iMAP Data.
baltimore_boundary.geojson
Administrative boundary data of Baltimore, sourced from Overpass Turbo.
Modeled Datasets
The following datasets were generated through our modeling and analysis:

Total_Scenic_Change_Influence_Data.xlsx
Contains sensitivity analysis results for scenic change influence.
Sensitivity_Analysis_Data_Table.csv
Correlation matrix of attraction points derived from sensitivity analysis.
Cluster_Centers_and_Populations.csv
Records the location and population information of clustered attraction points.
Traffic_Allocation_Summary_With_Reallocation.csv
Details changes in traffic data before and after a bridge collapse.
Bus_Station_Connectivity_Average_Count.csv
Average number of bus stops accessible from three clustered bus stops.

Code Structure
To enhance readability and usability, we have included descriptive tags at the beginning of the code files to clarify their corresponding scope. Note that not all code sections are explicitly referenced in the paper.
