from Cromosoma import Cromosoma
import random
import numpy as np
class AlgoritmoGenetico:

    def __init__(self, generaciones=20, individuos=50, cruza=0.8, mutacion=0.01):
        self._generaciones=generaciones
        self._individuos=individuos
        self._cruza=cruza
        self._mutacion=mutacion
        self._poblacion=[]

    def PoblacionInicial(self):
        for i in range(self._individuos):
            genes = np.random.randint(low=0, high=2, size=16).tolist()
            self._poblacion.append(Cromosoma(genes))
    
    def Algoritmo(self):
        ##Ciclo principal
        ##Calcular aptitud a la población
        ##Selección
        ##Cruza
        ##Mutación
        ##
        
    #def Seleccion(self):
        
    #def Cruza(self):

    #def Mutacion(self):

    #def Aptitud(self):
         

     def __str__(self):
        cadena = ''
        for c in self._poblacion: 
            cadena+=c.__str__()+'\n'
        return cadena

        
if __name__ == "__main__":
    A = AlgoritmoGenetico()
    A.PoblacionInicial()
    print(str(A.__str__()))
    #print(np.random.randint(low=0, high=2, size=16).tolist())
