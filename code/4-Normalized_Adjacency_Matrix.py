import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#This code calculates the correlation matrix of several influence centers based on the model, 
#generates 'Normalized_Adjacency_Matrix.png' images and corresponding 'Normalized_Adjacency_Matrix.csv' files
file_path = 'Cluster_Centers_and_Populations.csv'
data = pd.read_csv(file_path)
data['category'] = ['community'] * (len(data) - 3) + ['scenic_spot'] * 3
f_AB = 0.001
total_tourist_commute = 60000000 
total_scenic_commute = 15000000*1    #You can obtain results for sensitivity analysis by changing the values
num_communities = len(data[data['category'] == 'community'])
num_scenic_spots = len(data[data['category'] == 'scenic_spot'])
average_population = data[data['category'] == 'community']['Total Population'].mean()
nodes = list(data['Cluster'])
num_nodes = len(nodes)
adj_matrix = np.zeros((num_nodes, num_nodes))
communities = data[data['category'] == 'community']
for i in range(len(communities)):
    for j in range(len(communities)):
        if i != j:
            W_AB = (communities.iloc[i]['Total Population'] *
                    communities.iloc[j]['Total Population'] * f_AB)
            adj_matrix[i, j] = W_AB
for i, community in communities.iterrows():
    for j in range(num_nodes - num_scenic_spots, num_nodes):
        W_A_S = (total_tourist_commute / (num_communities * num_scenic_spots)) * \
                (community['Total Population'] / average_population)
        adj_matrix[i, j] = W_A_S
        adj_matrix[j, i] = W_A_S
for i in range(num_nodes - num_scenic_spots, num_nodes):
    for j in range(num_nodes - num_scenic_spots, num_nodes):
        if i != j:
            adj_matrix[i, j] = total_scenic_commute / num_scenic_spots
total_weight = np.sum(adj_matrix)
normalized_adj_matrix = adj_matrix / total_weight
labels = [f"N{i+1}" for i in range(num_nodes)]
plt.figure(figsize=(12, 8))
ax = sns.heatmap(
    normalized_adj_matrix, 
    annot=True,
    fmt=".4f", 
    cmap='YlGnBu', 
    xticklabels=labels, 
    yticklabels=labels
)
ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top')
plt.xlabel("Nodes (Communities and Scenic Spots)")
plt.ylabel("Nodes (Communities and Scenic Spots)")
plt.savefig('Normalized_Adjacency_Matrix.png')
print("Pictrue has been saved as a png file.")
adj_matrix_df = pd.DataFrame(normalized_adj_matrix, columns=nodes, index=nodes)
adj_matrix_df.to_csv('Normalized_Adjacency_Matrix.csv')
print("Data have been saved as a csv file.")
