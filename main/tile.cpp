#include "tile.h"
#include "point.h"
#include <ctime>
#include <math.h>
#include <iostream>
#define TILE_SIZE 0.15
#define DISCARD_POINT_DIST 0.0075

Tile::Tile() {
    tileAccuracy = 0;
    tileVisited = false;
}

Tile::Tile(Snapshot snap) {
    snapshots.insert(snap);
}

// returns the tile that a points belongs to
std::pair<int, int> Tile::calculateTile(Point p) {
    return std::pair<int, int>(trunc(p.x / TILE_SIZE), trunc(p.y / TILE_SIZE));
}

bool Tile::addSnapshotToTile(Snapshot s) {
    Snapshot newSnapshot;
    //check if point exists
    for(auto p : s.points){
        bool pointFound = false;
        for(auto s : snapshots){
            for(auto p_ : s.points){
                if(Point::calculateDistance(p_.x, p_.y, p.x, p.y) < DISCARD_POINT_DIST){
                    pointFound = true;
                    break;
                }
            }
            if(pointFound){
                break;
            }
        }
        if(!pointFound){
            newSnapshot.addPoint(p);
        }
    }
    snapshots.insert(newSnapshot);
    return true;
}
