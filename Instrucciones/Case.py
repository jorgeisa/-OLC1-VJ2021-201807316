from Abstract.Instruccion import Instruccion
from Abstract.NodoArbol import NodoArbol


class Case(Instruccion):
    def __init__(self, expresion, instrucciones, fila, columna):
        self.expresion = expresion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna
        self.valorCase = None

    def interpretar(self, tree, table):
        # Significa que es un case
        if self.expresion is not None:
            value = self.expresion.interpretar(tree, table) # 45
            if isinstance(value, Exception):
                return value
            self.valorCase = value
        # Signiifica que es un Default
        else:
            value = None
            self.valorCase = None
        return value

    def getInstrucciones(self):
        return self.instrucciones

    def getExpresion(self):
        return self.expresion

    def getNodo(self):
        # Significa que es un case si el valor no es None
        if self.valorCase is not None:
            nodo = NodoArbol("CASE")
            nodo.addHijoNodo(self.expresion.getNodo())
            nodo_instrucciones = NodoArbol("INSTRUCCIONES CASE")
        else:
            nodo = NodoArbol("DEFAULT")
            nodo_instrucciones = NodoArbol("INSTRUCCIONES DEFAULT")

        for instruccion in self.instrucciones:
            nodo_instrucciones.addHijoNodo(instruccion.getNodo())
        nodo.addHijoNodo(nodo_instrucciones)
        return nodo
