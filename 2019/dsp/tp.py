import  matplotlib.pyplot as plt
import  numpy as np
from    plotter import *
from    signal_generator import *
from    wiener import *

f0 = 3
fs = 100
N  = 100
M  = 4
A  = 1

sg     = signal_generator_class (     )
pl     = plotter_class          ( 3,2 )
wiener = wiener_class           (     )

u,t=sg.signal_triangular(fs,f0,A,N,50)
u=u-A/2
u,t=sg.signal_sin(fs,f0,A,N,np.pi/4)
#u,t=sg.signal_quad(10,1,5,100,50)
noise= np.random.normal(0,1,u.size)
original_u=u
u=u+0.2*noise

def filter(u,d,t,M):
    ah  = wiener.generateAHermitica ( u  ,M )
    phi = wiener.phi                ( ah    )
    z   = wiener.z                  ( ah ,d )
    w   = wiener.w                  ( ah ,d )
    D   = wiener.D                  ( ah ,w )
    e   = wiener.e                  ( ah ,d )
    return D,e


Mmin=4
Mmax=30
ee=np.zeros(Mmax-Mmin)
for i in range(Mmin,Mmax):
    d=original_u[i-1:]
    DD,ee[i-Mmin]=filter(u,d,t,i)

d=original_u[M-1:]
D,e=filter(u,d,t,M)
D=np.pad(D,(M-1,0),'constant')
d=np.pad(d,(M-1,0),'constant')
pl.plot_signal ( 1 ,t ,u ,'input [u]'      ,'time' ,'amplitud' ,trace='-'          )
pl.plot_signal ( 2 ,t ,d ,'deseada [d]'    ,'time' ,'amplitud' ,trace='-'          )
pl.plot_signal ( 3 ,t ,D ,'estimacion [D]' ,'time' ,'amplitud' ,trace='-'          )
pl.plot_signal ( 4 ,t ,d ,'deseada [d]'    ,'time' ,'amplitud' ,trace='-' ,center = N/2, zoom=N/4 )
pl.plot_signal ( 4 ,t ,D ,'[d vs D]'       ,'time' ,'amplitud' ,trace='-' ,center = N/2, zoom=N/4 )
pl.plot_signal ( 5 ,t ,[e for i in range(t.size)] ,'error minimo [e]' ,'time' ,'amplitud' ,trace='-'          )

t=np.linspace(Mmin,Mmax,Mmax-Mmin)
pl.plot_signal ( 6 ,t , ee ,'error minimo [e]' ,'M' ,'amplitud' ,trace='-'          )

pl.plot_show()
