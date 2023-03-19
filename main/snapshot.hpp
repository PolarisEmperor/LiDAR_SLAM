#ifndef __SNAPSHOT_HPP__
#define __SNAPSHOT_HPP__

#include <vector>
#include <point.hpp>

class Snapshot {

    public:
        Snapshot();
        std::vector<Point> points;
        unsigned short snapNum;
        unsigned char snapAccuracy;
        float snapAngle;
        bool snapVisited;

};

#endif