from Cromosoma import Cromosoma
import random
import numpy as np
import pandas as pd
import functools
class AlgoritmoGenetico:
    
    df_beneficios=pd.read_csv('CSV\Beneficios.csv')

    def __init__(self, generaciones=20, individuos=50, cruza=0.8, mutacion=0.01):
        self._generaciones=generaciones
        self._individuos=individuos
        self._pCruza=cruza
        self._pMutacion=mutacion
        self._poblacion=[]

    def PoblacionInicial(self):
        genes = np.random.randint(low=0, high=2, size=(self._individuos,16))
        self._poblacion=[Cromosoma(gen) for gen in genes]
    
    def Algoritmo(self):
       for generacion in self._generaciones:
           self.Seleccion()

        ##Calcular aptitud a la población
        ##Selección
        ##Cruza
        ##Mutación
        ##
    
    def SetFitness(self):
        #Accedemos a un ciclo para iterar sobre los individuos de la población
        for cromosoma in self._poblacion:
            #Dividimos en 4 bits la cadena binaria del cromosoma
            cadenas=np.array_split(cromosoma.get_genes(),4)
            inversiones=[]
            #Abrimos otro ciclo para iterar sobre cada cadena del cromosoma (que representan las inversiones de cada zona) 
            for cadenaBinaria in cadenas:
                c=0
                #Iteramos sobre los bits de la cadena para obtener su equivalente en decimal
                for bit in cadenaBinaria:
                    #Realizamos el desplazamiento y OR de los bits
                    c=(c<<1) | bit
                inversiones.append(c)
            #Aplicamos la función de aptitud y le asignamos el valor al cromosoma
            #Primero obtenemos los beneficios o ganancias por zona de acuerdo a la inversión
            beneficios=[self.df_beneficios[self.df_beneficios['Inversion']==inversiones[index]].iloc[0,(index+1)]for index in range(len(inversiones))]
            #Calculamos la suma de los ganancias de las inversiones 
            sumInvest=functools.reduce(lambda a,b:a+b,beneficios)
            #Obtenemos la variable que 'v' que equivale al valor absoluto de la diferencia de la suma anterior y 10
            v=abs(sumInvest-10)
            #Calculamos la función de aptitud para el cromosoma
            fx=sumInvest/(500*v+1)
            #Asignamos el valor de la función al individuo
            cromosoma.set_aptitud(fx)
            return
            

        
    def Seleccion(self):
        
        pass
        
    #def Cruza(self):

    #def Mutacion(self):
         
    def __str__(self):
        cadena = ''
        for cromo in self._poblacion: 
            cadena+=str(cromo)+'\n'
        return cadena

        
if __name__ == "__main__":
    A = AlgoritmoGenetico()
    A.PoblacionInicial()
    A.SetFitness()
