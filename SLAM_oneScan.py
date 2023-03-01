import numpy as np
import matplotlib.pyplot as plt
import math
import statistics

# SLAM options

# data points collected per 360 rotation
DataPointsPerScan = DataPointsPerScanAdjust = 512
# minimum distance between other points to be determined outlier
MinimumOutlierDistance = 3
# minimum change in angle (in degrees) for key point to be recorded
MinimumAngleChange = 50

# setup stuff
fig = plt.figure()
np.set_printoptions(suppress=True)

# reading distance data
LiDAR_raw_data_file = open("room1/data1.txt", "r")
point_distances = np.empty(DataPointsPerScan)
angles = np.arange(0, 2*np.pi, (2*np.pi / DataPointsPerScan), dtype=float)
for i in range(DataPointsPerScan):
    point_distances[i] = float(LiDAR_raw_data_file.readline().strip())

# determine and remove outliers
outliers = []
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
# TODO optimize by using previous outlier distances
point_distances = np.empty(DataPointsPerScanAdjust, dtype=float)
for i in range(0, DataPointsPerScanAdjust):
    point_distances[i] = math.sqrt(abs(math.pow(point_data_x[i] - point_data_x[i - 1], 2) + math.pow(point_data_y[i] - point_data_y[i - 1], 2)))

# calculate angle between points
point_angles = np.empty(DataPointsPerScanAdjust, dtype=float)
for i in range(DataPointsPerScanAdjust):
    point_distance_1 = point_distances[i]
    point_distance_2 = point_distances[i - 1]
    point_distance_3 = math.sqrt(abs(math.pow(point_data_x[i] - point_data_x[i - 2], 2) + math.pow(point_data_y[i] - point_data_y[i - 2], 2)))

    # floating point error, out of arccos domain
    if ((math.pow(point_distance_1, 2) + math.pow(point_distance_2, 2) - math.pow(point_distance_3, 2))/(2 * point_distance_1 * point_distance_2)) >= 1:
        point_angles[i] = np.arccos(1)
    elif ((math.pow(point_distance_1, 2) + math.pow(point_distance_2, 2) - math.pow(point_distance_3, 2))/(2 * point_distance_1 * point_distance_2)) <= -1:
        point_angles[i] = np.arccos(-1)
    else:
        point_angles[i] = np.arccos((math.pow(point_distance_1, 2) + math.pow(point_distance_2, 2) - math.pow(point_distance_3, 2))/(2 * point_distance_1 * point_distance_2))

# calculate rate of change between angles
roc_slope_angles = np.empty(DataPointsPerScanAdjust, dtype=float)
for i in range(DataPointsPerScanAdjust):
    roc_slope_angles[i] = abs(point_angles[i - 1]) - abs(point_angles[i])

# calculate rate of change of distances
roc_point_distances = np.empty(DataPointsPerScanAdjust, dtype=float)
for i in range(DataPointsPerScanAdjust):
    roc_point_distances[i] = abs(point_distances[i - 1] - point_distances[i])

# record and mark key points
print(roc_point_distances)
key_points = []
for i in range(DataPointsPerScanAdjust):
    if (abs(roc_slope_angles[i]) > np.deg2rad(MinimumAngleChange)) and (not ((i - 2) in key_points)):
        key_points.append(i - 2)
    if (roc_point_distances[i] > MinimumOutlierDistance) and (not ((i - 1) in key_points)):
        key_points.append(i - 1)

# convert negative key points to their positive counterparts
i = 0
while key_points[i] < 0:
    key_point = key_points[i]
    key_points.pop(i)
    key_points.append(DataPointsPerScanAdjust + key_point)
    i += 1

# combine key points into clusters and display clusters
key_clusters = []
keyClusterPoints = []
if key_points:
    keyClusterPoints = [key_points[0]]
i = 1

# TODO fix algorithm to use distance between two key points not point before it
while i < len(key_points):
    if (abs(keyClusterPoints[-1] - key_points[i]) <= 3) and (point_distances[key_points[i]] < MinimumOutlierDistance):
        keyClusterPoints.append(key_points[i])
    else:
        key_clusters.append([statistics.median_low(keyClusterPoints), len(keyClusterPoints)])
        keyClusterPoints = [key_points[i]]
    i += 1
if keyClusterPoints:
    key_clusters.append([statistics.median_low(keyClusterPoints), len(keyClusterPoints)])

for i in key_clusters:
    colors[i[0]] = [1, 0, 0]
    sizes[i[0]] = 100*i[1]

# show plot
plt.scatter(0, 0, color=[0, 0, 0], s=500)
plt.scatter(0, 0, color=[0, 1, 1], s=300)
plt.scatter(point_data_x, point_data_y, c=colors, s=sizes)
plt.show()

# cleanup
LiDAR_raw_data_file.close()
