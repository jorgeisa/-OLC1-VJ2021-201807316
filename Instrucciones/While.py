from Abstract.Instruccion import Instruccion
from Abstract.NodoArbol import NodoArbol
from Instrucciones.Return import Return
from Instrucciones.Continue import Continue
from Tabla_Simbolo.Excepcion import Excepcion
from Tabla_Simbolo.Tipo import TIPO
from Tabla_Simbolo.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break


class While(Instruccion):
    # while (condicion ) {
    # NUEVO AMBITO
    # }
    def __init__(self, condicion, instrucciones, fila, columna):
        self.condicion = condicion
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        while True:
            condicion = self.condicion.interpretar(tree, table)
            if isinstance(condicion, Excepcion): return condicion

            if self.condicion.tipo == TIPO.BOOLEANO:
                if bool(condicion) is True:   # VERIFICA SI ES VERDADERA LA CONDICION
                    nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO
                    for instruccion in self.instrucciones:
                        result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Excepcion) :
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        if isinstance(result, Break): return None
                        if isinstance(result, Return): return result
                        if isinstance(result, Continue): break
                else:
                    break
            else:
                return Excepcion(">Semantico", "Tipo de dato no booleano en IF.<", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoArbol("WHILE")
        nodo.addHijoValor("(")
        nodo.addHijoNodo(self.condicion.getNodo())
        nodo.addHijoValor(")")
        nodo_instrucciones = NodoArbol("INSTRUCCIONES WHILE")
        for instruccion in self.instrucciones:
            nodo_instrucciones.addHijoNodo(instruccion.getNodo())
        nodo.addHijoNodo(nodo_instrucciones)
        return nodo
