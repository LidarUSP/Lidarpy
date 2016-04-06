#!/usr/bin/env python
# -*- coding: cp1252 -*-

"""
Program created by Marcia Marques - Dez/15
Reads the 'Measurements_WLS70_corrected.txt'
and plots the data.
Plots the time series as an static graph.
! The plot depends on the configuration of the lidar (altitudes).
"""

# ============================================================================
import datetime as dt
import glob
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.widgets import CheckButtons
import numpy as np
import matplotlib.cm as cm

# ============================================================================
# Open only the first file
files = glob.glob("Data/*.sta")
infile = open(files[0])
infile_read = csv.reader(infile, delimiter='\t')

# Ignores some lines in the header
for i in range(0, 62):
    next(infile_read)
    i += 1

# Reads the levels of measurements
levels = infile_read.next()
levels = (len(levels) - 1)

# Closes the file
infile.close()

# ============================================================================
# Uses the 'Measurements_WLS70_corrected.txt' to make the plots
full_path = "Measurements_WLS70_corrected.txt"

# Counts the number of lines (opens and closes the file)
n_lines = 0
infile = open(full_path)
for line in infile.readlines():
    n_lines += 1
n_lines -= 1  # What matters are the lines after the header
infile.close()

print 'n_lines = ', n_lines

# ============================================================================
# Opens the files
infile = open(full_path)
infile_read = csv.reader(infile, delimiter='\t')

# Ignores the header
head = infile_read.next()

# Creates a list of zeros (variable)
Timestamp = [0] * n_lines
Timestamp_raw = [0] * n_lines

# Creates arrays of zeros (variables)
WiperCount = np.zeros(n_lines)
IntTemp = np.zeros(n_lines)
ExtTemp = np.zeros(n_lines)
Pressure = np.zeros(n_lines)
RelHumidity = np.zeros(n_lines)

# Creates matrices of zeros (variables)
Vhm = np.zeros(shape=(n_lines, levels))
dVh = np.zeros(shape=(n_lines, levels))
VhMax = np.zeros(shape=(n_lines, levels))
VhMin = np.zeros(shape=(n_lines, levels))
Dir = np.zeros(shape=(n_lines, levels))
um = np.zeros(shape=(n_lines, levels))
du = np.zeros(shape=(n_lines, levels))
vm = np.zeros(shape=(n_lines, levels))
dv = np.zeros(shape=(n_lines, levels))
wm = np.zeros(shape=(n_lines, levels))
dw = np.zeros(shape=(n_lines, levels))
CNRm = np.zeros(shape=(n_lines, levels))
dCNR = np.zeros(shape=(n_lines, levels))
CNRmax = np.zeros(shape=(n_lines, levels))
CNRmin = np.zeros(shape=(n_lines, levels))
sigmaFreqm = np.zeros(shape=(n_lines, levels))
dsigmaFreq = np.zeros(shape=(n_lines, levels))
Avail = np.zeros(shape=(n_lines, levels))

# Loop to assign the columns to the variables
i = 0
for row in infile_read:
    Timestamp_raw[i] = row[0]
    Timestamp[i] = dt.datetime(int(row[0][0:4]),
                               int(row[0][5:7]),
                               int(row[0][8:10]),
                               int(row[0][11:13]),
                               int(row[0][14:16]))
    WiperCount[i] = row[1]
    IntTemp[i] = row[2]
    ExtTemp[i] = row[3]
    Pressure[i] = row[4]
    RelHumidity[i] = row[5]

    for j in range(0, levels):
        Vhm[i][j] = row[6 + j * 18]
        dVh[i][j] = row[7 + j * 18]
        VhMax[i][j] = row[8 + j * 18]
        VhMin[i][j] = row[9 + j * 18]
        Dir[i][j] = row[10 + j * 18]
        um[i][j] = row[11 + j * 18]
        du[i][j] = row[12 + j * 18]
        vm[i][j] = row[13 + j * 18]
        dv[i][j] = row[14 + j * 18]
        wm[i][j] = row[15 + j * 18]
        dw[i][j] = row[16 + j * 18]
        CNRm[i][j] = row[17 + j * 18]
        dCNR[i][j] = row[18 + j * 18]
        CNRmax[i][j] = row[19 + j * 18]
        CNRmin[i][j] = row[20 + j * 18]
        sigmaFreqm[i][j] = row[21 + j * 18]
        dsigmaFreq[i][j] = row[22 + j * 18]
        Avail[i][j] = row[23 + j * 18]
    i += 1

# 18 is the number of variables that indicates the
# size of the block of variables, in other words
# the number of variable in that level.

# ============================================================================
fig = plt.figure(figsize=(200, 380), facecolor='#D0D0D0')

# Plots all the levels of the variable 'Vhm'
ax1 = plt.subplot2grid((2, 2), (0, 0), rowspan=1, colspan=3, axisbg='#A0A0A0')
ax1.grid(True)
# Number of levels to be considered
number = 23
c_map = plt.get_cmap('Blues')
colors = [c_map(i) for i in np.linspace(0, 1, number)]
for i, color in enumerate(colors, start=0):
    plt.plot(Timestamp, np.hsplit(Vhm, levels)[i], color=color, label='Vhm_{i}m'.format(i=i * 20 + 100))
plt.ylabel('Wind Speed $(m/s)$')
legend = plt.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), fontsize=8)
legend.get_frame().set_facecolor('#A0A0A0')

# Plots the CNR Threshold
CNRm_lim = [-26] * n_lines

# Plots all the levels of the variable 'CNRm'
ax2 = plt.subplot2grid((2, 2), (1, 0), rowspan=1, colspan=3, sharex=ax1, axisbg='#A0A0A0')
ax2.grid(True)
for i, color in enumerate(colors, start=0):
    plt.plot(Timestamp, np.hsplit(CNRm, levels)[i], color=color, label='CNRm_{i}m'.format(i=i * 20 + 100))
plt.plot(Timestamp, CNRm_lim, 'r', visible=True)
plt.ylabel('CNR $(dB)$')
legend = plt.legend(loc='center left', bbox_to_anchor=(1.02, 0.43), fontsize=8)
legend.get_frame().set_facecolor('#A0A0A0')

# Adjusts the timestamp axis
ax1.xaxis.set_major_locator(mticker.MaxNLocator(50))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
for label in ax2.xaxis.get_ticklabels():
    label.set_fontsize(8)
    label.set_rotation(90)

# Adjusts the graph area
plt.subplots_adjust(left=0.04, bottom=0.15, right=0.88, top=0.93, wspace=0.20, hspace=0.09)

ax2.set_xlabel('Timestamp', horizontalalignment='center')
plt.suptitle('Lidar WLS70', fontsize=20)
plt.setp(ax1.get_xticklabels(), visible=False)

plt.savefig('TimeSeries-low.png')
plt.show()