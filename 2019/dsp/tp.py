import  matplotlib.pyplot as plt
import  numpy as np
from    plotter import *
from    signal_generator import *
from    scipy import signal as sig
import  zplane as zp
import  scipy.io
from    filter import *
from    dft import *
from    wiener import *

f0 = 1
fs = 1000
ts = 1/fs
tm = 1
M  = 20


sg    = signal_generator_class (     )
pl    = plotter_class          ( 3,1 )
f     = filter_class           (     )
dft_c = dft_class              (     )
w_c   = wiener_class           (     )
t=np.linspace(0,tm,tm*fs,endpoint=False)

#u=np.sin(2*np.pi*f0*t+np.pi/4)
#pl.plot_signal ( 1 ,t ,u ,'sin' ,'time [msec]' ,'volt' ,trace='.' )
u,t=sg.signal_triangular(10,1,5,100,50)
#u=np.sin(2*np.pi*f0*t+np.pi/4)
#u,t=sg.signal_quad(10,1,5,100,50)
u=u-5/2

print ( f"u size= {u.shape} \n {u}"  )

d=u[M-1:]
u=u + np.random.normal(0,0.5,u.size)
pl.plot_signal ( 1 ,t ,u ,'input' ,'time' ,'amplitud' ,trace='-' )

ah = w_c.generateAHermitica  ( u,M  )
print         (f"ah=\n {ah}"  )

phi = w_c.phi ( ah   )
print         (f"phi size= {phi.shape} \n {phi}"  )
z = w_c.z     ( ah,d )
print         (f"z  size= {z.shape} =\n {z}")
w = w_c.w     ( ah,d )
print         ( f"w  size= {w.shape} =\n {w}" )
d_est = w_c.calcHermitica(ah)@w
print         ( f"d_est  size= {d_est.shape}=\n {d_est}")
e = w_c.e(ah,d_est)
print         ( f"e  size= {e.shape}=\n {e}")

pl.plot_signal ( 2 ,t[M-1:] ,d_est ,'sin' ,'time [msec]' ,'volt' ,trace='-' )






#mat                = scipy.io.loadmat('file.mat')
#ecg_lead           = mat[ 'ecg_lead'           ]
#qrs_pattern1       = mat[ 'qrs_pattern1'       ]
#heartbeat_pattern1 = mat[ 'heartbeat_pattern1' ]
#heartbeat_pattern2 = mat[ 'heartbeat_pattern2' ]
#qrs_detections     = mat[ 'qrs_detections'     ]
#
#lopass=np.load("lopass_fir.npz")['ba'][0]
#hipass=np.load("hipass_fir.npz")['ba'][0]
#
#
#ecg_lead=ecg_lead[int(12.1*60*fs):int(12.20*60*fs)]
##ecg_lead=ecg_lead[1210000:15000]
#
#t=np.linspace ( 0 ,ecg_lead.size ,ecg_lead.size )
#pl.plot_signal ( 1 ,t ,ecg_lead ,'ecg_lead' ,'time [msec]' ,'mvolt' ,trace='-' )
#
#fft    ,freq  = dft_c.abs ( fs ,ecg_lead.size  ,ecg_lead[:].flatten( ));
#pl.stem_signal ( 2 ,freq ,fft ,'fft' ,'frecuencia','Pnormal.',center=25/(fs/(fft.size*2)),zoom=25/(fs/(fft.size*2)) )
#
#y = f.fir       ( ecg_lead,lopass )
#t = np.linspace ( 0,y.size,y.size )
#pl.plot_signal  ( 3 ,t[:t.size-lopass.size//2],y[lopass.size//2:]   ,'fir' , 'time' ,'mvolt'  ,trace='-' )
#
#fft    ,freq  = dft_c.abs( fs ,y.size  ,y    );
#pl.stem_signal ( 4 ,freq ,fft ,'fft y' ,'frecuencia','Pnormal.',center=25/(fs/(fft.size*2)),zoom=25/(fs/(fft.size*2)))
#
#y = f.fir       ( ecg_lead,hipass )
#t = np.linspace ( 0,y.size,y.size )
#pl.plot_signal  ( 5 ,t[:t.size-hipass.size//2],y[hipass.size//2:]   ,'fir' , 'time' ,'mvolt'  ,trace='-' )
#
#fft    ,freq  = dft_c.abs( fs ,y.size  ,y    );
#pl.stem_signal ( 6 ,freq ,fft ,'fft y' ,'frecuencia','Pnormal',center=25/(fs/(fft.size*2)),zoom=25/(fs/(fft.size*2)))
#
pl.plot_show()
