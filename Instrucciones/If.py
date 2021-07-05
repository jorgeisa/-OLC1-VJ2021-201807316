from Abstract.Instruccion import Instruccion
from Abstract.NodoArbol import NodoArbol
from Instrucciones.Break import Break
from Instrucciones.Return import Return
from Instrucciones.Continue import Continue
from Tabla_Simbolo.Excepcion import Excepcion
from Tabla_Simbolo.Tipo import TIPO
from Tabla_Simbolo.TablaSimbolos import TablaSimbolos

class If(Instruccion):
    def __init__(self, condicion, instruccionesIf, instruccionesElse, elseif, fila, columna):
        self.condicion = condicion
        self.instruccionesIf = instruccionesIf
        self.instruccionesElse = instruccionesElse
        self.elseIf = elseif
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        condicion = self.condicion.interpretar(tree, table)
        if isinstance(condicion, Excepcion): return condicion

        if self.condicion.tipo == TIPO.BOOLEANO:
            if bool(condicion) is True:   # VERIFICA SI ES VERDADERA LA CONDICION
                nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO
                for instruccion in self.instruccionesIf:
                    result = instruccion.interpretar(tree, nuevaTabla)  # EJECUTA INSTRUCCION ADENTRO DEL IF
                    if isinstance(result, Excepcion) :
                        tree.getExcepciones().append(result)
                        tree.updateConsola(result.toString())
                    if isinstance(result, Break): return result
                    if isinstance(result, Return): return result
                    if isinstance(result, Continue): return result
            else:               #ELSE
                if self.instruccionesElse is not None:
                    nuevaTabla = TablaSimbolos(table)       #NUEVO ENTORNO
                    for instruccion in self.instruccionesElse:
                        result = instruccion.interpretar(tree, nuevaTabla) #EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Excepcion) :
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        if isinstance(result, Break): return result
                        if isinstance(result, Return): return result
                        if isinstance(result, Continue): return result

                elif self.elseIf is not None:
                    result = self.elseIf.interpretar(tree, table)
                    if isinstance(result, Excepcion): return result
                    if isinstance(result, Break): return result
                    if isinstance(result, Return): return result
                    if isinstance(result, Continue): return result
        else:
            return Excepcion("Semantico", ">Tipo de dato no booleano en IF.<", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoArbol("IF")
        nodo.addHijoValor("(")
        nodo.addHijoNodo(self.condicion.getNodo())
        nodo.addHijoValor(")")
        if self.instruccionesIf is not None:
            nodo_instrucciones_if = NodoArbol("INSTRUCCIONES IF")
            for instruccion in self.instruccionesIf:
                nodo_instrucciones_if.addHijoNodo(instruccion.getNodo())
            nodo.addHijoNodo(nodo_instrucciones_if)

        if self.instruccionesElse is not None:
            nodo_instrucciones_else = NodoArbol("INSTRUCCIONES ELSE")
            for instruccionElse in self.instruccionesElse:
                nodo_instrucciones_else.addHijoNodo(instruccionElse.getNodo())
            nodo.addHijoNodo(nodo_instrucciones_else)

        elif self.elseIf is not None:
            nodo_else = NodoArbol("ELSE")
            nodo_else.addHijoNodo(self.elseIf.getNodo())
            nodo.addHijoNodo(nodo_else)
            # nodo.addHijoNodo(self.elseIf.getNodo())
        return nodo
