from Abstract.Instruccion import Instruccion
from Abstract.NodoArbol import NodoArbol
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue
from Instrucciones.Return import Return
from Tabla_Simbolo.Excepcion import Excepcion
from Tabla_Simbolo.TablaSimbolos import TablaSimbolos

class Main(Instruccion):
    def __init__(self, instrucciones, fila, columna):
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        tabla_nueva = TablaSimbolos(table)
        for instruccionMain in self.instrucciones:
            value = instruccionMain.interpretar(tree, tabla_nueva)
            if isinstance(value, Excepcion):
                tree.getExcepciones().append(value)
                tree.updateConsola(value.toString())
            if isinstance(value, Break):
                no_break = Excepcion("Semantico", "> Excepcion MAIN: Sentencia break fuera de ciclo <", self.fila, self.columna)
                tree.getExcepciones().append(no_break)
                tree.updateConsola(no_break.toString())
            if isinstance(value, Return):
                no_break = Excepcion("Semantico", "> Excepcion MAIN: Sentencia return fuera de ciclo <", self.fila, self.columna)
                tree.getExcepciones().append(no_break)
                tree.updateConsola(no_break.toString())
            if isinstance(value, Continue):
                no_break = Excepcion("Semantico", "> Excepcion MAIN: Sentencia continue fuera de ciclo <", self.fila, self.columna)
                tree.getExcepciones().append(no_break)
                tree.updateConsola(no_break.toString())

    def getNodo(self):
        nodo = NodoArbol("MAIN")
        nodo.addHijoValor("(")
        nodo.addHijoValor(")")
        nodo.addHijoValor("{")
        nodo_instrucciones = NodoArbol("INSTRUCCIONES")
        for instruccion in self.instrucciones:
            nodo_instrucciones.addHijoNodo(instruccion.getNodo())
        nodo.addHijoNodo(nodo_instrucciones)
        nodo.addHijoValor("}")
        return nodo
