#ifndef __POINT_HPP__
#define __POINT_HPP__

#include <utility>
#include "point.h"

class Point {

public:
    Point();
    Point(float GPSx, float GPSy, float IMUAngle, float distance, float pointAngle, bool pointVisited);
    std::pair<float, float> CalculateCoordinate(float GPSx, float GPSy, float IMUAngle, float distance, float pointAngle);
    static float calculateDistance(float x1, float y1, float x2, float y2);

    float x;
    float y;
    float distance;
    float angle;
    bool visited;

};

#endif