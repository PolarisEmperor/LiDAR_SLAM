import numpy as np
import matplotlib.pyplot as plt
import math

# SLAM options

# data points collected per 360 rotation
DataPointsPerScan = DataPointsPerScanAdjust = 512
# minimum distance between other points to be determined outlier
MinimumOutlierDistance = 3
# minimum change in angle (in degrees) for critical point to be recorded
MinimumAngleChange = 60

# setup stuff
fig = plt.figure()
np.set_printoptions(suppress=True)

# reading distance data
LiDAR_raw_data_file = open("data2.txt", "r")
point_distances = np.empty(DataPointsPerScan)
angles = np.arange(0, 2*np.pi, (2*np.pi / DataPointsPerScan), dtype=float)
outliers = []
for i in range(DataPointsPerScan):
    point_distances[i] = float(LiDAR_raw_data_file.readline())

# determine and remove outliers
for i in range(DataPointsPerScan):
    if point_distances[i] == np.inf:
        outliers.append(i)

for i in range(DataPointsPerScan):
    prevPointFar = False
    nextPointFar = False
    previousPoint = (i - 2) if (i - 2) >= 0 else DataPointsPerScan + (i - 2)
    currentPoint = (i - 1) if (i - 1) >= 0 else DataPointsPerScan + (i - 1)
    nextPoint = i

    if currentPoint in outliers:
        continue

    if previousPoint in outliers:
        prevPointFar = True
    elif math.sqrt(abs(math.pow(point_distances[i - 2], 2) + math.pow(point_distances[i - 1], 2) - (2 * point_distances[i - 2] * point_distances[i - 1] * np.cos(angles[1])))) > MinimumOutlierDistance:
        prevPointFar = True
    if nextPoint in outliers:
        nextPointFar = True
    elif math.sqrt(abs(math.pow(point_distances[i - 1], 2) + math.pow(point_distances[i], 2) - (2 * point_distances[i - 1] * point_distances[i] * np.cos(angles[1])))) > MinimumOutlierDistance:
        nextPointFar = True

    if prevPointFar and nextPointFar:
        outliers.append(currentPoint)

# point / angle association
DataPointsPerScanAdjust = DataPointsPerScan - len(outliers)
colors = np.zeros(shape=[DataPointsPerScanAdjust, 3])
sizes = np.full(DataPointsPerScanAdjust, 10)
point_data_x = np.empty(DataPointsPerScanAdjust, dtype=float)
point_data_y = np.empty(DataPointsPerScanAdjust, dtype=float)
outlierAdjust = 0
for i in range(DataPointsPerScan):
    if i in outliers:
        outlierAdjust += 1
        continue
    point_data_x[i - outlierAdjust] = point_distances[i] * np.cos(angles[i])
    point_data_y[i - outlierAdjust] = point_distances[i] * np.sin(angles[i])

# calculate distances between points
point_distances = np.empty(DataPointsPerScanAdjust, dtype=float)
for i in range(0, DataPointsPerScanAdjust):
    point_distances[i] = math.sqrt(abs(math.pow(point_data_x[i] - point_data_x[i - 1], 2) + math.pow(point_data_y[i] - point_data_y[i - 1], 2)))

# calculate angle between points
point_angles = np.empty(DataPointsPerScanAdjust, dtype=float)
for i in range(DataPointsPerScanAdjust):
    point_distance_1 = point_distances[i]
    point_distance_2 = point_distances[i - 1]
    point_distance_3 = math.sqrt(abs(math.pow(point_data_x[i] - point_data_x[i - 2], 2) + math.pow(point_data_y[i] - point_data_y[i - 2], 2)))
    point_angles[i] = np.arccos((math.pow(point_distance_1, 2) + math.pow(point_distance_2, 2) - math.pow(point_distance_3, 2))/(2 * point_distance_1 * point_distance_2))
    # adjust angles if not interior angle

    if point_data_y[i - 1] > 0:
        if point_data_y[i - 1] < point_data_y[i - 2] and point_data_y[i - 1] < point_data_y[i]:
            point_angles[i] = 2 * np.pi - point_angles[i]
    else:
        if point_data_y[i - 1] > point_data_y[i - 2] and point_data_y[i - 1] > point_data_y[i]:
            point_angles[i] = 2 * np.pi - point_angles[i]
    if point_data_x[i - 1] > 0:
        if point_data_x[i - 1] < point_data_x[i - 2] and point_data_x[i - 1] < point_data_x[i]:
            point_angles[i] = 2 * np.pi - point_angles[i]
    else:
        if point_data_x[i - 1] > point_data_x[i - 2] and point_data_x[i - 1] > point_data_x[i]:
            point_angles[i] = 2 * np.pi - point_angles[i]

# calculate rate of change between angles
roc_slope_angles = np.empty(DataPointsPerScanAdjust, dtype=float)
for i in range(DataPointsPerScanAdjust):
    roc_slope_angles[i] = abs(point_angles[i - 1]) - abs(point_angles[i])

# calculate rate of change
roc_point_distances = np.empty(DataPointsPerScanAdjust, dtype=float)
for i in range(DataPointsPerScanAdjust):
    roc_point_distances[i] = abs(point_distances[i - 1] - point_distances[i])

# mark critical points
for i in range(DataPointsPerScanAdjust):
    if abs(roc_slope_angles[i]) > np.deg2rad(MinimumAngleChange):
        colors[i - 1] = [1, 0, 0]
        sizes[i - 1] = 50
    if roc_point_distances[i] > MinimumOutlierDistance:
        colors[i - 1] = colors[i] = [1, 0, 0]
        sizes[i - 1] = sizes[i] = 50

# show plot
plt.scatter(0, 0, color=[0, 0, 1], s=300)
plt.scatter(point_data_x, point_data_y, c=colors, s=sizes)
plt.show()

# cleanup
LiDAR_raw_data_file.close()


