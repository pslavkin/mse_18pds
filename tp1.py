import  numpy as np
from    plotter import *
from    dft import *
from    filter import *
from    dft import *

fs = 20

pl    = plotter_class ( 2,2 )
dft_c = dft_class     ( )
f     = filter_class  ( )


#signal = np.load('signalLowSNR.npy')
signal = np.load('signal.npy')
t = np.linspace ( 0,signal.size-1,signal.size )
pl.plot_signal  ( 1 ,t,signal ,'signal' , 'time' ,'volt'  ,trace='-' )
signal=signal[:2560]

pulse  = np.load('pulse.npy')
t = np.linspace ( 0,pulse.size-1,pulse.size )
pl.plot_signal  ( 2 ,t,pulse ,'pulse' , 'time' ,'volt'  ,trace='-' )

fft ,freq  = dft_c.abs ( fs ,signal.size  ,signal);
pl.stem_signal ( 3 ,freq[1:] ,fft[1:] ,'dft signal' ,'frecuencia','Pnormal.')

fft ,freq  = dft_c.abs ( fs ,pulse.size  ,pulse);
pl.stem_signal ( 4 ,freq ,fft ,'dft pulse' ,'frecuencia','Pnormal.')


pl    = plotter_class ( 2,2 )

hipass = np.load("hipass_fir.npz")['ba'][0]
lopass = np.load("lopass_fir.npz")['ba'][0]
y      = f.fir  ( signal ,hipass )
y      = f.fir  ( y      ,lopass )
t      = np.linspace ( 0,y.size-1,y.size )
pl.plot_signal  ( 1 ,t,y ,'signal Hipass->lopass' , 'time' ,'mvolt'  ,trace='-' )
signal=y

y = f.fir       ( pulse,hipass )
y = f.fir       ( y,lopass )
t = np.linspace ( 0,y.size-1,y.size )
pl.plot_signal  ( 2 ,t,y ,'pulse Hipass->lopass' , 'time' ,'mvolt'  ,trace='-' )


ans         = signal[81::20]
ans[ans>=0] = 1
ans[ans<0]  = 0
ans=np.uint8(ans)
t = np.linspace ( 0,ans.size-1,ans.size )
pl.stem_signal  ( 3 ,t,ans ,'bits decodificados' , 'time' ,'bit'  ,trace='.' )
ans= np.packbits(ans)
t = np.linspace ( 0,ans.size-1,ans.size )
pl.stem_signal  ( 4 ,t,ans ,'bytes decodificados' , 'time' ,'dato'  ,trace='.' )
print(ans)


pl    = plotter_class ( 2,2 )
ans=np.zeros(0)
for i in range(2560//20):
    ans=np.append(ans,np.correlate(signal[i*20+80:i*20+100],pulse))

ans[ans>=0] = 1
ans[ans<0]  = 0
t = np.linspace ( 0,ans.size-1,ans.size )
pl.stem_signal  ( 1 ,t,ans ,'correlacion' , 'time' ,'dato'  ,trace='.' )
ans = np.uint8(ans)
ans = np.packbits(ans)
t   = np.linspace ( 0,ans.size-1,ans.size )
pl.stem_signal  ( 2 ,t,ans ,'bytes decodificados' , 'time' ,'dato'  ,trace='.' )
print(ans)


pl.plot_show()
