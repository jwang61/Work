import WalabotAPI as wlbt
import numpy as np
import sys

#Number of arguments(program, output file, mti, average number of frames)
ARG_LENGTH = 4 
#phi values
PHI_MIN = -45   #[-90, 90]
PHI_MAX = 45    #[-90, 90]
PHI_RES = 2     #[0.1, 10]
#R values
R_MIN = 10      #[1, 1000] 
R_MAX = 1000    #[1, 1000]
R_RES = 5       #[0.1, 10]
#theta values
THETA_MIN = -20 #[-90, 90]
THETA_MAX = 20  #[-90, 90]
THETA_RES = 10  #[0.1, 10]
#threshold values
THRESH = 75     #[0.1, 100]
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
    outfile = str(sys.argv[1])
    mti = bool(sys.argv[2])
    avgframe = int(sys.argv[3])
    wlbt.Init()
    if (not isConnected()):
        sys.exit("No Device Found")

    wlbt.SetProfile(wlbt.PROF_SENSOR)
    wlbt.SetArenaR(R_MIN, R_MAX, R_RES)
    wlbt.SetArenaTheta(THETA_MIN, THETA_MAX, THETA_RES)
    wlbt.SetArenaPhi(PHI_MIN, PHI_MAX, PHI_RES)
    wlbt.SetThreshold(THRESH)
    wlbt.SetDynamicImageFilter(mti)
    wlbt.Start()

    if (not mti):
       pass
       #calibrate() 

    log = open(outfile, 'w')
    count, sumFPS = 0, 0
    while (True):
        print "Frame {}".format(count)
        wlbt.Trigger()
        fullImage = wlbt.GetRawImageSlice()[0]
        for i in range(avgframe - 1):
            print "trigger ++"
            wlbt.Trigger()
            rawImage = wlbt.GetRawImageSlice()[0]
            fullImage = np.add(fullImage, rawImage)
        fullImage = np.divide(fullImage, avgframe)
        log.write(str(fullImage) + "\n")
        count += 1

    #print "Average FPS was {}".format(sumFPS/count)
    log.close()

            
if __name__ == '__main__':
    main()
    
    
