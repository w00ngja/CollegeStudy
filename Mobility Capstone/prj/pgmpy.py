import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

# Input data: candidate locations
candidate_locations = np.array([[2, 2], [2, 6], [6, 2], [6, 6]])

# Voronoi diagram computation
vor = Voronoi(candidate_locations)

# Plotting Voronoi diagram
voronoi_plot_2d(vor)

# Plotting input candidate locations
plt.plot(candidate_locations[:, 0], candidate_locations[:, 1], 'ko')

# Custom evaluation criteria for selecting charging station locations
# Adjust the condition as per your requirements
charging_station_locations = []
for region in vor.regions:
    if len(region) > 0 and -1 not in region:
        x, y = vor.vertices[region][0]
        if x > 1 and y > 1:  # Example condition: select locations with x, y > 1
            charging_station_locations.append(x)

charging_station_locations = np.array(charging_station_locations)

# Plotting selected charging station locations
plt.plot(charging_station_locations, charging_station_locations, 'ro')

# Setting plot limits
plt.xlim(vor.min_bound[0] - 1, vor.max_bound[0] + 1)
plt.ylim(vor.min_bound[1] - 1, vor.max_bound[1] + 1)

# Displaying the plot
plt.show()
