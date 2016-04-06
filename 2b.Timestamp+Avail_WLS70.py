#!/usr/bin/env python
# -*- coding: cp1252 -*-

"""
Program created by Marcia Marques - Dec/15
Based on the file "Measurements_WLS70.txt" creates the file
"Measurements_WLS70_correct+avail.txt" with a corrected timestamp,
in other words, fixed time intervals, even though absent data.
And takes into account only the data at 100% availability or
other value to be defined here.
"""

# ============================================================================
import datetime as dt
import numpy as np
import glob
import csv

# ============================================================================
# Open only the first file
files = glob.glob("Data/*.sta")
infile = open(files[0])
infile_read = csv.reader(infile, delimiter='\t')

# Ignores some lines in the header
# Double header were corrected manually
for i in range(0, 62):
    next(infile_read)
    i += 1

# Reads the levels of measurements
levels = infile_read.next()
levels = (len(levels) - 1)

# Just ignores the next line
jump = infile_read.next()

# Reads the name of the variables (each column)
head = infile_read.next()
# Remove empty spaces
while '' in head:
    head.remove('')

# Creates the output file
out = open('Measurements_WLS70_corrected+avail.txt', 'w')
# Writes the header of the output file with only the name of the variables
for i in range(0, len(head)):
    out.write(head[i])
    out.write('\t')
out.write("\n")
out.close()

# Closes the file
infile.close()

# ============================================================================
# Uses the 'Measurements_WLS70.txt' to make the corrections
full_path = "Measurements_WLS70.txt"

# Counts the number of lines (opens and closes the file)
n_lines = 0
infile = open(full_path)
for line in infile.readlines():
    n_lines += 1
infile.close()
n_lines -= 1  # What matters are the lines after the header

print 'n_lines = ', n_lines

# ============================================================================
# Opens the file
infile = open(full_path)
infile_read = csv.reader(infile, delimiter='\t')

# Ignores the header
next(infile_read)

# Creates lists of zeros (variables)
Timestamp_raw = [0] * n_lines
Timestamp = [0] * n_lines

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

# Timestamp reference:
# print "all", row[0][0:16]
# print "year", row[0][6:10]
# print "month", row[0][3:5]
# print "day", row[0][0:2]
# print "hour", row[0][11:13]
# print "minute", row[0][14:16]

# Loop to assign the columns to the variables
i = 0
for row in infile_read:
    Timestamp_raw[i] = row[0]
    Timestamp[i] = dt.datetime(int(row[0][6:10]),
                               int(row[0][3:5]),
                               int(row[0][0:2]),
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

# Replace spurious values by 'NaN'
np.place(Vhm, Vhm == 50000, 'NaN')
np.place(Vhm, Vhm == -50000, 'NaN')
np.place(dVh, dVh == 50000, 'NaN')
np.place(dVh, dVh == -50000, 'NaN')
np.place(VhMin, VhMin == 50000, 'NaN')
np.place(VhMin, VhMin == -50000, 'NaN')
np.place(VhMax, VhMax == 50000, 'NaN')
np.place(VhMax, VhMax == -50000, 'NaN')
np.place(Dir, Dir == 50000, 'NaN')
np.place(Dir, Dir == -50000, 'NaN')
np.place(um, um == 50000, 'NaN')
np.place(um, um == -50000, 'NaN')
np.place(du, du == 50000, 'NaN')
np.place(du, du == -50000, 'NaN')
np.place(vm, vm == 50000, 'NaN')
np.place(vm, vm == -50000, 'NaN')
np.place(dv, dv == 50000, 'NaN')
np.place(dv, dv == -50000, 'NaN')
np.place(wm, wm == 50000, 'NaN')
np.place(wm, wm == -50000, 'NaN')
np.place(dw, dw == 50000, 'NaN')
np.place(dw, dw == -50000, 'NaN')
np.place(CNRm, CNRm == 50000, 'NaN')
np.place(CNRm, CNRm == -50000, 'NaN')
np.place(dCNR, dCNR == 50000, 'NaN')
np.place(dCNR, dCNR == -50000, 'NaN')
np.place(CNRmax, CNRmax == 50000, 'NaN')
np.place(CNRmax, CNRmax == -50000, 'NaN')
np.place(CNRmin, CNRmin == 50000, 'NaN')
np.place(CNRmin, CNRmin == -50000, 'NaN')
np.place(sigmaFreqm, sigmaFreqm == 50000, 'NaN')
np.place(sigmaFreqm, sigmaFreqm == -50000, 'NaN')
np.place(dsigmaFreq, dsigmaFreq == 50000, 'NaN')
np.place(dsigmaFreq, dsigmaFreq == -50000, 'NaN')
np.place(Avail, Avail == 50000, 'NaN')
np.place(Avail, Avail == -50000, 'NaN')

# Time step
delta = dt.timedelta(minutes=10)

# Creates empty list to the corrected timestamp
Timestamp_correct = list()

# Initial timestamp
Timestamp_step = Timestamp[0]

# Loop to create the corrected timestamp
while Timestamp_step != Timestamp[n_lines - 1]:
    Timestamp_correct.append(Timestamp_step)
    Timestamp_step = Timestamp_step + delta

# Adding the last timestamp
Timestamp_correct.append(Timestamp[n_lines - 1])

print 'len(Timestamp)', len(Timestamp)
print 'len(Timestamp_correct)', len(Timestamp_correct)

# Corrects the timestamp
i = 0
while len(Timestamp) != len(Timestamp_correct):
    if Timestamp_correct[i] == Timestamp[i]:
        i += 1
    elif str(Timestamp_correct[i] - Timestamp[i]) == "1 day, 0:00:00":
        i += 1
    else:
        Timestamp.insert(i, Timestamp_correct[i])
        WiperCount = np.insert(WiperCount, i, 'NaN')
        IntTemp = np.insert(IntTemp, i, 'NaN')
        ExtTemp = np.insert(ExtTemp, i, 'NaN')
        Pressure = np.insert(Pressure, i, 'NaN')
        RelHumidity = np.insert(RelHumidity, i, 'NaN')
        Vhm = np.insert(Vhm, i, 'NaN', axis=0)
        dVh = np.insert(dVh, i, 'NaN', axis=0)
        VhMax = np.insert(VhMax, i, 'NaN', axis=0)
        VhMin = np.insert(VhMin, i, 'NaN', axis=0)
        Dir = np.insert(Dir, i, 'NaN', axis=0)
        um = np.insert(um, i, 'NaN', axis=0)
        du = np.insert(du, i, 'NaN', axis=0)
        vm = np.insert(vm, i, 'NaN', axis=0)
        dv = np.insert(dv, i, 'NaN', axis=0)
        wm = np.insert(wm, i, 'NaN', axis=0)
        dw = np.insert(dw, i, 'NaN', axis=0)
        CNRm = np.insert(CNRm, i, 'NaN', axis=0)
        dCNR = np.insert(dCNR, i, 'NaN', axis=0)
        CNRmax = np.insert(CNRmax, i, 'NaN', axis=0)
        CNRmin = np.insert(CNRmin, i, 'NaN', axis=0)
        sigmaFreqm = np.insert(sigmaFreqm, i, 'NaN', axis=0)
        dsigmaFreq = np.insert(dsigmaFreq, i, 'NaN', axis=0)
        Avail = np.insert(Avail, i, 'NaN', axis=0)
        i += 1

# Corrects the availability
for i in range(0, len(Timestamp_correct)):
    for j in range(0, levels):
        if Avail[i][j] < 100:
            Vhm[i][j] = "NaN"
            dVh[i][j] = "NaN"
            VhMax[i][j] = "NaN"
            VhMin[i][j] = "NaN"
            Dir[i][j] = "NaN"
            um[i][j] = "NaN"
            du[i][j] = "NaN"
            vm[i][j] = "NaN"
            dv[i][j] = "NaN"
            wm[i][j] = "NaN"
            dw[i][j] = "NaN"
            CNRm[i][j] = "NaN"
            dCNR[i][j] = "NaN"
            CNRmax[i][j] = "NaN"
            CNRmin[i][j] = "NaN"
            sigmaFreqm[i][j] = "NaN"
            dsigmaFreq[i][j] = "NaN"

# ============================================================================
# Writing the output file
out = open('Measurements_WLS70_corrected+avail.txt', 'a')
for i in range(len(Timestamp_correct)):
    out.write(str(Timestamp_correct[i]))
    out.write('\t')
    out.write(str(WiperCount[i]))
    out.write('\t')
    out.write(str(IntTemp[i]))
    out.write('\t')
    out.write(str(ExtTemp[i]))
    out.write('\t')
    out.write(str(Pressure[i]))
    out.write('\t')
    out.write(str(RelHumidity[i]))
    out.write('\t')
    for j in range(0, levels):
        Vhm[i][j].tofile(out, 'str')
        out.write('\t')
        dVh[i][j].tofile(out, 'str')
        out.write('\t')
        VhMax[i][j].tofile(out, 'str')
        out.write('\t')
        VhMin[i][j].tofile(out, 'str')
        out.write('\t')
        Dir[i][j].tofile(out, 'str')
        out.write('\t')
        um[i][j].tofile(out, 'str')
        out.write('\t')
        du[i][j].tofile(out, 'str')
        out.write('\t')
        vm[i][j].tofile(out, 'str')
        out.write('\t')
        dv[i][j].tofile(out, 'str')
        out.write('\t')
        wm[i][j].tofile(out, 'str')
        out.write('\t')
        dw[i][j].tofile(out, 'str')
        out.write('\t')
        CNRm[i][j].tofile(out, 'str')
        out.write('\t')
        dCNR[i][j].tofile(out, 'str')
        out.write('\t')
        CNRmax[i][j].tofile(out, 'str')
        out.write('\t')
        CNRmin[i][j].tofile(out, 'str')
        out.write('\t')
        sigmaFreqm[i][j].tofile(out, 'str')
        out.write('\t')
        dsigmaFreq[i][j].tofile(out, 'str')
        out.write('\t')
        Avail[i][j].tofile(out, 'str')
        out.write('\t')
    out.write("\n")
out.close()

# Closes the file
infile.close()