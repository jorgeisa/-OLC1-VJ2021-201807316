from Abstract.Instruccion import Instruccion
from Abstract.NodoArbol import NodoArbol
from Tabla_Simbolo.Excepcion import Excepcion
from Tabla_Simbolo.Tipo import TIPO, OperadorRelacional


class Relacional(Instruccion):
    def __init__(self, operador, OperacionIzq, OperacionDer, fila, columna):
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.fila = fila
        self.columna = columna
        self.tipo = TIPO.BOOLEANO  # Tipo booleano ya que siempre retornara un booleano

    def interpretar(self, tree, table):
        # Siempre tienen que venir derecha e izquierda
        izq = self.OperacionIzq.interpretar(tree, table)
        if isinstance(izq, Excepcion): return izq
        der = self.OperacionDer.interpretar(tree, table)
        if isinstance(der, Excepcion): return der

        # ----------------------------------- IGUALACION == ------------------------------------------------------------
        if self.operador == OperadorRelacional.IGUALIGUAL:
            # /////////////////////////////////// IGUALACION - INT ///////////////////////////////////////////////////
            # Int == Int o Int == Double (Es casteado automaticamente con el obtenerVal
            if self.OperacionIzq.tipo == TIPO.ENTERO and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                          self.OperacionDer.tipo == TIPO.DECIMAL):
                return self.obtenerVal(self.OperacionIzq.tipo, izq) == self.obtenerVal(self.OperacionDer.tipo, der)
            # Int == String
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.CADENA:
                return str(self.obtenerVal(self.OperacionIzq.tipo, izq)) == self.obtenerVal(self.OperacionDer.tipo, der)

            # /////////////////////////////////// IGUALACION - Double //////////////////////////////////////////////////
            # Double == int y Double == Double
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                          self.OperacionDer.tipo == TIPO.DECIMAL):
                return self.obtenerVal(self.OperacionIzq.tipo, izq) == self.obtenerVal(self.OperacionDer.tipo, der)
            # Double == String
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.CADENA:
                return str(self.obtenerVal(self.OperacionIzq.tipo, izq)) == self.obtenerVal(self.OperacionDer.tipo, der)

            # /////////////////////////////////// IGUALACION - Boolean/////////////////////////////////////////////////
            # Boolean == Boolean
            elif self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) == self.obtenerVal(self.OperacionDer.tipo, der)
            # Boolean == cadena
            elif self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.CADENA:
                return str(self.obtenerVal(self.OperacionIzq.tipo, izq)).lower() == \
                       str(self.obtenerVal(self.OperacionDer.tipo, der)).lower()

            # /////////////////////////////////// IGUALACION - Char /////////////////////////////////////////////////
            # Char == Char
            elif self.OperacionIzq.tipo == TIPO.CARACTER and self.OperacionDer.tipo == TIPO.CARACTER:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) == self.obtenerVal(self.OperacionDer.tipo, der)

            # /////////////////////////////////// IGUALACION - String /////////////////////////////////////////////////
            # String == Int o String == Double
            elif self.OperacionIzq.tipo == TIPO.CADENA and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                            self.OperacionDer.tipo == TIPO.DECIMAL or
                                                            self.OperacionDer.tipo == TIPO.BOOLEANO):
                der_valor = str(self.obtenerVal(self.OperacionDer.tipo, der))
                return str(self.obtenerVal(self.OperacionIzq.tipo, izq)).lower() == der_valor.lower()

            elif self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.CADENA:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) == self.obtenerVal(self.OperacionDer.tipo, der)

            return Excepcion(">Semantico", "Tipo Erroneo de operacion para Igualacion ==.<", self.fila, self.columna)

        # ----------------------------------- Diferenciacion =! --------------------------------------------------------
        elif self.operador == OperadorRelacional.DIFERENTE:
            # ////////////////////////////// DIFERENCIACION - INT /////////////////////////////////////////////////////
            # Int == Int o Int == Double
            if self.OperacionIzq.tipo == TIPO.ENTERO and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                          self.OperacionDer.tipo == TIPO.DECIMAL):
                return self.obtenerVal(self.OperacionIzq.tipo, izq) != self.obtenerVal(self.OperacionDer.tipo, der)
            # Int == String
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.CADENA:
                return str(self.obtenerVal(self.OperacionIzq.tipo, izq)) != self.obtenerVal(self.OperacionDer.tipo, der)

            # ////////////////////////////// DIFERENCIACION - DOUBLE ///////////////////////////////////////////////////
            # Double =! Int o Double =! Double
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                             self.OperacionDer.tipo == TIPO.DECIMAL):
                return self.obtenerVal(self.OperacionIzq.tipo, izq) != self.obtenerVal(self.OperacionDer.tipo, der)
            # Double =! String
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and (self.OperacionDer.tipo == TIPO.CADENA):
                return str(self.obtenerVal(self.OperacionIzq.tipo, izq)) != self.obtenerVal(self.OperacionDer.tipo, der)

            # ////////////////////////////// DIFERENCIACION - BOOLEAN //////////////////////////////////////////////////
            # Boolean =! Boolean
            elif self.OperacionIzq.tipo == TIPO.BOOLEANO and (self.OperacionDer.tipo == TIPO.BOOLEANO):
                return self.obtenerVal(self.OperacionIzq.tipo, izq) != self.obtenerVal(self.OperacionDer.tipo, der)
            # Boolean =! String
            elif self.OperacionIzq.tipo == TIPO.BOOLEANO and (self.OperacionDer.tipo == TIPO.CADENA):
                return str(self.obtenerVal(self.OperacionIzq.tipo, izq)).lower() != str(self.obtenerVal(self.OperacionDer.tipo, der)).lower()

            # ////////////////////////////// DIFERENCIACION - CHAR //////////////////////////////////////////////////
            elif self.OperacionIzq.tipo == TIPO.CARACTER and (self.OperacionDer.tipo == TIPO.CARACTER):
                return self.obtenerVal(self.OperacionIzq.tipo, izq) != self.obtenerVal(self.OperacionDer.tipo, der)

            # ////////////////////////////// DIFERENCIACION - STRING //////////////////////////////////////////////////
            # Striong =! Int o String =! Double o String =! Boolean
            elif self.OperacionIzq.tipo == TIPO.CADENA and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                            self.OperacionDer.tipo == TIPO.DECIMAL or
                                                            self.OperacionDer.tipo == TIPO.BOOLEANO):
                return str(self.obtenerVal(self.OperacionIzq.tipo, izq)).lower() != \
                       str(self.obtenerVal(self.OperacionDer.tipo, der)).lower()
            elif self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.CADENA:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) != self.obtenerVal(self.OperacionDer.tipo, der)

            return Excepcion("Semantico", ">Tipo Erroneo de operacion para Diferenciacion =!.<", self.fila, self.columna)

        # ----------------------------------- MENOR QUE < --------------------------------------------------------
        elif self.operador == OperadorRelacional.MENORQUE:
            # ////////////////////////////// MENOR QUE - INT //////////////////////////////////////////////////
            # Int < Int o Int < Double
            if self.OperacionIzq.tipo == TIPO.ENTERO and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                          self.OperacionDer.tipo == TIPO.DECIMAL):
                return self.obtenerVal(self.OperacionIzq.tipo, izq) < self.obtenerVal(self.OperacionDer.tipo, der)

            # ////////////////////////////// MENOR QUE - DOUBLE //////////////////////////////////////////////////
            # Double < Int y Double < Double
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                             self.OperacionDer.tipo == TIPO.DECIMAL):
                return self.obtenerVal(self.OperacionIzq.tipo, izq) < self.obtenerVal(self.OperacionDer.tipo, der)

            # ////////////////////////////// MENOR QUE - Boolean //////////////////////////////////////////////////
            # Boolean < Boolean
            elif self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) < self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", ">Tipo Erroneo de operacion para Menor que <.<", self.fila, self.columna)

        # ----------------------------------- MAYOR QUE > --------------------------------------------------------
        elif self.operador == OperadorRelacional.MAYORQUE:
            # ////////////////////////////// MAYOR QUE - INT //////////////////////////////////////////////////
            # Int > Int o Int > Double
            if self.OperacionIzq.tipo == TIPO.ENTERO and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                          self.OperacionDer.tipo == TIPO.DECIMAL):
                return self.obtenerVal(self.OperacionIzq.tipo, izq) > self.obtenerVal(self.OperacionDer.tipo, der)

            # ////////////////////////////// MAYOR QUE - DOUBLE //////////////////////////////////////////////////
            # Double > Int y Double > Double
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                             self.OperacionDer.tipo == TIPO.DECIMAL):
                return self.obtenerVal(self.OperacionIzq.tipo, izq) > self.obtenerVal(self.OperacionDer.tipo, der)

            # ////////////////////////////// MAYOR QUE - Boolean //////////////////////////////////////////////////
            # Boolean > Boolean
            elif self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) > self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion(">Semantico", "Tipo Erroneo de operacion para Mayor que >.<", self.fila, self.columna)

        # ----------------------------------- MENOR IGUAL <= --------------------------------------------------------
        elif self.operador == OperadorRelacional.MENORIGUAL:
            # ////////////////////////////// MENOR IGUAL - INT //////////////////////////////////////////////////
            # Int <= Int o Int <= Double
            if self.OperacionIzq.tipo == TIPO.ENTERO and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                          self.OperacionDer.tipo == TIPO.DECIMAL):
                return self.obtenerVal(self.OperacionIzq.tipo, izq) <= self.obtenerVal(self.OperacionDer.tipo, der)

            # ////////////////////////////// MENOR IGUAL - DOUBLE //////////////////////////////////////////////////
            # Double <= Int y Double <= Double
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                             self.OperacionDer.tipo == TIPO.DECIMAL):
                return self.obtenerVal(self.OperacionIzq.tipo, izq) <= self.obtenerVal(self.OperacionDer.tipo, der)

            # ////////////////////////////// MENOR IGUAL - Boolean //////////////////////////////////////////////////
            # Boolean <= Boolean
            elif self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) <= self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", ">Tipo Erroneo de operacion para Menor Igual <=.<", self.fila, self.columna)

        # ----------------------------------- MAYOR IGUAL >= --------------------------------------------------------
        elif self.operador == OperadorRelacional.MAYORIGUAL:
            # ////////////////////////////// MAYOR IGUAL - INT //////////////////////////////////////////////////
            # Int >= Int o Int >= Double
            if self.OperacionIzq.tipo == TIPO.ENTERO and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                          self.OperacionDer.tipo == TIPO.DECIMAL):
                return self.obtenerVal(self.OperacionIzq.tipo, izq) >= self.obtenerVal(self.OperacionDer.tipo, der)

            # ////////////////////////////// MAYOR IGUAL - DOUBLE //////////////////////////////////////////////////
            # Double >= Int y Double >= Double
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                             self.OperacionDer.tipo == TIPO.DECIMAL):
                return self.obtenerVal(self.OperacionIzq.tipo, izq) >= self.obtenerVal(self.OperacionDer.tipo, der)

            # ////////////////////////////// MAYOR IGUAL - Boolean //////////////////////////////////////////////////
            # Boolean >= Boolean
            elif self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.BOOLEANO:
                return self.obtenerVal(self.OperacionIzq.tipo, izq) >= self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", ">Tipo Erroneo de operacion para Mayo Igual >=.<", self.fila, self.columna)
        return Excepcion("Semantico", ">Tipo de Operacion no Especificado. Operacion Relacional <", self.fila, self.columna)

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

    def obtenerTipoRelacional(self, tipo):
        if tipo == OperadorRelacional.MENORQUE:
            return "<"
        elif tipo == OperadorRelacional.MAYORQUE:
            return ">"
        elif tipo == OperadorRelacional.MENORIGUAL:
            return "<="
        elif tipo == OperadorRelacional.MAYORIGUAL:
            return ">="
        elif tipo == OperadorRelacional.IGUALIGUAL:
            return "=="
        elif tipo == OperadorRelacional.DIFERENTE:
            return "!="
        return "None"

    def getNodo(self):
        nodo = NodoArbol("RELACIONAL")
        nodo.addHijoNodo(self.OperacionIzq.getNodo())
        nodo.addHijoValor(str(self.obtenerTipoRelacional(self.operador)))
        nodo.addHijoNodo(self.OperacionDer.getNodo())
        return nodo
