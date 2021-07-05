from Abstract.Instruccion import Instruccion
from Abstract.NodoArbol import NodoArbol
from Instrucciones.Continue import Continue
from Instrucciones.Return import Return
from Tabla_Simbolo.Excepcion import Excepcion
from Tabla_Simbolo.Tipo import TIPO
from Tabla_Simbolo.TablaSimbolos import TablaSimbolos
from Instrucciones.Break import Break
from Instrucciones.Declaracion import Declaracion
from Instrucciones.Asignacion import Asignacion


class For(Instruccion):
    def __init__(self, declara_asigna, expresion, uno_un_uno, instrucciones, fila, columna):
        self.declara_asigna = declara_asigna
        self.expresion = expresion
        self.uno_en_uno = uno_un_uno
        self.instrucciones = instrucciones
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):

        # Si es una declaracion
        if isinstance(self.declara_asigna, Declaracion):
            tabla_sim = TablaSimbolos(table)

        elif isinstance(self.declara_asigna, Asignacion):
            tabla_sim = table
        else:
            return Excepcion("Semantico", "Expresion no es Declaracion o Asignacion FOR", self.fila, self.columna)

        # Realizando la operacion
        valor_asig_decl = self.declara_asigna.interpretar(tree, tabla_sim)
        if isinstance(valor_asig_decl, Excepcion): return valor_asig_decl

        while True:
            valor_condicion = self.expresion.interpretar(tree, tabla_sim)
            if isinstance(valor_condicion, Excepcion): return valor_condicion

            if self.expresion.tipo == TIPO.BOOLEANO:
                if bool(valor_condicion) is True:  # VERIFICA SI ES VERDADERA LA CONDICION

                    tabla_sim = TablaSimbolos(tabla_sim)

                    for instruccion in self.instrucciones:
                        result = instruccion.interpretar(tree, tabla_sim)  # EJECUTA INSTRUCCION ADENTRO DEL IF
                        if isinstance(result, Excepcion):
                            tree.getExcepciones().append(result)
                            tree.updateConsola(result.toString())
                        if isinstance(result, Break): return None
                        if isinstance(result, Return): return result
                        if isinstance(result, Continue): break
                    valor_unoauno = self.uno_en_uno.interpretar(tree, tabla_sim)
                    if isinstance(valor_unoauno, Excepcion): return valor_unoauno
                else:
                    break
            else:
                return Excepcion("Semantico", ">Tipo de dato no booleano en WHILE.<", self.fila, self.columna)

    def getNodo(self):
        nodo = NodoArbol("FOR")
        nodo.addHijoValor("(")
        nodo.addHijoNodo(self.declara_asigna.getNodo())
        nodo.addHijoNodo(self.expresion.getNodo())
        nodo.addHijoNodo(self.uno_en_uno.getNodo())
        nodo.addHijoValor(")")

        nodo_instrucciones = NodoArbol("INSTRUCCIONES FOR")

        for instruccion in self.instrucciones:
            nodo_instrucciones.addHijoNodo(instruccion.getNodo())
        nodo.addHijoNodo(nodo_instrucciones)
        return nodo
