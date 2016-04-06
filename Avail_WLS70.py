"""
Plots the availability of the data
"""

# ============================================================================
import datetime as dt
import csv
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker
import matplotlib.dates as mdates

# ============================================================================
# Uses the 'Avail.txt' to make the plot
full_path = "Avail.txt"

# Counts the number of lines (opens and closes the file)
infile = open(full_path)
n_lines = 0
for line in infile.readlines():
    n_lines += 1
infile.close()

# ============================================================================
# Counts the number of columns (opens and closes the file)
infile = open(full_path)
infile_read = csv.reader(infile, delimiter='\t')

first_row = next(infile_read)
n_cols = len(first_row)
levels = n_cols - 2  # Ignores the Timestamp columns (date and hour)

infile.close()

print 'n_lines = ', n_lines
print 'levels = ', levels

# ============================================================================
# Opens the files
infile = open(full_path)
infile_read = csv.reader(infile, delimiter='\t')

# Creates a list of zeros (variable)
Timestamp = [0] * n_lines

# Creates matrices of zeros (variables)
Avail = np.zeros(shape=(n_lines, levels))

# Loop to assign the columns to the variables
i = 0
for row in infile_read:
    Timestamp[i] = dt.datetime(int(row[0][0:4]),
                               int(row[0][5:7]),
                               int(row[0][8:10]),
                               int(row[0][11:13]),
                               int(row[0][14:16]))
    for j in range(0, levels):
        Avail[i][j] = row[1 + j]
    i += 1

x = Timestamp
y = np.array(range(100, 1020, 20))
z = Avail.transpose()

ax = plt.subplot2grid((1, 1), (0, 0), rowspan=1, colspan=1)
clevs = np.linspace(0.0, 100.0, num=41)
CS = plt.contourf(x, y, z, cmap=plt.cm.jet, levels=clevs)
c_bar = plt.colorbar(CS)

# Adjusts the timestamp axis
ax.xaxis.set_major_locator(mticker.MaxNLocator(30))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
for label in ax.xaxis.get_ticklabels():
    label.set_fontsize(8)
    label.set_rotation(90)

# Adjusts the graph area
plt.subplots_adjust(bottom=0.22)

plt.suptitle('WLS70', fontsize=20, horizontalalignment='center')
plt.ylabel('Height $(m)$')
plt.xlabel('Timestamp')
c_bar.set_label('Data Availability $(\%)$')

plt.savefig('Avail_WLS70.png')
plt.show()