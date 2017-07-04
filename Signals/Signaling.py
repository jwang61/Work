# --------------------------------------DATA COLLECTION-------------------------------------------
# |   File: DataCollection                                                                       |
# |   Type: .py (python)                                                                         |      
# |   Purpose: Subtracts an initially recorded background from newly collected data and saves it |
# |   into a csv file called 'raw_data'
# ------------------------------------------------------------------------------------------------

import sys
import os
import WalabotAPI as wlbt
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft

REMOVEBACKGROUND = False
SAVEFIGS = False
AVGFRAME = 8
PAIRS = (1, 2,  )  #3, 14, 32
# _______________________________________________________________________________________________________
#|                                            COLOR MATRIX                                               |
#| ______________________________________________________________________________________________________|

# The matrix with 40 different colors; this is to be used later when plotting data from the antenna
# pairs. THe size of this matrix is 40 because that correlates with the total number of available 
# antenna pairs.
COLORS = [
"0000FF", "00FF00", "FF0000", "00FFFF", "008000", "000000", "ADD8E6", "F8F8FF", "F0FFF0", "6495ED",
"6A5ACD", "FAF0E6", "00008B", "B0E0E6", "2E8B57", "BDB76B", "FFFAFA", "A0522D", "0000CD", "4169E1",
"E0FFFF", "008000", "9370DB", "191970", "FFF8DC", "AFEEEE", "FFE4C4", "708090", "008B8B", "F0E68C",
"F5DEB3", "008080", "9932CC", "FA8072", "00BFFF", "663399", "8B0000", "4682B4", "DB7093", "778899"]

# This is the default number of cycles that the WalaBot will use to calibrate and find average background
CCYCLES = 10 
   
# ________________________________________________________________________________________________________
#|                                                 CALIBRATION                                            |
#| _______________________________________________________________________________________________________|
# Scans the arena n times and takes the average of those scans for the background signals' frame

def calibrate(pairs, numPairs):
    print("Calibrating")
    # Lets the user know calibration has begun
    background = []
    for i in range(CCYCLES):
        wlbt.Trigger()

        for pair in pairs:
            targets = wlbt.GetSignal(pair)
            background.append(targets[0])

    background = np.asarray(background)
    average_background = [sum([background[i+x] for x in range(0, numPairs*CCYCLES, numPairs)]) for i in range(numPairs)]

    average_background = np.asarray(average_background)
    average_background /= CCYCLES

    print("Calibration Complete")
    return average_background

def main():
   
    # The custom-made function to plot the data, depending on the number of antenna pairs chosen
    # function for a lot of data (PROF_SENSOR PROFILE)

        # The for loop goes up to the size of 'numPairs', which is the number of antenna pairs, so that
        # the loop can plot data from every antenna pair used.
           # 'timeAxis' is a 1D array contining the time domain values for the obtained raw signals. 
           # 'signal_list' is a multidimensional array (the number of dimensions is equal to antenna
           #  pairs being used). Each element of the array refers to the obtained signal values for
           #  the correspoding antenna pair. For example, if the 'number' is 3, then the backscattered
           #  amplitudes btained from teh 3rd antenna pair will be plotted. 
           # 'COLORS' is used to change the line color for each antenna pair. 

            # _______________________________________________________________________________________________________
    #|                                     INITIALIZING/CNNECTING WALABOT                                    |
    #| ______________________________________________________________________________________________________|

    # Reading in input parameters
    outfile = None
    if len(sys.argv) > 1:
        outfile = sys.argv[1]
    # Load the python WalabotAPI into the program as 'wlbt' and initialize it
    wlbt.Init()
    wlbt.SetSettingsFolder()

    # Establish a connection between the Walabot and the computer
    wlbt.ConnectAny()

    # Set sensor profile
    wlbt.SetProfile(wlbt.PROF_SENSOR)

    # Set filtering to none
    wlbt.SetDynamicImageFilter(wlbt.FILTER_TYPE_NONE)


    # ________________________________________________________________________________________________________
    #|                                    GET ANTENNA PAIRS AND START WALABOT                                 |
    #| _______________________________________________________________________________________________________|


    # Get the list of antenna pairs that are available and store it in an array and store the number of antenna in numPairs
    allpairs = wlbt.GetAntennaPairs()
    pairs = []
    for index in PAIRS:
        pairs.append(allpairs[index])
        print allpairs[index]
    numPairs = len(pairs)
    # Start the Walabot device
    wlbt.Start()


    # ________________________________________________________________________________________________________
    #|                                              LIVE-UPDATING GRAPH                                       |
    #| _______________________________________________________________________________________________________|

    # Based on the user parameter input, a output file will be created that will store the data
    # If file already exists, user will be prompted whether to replace the file
    f = None
    if outfile:
        filePath = os.path.join(os.getcwd(), outfile)    
        if os.path.isfile(filePath):
            print "WARNING: Output file already exists and will be replaced. Press any key to confirm."
            raw_input()
        f = open(outfile, "w")

    # Initializing a zero-filled array, which is then updated with the collected data. The size of the array
    # depends on the number of antenna pairs to be used.  
    timeAxis = []
    signal_list = []
    average_background = calibrate(pairs, numPairs)
    # Initializing the figure window for plotting
    plt.ion()  
    fig = plt.figure()
    ax = fig.add_subplot(111) 
    axes = plt.gca()
    axes.set_ylim([-1, 1])
    #ax.set_yscale("log")
    plt.axvline(x=0.000000005)
    # ________________________________________________________________________________________________________
    #|                                           RAW SIGNALS' COLLECTION                                      |
    #| _______________________________________________________________________________________________________|

    # Using a 'try-and-except' here to allow user to stop the data collection whenever they want
    # by using Ctrl+C
    try:
        j=1 # Counter variable for saving the figure
        line_list = []
        # The infinite loop that runs until the user stops the program with keyboard interrupt.
        # This loop allows the Wlaabot to continuously scan the the arena that has been set.
        while True: 
            sum_list = []
            for frame in range(AVGFRAME):
                   
                # Walabot API function used to initiate the scan 
                wlbt.Trigger()
            
                # The elements in the previously declared 'signal_list' are cleared. This is done so that 
                # every time this loop runs, the 'signal_list' is updated with the new values and doesn't
                # carry on the previous values. Having the previous values in the list would disrupt the 
                # plotting because the size of the 'signal_list' wouldn't match the 'timeAxis' in that case.
                signal_list = []
                ft_list = [] 

                # The for loop goes up to the number of antenna pairs used. This loop allows the Walabot
                # to get the raw signals from each one of the selected number of antenna pairs, for every 
                # scan. 
                    # 'GetSignal' from WalabotAPI which returns the time domain values and the returned signal
                    # amplitudes. The data from this function is stored in 'targets' (2D array). The first array 
                    # within 'targets' has the returned signal amplitudes and thus, those values are appended to 
                    # 'signal_list'. The second array in 'targets' contains the time domain values and thus, is 
                    # assigned to the 'timeAxis'
                for pair in pairs:
                    targets = wlbt.GetSignal(pair)
                    signal_list.append(targets[0])
                timeAxis = targets[1]


                # background frame subtracted  
                if REMOVEBACKGROUND:
                    signal_list -= average_background
                
                if sum_list == []:
                    sum_list = signal_list
                else:
                    for count in range(len(signal_list)):
                        sum_list[count] = np.add(signal_list[count], sum_list[count])
            signal_list = [np.divide(sums, AVGFRAME) for sums in sum_list]
            factor = np.linspace(8, 16, 5000)
            for signal in signal_list:
                for i in range(500, 5000):
                    signal[i]*= factor[i] 
                for i in range(0, 250):
                    signal[i]/= 3
            # Loop for writing the collected data to a csv file if file parameter was passed.
            if f:
                for i in range(len(signal_list[0])):
                    for k in range(numPairs):
                        f.write(str(signal_list[k][i])+',')
                    f.write('\n')
         
            # The builtin function which updates the figure, with the plots from the previously defined
            # function
            if line_list == []:
                for number in range(numPairs):
                    line_list.append(ax.plot(timeAxis[::5], signal_list[number][::5], '#'+COLORS[number], linewidth=0.5)[0])
            else:
                for number in range(numPairs):
                    line_list[number].set_ydata(signal_list[number][::5])
                fig.canvas.draw()
            # Saves the graphs from each scan of the Walabot (optional)
            if SAVEFIGS:
                plt.savefig("frame"+str(j)+".png")


            print(j)

            j+=1


    except KeyboardInterrupt:
        pass

    if f:
        f.close()    # close file
    wlbt.Stop()  # stops Walabot when finished scanning
    wlbt.Disconnect()  # stops communication with Walabot
    print "Walabot disconnected"

if __name__ == "__main__":
    main()
