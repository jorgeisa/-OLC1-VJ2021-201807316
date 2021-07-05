from Abstract.Instruccion import Instruccion
from Abstract.NodoArbol import NodoArbol
from Instrucciones.Break import Break
from Instrucciones.Continue import Continue
from Instrucciones.Return import Return
from Tabla_Simbolo.Excepcion import Excepcion
from Tabla_Simbolo.Tipo import OperadorRelacional
from Expresiones.Relacional import Relacional
from Tabla_Simbolo.TablaSimbolos import TablaSimbolos


class Switch(Instruccion):
    def __init__(self, expresion, switch_lista_case, switch_default, fila, columna):
        self.expresion = expresion
        self.switch_lista_case = switch_lista_case
        self.switch_default = switch_default
        self.fila = fila
        self.columna = columna

    def interpretar(self, tree, table):
        value = self.expresion.interpretar(tree, table)
        if isinstance(value, Excepcion): return value

        if self.switch_lista_case is not None:
            for instruccion_case in self.switch_lista_case:
                result = instruccion_case.interpretar(tree, table)  # Nos va a retornar el valor de la clase CASE
                if isinstance(result, Excepcion):
                    tree.getExcepciones().append(result)
                    tree.updateConsola(result.toString())

                # Realizando una operacion con la clase relacional
                # Realizando la operacion entre expresion de Switch y Case
                op_relacional = Relacional(OperadorRelacional.IGUALIGUAL, self.expresion, instruccion_case.getExpresion(), self.fila, self.columna)

                # SW  instruccion - primitivo interpretar = 10
                #     CS  True
                #     CS  5
                # Interpretando ambas expresiones, retorna True
                op_valor = op_relacional.interpretar(tree, table)  # IF ==

                # Verificando si no hay error
                if isinstance(op_valor, Excepcion): return op_valor

                if op_valor:
                    nuevaTabla = TablaSimbolos(table) # Nuevo ambito de cada case
                    for instruccion_caseIn in instruccion_case.getInstrucciones():
                        result_caseIns = instruccion_caseIn.interpretar(tree, nuevaTabla)
                        if isinstance(result_caseIns, Excepcion):
                            tree.getExcepciones().append(result_caseIns)
                            tree.updateConsola(result_caseIns.toString())
                        # si encuentra break
                        if isinstance(result_caseIns, Break): return None # NONE
                        if isinstance(result_caseIns, Return): return result_caseIns
                        if isinstance(result_caseIns, Continue): return result_caseIns

        if self.switch_default is not None:
            nuevaTabla = TablaSimbolos(table)
            for instruccion_caseIns in self.switch_default.getInstrucciones():
                result_caseIns = instruccion_caseIns.interpretar(tree, nuevaTabla)
                if isinstance(result_caseIns, Excepcion):
                    tree.getExcepciones().append(result_caseIns)
                    tree.updateConsola(result_caseIns.toString())
                # si encuentra break
                if isinstance(result_caseIns, Break): return None
                if isinstance(result_caseIns, Return): return result_caseIns
                if isinstance(result_caseIns, Continue): return result_caseIns

    def getNodo(self):
        nodo = NodoArbol("SWITCH")
        nodo.addHijoValor("(")
        nodo.addHijoNodo(self.expresion.getNodo())
        nodo.addHijoValor(")")
        if self.switch_lista_case is not None:
            nodo_lista_case = NodoArbol("LISTA CASE")

            for case in self.switch_lista_case:
                nodo_lista_case.addHijoNodo(case.getNodo())
            nodo.addHijoNodo(nodo_lista_case)

        if self.switch_default is not None:
            nodo.addHijoNodo(self.switch_default.getNodo())
        return nodo
