import numpy as np

class wiener_class:

    def __init__(self):
        return
# genera la matriz A hermitica basada en el vector de entrada Nx1 y el numero de coeficientes M
# elegido. resultando en una matriz de M filas y N (N-M) columnas
    def generateAHermitica(self,u,M):
        col=u.size-M
        aH=np.zeros((M,col))
        for i in range(M):
            aH[i]=u[M-i:M-i+col]
        return aH

#simplemente calcula la matriz hermitica de otra matriz, para hacer mas legible el codigo y 
#reutilizar la funcion repetidamente, si entra MxN sale NxM
    def calcHermitica(self,aH):
        return aH.transpose().conjugate()

#calcula la matriz phi de autocorrelacion, basado en la matriz hermitica, es un calculo simple
# pero de nuevo se lo define como funcion por modularidad, el resultado sera una matriz de MxM
    def phi(self,aH):
        return aH@self.calcHermitica(aH)

#calcula el vector correlacion cruzada z, que es simplemente A hermitica por el vector d. el
#resultado sera de dimension Mx1
    def z(self,aH,d):
        return aH@d

#calcula el vector w que seran los parametros del filtro Mx1
    def w(self,aH,d):
        return np.linalg.inv(self.phi(aH))@self.z(aH,d)

#calcula e (1x1) que es el error cuadratico medio entre el vector deseado y lo obtenido a
#la salida del filtro
    def e(self,aH,d):
        return self.calcHermitica(d)@d - self.w(aH,d)@self.z(aH,d)

#calcula la estimacion del filtro Mx1
    def D(self,aH,w):
        return self.calcHermitica(aH)@w

#defino una funcion que usando todas las anteriores realiza el filtrado y devuelve la
#estimacion y el error
    def filter(self,u,d,t,M):
        ah  = self.generateAHermitica ( u  ,M )
        phi = self.phi                ( ah    )
        z   = self.z                  ( ah ,d )
        w   = self.w                  ( ah ,d )
        D   = self.D                  ( ah ,w )
        e   = self.e                  ( ah ,d )
        return D,e
