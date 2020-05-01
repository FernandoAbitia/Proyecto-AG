class Cromosoma:

    def __init__(self):
        self._genes = []
        self._aptutid = 0

    def get_aptitud(self):
        return self._aptitud

    def set_aptitud(self, aptitud):
        self._aptitud=aptitud

    def get_genes(self):
        return self._genes

    def set_genes(self, genes):
        self._genes=genes

    def __str__(self):
        return self._genes.__str__()

##if __name__ == "__main__":
##    C1 = Cromosoma()
##    genes = [0,1,1,0,1,1,1,0,0,0,1,0,0,0,1,1]
##    C1.set_genes(genes)
##    print(str(C1.__str__()))
    
