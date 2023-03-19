import numpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
np.set_printoptions(threshold=np.inf)

# data points collected per 360 rotation
DataPointsPerScan = 512
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
colors = []
distances = []
for i in range(1):
    LiDAR_x, LiDAR_y, LiDAR_yaw = LiDAR_raw_data_file.readline().strip().split(' ')

    for j in range(DataPointsPerScan):
        distances.append(float(LiDAR_raw_data_file.readline().strip()))
        coords_x.append(float(LiDAR_x) + (distances[-1] * np.cos(-float(LiDAR_yaw) + angles[j])))
        coords_y.append(float(LiDAR_y) + (distances[-1] * np.sin(-float(LiDAR_yaw) + angles[j])))
        colors.append(cm.rainbow(distances[-1]*2))

    # show plot
    plt.scatter(float(LiDAR_x), float(LiDAR_y), color=[0, 0, 0], s=500)
    plt.scatter(float(LiDAR_x), float(LiDAR_y), color=[1, 0, 1], s=300)

    LiDAR_raw_data_file.readline()

sort = np.flip(np.argsort(distances))
plt.scatter(numpy.array(coords_x)[sort], numpy.array(coords_y)[sort], color=numpy.array(colors)[sort])
plt.gca().invert_yaxis()
plt.show()

print(coords_x*100)
print(max(distances))

# cleanup
LiDAR_raw_data_file.close()
