#ifndef __TILE_HPP__
#define __TILE_HPP__

#include <unordered_set>
#include <snapshot.hpp>

class Tile {

    public:
        Tile();
        std::unordered_set<Snapshot> snapshots;
        unsigned char tileAccuracy;
        bool tileVisited;

};

#endif