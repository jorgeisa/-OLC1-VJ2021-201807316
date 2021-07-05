class Simbolo:
    def __init__(self, identificador, tipo, fila, columna, valor):
        self.id = identificador
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        self.valor = valor
        self.bandera_arreglo = False
        self.dimension_arreglo = None
        self.longitud_arreglo = 0

    def getID(self):
        return self.id

    def setID(self, id):
        self.id = id

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo

    def getValor(self):
        return self.valor

    def setValor(self, valor):
        self.valor = valor

    def getFila(self):
        return self.fila

    def getColumna(self):
        return self.columna

    def getBanderaArreglo(self):
        return self.bandera_arreglo

    def setBanderaArreglo(self, bandera_arreglo):
        self.bandera_arreglo = bandera_arreglo

    def getDimensionArreglo(self):
        return self.dimension_arreglo

    def setDimensionArreglo(self, dimension_arreglo):
        self.dimension_arreglo = dimension_arreglo

    def getLongitudArreglo(self):
        return self.longitud_arreglo

    def setLongitudArreglo(self, longitud):
        self.longitud_arreglo = longitud