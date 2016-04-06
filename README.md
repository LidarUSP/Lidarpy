#Lidarpy
Repository which contains python programms to analyse lidar data

Founded by:
* [Marcia Marques](https://github.com/orgs/LidarUSP/people/MarciaMarques) (IPEN/USP) - main contributor
* [Thomas Martin](https://github.com/TomCMM) (IAG/USP)

## File/folder description
- Data
   Contains data of the lidar for the summer 2014/2015

- 1.LIDAR_WLS70.py
  * Take all the ".sta" output of the lidar and merge them into one unique file

- 2.TimestampXXXXX.py
  * Corrects the timestamp, filters the data by the availability and rewrite the file
  1. a = Create a complete timeseries, filling the missing data with 'nan'
  2. b = a + select date with a certain amount of data availability
  3. c = a + b + allow to write one variable by file

- Avail_WLS70.py
  * Plots the data availability 

- TimeSeries
  *high = Make time serie plot of the upper part
  *low = Make time serie plot of the lower part

## Graphics Example
### Time Series plot
![alt text](https://github.com/LidarUSP/Lidarpy/blob/master/plot/TimeSeries-high.png "Time Serie plot")

### Data Availability 
![alt text](https://github.com/LidarUSP/Lidarpy/blob/master/plot/Avail_WLS70.png "Availability plot")
