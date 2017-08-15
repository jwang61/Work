import WalabotAPI as wlbt
import numpy as np
import matplotlib.pyplot as plt
import cv2
import sys

#Number of arguments(program, output file, mti, average number of frames)
ARG_LENGTH = 1 
#phi values
PHI_MIN = -15   #[-90, 90]
PHI_MAX = 15    #[-90, 90]
PHI_RES = 1     #[1, 10]
#R values
R_MIN = 120     #[1, 1000] 
R_MAX = 180     #[1, 1000]
R_RES = 5       #[0.1, 10]
#theta values
THETA_MIN = -10 #[-90, 90]
THETA_MAX = 10  #[-90, 90]
THETA_RES = 5   #[5, 10]
#threshold values
THRESH = 75     #[0.1, 100]
MTI = False

def isConnected():
    try:
        wlbt.ConnectAny()
    except wlbt.WalabotError as err:
        if err.code == wlbt.WALABOT_INSTRUMENT_NOT_FOUND:
            return False
        else:
            raise err
    print "Connected"
    return True

def calibrate():
    wlbt.StartCalibration()
    while wlbt.GetStatus()[0] == wlbt.STATUS_CALIBRATING:
        wlbt.Trigger()
    print "Calibrated"

def main():
    if (len(sys.argv) < ARG_LENGTH):
        sys.exit("Not enough parameters")
    wlbt.Init()
    if (not isConnected()):
        sys.exit("No Device Found")

    wlbt.SetProfile(wlbt.PROF_SENSOR)
    wlbt.SetArenaR(R_MIN, R_MAX, R_RES)
    wlbt.SetArenaTheta(THETA_MIN, THETA_MAX, THETA_RES)
    wlbt.SetArenaPhi(PHI_MIN, PHI_MAX, PHI_RES)
    wlbt.SetThreshold(THRESH)
    wlbt.SetDynamicImageFilter(MTI)
    wlbt.Start()
    
    plt.ion()
    fig = plt.figure(figsize=(20,20))
    ax = fig.add_subplot(211)
    ax2 = fig.add_subplot(221)

    framecount = 0
    wlbt.Trigger()
    curImage = np.array(wlbt.GetRawImageSlice()[0])
    image = ax.imshow(curImage, cmap = plt.cm.Reds, interpolation="none", extent=[PHI_MIN, PHI_MAX, R_MAX, R_MIN])
    image2 = ax2.imshow(curImage, cmap = plt.cm.Reds, interpolation="none", extent=[PHI_MIN, PHI_MAX, R_MAX, R_MIN])

    try: 
        while (True):
            #print "Frame {}".format(framecount)
            wlbt.Trigger()
            prevImage = curImage
            curImage = np.array(wlbt.GetRawImageSlice()[0])
            imageDiff = cv2.absdiff(prevImage, curImage)
            image.set_data(imageDiff)
            image2.set_data(curImage)
            fig.canvas.draw()
            framecount += 1
            plt.savefig("images/frame{0:04d}.png".format(framecount))
    except KeyboardInterrupt:
        pass

    wlbt.Stop()
    wlbt.Disconnect()
    print "WalaBot Disconnected"

if __name__ == "__main__":
    main()
