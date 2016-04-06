#!/usr/bin/env python
# -*- coding: cp1252 -*-

"""
Program created by Marcia Marques - Dec/15
Compiles all files '.sta' in the specified directory
in an unique file 'Measurements_WLS70.txt'.
"""

# ============================================================================
import numpy as np
import glob
import csv
import os

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

# Just ignores the next line
jump = infile_read.next()

# Reads the name of the variables (each column)
head = infile_read.next()
# Remove empty spaces
while '' in head:
    head.remove('')

# Creates the output file
out = open('Measurements_WLS70.txt', 'w')
# Writes the header of the output file with only the name of the variables
for i in range(0, len(head)):
    out.write(head[i])
    out.write('\t')
out.write("\n")
out.close()

# Closes the file
infile.close()

# ============================================================================
# Lists all the files '.sta' in the specified directory
directory = 'Data'
archives = os.listdir(directory)
archives.sort()

# Loop to do the same with all the files
for archive in archives:
    full_path = os.path.join(directory, archive)
    if os.path.isfile(full_path):

        print full_path

        # Counts the number of lines (opens and closes the file)
        n_lines = 0
        infile = open(full_path)
        for line in infile.readlines():
            n_lines += 1
        infile.close()
        n_lines -= 65  # What matters are the lines after the header

        print 'n_lines = ', n_lines

        # ============================================================================

        # Opens the files
        infile = open(full_path)
        infile_read = csv.reader(infile, delimiter='\t')

        # Ignores the header
        for i in range(0, 65):
            next(infile_read)
            i += 1

        # Creates a list of zeros (variable)
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

        # Loop to assign the columns to the variables
        i = 0
        for row in infile_read:
            Timestamp[i] = row[0]
            WiperCount[i] = row[1]
            IntTemp[i] = row[2]
            ExtTemp[i] = row[3]
            Pressure[i] = row[4]
            RelHumidity[i] = row[5]

            for j in range(0, levels):
                Vhm[i][j] = row[6 + j * 19]
                dVh[i][j] = row[7 + j * 19]
                VhMax[i][j] = row[8 + j * 19]
                VhMin[i][j] = row[9 + j * 19]
                Dir[i][j] = row[10 + j * 19]
                um[i][j] = row[11 + j * 19]
                du[i][j] = row[12 + j * 19]
                vm[i][j] = row[13 + j * 19]
                dv[i][j] = row[14 + j * 19]
                wm[i][j] = row[15 + j * 19]
                dw[i][j] = row[16 + j * 19]
                CNRm[i][j] = row[17 + j * 19]
                dCNR[i][j] = row[18 + j * 19]
                CNRmax[i][j] = row[19 + j * 19]
                CNRmin[i][j] = row[20 + j * 19]
                sigmaFreqm[i][j] = row[21 + j * 19]
                dsigmaFreq[i][j] = row[22 + j * 19]
                Avail[i][j] = row[23 + j * 19]
            i += 1

        i = 0
        j = 0

        # 19 is the number of variables + 1 (that refers to a column space)
        # that indicates the size of the block of variables, in other words
        # the number of variable in that level

        # ============================================================================

        # Writing the output file
        out = open('Measurements_WLS70.txt', 'a')
        for i in range(n_lines):
            out.write(str(Timestamp[i]))
            out.write('\t')
            WiperCount[i].tofile(out, 'str')
            out.write('\t')
            IntTemp[i].tofile(out, 'str')
            out.write('\t')
            ExtTemp[i].tofile(out, 'str')
            out.write('\t')
            Pressure[i].tofile(out, 'str')
            out.write('\t')
            RelHumidity[i].tofile(out, 'str')
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
        # ============================================================================

        # Closes the files
        infile.close()