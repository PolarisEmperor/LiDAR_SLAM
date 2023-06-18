#include <math.h>
#include <iostream>
#include "point.h"

Point::Point() {
    x = y = 0;
    distance = 0;
    angle = 0;
    visited = false;
}

Point::Point(float gx, float gy, float ia, float d, float a, bool v) {
    std::pair<float, float> coordinates = CalculateCoordinate(gx, gy, ia, d, a);
    x = coordinates.first;
    y = coordinates.second;
    distance = d;
    angle = a;
    visited = v;
}

// find absolute coordinates of a point
std::pair<float, float> Point::CalculateCoordinate(float gx, float gy, float ia, float d, float a) {
    float angle = a - ia;
    float xCoord = (d * cos(angle));
    float yCoord = (d * sin(angle));
    return std::make_pair(gx + xCoord, gy + yCoord);
}

float Point::calculateDistance(float x1, float y1, float x2, float y2){
    return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2));
}