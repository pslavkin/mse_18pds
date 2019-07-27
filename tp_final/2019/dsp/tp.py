import  matplotlib.pyplot as plt
import  numpy as np
from    plotter import *
from    signal_generator import *
from    wiener import *

sg     = signal_generator_class ( )
wiener = wiener_class           ( )

f0       = 3
fs       = 200
N        = 500
A        = 1
#numero de coeficientes pedido en el TP
M        = 4
#estos dos parametros son para hacer una corrida con varios M y comparar el error
Mmin     = 2
Mmax     = 100
#se sube el ruido de 0.02 pedido en el tp para que se aprecie mejor en las curvas el funcionamiento del filtro
n        = 0.2
#estos dos parametros son para definir una cota max y min del ruido sumado a la senial y probar
#dentro de ese rango el error obtenido
noiseMin = 0.01
noiseMax = 0.5

#agrupo las poeraciones comunes para repetir la experiencias con distintas seniales
def run(u,U):
    #hago un barrdo ,amtemoemdp fokp el error en u, pero cambiando la cantidad de coeficientes para
    #ver como baja el error a medida que el filtro crece
    eM=np.zeros(Mmax-Mmin)
    for i in range(Mmin,Mmax):
        d             = U[i-1:]
        DD,eM[i-Mmin] = wiener.filter(u,d,t,i)
    teM=np.linspace(Mmin,Mmax,Mmax-Mmin)

    #ahora mantengo fijo el M, y modifico el error en la senial para ver como aumenta el error a
    #medida que la senial se deteriora
    eNoise=[]
    varNoise=np.linspace(noiseMin,noiseMax,100)
    for i in varNoise:
        d    = U[M-1:]
        DD,e = wiener.filter(U+i*noise,d,t,M)
        eNoise.append(e)

    #la senial deseada la tomo M posiciones a posteriori de la original ya que el filtro tarda M taps en predecir
    d   = U[M-1:]
    #ejecuto el filtro y guardo el vector estimado D y tambien el error
    D,e = wiener.filter ( u,d,t,M  )
    #agrego ceros en la primera arte del vector estimado y del deseado para que sean
    #coincidentes con el vector original de entrada y tambien para que tengan la misma longitud
    #que t y se pueda visualizar todo sobre la misma escala temporal
    D   = np.pad ( D,(M-1,0 ),'constant')
    d   = np.pad ( d,(M-1,0 ),'constant')
    #dibujo las curvas
    pl  = plotter_class ( 3,2 )
    pl.plot_signal ( 1 ,t        ,u      ,'input [u]'                   ,'time'  ,'amplitud' ,trace='-'                         )
    pl.plot_signal ( 2 ,t        ,d      ,'deseada [d]'                 ,'time'  ,'amplitud' ,trace='-'                         )
    pl.plot_signal ( 3 ,t        ,D      ,'estimacion [D]'              ,'time'  ,'amplitud' ,trace='-'                         )
    pl.plot_signal ( 4 ,t        ,d      ,'deseada [d]'                 ,'time'  ,'amplitud' ,trace='-',center = N/2 ,zoom=N/10 )
    pl.plot_signal ( 4 ,t        ,D      ,'[d vs D]'                    ,'time'  ,'amplitud' ,trace='-',center = N/2 ,zoom=N/10 )
    pl.plot_signal ( 5 ,varNoise ,eNoise ,f'error vs noise @M={M}'      ,'noise' ,'error'    ,trace='-'                         )
    pl.plot_signal ( 6 ,teM      ,eM     ,'error minimo [e] @noise={n}' ,'M'     ,'erorr'    ,trace='-'                         )
    pl.plot_show()

# experimentos

#senoidal original solicitada en el TP
u ,t  = sg.signal_sin    ( fs ,f0 ,A ,N   ,np.pi/4 )
noise = np.random.normal ( 0,1,u.size              )
U     = u
u     = u+n*noise
run(u,U)

# triangular
u ,t  = sg.signal_triangular ( fs ,f0 ,A ,N   ,50 )
noise = np.random.normal     ( 0,1,u.size         )
U     = u
u     = u+n*noise
run(u,U)

#cuadrada
u ,t  = sg.signal_quad   ( fs ,f0  ,A ,N ,50 )
noise = np.random.normal ( 0,1,u.size        )
U     = u
u     = u+n*noise
run(u,U)


