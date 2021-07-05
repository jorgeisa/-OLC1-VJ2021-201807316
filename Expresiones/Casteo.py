from Abstract.Instruccion import Instruccion
from Abstract.NodoArbol import NodoArbol
from Tabla_Simbolo.Excepcion import Excepcion
from Tabla_Simbolo.Tipo import TIPO, OperadorLogico


class Casteo(Instruccion):
    def __init__(self, tipo, expresion, fila, columna):
        self.tipo = tipo
        self.expresion = expresion
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        valor_expresion = self.expresion.interpretar(tree, table)

        if self.tipo == TIPO.DECIMAL:
            if (self.expresion.tipo == TIPO.ENTERO) or (self.expresion.tipo == TIPO.CARACTER) \
                    or (self.expresion.tipo == TIPO.CADENA):
                try:
                    if self.expresion.tipo == TIPO.CARACTER:
                        return float(ord(self.obtenerVal(self.expresion.tipo, valor_expresion)))
                    return float(self.obtenerVal(self.expresion.tipo, valor_expresion))
                except:
                    if self.expresion.tipo == TIPO.ENTERO:
                        return Excepcion("Semantico", "> Excepcion CASTEO DOUBLE: Error casteo de INT a DOUBLE. <",
                                         self.fila, self.columna)
                    elif self.expresion.tipo == TIPO.CARACTER:
                        return Excepcion("Semantico", "> Excepcion CASTEO DOUBLE: Error casteo de CARACTER a DOUBLE. <",
                                         self.fila, self.columna)
                    else:
                        return Excepcion("Semantico", "> Excepcion CASTEO DOUBLE: Error casteo de CADENA a DOUBLE. <",
                                         self.fila, self.columna)
            return Excepcion("Semantico", "> Excepcion CASTEO DOUBLE: Tipo erroneo para casteo. <",
                             self.fila, self.columna)
        elif self.tipo == TIPO.ENTERO:
            if (self.expresion.tipo == TIPO.DECIMAL) or (self.expresion.tipo == TIPO.CARACTER) \
                    or (self.expresion.tipo == TIPO.CADENA):
                try:
                    if self.expresion.tipo == TIPO.CARACTER:
                        return int(ord(self.obtenerVal(self.expresion.tipo, valor_expresion)))
                    return int(self.obtenerVal(self.expresion.tipo, valor_expresion))
                except:
                    if self.expresion.tipo == TIPO.DECIMAL:
                        return Excepcion("Semantico", "> Excepcion CASTEO INT: Error casteo de DECIMAL a INT. <",
                                         self.fila, self.columna)
                    elif self.expresion.tipo == TIPO.CARACTER:
                        return Excepcion("Semantico", "> Excepcion CASTEO INT: Error casteo de CARACTER a INT. <",
                                         self.fila, self.columna)
                    else:
                        return Excepcion("Semantico", "> Excepcion CASTEO INT: Error casteo de CADENA a INT. <",
                                         self.fila, self.columna)
            return Excepcion("Semantico", "> Excepcion CASTEO INT: Tipo erroneo para casteo. <",
                             self.fila, self.columna)
        elif self.tipo == TIPO.CADENA:
            if (self.expresion.tipo == TIPO.DECIMAL) or (self.expresion.tipo == TIPO.ENTERO):
                try:
                    return str(self.obtenerVal(self.expresion.tipo, valor_expresion))
                except:
                    if self.expresion.tipo == TIPO.DECIMAL:
                        return Excepcion("Semantico", "> Excepcion CASTEO STRING: Error casteo de DECIMAL a STRING. <",
                                         self.fila, self.columna)
                    elif self.expresion.tipo == TIPO.ENTERO:
                        return Excepcion("Semantico", "> Excepcion CASTEO STRING: Error casteo de INT a STRING. <",
                                         self.fila, self.columna)
            return Excepcion("Semantico", "> Excepcion CASTEO STRING: Tipo erroneo para casteo. <",
                             self.fila, self.columna)
        elif self.tipo == TIPO.CARACTER:
            if self.expresion.tipo == TIPO.ENTERO:
                try:
                    return chr(self.obtenerVal(self.expresion.tipo, valor_expresion))
                except:
                    return Excepcion("Semantico", "> Excepcion CASTEO CARACTER: Error casteo de INT a CHAR. <",
                                         self.fila, self.columna)
            return Excepcion("Semantico", "> Excepcion CASTEO CARACTER: Tipo erroneo para casteo. <",
                             self.fila, self.columna)
        elif self.tipo == TIPO.BOOLEANO:
            if self.expresion.tipo == TIPO.CADENA:
                try:
                    if str(self.obtenerVal(self.expresion.tipo, valor_expresion)).lower() == "true":
                        return True
                    elif str(self.obtenerVal(self.expresion.tipo, valor_expresion)).lower() == "false":
                        return False
                    else:
                        return Excepcion("Semantico",
                                         "> Excepcion CASTEO BOOLEAN: Cadena invalida en casteo de BOOLEAN A STRING <",
                                         self.fila, self.columna)
                except:
                    return Excepcion("Semantico", "> Excepcion CASTEO BOOLEAN: Error en casteo de BOOLEAN A STRING <",
                                     self.fila, self.columna)
            return Excepcion("Semantico", "> Excepcion CASTEO BOOLEAN: Tipo erroneo para casteo. <",
                             self.fila, self.columna)
        else:
            return Excepcion("Semantico", "> Excepcion CASTEO: Tipo no valido de casteo. <", self.fila, self.columna)

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

    def getNodo(self):
        nodo = NodoArbol("CASTEO")
        nodo.addHijoValor(str(self.obtenerTipo(self.tipo)))
        nodo.addHijoNodo(self.expresion.getNodo())
        return nodo
