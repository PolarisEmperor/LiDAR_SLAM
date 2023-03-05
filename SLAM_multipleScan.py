import numpy as np
import matplotlib.pyplot as plt
import math

# data points collected per 360 rotation
DataPointsPerScan = DataPointsPerScanAdjust = 512
# minimum distance between other points to be determined outlier
MinimumOutlierDistance = 3
# minimum change in angle (in degrees) for key point to be recorded
MinimumAngleChange = 50
# minimum distance between key points to be clustered into one point
ClusterThreshold = 20

# setup stuff
fig = plt.figure()
np.set_printoptions(suppress=True)
LiDAR_raw_data_file = open("b.txt", "r")

# reading distance data
angles = np.arange(0, 2 * np.pi, (2 * np.pi / DataPointsPerScan), dtype=float)
coords_x = []
coords_y = []
for i in range(13):
    point_distances = np.empty(DataPointsPerScan)
    LiDAR_x, LiDAR_y, LiDAR_yaw = LiDAR_raw_data_file.readline().strip().split(' ')

    for j in range(DataPointsPerScan):
        point_distances[j] = float(LiDAR_raw_data_file.readline().strip())
        coords_x.append(float(LiDAR_x) + (point_distances[j] * np.cos(-float(LiDAR_yaw) + angles[j])))
        coords_y.append(float(LiDAR_y) + (point_distances[j] * np.sin(-float(LiDAR_yaw) + angles[j])))

    # show plot
    plt.scatter(float(LiDAR_x), float(LiDAR_y), color=[0, 0, 0], s=500)
    plt.scatter(float(LiDAR_x), float(LiDAR_y), color=[1, 0, 1], s=300)

    LiDAR_raw_data_file.readline()

plt.scatter(coords_x, coords_y, color=[0, 0, 0])
plt.gca().invert_yaxis()
plt.show()

# cleanup
LiDAR_raw_data_file.close()
