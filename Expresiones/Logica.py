from Abstract.Instruccion import Instruccion
from Abstract.NodoArbol import NodoArbol
from Tabla_Simbolo.Excepcion import Excepcion
from Tabla_Simbolo.Tipo import TIPO, OperadorLogico


class Logica(Instruccion):
    def __init__(self, operador, OperacionIzq, OperacionDer, fila, columna):
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.BOOLEANO

    def interpretar(self, tree, table):
        izq = self.OperacionIzq.interpretar(tree, table)
        if isinstance(izq, Excepcion): return izq

        if self.OperacionDer is not None:
            der = self.OperacionDer.interpretar(tree, table)
            if isinstance(der, Excepcion): return der

        # ----------------------------- AND -------------------------------------------
        if self.operador == OperadorLogico.AND:
            # Boolean and Boolean
            if self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) and self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", ">Tipo Erroneo de operacion para &&.<", self.fila, self.columna)
        # ----------------------------- OR ---------------------------------------------
        elif self.operador == OperadorLogico.OR:
            # Boolean or Boolean
            if self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) or self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", ">Tipo Erroneo de operacion para ||.<", self.fila, self.columna)
        # ----------------------------- NOT ---------------------------------------------
        elif self.operador == OperadorLogico.NOT:
            if self.OperacionIzq.tipo == TIPO.BOOLEANO:
                return not self.obtenerVal(self.OperacionIzq.tipo, izq)
            return Excepcion(">Semantico", "Tipo Erroneo de operacion para !.<", self.fila, self.columna)
        return Excepcion("Semantico", ">Tipo de Operacion no Especificado. Operacion Logica.<", self.fila, self.columna)

    def obtenerVal(self, tipo, val):
        if tipo == TIPO.ENTERO:
            return int(val)
        elif tipo == TIPO.DECIMAL:
            return float(val)
        elif tipo == TIPO.BOOLEANO:
            return bool(val)
        return str(val)

    def obtenerTipo(self, tipo):
        if tipo == TIPO.ENTERO:
            return "Int"
        elif tipo == TIPO.DECIMAL:
            return "Double"
        elif tipo == TIPO.BOOLEANO:
            return "Boolean"
        elif tipo == TIPO.CARACTER:
            return "Char"
        elif tipo == TIPO.CADENA:
            return "String"
        elif tipo == TIPO.NULO:
            return "Null"
        elif tipo == TIPO.ARREGLO:
            return "Array"

    def obtenerTipoLogico(self, tipo):
        if tipo == OperadorLogico.NOT:
            return "!"
        elif tipo == OperadorLogico.AND:
            return "&&"
        elif tipo == OperadorLogico.OR:
            return "||"
        return "None"

    def getNodo(self):
        nodo = NodoArbol("LOGICA")
        # Si no es unaria (Solo viene operador izquierdo como !numero)
        if self.OperacionDer is not None:
            nodo.addHijoNodo(self.OperacionIzq.getNodo())
            nodo.addHijoValor(str(self.obtenerTipoLogico(self.operador)))
            nodo.addHijoNodo(self.OperacionDer.getNodo())
        else:
            nodo.addHijoValor(str(self.obtenerTipoLogico(self.operador)))
            nodo.addHijoNodo(self.OperacionIzq.getNodo())
        return nodo
