import  matplotlib.pyplot as plt
import  numpy as np
from    plotter import *
from    signal_generator import *
from    wiener import *

f0 = 3
fs = 100
N  = 1000
M  = 4
A  = 1

sg     = signal_generator_class (     )
pl     = plotter_class          ( 3,2 )
wiener = wiener_class           (     )

u,t=sg.signal_triangular(fs,f0,A,N,50)
u=u-A/2
u,t=sg.signal_sin(fs,f0,A,N,np.pi/4)
#u,t=sg.signal_quad(10,1,5,100,50)
d=u
noise= np.random.normal(0,1,u.size)
u=u+0.2*noise

def filter(u,d,t,M):
    d=d[M-1:]
    ah  = wiener.generateAHermitica ( u  ,M )
    phi = wiener.phi                ( ah    )
    z   = wiener.z                  ( ah ,d )
    w   = wiener.w                  ( ah ,d )
    D   = wiener.D                  ( ah ,w )
    e   = wiener.e                  ( ah ,D )
    return D,e


D,e=filter(u,d,t,M)
D=np.pad(D,(M-1,0),'constant')

pl.plot_signal ( 1 ,t ,u ,'input [u]'      ,'time' ,'amplitud' ,trace='-'          )
pl.plot_signal ( 2 ,t ,d ,'deseada [d]'    ,'time' ,'amplitud' ,trace='-'          )
pl.plot_signal ( 3 ,t ,D ,'estimacion [D]' ,'time' ,'amplitud' ,trace='-'          )
pl.plot_signal ( 4 ,t ,d ,'deseada [d]'    ,'time' ,'amplitud' ,trace='-' ,center = 100, zoom=40 )
pl.plot_signal ( 4 ,t ,D ,'[d vs D]'       ,'time' ,'amplitud' ,trace='-' ,center = 100, zoom=40 )
pl.plot_signal ( 5 ,t ,d-D ,'error [E]' ,'time' ,'amplitud' ,trace='-'          )
pl.plot_signal ( 5 ,t ,[e for i in range(t.size)] ,'error minimo [e]' ,'time' ,'amplitud' ,trace='-'          )

Mmin=2
Mmax=200
ee=np.zeros(Mmax-Mmin)
for i in range(Mmin,Mmax):
    print(i)
    D,ee[i-Mmin]=filter(u,d,t,i)

t=np.linspace(Mmin,Mmax,Mmax-Mmin)
print (t)
print (ee)

pl.plot_signal ( 6 ,t , ee ,'error minimo [e]' ,'M' ,'amplitud' ,trace='-'          )

pl.plot_show()
