# ---------------------------------------------HEATMAP-------------------------------------------
# |   File: Heatmap                                                                              |
# |   Type: .py (python)                                                                         |      
# |   Purpose: Reads data from 'raw_data.csv' and 'TOF.csv' to plot ellipse-based heatmaps for   | 
# |   signal intensity at different locations, relative to Walabot.                              |
# ------------------------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse

RANGE = 8192
ANTPAIRS = 40
TOFFILE = 'TOF.csv'
def main():
    # _______________________________________________________________________________________________________
    #|                                          REQUIRED PARAMETERS                                          |
    #| ______________________________________________________________________________________________________|

    # The user is prompted to enter the following parameters so that the program can identify which data frame
    # and antenna pair to use, along with the range for the heatmap. Note that the range here is set by number 
    # of points, NOT by the distance from Walabot. 
    parser = argparse.ArgumentParser(description = "There are four required parameters to generate a heatmap.")
    parser.add_argument('frameNumber', type=int, help= 'Frame number')
    parser.add_argument('antennaPair', type=int, help='Antenna pair')
    parser.add_argument('lowerlimit', type=int, help='Lower limit range')
    parser.add_argument('upperlimit', type=int, help='Upper limit range')
    parser.add_argument('-file', '--datafile', type=str, help='File containing collected data', default='raw_data.csv') 

    argDict = parser.parse_args()
    upperlimit = argDict.upperlimit
    lowerlimit = argDict.lowerlimit
    datafile = argDict.datafile
    # Based on user input, the starting value of range for reading rows from 'raw_data.csv' is calculated
    # Since python indexing is zero-based, the user input needs to be subtracted by 1 
    rowStartRange = (((argDict.frameNumber - 1) * RANGE) + 1)
    rowEndRange = (rowStartRange) + RANGE - 1
    antennaPair = (argDict.antennaPair - 1)

    # _______________________________________________________________________________________________________
    #|                                            IMPORTING DATA                                             |
    #| ______________________________________________________________________________________________________|

    pd.set_option('precision', 18) # precision of values read from the csv file

    # 'TOF.csv' is a one-column file and doesn't require a certain range of data to be read, hence, loadtxt
    # from numpy library is used to import the data as a numpy array into 'roundtrip'. User needs to set 
    # file path to 'TOF.csv' file
    roundtrip = np.loadtxt(TOFFILE,dtype=float,delimiter=',',skiprows=42,usecols=(0,))

    # 'raw_data.csv' is a large file (size varies depending on how much data is collected), so instead of 
    # importing all the data from it, only a certain column (based on user specified antenna pair) from a 
    # frame (also user input based) is imported into the variable 'power'. The absolute values of the signals
    # is taken 
    io = pd.read_csv(datafile, sep=",", header=None)
    power = abs(io.ix[(rowStartRange + 40):rowEndRange,antennaPair].as_matrix())
    # NOTE: The first 40 values from each frame are disregarded because they correspond to a distance (~5cm)  that  
    # Walabot cannot detect with its long-range sensing profile. 
     

    # _______________________________________________________________________________________________________
    #|                                        PLOTTING ELLIPSES' HEATMAP                                     |
    #| ______________________________________________________________________________________________________|


    # Based on the upper and lower range limits, the max and min of the obtained signals is determined. These
    # values are used to set the max and min intensity values for the heatmap
    z_min = min(power[lowerlimit:upperlimit-1])
    z_max = max(power[lowerlimit:upperlimit-1])


    # 'theta' is used to convert the points on an ellipse into cartesian coordinates. Only one half of the ellipse
    # is considered because the field-of-interest is in front of Walabot
    theta = np.linspace(0,np.pi,225)


    # Initializing empty numpy arrays, which will be updated in the for loop
    majoraxisradius = np.empty(upperlimit)
    minoraxisradius = np.empty(upperlimit)

    # for loop used to make plot every ellipse in cartesian coordinates
    for i in range(lowerlimit, upperlimit,10):

        majoraxisradius[i] = roundtrip[i]/2
        minoraxisradius[i] = np.sqrt(roundtrip[i]**2 - 0.0735**2)/2 

        x = majoraxisradius[i] * np.cos(theta) 
        # 225 points for horizontal axis, for EACH ellipse 

        y = minoraxisradius[i] * np.sin(theta) 
        # 225 corresponding points for vertical axis, for EACH ellipse 

        z = np.full(225, power[i])
        # Setting the signal intensity value for the 'x' and 'y'  

        x1 = x.reshape(15,15)
        y1 = y.reshape(15,15)
        z1 = z.reshape(15,15)

        plt.pcolor(x1,y1,z1, cmap='jet', vmin=z_min, vmax=z_max) 
        # function in matplotlib for plotiing heatmaps

    plt.colorbar() # adds the colorbar on the side of the heatmap
    plt.show() # shows the colorbar



if __name__ == "__main__":
    main()
