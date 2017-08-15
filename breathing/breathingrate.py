import numpy as np
import pylab as plt
import matplotlib as mpl
from peakdetect import peakdetect
import time

def breathingrate(Data):

    timestep=0.083 # 0.083s for Walabot
    n=np.size(Data)
    Time=np.arange(0,n*timestep,timestep)

    peaks = peakdetect(Data,Time,lookahead=6,delta=0.002) # average breathing rarly goes above 1breath/2second, set lookahead as half of that for 1 peak/second
    maxpeaks = np.array(peaks)[0]
    minpeaks =np.array(peaks)[1] 

    maxX = [peakP[0] for peakP in maxpeaks]
    maxY = [peakP[1] for peakP in maxpeaks]

    minX = [peakP[0] for peakP in minpeaks]
    minY = [peakP[1] for peakP in minpeaks]

    bpm = len(maxX) / ((Time[-1]-Time[0])/60) # turn peaks into breaths/minute
    print(bpm)

    return bpm, maxX, maxY, minX, minY
