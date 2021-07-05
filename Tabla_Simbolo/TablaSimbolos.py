from Tabla_Simbolo.Excepcion import Excepcion
from Tabla_Simbolo.Tipo import TIPO


class TablaSimbolos:
    def __init__(self, anterior=None):
        self.tabla = {}
        self.anterior = anterior
        self.funciones = []

    def setTabla(self, simbolo):
        if simbolo.id.lower() in self.tabla:
            return Excepcion("Semantico", "Variable " + simbolo.id + " ya existe", simbolo.fila, simbolo.columna)
        else:
            self.tabla[simbolo.id.lower()] = simbolo
            return None

    def getTabla(self, id):  # obtener una variable
        tablaActual = self
        while tablaActual.tabla is not None:
            if id.lower() in tablaActual.tabla:
                return tablaActual.tabla[id.lower()]  # RETORNA SIMBOLO
            else:
                tablaActual = tablaActual.anterior
                if tablaActual is None: return None
        return None

    def actualizarTabla(self, simbolo):
        tablaActual = self
        while tablaActual is not None:
            if simbolo.id.lower() in tablaActual.tabla:
                if (tablaActual.tabla[simbolo.id.lower()].getTipo() is TIPO.NULO) or \
                        (tablaActual.tabla[simbolo.id.lower()].getTipo() == simbolo.getTipo()) or \
                        (simbolo.getTipo() is TIPO.NULO):

                    tablaActual.tabla[simbolo.id.lower()].setValor(simbolo.getValor())
                    tablaActual.tabla[simbolo.id.lower()].setTipo(simbolo.getTipo())
                    return None  # VARIABLE ACTUALIZADA
                return Excepcion("Semantico", ">Tipo de dato no valido para Asignacion.<", simbolo.getFila(),
                                 simbolo.getColumna())
            else:
                tablaActual = tablaActual.anterior
                if tablaActual is None: return Excepcion("Semantico", ">Variable No encontrada en Asignacion<", simbolo.getFila(), simbolo.getColumna())
        return Excepcion("Semantico", ">Variable No encontrada en Asignacion<", simbolo.getFila(), simbolo.getColumna())
