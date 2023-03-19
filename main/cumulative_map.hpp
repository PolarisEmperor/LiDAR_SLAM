#ifndef __CUMULATIVE_MAP_HPP__
#define __CUMULATIVE_MAP_HPP__

#include <unordered_map>
#include <tile.hpp>

class TileMap {

    public:
        TileMap();
        std::unordered_map<signed char, std::unordered_map<signed char, Tile>> tiles;
        unsigned short int tileCount;

};


#endif