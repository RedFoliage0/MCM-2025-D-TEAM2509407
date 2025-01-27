import matplotlib.pyplot as plt
import numpy as np
#This code is designed to draw a conceptual diagram of the optimized bus route
lines = 6
points_per_line = 5 
circle_radius = 10 
line_length = 4 
angles = np.linspace(0, 2 * np.pi, lines, endpoint=False)
fig, ax = plt.subplots(figsize=(8, 8))
for angle in angles:
    mid_x = circle_radius * np.cos(angle)
    mid_y = circle_radius * np.sin(angle)
    x_line = np.linspace(mid_x - line_length * np.cos(angle), mid_x + line_length * np.cos(angle), points_per_line)
    y_line = np.linspace(mid_y - line_length * np.sin(angle), mid_y + line_length * np.sin(angle), points_per_line)
    ax.plot(x_line, y_line, 'o', color='blue', markersize=8)
    ax.plot(x_line, y_line, '-', color='black')
circle = plt.Circle((0, 0), circle_radius, color='red', fill=False, linestyle='--', linewidth=1)
ax.add_artist(circle)
ax.set_aspect('equal')
ax.axis('off')
plt.savefig('Conceptual_Diagram_Of_Bus_Route_Optimization.png')
print("Pictrue has been saved as a png file.")