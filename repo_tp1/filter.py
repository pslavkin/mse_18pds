import numpy as np
from scipy.signal import fftconvolve, lfilter, firwin
from scipy import signal

class filter_class:

    def __init__(self):
        pass

    def qrs2ecg(self,qrs,ecg):
        det=np.zeros(ecg.size)
        j=0
        for i in range(ecg.size):
            if qrs[j]==i :
                det[i]=5000
                j+=1
                if j>=qrs.size:
                    break
        return det

    def fir(self,x,h):
        y = signal.convolve(x, h)
        return y

    def iir(self,x,b,a):
        y=lfilter(b,a,x)
        return y
