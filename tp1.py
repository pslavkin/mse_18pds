import  numpy   as np
from    plotter import *
from    dft     import *
from    filter  import *
from    dft     import *

fs    = 20                      #frecuencia de sampleo de la senial
pl    = plotter_class ( 2,2 )   #objeto para generar un grafico de 2x2
dft_c = dft_class     ( )       #objeto para analisis de espectro
f     = filter_class  ( )       #objero para funciones de filtrado

signal = np.load('signalLowSNR.npy')        #lee la senial a decodidicar
#signal = np.load('signal.npy')
signal=signal[:2560*2]                      #tomo una pocrion para debug, luego comentar
pl.plot_signal  ( 1 ,pl.spaceX(signal) ,signal ,'signal' ,'time' ,'volt' ,trace='-' )

pulse  = np.load('pulse.npy')               #cargo el pulso original para plotearlo
pl.plot_signal  ( 2 ,pl.spaceX(pulse)  ,pulse  ,'pulse'  ,'time' ,'volt' ,trace='-' )

fft ,freq  = dft_c.abs ( fs ,signal.size  ,signal); #tomo la dft de la senial para verla
pl.stem_signal ( 3 ,freq[1:] ,fft[1:] ,'dft signal' ,'frecuencia' ,'Pnormal.')

fft ,freq  = dft_c.abs ( fs ,pulse.size  ,pulse);   #tomo la dft del pulso para verlo
pl.stem_signal ( 4 ,freq     ,fft     ,'dft pulse'  ,'frecuencia' ,'Pnormal.')
#========================================================================

pl    = plotter_class ( 2,2 )       #nuevo grafico

hipass = np.load("hipass_fir.npz")['ba'][0]     #leo los parametros del pasabajo 
lopass = np.load("lopass_fir.npz")['ba'][0]     # y pasaaltos diseniados

signal = f.fir ( signal ,hipass )               #aplico el filtrado a la senial y la muestro
signal = f.fir ( signal ,lopass )
pl.plot_signal ( 1 ,pl.spaceX(signal ),signal ,'signal Hipass->lopass' ,'time' ,'mvolt' ,trace='-' )

ans = f.fir ( pulse ,hipass )                   #aplico el filtrado al pulso para verificar que no este
ans = f.fir ( ans   ,lopass )                   #recortando demasiado
pl.plot_signal ( 2 ,pl.spaceX(ans    ),ans    ,'pulse Hipass->lopass'  ,'time' ,'mvolt' ,trace='-' )

groupDelay  = hipass.size//2+lopass.size//2     #calculo el retado basado en el largo de la respuesta al impulso de cada filtro
signal      = signal[groupDelay+1:]             #demoro la senial original dicaha cantirdad,lo previo es descartado, notar el +!
#esto es lo importante, aca lo que hago es quedarme solo con el primer pulso de cada 20, que es el 
#sample que tiene la mayor energia y es el que usare para comparar contra un umbral para decidir si
#el pulso es 1 o -1
ans         = signal[::pulse.size]
ans[ans>=0] = 1                                 #digitalizo la senial con un comparador
ans[ans<0]  = 0
ans         = np.uint8(ans)                     #lo necesito apra empaquetar luego a bytes
pl.stem_signal  ( 3 ,pl.spaceX(ans) ,ans ,'bits decodificados'  ,'time' ,'bit'  ,trace='.' )

ans = np.packbits(ans)                          #empaqueto de 8 por comodidad
pl.stem_signal  ( 4 ,pl.spaceX(ans) ,ans ,'bytes decodificados' ,'time' ,'dato' ,trace='.' )

print(ans)                                      #muestra los resultados

pl    = plotter_class ( 2,2 )
ans=np.zeros(0)
for i in range(signal.size//pulse.size):
    ans=np.append(ans,np.correlate(signal[i*pulse.size:(i+1)*pulse.size],pulse))

ans[ans>=0] = 1
ans[ans<0]  = 0
pl.plot_signal  ( 1 ,pl.spaceX(ans),ans ,'correlacion' , 'time' ,'dato'  ,trace='-' )
ans = np.uint8(ans)
ans = np.packbits(ans)
pl.stem_signal  ( 2 ,pl.spaceX(ans),ans ,'bytes decodificados' , 'time' ,'dato'  ,trace='.' )
print(ans)                                      #muestra los resultados

pl.plot_show()
