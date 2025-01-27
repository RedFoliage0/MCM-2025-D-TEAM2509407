import pandas as pd
import matplotlib.pyplot as plt
#This code is designed to draw a line chart for sensitivity analysis
file_path = 'Sensitivity_Analysis_Data_Table.csv'
data = pd.read_csv(file_path)
data.set_index(data.columns[0], inplace=True)
absolute_data = data.abs()
for index, row in absolute_data.iterrows():
    plt.figure(figsize=(8, 6))
    plt.plot(absolute_data.columns, row, marker='o', label=index)
    plt.xlabel('Total Scenic Commute Change (%)')
    plt.ylabel('Percent Change (Absolute)')
    plt.ylim(0, max(row.max() * 1.1, 5))
    plt.grid(True)
    plt.legend()
    for x, y in zip(absolute_data.columns, row):
        plt.text(x, y, f'{y:.2f}', ha='center', va='bottom')
    file_name = f'{index}_Sensitivity_Analysis.png'
    plt.savefig(file_name)
print("Pictrues have been saved as png files.")
plt.show()