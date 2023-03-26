#ifndef __TILE_HPP__
#define __TILE_HPP__

#include <unordered_set>
#include <snapshot.hpp>

class Tile {

    public:
        Tile();
        Tile(std::vector<Point> points, bool visited);
        bool addSnapshotToTile(Snapshot snapshot);
        static std::pair<int, int> calculateTile(Point point);

        std::unordered_set<Snapshot> snapshots;
        unsigned short tileAccuracy;
        bool tileVisited;

};

#endif