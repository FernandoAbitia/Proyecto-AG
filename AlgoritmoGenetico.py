from Cromosoma import Cromosoma
from functools import reduce
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
        inv=[]
        #Ciclo inicial que itera tantas veces como individuos haya
        for i in range(self._individuos):
                inv = [str(bin(x))[2:].zfill(4) for x in self.generarInversion(0,list(),0)]
                Genes = [int(i) for e in inv for i in e]
                self._poblacion.append(Cromosoma(Genes))
    
    def Algoritmo(self):
        self.PoblacionInicial()
        for generacion in range(self._generaciones):
           self.SetFitness()
           self.Seleccion()
           self.Cruza()
           print(A)
           
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
        while len(descendientes) != len(self._poblacion):
            seleccionado1 = self._poblacion[random.randint(0,49)]
            seleccionado2 = self._poblacion[random.randint(0,49)]
            if seleccionado1 != seleccionado2:
                if seleccionado1.get_aptitud() > seleccionado2.get_aptitud():
                    subTorneo = [seleccionado1,seleccionado2, seleccionado1]
                    descendientes.append(seleccionado1) 
                else:
                    subTorneo = [seleccionado1,seleccionado2, seleccionado2]
                    descendientes.append(seleccionado2)  
                torneo.append(subTorneo)
        self._poblacion= descendientes  
        return torneo

    def Cruza(self):
        nPoblacion = []#Nueva población
        while (len(self._poblacion)!=0):#Ciclo que itera en número de cromosomas en la población
            p1 = self._poblacion.pop(0)#Obtener el primer padre de la población
            p2 = self._poblacion.pop(0)#Obtener el segundo padre
            if (random.uniform(0,1) < self._pCruza):#Si la probabilidad obtenida es menor a la de cruza, los padres pasan tal cual a la nueva población
                nPoblacion.extend([p1,p2])
                continue
            g1 = p1.get_genes()#Obtener los genes del padre 1
            g2 = p2.get_genes()#Obtener los genes del padre 2
            while (True):#Ciclo que verifica que los puntos de cruza sean diferentes a la longitud de toda la lista
                x1 = random.randint(0,(len(g1)/2))
                x2 = random.randint(x1+1,(len(g1)-1))
                if ((x2-x1)<16):
                    break
            ch1 = g1[0:x1] + g2[x1:x2+1] + g1[x2+1:len(g1)]#Crear el primer hijo
            ch2 = g2[0:x1] + g1[x1:x2+1] + g2[x2+1:len(g2)]#Crear el segundo hijo
            ch1 = self.Mutacion(ch1)#Aplicar una probable mutación
            ch2 = self.Mutacion(ch2)#Aplicar una probable mutación
            L=[]
            L.extend([ch1,ch2])#Lista que guarda los genes de los hijos para iterarlos en el posterior ciclo
            C=[]#Lista que almacena los valores finales del los genes (en caso de anular una cadena)
            for i in range(2):#Ciclo que itera los genes de los cromosomas hijo
                k=0#Variable que se utiliza para tomar rangos de cadenas de la lista de genes
                genes=L.pop(0)#Obtener la lista de genes del primer /segundo hijo
                R = self.getInversion(genes)#Obtener los valores de la lista en decimal (inversiones)
                for inversion in R:#Ciclo para verificar cada inversion
                    if (inversion>10):
                        genes[k:k+4]=[0,0,0,0]#Si la inversión es mayor a 10 se anula y se deja 0
                    k+=4#Incrementar el rango para tomar la siguiente cadena
                    C.append(genes)#Agregar la lista de genes a la lista de genes finales
            ch1 = C.pop(0)#Obtener la lista de genes finales del hijo 1
            ch2 = C.pop(0)#Obtener la lista de genes finales del hijo 2
            nPoblacion.extend([Cromosoma(ch1),Cromosoma(ch2)])# Agregar los nuevos cromosomas hijo a la nueva población
        self._poblacion=nPoblacion#Reasignar la variable de la población

    def Mutacion(self, genes):
        if (random.uniform(0,1)<self._pMutacion):
            return genes
        p = random.randint(0,(len(genes)-1))
        bit = random.randint(0,1)
        genes[p]=bit
        return genes
                           
    def __str__(self):
        cadena = ''
        for cromo in self._poblacion: 
            cadena+=str(cromo)+ ' Fitness: '+str(cromo.get_aptitud())+'\n'
        return cadena

    def printTorneo(self, torneo):
        cadena = 'TORNEO\n\t\t\t\t\tPARTICIPANTES\t\t\t\t\t\t\t\t\tGANADOR\n\n'
        for cromo in torneo: 
            for cromosoma in cromo:
                cadena+=str(cromosoma)+'  '
            cadena+='\n'
        return cadena

    def generarInversion(self, count,list, acomulado):
        if count == 3:
            list.append((10-acomulado))
            return 
        inversion = random.randint(0,(10-acomulado))
        acomulado+= inversion
        count= count + 1
        list.append(inversion)
        self.generarInversion(count,list,acomulado)
        return list
            
if __name__ == "__main__":
    A = AlgoritmoGenetico()
    A.Algoritmo()

    
