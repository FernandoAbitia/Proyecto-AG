class Cromosoma:

    def __init__(self, genes):
        self._genes=genes
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


    
