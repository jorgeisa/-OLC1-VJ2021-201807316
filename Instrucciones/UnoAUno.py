from Abstract.Instruccion import Instruccion
from Abstract.NodoArbol import NodoArbol
from Tabla_Simbolo.Excepcion import Excepcion
from Tabla_Simbolo.Tipo import TIPO, OperadorAritmetico
from Expresiones.Identificador import Identificador
from Tabla_Simbolo.Simbolo import Simbolo


class UnoAUno(Instruccion):
    def __init__(self, identificador, operador, fila, columna):
        self.identificador = identificador
        self.operador = operador
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        # Retorna None si no encontro el simbolo en la tabla
        simbolo = table.getTabla(self.identificador.lower())

        # verificando que no sea None (Encontrar el id en la tabla)
        if simbolo is None:
            return Excepcion("Semantico", ">Variable " + self.identificador + " no encontrada.<", self.fila, self.columna)

        if self.operador == OperadorAritmetico.MASMAS:
            if simbolo.getTipo() == TIPO.ENTERO or simbolo.getTipo() == TIPO.DECIMAL:
                # Obteniendo el valor
                valor = simbolo.getValor()
                valor = valor + 1
                simbolo.setValor(valor)
                result = table.actualizarTabla(simbolo)
                if isinstance(result, Excepcion): return result
                return None
            return Excepcion("Semantico", ">Tipo Erroneo de operacion para Incremento ++.<", self.fila, self.columna)
        elif self.operador == OperadorAritmetico.MENOSMENOS:
            if simbolo.getTipo() == TIPO.ENTERO or simbolo.getTipo() == TIPO.DECIMAL:
                # Obteniendo el valor
                valor = simbolo.getValor()
                valor = valor - 1
                simbolo.setValor(valor)
                result = table.actualizarTabla(simbolo)
                if isinstance(result, Excepcion): return result
                return None
            return Excepcion("Semantico", ">Tipo Erroneo de operacion para Decremento --.<", self.fila, self.columna)
        return Excepcion("Semantico", ">Tipo de Operacion no Especificado para Inc/Dec.<", self.fila, self.columna)

    def obtenerTipoArtmetico(self, tipo):
        if tipo == OperadorAritmetico.MASMAS:
            return "++"
        elif tipo == OperadorAritmetico.MENOSMENOS:
            return "--"
        return "None"

    def getNodo(self):

        if self.operador == OperadorAritmetico.MENOSMENOS:
            nodo = NodoArbol("DECREMENTO")
        else:
            nodo = NodoArbol("INCREMENTO")

        nodo.addHijoValor(str(self.identificador))
        nodo.addHijoValor(str(self.obtenerTipoArtmetico(self.operador)))

        return nodo
