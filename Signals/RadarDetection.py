#
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
from drawnow import drawnow
import numpy as np


# _______________________________________________________________________________________________________
#|                                            COLOR MATRIX                                               |
#| ______________________________________________________________________________________________________|

# These are the colors that will be used for drawing of the antenna signals
COLORS = ("0000FF", "00FF00", "FF0000")

# These integers are the indices of the pairs that will be used.
PAIRS = (8, 14, 32)
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

    def makeFig():
        for number in range(numPairs):
           plt.plot(timeAxis[::20], signal_list[number][::20], '#'+COLORS[number], linewidth=0.5)

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
    # Initializing the figure window for plotting
    plt.ion()  
    fig = plt.figure()
     
    # ________________________________________________________________________________________________________
    #|                                           RAW SIGNALS' COLLECTION                                      |
    #| _______________________________________________________________________________________________________|

    # Using a 'try-and-except' here to allow user to stop the data collection whenever they want
    # by using Ctrl+C
    try:
        j=1 # Counter variable for saving the figure

        # The infinite loop that runs until the user stops the program with keyboard interrupt.
        # This loop allows the Wlaabot to continuously scan the the arena that has been set.
        while True: 

            # Walabot API function used to initiate the scan 
            wlbt.Trigger()
        
            # The elements in the previously declared 'signal_list' are cleared. This is done so that 
            # every time this loop runs, the 'signal_list' is updated with the new values and doesn't
            # carry on the previous values. Having the previous values in the list would disrupt the 
            # plotting because the size of the 'signal_list' wouldn't match the 'timeAxis' in that case.
            signal_list = []
        

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

            # Loop for writing the collected data to a csv file if file parameter was passed.
            if f:
                for i in range(len(signal_list[0])):
                    for k in range(numPairs):
                        f.write(str(signal_list[k][i])+',')
                    f.write('\n')
         
            # The builtin function which updates the figure, with the plots from the previously defined
            # function
            drawnow(makeFig)

            # Saves the graphs from each scan of the Walabot (optional)
            plt.savefig("images/frame"+str(j)+".png")

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
