import numpy as np
import scipy.fftpack as sc

class dft_class:
    def __init__(self):
        pass

    def inv_fft(self, fs, N, signal):
        return N*sc.ifft(signal)

    def abs(self, fs, N, signal):
        freq = np.linspace(0, fs, N)
        return (1/N)*np.abs(sc.fft(signal))[:N//2], freq[:N//2]

    def full(self, fs, N, signal):
        freq = np.linspace(0, fs, N)
        return (1/N)*np.abs(sc.fft(signal))[:N//1], freq[:N//1]

    def power_bin(self, fs, fft,f0):
        delta_bin = fs/(2*len(fft))         #fft viene solo la mitad, de 0 a N // 2 por eso el 2
        bin       = int(f0/delta_bin)       # este es el bin dentro de la fft que representa f0
        return 2*(np.abs(fft[bin])**2)      # ojo que fft est anormalizada con 2/N. para ser justos

    def power_adjacent(self, fs, fft,f0):
        delta_bin = fs/(2*len(fft))
        bin       = int(f0/delta_bin)+1
        return 2*(np.abs(fft[bin])**2)

    def power_total_except_bin(self, fs, fft,f0):
        delta_bin = fs/(2*len(fft))
        bin       = int(f0/delta_bin)
        return self.power_total(fs,fft,f0)-2*(fft[bin]**2)

    def power_total(self, fs, fft,f0):
        ans  = sum(fft**2)
        ans *= 2
        return ans

    def max_bin(self,fs, fft):
        delta_bin = fs/(2*len(fft))
        f0 = delta_bin*np.argmax(fft)
        return f0

