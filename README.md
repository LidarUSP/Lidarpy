# Lidarpy
Repository which contains code to analyse lidar data

## File/folder description
*Data
   Contain data of the Lidar for the summer 2015

1. LIDAR_WLS70.py
  * Take all the ".sta" output of the lidar and merge them into one unique file

2. TimestampXXXXX.py
  * Control the timestamp, the data availability and split the file
  1. a = Create a complete timeserie and fill the missing data with nan (?)
  2. b = a + select date with a certain amount of data availability
  3. c = a + b + allow to write one variable by file
