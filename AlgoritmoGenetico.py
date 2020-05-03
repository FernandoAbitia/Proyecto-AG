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
        #Definimos una lista que almacenará las inversiones (para validación)
        inv=[]
        #Ciclo inicial que itera tantas veces como individuos haya
        for i in range(self._individuos):
            #Definimos un ciclo que se repetirá hasta obtener una lista de genes cuyas cadenas no superen
            #el valor 10 en decimal (por cadena individual)
            while True:
                #Se genera una nueva lista de genes
                genes = np.random.randint(low=0, high=2, size=(16))
                #Obtenemos la lista de inversiones en valor decimal
                inv=self.getInversion(genes)
                #Si alguna de las cadenas supera el valor 10 en decimal, el ciclo while se reinicializa
                if (any((c>10) for c in inv)):
                    continue
                #De lo contrario, agregamos a la población un nuevo cromosoma con una lista de genes con cadenas binarias válidas
                self._poblacion.append(Cromosoma(genes))
                #Salimos del ciclo while y se procede a la siguiente iteración del ciclo for
                break
    
    def Algoritmo(self):
        for generacion in self._generaciones:
           self.Seleccion()

        ##Calcular aptitud a la población
        ##Selección
        ##Cruza
        ##Mutación
        ##
           
    def getInversion(self, genes):
        #Dividimos en 4 bits la cadena binaria del cromosoma
        cadenas=np.array_split(genes,4)
        #Definimos una lista que guardará las 4 inversiones (1 para cada lista/cadena)
        x = []
        #Abrimos otro ciclo para iterar sobre cada cadena del cromosoma (que representan las inversiones de cada zona)
        for cadenaBinaria in cadenas:
            c=0
            #Iteramos sobre los bits de la cadena para obtener su equivalente en decimal
            for bit in cadenaBinaria:
                #Realizamos el desplazamiento y OR de los bits
                c=(c<<1) | bit
            #Agregamos el valor decimal de la cadena binaria a la lista
            x.append(c)
        return x
    
    def SetFitness(self):
        inversiones=[]
        #Accedemos a un ciclo para iterar sobre los individuos de la población
        for cromosoma in self._poblacion:
            inversiones=self.getInversion(cromosoma.get_genes())
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
        torneo = []
        descendientes = []
        while descendientes.__len__ != self._poblacion.__len__:
            seleccionado1 = self._poblacion[random.randint(0,50)]
            seleccionado2 = self._poblacion[random.randint(0,50)]
            if seleccionado1.get_aptitud() > seleccionado2.get_aptitud():
                subTorneo = [seleccionado1,seleccionado2, seleccionado1]
                descendientes.append(seleccionado1)        
            else:
                subTorneo = [seleccionado1,seleccionado2, seleccionado2]
                descendientes.append(seleccionado2)        
            torneo.append(subTorneo)
        self._poblacion= descendientes.sort(key=lambda x: x.get_aptitud())

        
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
    print(A)
    #A.SetFitness()
