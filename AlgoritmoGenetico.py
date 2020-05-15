from Cromosoma import Cromosoma
import random
import numpy as np
import pandas as pd
df_beneficios=pd.read_csv('CSV\Beneficios.csv')
class AlgoritmoGenetico:

    def __init__(self, generaciones=50, individuos=50, cruza=0.8, mutacion=0.01):
        self._generaciones=generaciones
        self._individuos=individuos
        self._pCruza=cruza
        self._pMutacion=mutacion
        self._poblacion=[]

    def PoblacionInicial(self):
        inv=[]
        #Ciclo inicial que itera tantas veces como individuos haya
        for i in range(self._individuos):
                inv = [str(bin(x))[2:].zfill(4) for x in self.generarInversion()]
                Genes = [int(i) for e in inv for i in e]
                self._poblacion.append(Cromosoma(Genes))
        return self._poblacion

    def Algoritmo(self):
        self.PoblacionInicial()
        self.SetFitness()
        print('PRIMERA GENERACIÓN')
        print(A)
        for generacion in range(self._generaciones):
           self.Seleccion_Tournament()
           self.Cruza()
           self.SetFitness()
        print('ÚLTIMA GENERACIÓN')
        self._poblacion.sort(key= lambda x: x.get_aptitud(), reverse=True) 
        print(A)
        print('MEJOR INVERSIÓN POR ZONA DE ACUERDO A LA EVOLUCIÓN DE LOS VALORES DE LA POBLACIÓN:')
        investFinal=self.getInversion(self._poblacion.pop(0).get_genes())
        for index in range(len(investFinal)): 
            print(f'ZONA {index+1}: {investFinal[index]}')
        print(f'GANANCIA MÁXIMA CALCULADA ${sum(self.getBeneficios(investFinal))} MILLONES')

    def getBeneficios(self,inversiones):
        beneficios=[]
        for index in range(len(inversiones)):
            inversion=inversiones[index]
            if(inversion>10):
                #genesTemp[(index*4):(index*4)+4]=[0,0,0,0]
                inversiones[index]=0
            beneficios.append(df_beneficios[df_beneficios['Inversion']==inversiones[index]].iloc[0,(index+1)])    
        return beneficios
           
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
            genesTemp=cromosoma.get_genes()
            inversiones=self.getInversion(genesTemp)

            #Aplicamos la función de aptitud y le asignamos el valor al cromosoma
            #Primero obtenemos los beneficios o ganancias por zona de acuerdo a la inversión
            beneficios=self.getBeneficios(inversiones)

            #Calculamos la suma de las inversiones de cada zona
            sumaInvest=sum(inversiones)

            #Calculamos la suma de los ganancias de las inversiones 
            sumBen=sum(beneficios)

            #Obtenemos la variable que 'v' que equivale al valor absoluto de la diferencia de la suma anterior y 10
            v=abs(sumaInvest-10)

            #Calculamos la función de aptitud para el cromosoma
            fx=sumBen/(500*v+1)

            #Asignamos el valor de la función al individuo
            cromosoma.set_aptitud(fx)
            #print( str(cromosoma) + str(cromosoma.get_aptitud()) )
        return
        
    def Seleccion_Tournament(self):
        #print('------SELECCIÓN-------')
        torneo = []
        descendientes = []
        while len(descendientes) != len(self._poblacion):
            num1=random.randint(0,49)
            num2=random.randint(0,49)

            if(num1==num2):
                continue

            seleccionado1 = self._poblacion[num1]
            seleccionado2 = self._poblacion[num2]

            if seleccionado1.get_aptitud() > seleccionado2.get_aptitud():
                subTorneo = [seleccionado1,seleccionado2, seleccionado1]
                descendientes.append(seleccionado1)
                torneo.append(subTorneo) 
            else:
                subTorneo = [seleccionado1,seleccionado2, seleccionado2]
                descendientes.append(seleccionado2)  
                torneo.append(subTorneo)

        self._poblacion= descendientes
        self._poblacion.sort(key= lambda x: x.get_aptitud(), reverse=True)  
        return torneo

    def Cruza(self):
        nPoblacion = []#Nueva población
        while (len(self._poblacion)!=0):#Ciclo que itera en número de cromosomas en la población

            p1 = self._poblacion.pop(0)#Obtener el primer padre de la población
            p2 = self._poblacion.pop(0)#Obtener el segundo padre

            if (random.uniform(0,1) > self._pCruza):#Si la probabilidad obtenida es mayor a la de cruza, los padres pasan tal cual a la nueva población
                nPoblacion.extend([p1,p2])
                continue

            g1 = p1.get_genes()#Obtener los genes del padre 1
            g2 = p2.get_genes()#Obtener los genes del padre 2

            while (True):#Ciclo que verifica que los puntos de cruza sean diferentes a la longitud de toda la lista
                x1 = random.randint(0,(len(g1)/2))
                x2 = random.randint(x1+1,(len(g1)-1))
                if ((x2-x1)<15):
                    break

            ch1 = g1[0:x1] + g2[x1:x2+1] + g1[x2+1:len(g1)]#Crear el primer hijo
            ch2 = g2[0:x1] + g1[x1:x2+1] + g2[x2+1:len(g2)]#Crear el segundo hijo

            ch1 = self.Mutacion(ch1)#Aplicar una probable mutación
            ch2 = self.Mutacion(ch2)#Aplicar una probable mutación

            nP1=Cromosoma(ch1,p1.get_aptitud())
            nP2=Cromosoma(ch2,p2.get_aptitud())

            nPoblacion.extend([nP1,nP2])# Agregar los nuevos cromosomas hijo a la nueva población
        self._poblacion=nPoblacion#Reasignar la variable de la población

    def Mutacion(self, genes):
        if (random.uniform(0,1)>self._pMutacion):
            return genes

        p = random.randint(0,(len(genes)-1))
        bit = 1 if genes[p]==0 else 0
        genes[p]=bit
        return genes
                           
    def __str__(self):
        cadena = ''
        for cromo in self._poblacion: 
            cadena+='Cromosoma:'+str(cromo.get_genes())+'- Inversión: '+str(self.getInversion(cromo.get_genes()))+ '- Fitness: '+str(cromo.get_aptitud())+'\n'
        return cadena

    def printTorneo(self, torneo):
        cadena = 'TORNEO\n\t\t\t\t\tPARTICIPANTES\t\t\t\t\t\t\t\t\tGANADOR\n\n'
        for cromo in torneo: 
            for cromosoma in cromo:
                cadena+=str(self.getInversion(cromosoma.get_genes()))+' Fitness: '+str(round(cromosoma.get_aptitud(),2))+'   '
            cadena+='\n'
        return cadena

    def generarInversion(self):
        suma=0
        temp=[]
        while(suma!=10):
            temp=[random.randint(0,10) for index in range(4)]
            suma=sum(temp)
        return temp
            
if __name__ == "__main__":
    A = AlgoritmoGenetico()
    print('\nALGORITMO GENÉTICO QUE DETERMINA LA MEJOR INVERSIÓN DE LAS CUATRO ZONAS DE LA SIGUIENTE TABLA:\n')
    print(str(df_beneficios)+'\n')
    A.Algoritmo()