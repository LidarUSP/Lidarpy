#===============================================================================
# DESCRIPTION
#     make an daily avearged hovermoller plot  of the lidar data
#    
#===============================================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_var(inpath,filename):
    """
    read a splitted file variable (from the ...2.c.py)
    return a dataframe
    """
    data = pd.read_csv(inpath+filename,delim_whitespace=True, index_col=0, parse_dates=[[0,1]], header=None)
    data.columns = np.arange(100,1550,50)
    data.index.name = "Date"
    return data

if __name__ == "__main__":
    inpath="/home/thomas/PhD/obs-lcb/lidar/obs/data/"

    u = read_var(inpath, 'um.csv')
    w = read_var(inpath, 'wm.csv')
    cnr = read_var(inpath, 'CNRm.csv')

    u_daily = u.groupby(lambda t: (t.hour)).mean() # zonal wind
    w_daily = w.groupby(lambda t: (t.hour)).mean() # vertical wind
    cnr_daily = cnr.groupby(lambda t: (t.hour)).mean() # signal noise ratio

    plt.close('all')
    plt.figure()

    levels = np.linspace(cnr_daily.min().min(), cnr_daily.max().max(),100)

    plt.contourf(cnr_daily.index,cnr_daily.columns,cnr_daily.values.T, levels=levels)
    plt.colorbar()
    a=plt.quiver(u_daily.index, u_daily.columns, u_daily.values.T, w_daily.values.T)
    qk = plt.quiverkey(a, 0.9, 1.05, 10, r'$10 \frac{m}{s}$', labelpos='E', fontproperties={'weight': 'bold'})

    plt.xlabel('Time (hours)')
    plt.ylabel('Altitude (m)')

    plt.show()
