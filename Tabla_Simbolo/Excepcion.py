class Excepcion:
    def __init__(self, tipo, descripcion, fila, columna):
        self.tipo = tipo
        self.descripcion = descripcion
        self.fila = fila
        self.columna = columna

    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo

    def getDescripcion(self):
        return self.descripcion

    def setDescripcion(self, descripcion):
        self.descripcion = descripcion

    def getFila(self):
        return self.fila

    def setFila(self, fila):
        self.fila = fila

    def getColumna(self):
        return self.columna

    def setColumna(self, columna):
        self.columna = columna

    def toString(self):
        return self.tipo + " - " + self.descripcion + " [" + str(self.fila) + "," + str(self.columna) + "]"

