#include "cumulative_map.h"
#include "tile.h"
#include <math.h>
#include <unordered_map>
#include <fstream>
#include <sstream>
#include <string>
#include <iostream>
#define LIDAR_RESOLUTION 512 

TileMap::TileMap() {
    tileCount = 0;
}

Tile& TileMap::getTile(std::pair<int, int> &t) {
    return tiles[t.first][t.second];
}

void TileMap::createTile(std::pair<int, int> &t, Tile tile) {
    if (!tiles.count(t.first)){
        tiles[t.first] = std::unordered_map<int, Tile>();
    }
    if (!tiles[t.first].count(t.second)){
        tiles[t.first][t.second] = tile;
    }
}

bool TileMap::tileExists(std::pair<int, int> &t) {
    if (tiles.count(t.first)) {
        if (tiles[t.first].count(t.second))
            return true;
    }
    return false;
}

void TileMap::addSnapshot(float* distList, float GPSx, float GPSy, float IMUa) {
    std::vector<Point> pointList;

    //convert distance list to vector of points
    for (int i = 0; i < LIDAR_RESOLUTION; i++) {
        if (!isnormal(distList[i]))
            continue;

        float pointAngle = (i * ((2 * M_PI) / LIDAR_RESOLUTION));
        pointList.push_back(Point(GPSx, GPSy, IMUa, distList[i], pointAngle, false));
    }

    //TODO - check backward: 512 and 0 may be part of same snap
    std::pair<int, int> previousTile = Tile::calculateTile(pointList[0]);
    int start = 0;
    int tTime = 0;
    for (int i = 1; i < pointList.size(); i++) {
        if (Tile::calculateTile(pointList[i]) != previousTile) {
            Snapshot s = Snapshot(std::vector<Point>(pointList.begin() + start, pointList.begin() + (i - 1)), snapshotCount, false);

            if (tileExists(previousTile)) {
                Tile& t = getTile(previousTile);
                t.addSnapshotToTile(s);
            }
            else {
                createTile(previousTile, Tile(s));
            }

            start = i;
            previousTile = Tile::calculateTile(pointList[i]);
        }
    }

    snapshotCount++;
}
