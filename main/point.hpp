#ifndef __POINT_HPP__
#define __POINT_HPP__

#include <unordered_set>
#include <utility>
#include "point.hpp"

class Point {

    public:
        Point();
        Point(float GPSx, float GPSy, float IMUAngle, float distance, float pointAngle, bool pointVisited);
        std::pair<float, float> CalculateCoordinate(float GPSx, float GPSy, float IMUAngle, float distance, float pointAngle);
        
        float x;
        float y;
        float distance;
        float angle;
        bool visited;

};

#endif