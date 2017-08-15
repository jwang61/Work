import WalabotAPI as wlbt
import numpy as np
import numpy.fft as fft
import matplotlib.pyplot as plt
import datetime

#WalaBot arena settings
R_MIN, R_MAX, R_RES = 140, 200, 0.1  # SetArenaR values
THETA_MIN, THETA_MAX, THETA_RES = -4, 4, 1  # SetArenaTheta values
PHI_MIN, PHI_MAX, PHI_RES = -4, 4, 1  # SetArenaPhi values

#Global Parameters
NUMPOINTS = 150
Y_MIN, Y_MAX = -1, 1
SPLINEORDER = 5
MOVINGAVG = 3
PULSETIME = 0.27

def setupWalabot():
    wlbt.Init()
    wlbt.SetSettingsFolder()
    wlbt.Connect('vMaker18EU')
    wlbt.SetProfile(wlbt.PROF_SENSOR_NARROW)
    wlbt.SetArenaR(R_MIN, R_MAX, R_RES)
    wlbt.SetArenaTheta(THETA_MIN, THETA_MAX, THETA_RES)
    wlbt.SetArenaPhi(PHI_MIN, PHI_MAX, PHI_RES)
    wlbt.SetDynamicImageFilter(wlbt.FILTER_TYPE_NONE)
    
    wlbt.Start()

def main():
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    ax.set_ylim([Y_MIN, Y_MAX])
    #f = open(datetime.datetime.now().strftime("%y%m%d-%H%M%S.csv"), 'w')
    try:
        j=1 # Counter variable for saving the figure
        energy = [0]*NUMPOINTS
        avgEnergy = [0]*NUMPOINTS
        time = [PULSETIME*n for n in range(NUMPOINTS)]
        freq = np.linspace(0, 1/(2*PULSETIME), NUMPOINTS//2)
        freq2 = np.linspace(0, 1/(2*PULSETIME), NUMPOINTS//4)
        spectrum = abs(fft.fft(avgEnergy))
        spectrum2 = abs(fft.fft(avgEnergy[NUMPOINTS//2:]))
 
        time2 = datetime.datetime.now()
        line = ax.plot(time, avgEnergy)
        line2 = ax2.plot(freq, spectrum[:NUMPOINTS//2])
        line3 = ax2.plot(freq2, spectrum2[:NUMPOINTS//4])
        # The infinite loop that runs until the user stops the program with keyboard interrupt.
        # This loop allows the Wlaabot to continuously scan the the arena that has been set.
        while True: 
            time1 = time2
            time2 = datetime.datetime.now()
            #print time2-time1
            # Walabot API function used to initiate the scan 
            wlbt.Trigger()
            ener = wlbt.GetImageEnergy()
            energy = energy[1:] + [ener]
            avgEnergy = avgEnergy[1:] + [sum(energy[-MOVINGAVG:])/MOVINGAVG]
            spectrum = abs(fft.fft(avgEnergy))
            spectrum2 = abs(fft.fft(avgEnergy[NUMPOINTS//2:]))
            line[0].set_ydata(avgEnergy)
            line2[0].set_ydata(spectrum[:NUMPOINTS//2])
            line3[0].set_ydata(spectrum2[:NUMPOINTS//4])
            #print freq[np.argmax(spectrum[5:NUMPOINTS//2]) + 5]
            

            if j%10 == 1:
                y_max = max(avgEnergy)
                y_min = min(avgEnergy)
                ax.set_ylim([y_min, y_max])
                y_max = max(spectrum[5:NUMPOINTS//2])
                y_min = min(spectrum[5:NUMPOINTS//2])
                ax2.set_ylim([y_min, y_max])
            fig.canvas.draw()
            
            j+=1
            if j%50 == 0 :
                plt.savefig('shot{}.png'.format(j))
                print 'screenshot'

    except KeyboardInterrupt:
        pass

    #if f:
        #f.close()    # close file
    wlbt.Stop()  # stops Walabot when finished scanning
    wlbt.Disconnect()  # stops communication with Walabot
    print "Walabot disconnected"


if __name__ == "__main__":
    setupWalabot()
    main()
