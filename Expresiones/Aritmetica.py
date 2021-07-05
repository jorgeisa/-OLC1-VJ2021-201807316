from Abstract.Instruccion import Instruccion
from Abstract.NodoArbol import NodoArbol
from Expresiones.AccesoArreglo import AccesoArreglo
from Tabla_Simbolo.Excepcion import Excepcion
from Expresiones.Identificador import Identificador
from Tabla_Simbolo.Tipo import TIPO, OperadorAritmetico
from Tabla_Simbolo.Simbolo import Simbolo


class Aritmetica(Instruccion):
    def __init__(self, operador, OperacionIzq, OperacionDer, fila, columna):
        self.operador = operador
        self.OperacionIzq = OperacionIzq
        self.OperacionDer = OperacionDer
        self.fila = fila
        self.columna = columna
        self.tipo = None

    def interpretar(self, tree, table):
        izq = self.OperacionIzq.interpretar(tree, table)
        if isinstance(izq, Excepcion): return izq
        if self.OperacionDer is not None:
            der = self.OperacionDer.interpretar(tree, table)
            if isinstance(der, Excepcion): return der

        # Si el izquierdo es de tipo identificador
        if self.operador == OperadorAritmetico.MASMAS:
            if isinstance(self.OperacionIzq, Identificador):
                if (self.OperacionIzq.tipo == TIPO.ENTERO) or (self.OperacionIzq.tipo == TIPO.DECIMAL):
                    self.tipo = self.OperacionIzq.tipo
                    simbolo = table.getTabla(self.OperacionIzq.identificador)

                    if simbolo is None:
                        return Excepcion("Semantico", ">Variable " + self.OperacionIzq.identificador + " no encontrada. Operacion ++.<", self.fila, self.columna)

                    valor_sim = simbolo.getValor()
                    valor_sim = valor_sim + 1
                    simbolo.setValor(valor_sim)
                    result = table.actualizarTabla(simbolo)
                    if isinstance(result, Excepcion): return result
                    return valor_sim
                return Excepcion("Semantico", "Tipo Erroneo de operacion para ++.", self.fila, self.columna)

        elif self.operador == OperadorAritmetico.MENOSMENOS:
            if isinstance(self.OperacionIzq, Identificador):
                if (self.OperacionIzq.tipo == TIPO.ENTERO) or (self.OperacionIzq.tipo == TIPO.DECIMAL):
                    self.tipo = self.OperacionIzq.tipo
                    simbolo = table.getTabla(self.OperacionIzq.identificador)

                    if simbolo is None:
                        return Excepcion("Semantico", ">Variable " + self.OperacionIzq.identificador +
                                         " no encontrada. Operacion --.<", self.fila, self.columna)

                    valor_sim = simbolo.getValor()
                    valor_sim = valor_sim - 1
                    simbolo.setValor(valor_sim)
                    result = table.actualizarTabla(simbolo)
                    if isinstance(result, Excepcion): return result
                    return valor_sim
                return Excepcion("Semantico", ">Tipo Erroneo de operacion para --.<", self.fila, self.columna)
            return Excepcion("Semantico", ">La operacion -- requiere identificador.<", self.fila, self.columna)

        # -------------------------------------------- SUMA -----------------------------------------------------------
        elif self.operador == OperadorAritmetico.MAS:  # SUMA
            # //////////////////////////////////SUMA - INT//////////////////////////////////////////////////////////
            # Int + Int
            if self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            # Int + Double
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            # Int + Boolean
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.BOOLEANO:
                self.tipo = TIPO.ENTERO
                bool_valor = self.obtenerVal(self.OperacionDer.tipo, der)
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + int(bool_valor)
            # Int + String
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.CADENA:
                self.tipo = TIPO.CADENA
                return str(self.obtenerVal(self.OperacionIzq.tipo, izq)) + self.obtenerVal(self.OperacionDer.tipo, der)

            # //////////////////////////////////SUMA - DOUBLE///////////////////////////////////////////////////////////
            # Double + Int y Double + Double
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                             self.OperacionDer.tipo == TIPO.DECIMAL):
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            # Double + Boolean
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.BOOLEANO:
                self.tipo = TIPO.DECIMAL
                bool_valor = self.obtenerVal(self.OperacionDer.tipo, der)
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + int(bool_valor)
            # Double + String
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and self.OperacionDer.tipo == TIPO.CADENA:
                self.tipo = TIPO.CADENA
                return str(self.obtenerVal(self.OperacionIzq.tipo, izq)) + self.obtenerVal(self.OperacionDer.tipo, der)

            # //////////////////////////////////SUMA - BOOLEAN//////////////////////////////////////////////////////////
            # Boolean + Int
            elif self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                bool_valor = self.obtenerVal(self.OperacionIzq.tipo, izq)
                return int(bool_valor) + self.obtenerVal(self.OperacionDer.tipo, der)
            # Boolean + Double
            elif self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                bool_valor = self.obtenerVal(self.OperacionIzq.tipo, izq)
                return int(bool_valor) + self.obtenerVal(self.OperacionDer.tipo, der)
            # Boolean + Boolean
            elif self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.BOOLEANO:
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            # Boolean + String
            elif self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.CADENA:
                self.tipo = TIPO.CADENA
                return str(self.obtenerVal(self.OperacionIzq.tipo, izq)) + self.obtenerVal(self.OperacionDer.tipo, der)

            # //////////////////////////////////SUMA - CHAR//////////////////////////////////////////////////////////
            # Caracter + caracter y Carater + String
            elif self.OperacionIzq.tipo == TIPO.CARACTER and (self.OperacionDer.tipo == TIPO.CARACTER or
                                                              self.OperacionDer.tipo == TIPO.CADENA):
                self.tipo = TIPO.CADENA
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)

            # //////////////////////////////////SUMA - STRING//////////////////////////////////////////////////////////
            # String + Int
            elif self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.CADENA
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + str(self.obtenerVal(self.OperacionDer.tipo, der))
            # String + Double
            elif self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.CADENA
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + str(self.obtenerVal(self.OperacionDer.tipo, der))
            # String + Boolean
            elif self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.BOOLEANO:
                self.tipo = TIPO.CADENA
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + str(self.obtenerVal(self.OperacionDer.tipo, der))
            # String + Char
            elif self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.CARACTER:
                self.tipo = TIPO.CADENA
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            # String + String
            elif self.OperacionIzq.tipo == TIPO.CADENA and self.OperacionDer.tipo == TIPO.CADENA:
                self.tipo = TIPO.CADENA
                return self.obtenerVal(self.OperacionIzq.tipo, izq) + self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", ">Tipo Erroneo de operacion para +.<", self.fila, self.columna)

        # ------------------------------------------- RESTA ------------------------------------------------------------
        elif self.operador == OperadorAritmetico.MENOS:  # RESTA
            # /////////////////////////////////////// RESTA - INT //////////////////////////////////////////////////////
            # Int - Int
            if self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) - self.obtenerVal(self.OperacionDer.tipo, der)
            # Int - Double
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) - self.obtenerVal(self.OperacionDer.tipo, der)
            # Int - Boolean
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.BOOLEANO:
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) - self.obtenerVal(self.OperacionDer.tipo, der)

            # //////////////////////////////////// RESTA - DOUBLE //////////////////////////////////////////////////////
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                           self.OperacionDer.tipo == TIPO.DECIMAL or
                                                           self.OperacionDer.tipo == TIPO.BOOLEANO):
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) - self.obtenerVal(self.OperacionDer.tipo, der)

            # //////////////////////////////////// RESTA - BOOLEAN//////////////////////////////////////////////////////
            # Boolean - Int
            elif self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) - self.obtenerVal(self.OperacionDer.tipo, der)
            # Boolean - Double
            elif self.OperacionIzq.tipo == TIPO.BOOLEANO and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) - self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", ">Tipo Erroneo de operacion para -.<", self.fila, self.columna)

        # ------------------------------------------- MULTIPLICACION ---------------------------------------------------
        elif self.operador == OperadorAritmetico.POR:
            # //////////////////////////////////// MULTIPLICAR - INT ///////////////////////////////////////////////////
            # Int * Int
            if self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                return self.obtenerVal(self.OperacionIzq.tipo, izq) * self.obtenerVal(self.OperacionDer.tipo, der)
            # Int * Double
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) * self.obtenerVal(self.OperacionDer.tipo, der)

            # //////////////////////////////////// MULTIPLICAR - DOUBLE ////////////////////////////////////////////////
            # Double * Double
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                           self.OperacionDer.tipo == TIPO.DECIMAL):
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) * self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", ">Tipo Erroneo de operacion para *.<", self.fila, self.columna)

        # ------------------------------------------- DIVISION ---------------------------------------------------
        elif self.operador == OperadorAritmetico.DIV:
            # //////////////////////////////////// DIVISION - INT ///////////////////////////////////////////////////
            # Int * Int e Int * Double
            if self.OperacionIzq.tipo == TIPO.ENTERO and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                          self.OperacionDer.tipo == TIPO.DECIMAL):
                if self.obtenerVal(self.OperacionDer.tipo, der) == 0:
                    return Excepcion("Semantico", ">Operacion Invalida. No se permite division entre 0.<", self.fila, self.columna)
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) / self.obtenerVal(self.OperacionDer.tipo, der)
            # //////////////////////////////////// DIVISON - DOUBLE ////////////////////////////////////////////////
            # Double * Double y Double * Int
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                           self.OperacionDer.tipo == TIPO.DECIMAL):

                if self.obtenerVal(self.OperacionDer.tipo, der) == 0:
                    return Excepcion("Semantico", ">Operacion Invalida. No se permite division entre 0.<", self.fila, self.columna)
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) / self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", ">Tipo Erroneo de operacion para division /.<", self.fila, self.columna)

        # ------------------------------------------- POTENCIA ---------------------------------------------------
        elif self.operador == OperadorAritmetico.POT:
            # //////////////////////////////////// POTENCIA - INT ///////////////////////////////////////////////////
            # Int ** Int
            if self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                base = self.obtenerVal(self.OperacionIzq.tipo, izq)
                exponente = self.obtenerVal(self.OperacionDer.tipo, der)
                return pow(base, exponente)
            # Int ** Double
            elif self.OperacionIzq.tipo == TIPO.ENTERO and self.OperacionDer.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                base = self.obtenerVal(self.OperacionIzq.tipo, izq)
                exponente = self.obtenerVal(self.OperacionDer.tipo, der)
                return pow(base, exponente)
            # //////////////////////////////////// POTENCIA - DOUBLE ////////////////////////////////////////////////
            # Double * Double y Double * Int
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                           self.OperacionDer.tipo == TIPO.DECIMAL):
                self.tipo = TIPO.DECIMAL
                base = self.obtenerVal(self.OperacionIzq.tipo, izq)
                exponente = self.obtenerVal(self.OperacionDer.tipo, der)
                return pow(base, exponente)
            return Excepcion("Semantico", ">Tipo Erroneo de operacion para potencia, **.<", self.fila, self.columna)

        # ------------------------------------------- MODULO ----------------------------------------------------------
        elif self.operador == OperadorAritmetico.MOD:
            # //////////////////////////////////// MODULO - INT ///////////////////////////////////////////////////
            # Int % Int e Int % Double
            if self.OperacionIzq.tipo == TIPO.ENTERO and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                          self.OperacionDer.tipo == TIPO.DECIMAL):
                if self.obtenerVal(self.OperacionDer.tipo, der) == 0:
                    return Excepcion("Semantico", ">Operacion Invalida. No se permite modulo % entre 0.<", self.fila,
                                     self.columna)

                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) % self.obtenerVal(self.OperacionDer.tipo, der)

            # //////////////////////////////////// MODULO - DOUBLE ///////////////////////////////////////////////////
            # Double % Int y Double % Double
            elif self.OperacionIzq.tipo == TIPO.DECIMAL and (self.OperacionDer.tipo == TIPO.ENTERO or
                                                          self.OperacionDer.tipo == TIPO.DECIMAL):
                if self.obtenerVal(self.OperacionDer.tipo, der) == 0:
                    return Excepcion("Semantico", ">Operacion Invalida. No se permite modulo % entre 0.<", self.fila,
                                     self.columna)
                self.tipo = TIPO.DECIMAL
                return self.obtenerVal(self.OperacionIzq.tipo, izq) % self.obtenerVal(self.OperacionDer.tipo, der)
            return Excepcion("Semantico", ">Tipo Erroneo de operacion para %.<", self.fila, self.columna)

        # ------------------------------------------- NEGACION UNARIA -------------------------------------------------
        elif self.operador == OperadorAritmetico.UMENOS:  # NEGACION UNARIA
            if self.OperacionIzq.tipo == TIPO.ENTERO:
                self.tipo = TIPO.ENTERO
                return - self.obtenerVal(self.OperacionIzq.tipo, izq)
            elif self.OperacionIzq.tipo == TIPO.DECIMAL:
                self.tipo = TIPO.DECIMAL
                return - self.obtenerVal(self.OperacionIzq.tipo, izq)
            return Excepcion("Semantico", ">Tipo Erroneo de operacion para - unario.<", self.fila, self.columna)
        return Excepcion("Semantico", ">Invalido, Tipo de Operacion no Especificado.<", self.fila, self.columna)

    def obtenerVal(self, tipo, val):
        if tipo == TIPO.ENTERO:
            return int(val)
        elif tipo == TIPO.DECIMAL:
            return float(val)
        elif tipo == TIPO.BOOLEANO:
            return bool(val)
        # elif tipo == TIPO.CARACTER or tipo == TIPO.CADENA:
        #     return str(val)
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

    def obtenerTipoAritmetico(self, tipo):
        if tipo == OperadorAritmetico.MAS:
            return "+"
        elif tipo == OperadorAritmetico.MENOS:
            return "-"
        elif tipo == OperadorAritmetico.POR:
            return "*"
        elif tipo == OperadorAritmetico.DIV:
            return "/"
        elif tipo == OperadorAritmetico.POT:
            return "**"
        elif tipo == OperadorAritmetico.MOD:
            return "%"
        elif tipo == OperadorAritmetico.UMENOS:
            return "-"
        elif tipo == OperadorAritmetico.MASMAS:
            return "++"
        elif tipo == OperadorAritmetico.MENOSMENOS:
            return "--"

    def getNodo(self):
        nodo = NodoArbol("ARITMETICA")
        # Si no es unaria (Solo viene operador izquierdo como -numero)
        if self.OperacionDer is not None:
            nodo.addHijoNodo(self.OperacionIzq.getNodo())
            nodo.addHijoValor(str(self.obtenerTipoAritmetico(self.operador)))
            nodo.addHijoNodo(self.OperacionDer.getNodo())
        else:
            nodo.addHijoValor(str(self.obtenerTipoAritmetico(self.operador)))
            nodo.addHijoNodo(self.OperacionIzq.getNodo())
        return nodo
