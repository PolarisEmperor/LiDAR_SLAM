#include "cumulative_map.h"
#include <math.h>
#include <unordered_map>
#include <fstream>
#include <sstream>
#include <string>
#include <iostream>
#define LIDAR_RESOLUTION 512
#define WAYPOINT_RESOLUTION 0.01

//find nearest unvisited point, returns -999, -999 if walltrace, 999, 999 if done
std::pair<float, float> findTarget(TileMap& tm){

}

//find list of waypoints to drive to target point
std::vector< std::pair<float, float> > calculateWaypoints(std::pair<float, float>){


}

//send driving instructions to robot
bool navigateToWaypoint(std::pair<float, float>){
    
}

int main() {
    std::ifstream file;
    std::string line;
    file.open("/Users/dhruvachakravarthi/Documents/a.txt");

    float GPSx, GPSy, IMUa;
    float* LiDAR = (float*)malloc(LIDAR_RESOLUTION * sizeof(float));
    
    std::getline(file, line);
    std::cout << line << std::endl;
    GPSx = std::stof(line);

    std::getline(file, line);
    std::cout << line << std::endl;
    GPSy = std::stof(line);

    std::getline(file, line);
    std::cout << line << std::endl;
    IMUa = std::stof(line);

    for(int i  = 0; i < 512; i++){
        std::getline(file, line);
        //std::cout << line << std::endl;
        LiDAR[i] = std::stof(line);
    }
    
    file.close();

    TileMap tm;
    tm.addSnapshot(LiDAR, GPSx, GPSy, IMUa);
    tm.addSnapshot(LiDAR, GPSx, GPSy, IMUa);
    return 0;
}