#ifndef __CUMULATIVE_MAP_HPP__
#define __CUMULATIVE_MAP_HPP__

#include <unordered_map>
#include "tile.h"

class TileMap {

public:
    TileMap();
    
    Tile& getTile(std::pair<int, int> tile);
    void createTile(std::pair<int, int> tile, Snapshot snapshot);
    bool tileExists(std::pair<int, int> tile);
    void addSnapshot(float* LiDAR_scan, float GPSx, float GPSy, float IMUa);
    

    std::unordered_map<int, std::unordered_map<int, Tile> > tiles;
    unsigned short tileCount;
    unsigned short snapshotCount;
};


#endif