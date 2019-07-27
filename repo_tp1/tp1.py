import  numpy   as np
from    plotter import *
from    filter  import *

fs    = 20                      #frecuencia de sampleo de la senial
#pl    = plotter_class ( 2,2 )   #objeto para generar un grafico de 2x2
f     = filter_class  ( )       #objero para funciones de filtrado

signal = np.load('signalLowSNR.npy')        #lee la senial a decodidicar
#signal = np.load('signal.npy')
signalOriginal=signal
#signal=signal[:2560*1]                      #tomo una pocrion para debug, luego comentar
#pl.plot_signal  ( 1 ,pl.spaceX(signal) ,signal ,'signal' ,'time' ,'volt' ,trace='-' )
#
pulse  = np.load('pulse.npy')               #cargo el pulso original para plotearlo
#pl.plot_signal  ( 2 ,pl.spaceX(pulse)  ,pulse  ,'pulse'  ,'time' ,'volt' ,trace='-' )
#
#pl.plot_dft_signal ( 3 ,fs ,signal ,'dft signal' ,'Hz' ,'Pnormal' ,trace='-' ,center=signal.size//2 ,zoom=signal.size//2-1)
#pl.plot_dft_signal ( 4 ,fs ,pulse  ,'dft pulse'  ,'Hz' ,'Pnormal' ,trace='-')
##========================================================================
#pl    = plotter_class ( 2,2 )       #nuevo grafico
#
#hipass = np.load("hipass_fir.npz")['ba'][0]     #leo los parametros del pasabajo 
#lopass = np.load("lopass_fir.npz")['ba'][0]     # y pasaaltos diseniados
#pl.plot_dft_signal ( 1 ,fs,hipass,'Hipass H(n)' ,'Hz' ,'amp' ,trace='-' )
#pl.plot_dft_signal ( 2 ,fs,lopass,'Lopass H(n)' ,'Hz' ,'amp' ,trace='-' )
#
#signal = f.fir ( signal ,hipass )               #aplico el filtrado a la senial y la muestro
#signal = f.fir ( signal ,lopass )
#pl.plot_signal ( 3 ,pl.spaceX(signal ),signal ,'signal Hipass->lopass' ,'time' ,'mvolt' ,trace='-' )
#
#ans = f.fir ( pulse ,hipass )                   #aplico el filtrado al pulso para verificar que no este
#ans = f.fir ( ans   ,lopass )                   #recortando demasiado
#pl.plot_signal ( 4 ,pl.spaceX(ans    ),ans    ,'pulse Hipass->lopass'  ,'time' ,'mvolt' ,trace='-' )
##==============================================================================
#
#groupDelay  = hipass.size//2+lopass.size//2     #calculo el retado basado en el largo de la respuesta al impulso de cada filtro
#signal      = signal[groupDelay+1:]             #demoro la senial original dicaha cantirdad,lo previo es descartado, notar el +!
##esto es lo importante, aca lo que hago es quedarme solo con el primer pulso de cada 20, que es el 
##sample que tiene la mayor energia y es el que usare para comparar contra un umbral para decidir si
##el pulso es 1 o -1
#pl    = plotter_class ( 2,2 )
#
#ans         = signal[::pulse.size]
#ans[ans>=0] = 1                                 #digitalizo la senial con un comparador
#ans[ans<0]  = 0
#ans         = np.uint8(ans)                     #lo necesito apra empaquetar luego a bytes
#pl.stem_signal  ( 1 ,pl.spaceX(ans) ,ans ,'bits tecnica umbral'  ,'time' ,'bit'  ,trace='.' )
#
#ans = np.packbits(ans)                          #empaqueto de 8 por comodidad
#pl.stem_signal  ( 2 ,pl.spaceX(ans) ,ans ,'bytes tecnca umbral' ,'time' ,'dato' ,trace='.' )
#
#print(f"tecnica umbral=\n{ans}")                                      #muestra los resultados
#
#ans=np.zeros(0)
#ans2=np.zeros(0)
#for i in range(signal.size//pulse.size):
#    ans=np.append(ans,np.correlate(signal[i*pulse.size:(i+1)*pulse.size],pulse))
#
#ans[ans>=0] = 1                                 #digitalizo la senial con un comparador
#ans[ans<0]  = 0
#ans         = np.uint8(ans)                     #lo necesito apra empaquetar luego a bytes
#pl.stem_signal  ( 3 ,pl.spaceX(ans),ans ,'bits tecnica correlacion' , 'time' ,'dato'  ,trace='.' )
#ans = np.packbits(ans)                          #empaqueto de 8 por comodidad
#pl.stem_signal  ( 4 ,pl.spaceX(ans),ans ,'bytes tecnica correlacion' , 'time' ,'dato'  ,trace='.' )
#print(f"tecnica correlacion=\n{ans}")                                      #muestra los resultados
#

#tecnica de filtro adaptado
pl    = plotter_class ( 3,1 )
pulse=np.flip(pulse)
signal=signalOriginal[:2560*4]
hipass = np.load("hipass_fir.npz")['ba'][0]     #leo los parametros del pasabajo 
ans = f.fir ( signal ,hipass )                   #aplico el filtrado al pulso para verificar que no este
ans = f.fir ( ans   ,pulse )                   #recortando demasiado
pl.plot_signal ( 1 ,pl.spaceX(ans),ans    ,'Hipass->filtrado adaptado'  ,'time' ,'mvolt' ,trace='-' , center='400', zoom='200')
pl.plot_signal ( 2 ,pl.spaceX(pulse),pulse ,'Pulse flipeado'  ,'time' ,'mvolt' ,trace='-' )

groupDelay  = hipass.size//2+pulse.size//2      #calculo el retado basado en el largo de la respuesta al impulso de cada filtro
ans         = ans[groupDelay+pulse.size//2::pulse.size]       #demoro la senial original dicaha cantirdad,lo previo es descartado, notar el +!
ans[ans>=0] = 1                                 #digitalizo la senial con un comparador
ans[ans<0]  = 0
ans         = np.uint8(ans)                     #lo necesito apra empaquetar luego a bytes
#pl.stem_signal  ( 3 ,pl.spaceX(ans) ,ans ,'bits tecnica filtro adaptado'  ,'time' ,'bit'  ,trace='.' )
ans = np.packbits(ans)                          #empaqueto de 8 por comodidad
pl.stem_signal  ( 3 ,pl.spaceX(ans) ,ans ,'bytes tecnica filtro adaptado' ,'time' ,'dato' ,trace='.' )
print(f"tecnica filtro adaptado=\n{ans}")                                      #muestra los resultados


pl.plot_show()
