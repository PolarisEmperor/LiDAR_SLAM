#ifndef __POINT_HPP__
#define __POINT_HPP__

#include <unordered_set>
#include <point.hpp>

class Point {

    public:
        Point();
        signed short x;
        signed short y;
        unsigned short distance;
        float angle;
        bool visited;

};

#endif