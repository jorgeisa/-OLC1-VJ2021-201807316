"""
Isaac Xicol
JPR Analyzer
"""
import os.path
import sys

from Abstract.NodoArbol import NodoArbol

errors = []
console = ""

reserved = {
    'var':      'RVAR',
    'new':      'RNEW',
    'print':    'RPRINT',

    # Tipos de datos primitivos
    'false':    'RFALSE',
    'true':     'RTRUE',
    'null':     'RNULL',

    'int':      'RINT',
    'double':   'RDOUBLE',
    'boolean':  'RBOOLEAN',
    'char':     'RCHAR',
    'string':   'RSTRING',

    'if':       'RIF',
    'else':     'RELSE',
    'switch':   'RSWITCH',
    'case':     'RCASE',
    'default':  'RDEFAULT',

    'while':    'RWHILE',
    'for':      'RFOR',
    'break':    'RBREAK',
    'continue': 'RCONTINUE',
    'return':   'RRETURN',

    'func':     'RFUNC',

    'read':     'RREAD',
    'main':     'RMAIN',
}

tokens = [
    # Comentarios
    'COMMENTUNLINE',    # Comentario Unilinea
    'COMMENTLINES',     # Comentario multilinea

    # Caracteres Especiales
    'TWOPOINTS',        # Dos Puntos

    # Operadores Aritmeticos
    'PLUSSIGN',         # Signo Mas
    'SUBTRACTIONSIGN',  # Signo Menos
    'MULTIPLICATIONSIGN',  # Signo Multiplicacion
    'DIVISIONSIGN',     # Signo Division
    'POWERSIGN',        # Signo de potencia
    'MODULESIGN',       # Signo Modulo

    # Operadores Relacionales
    'EQUALIZATIONSIGN',  # Signo de Igualacion
    'DIFFERENTIATIONSIGN',  # Signo de diferenciacion
    'SMALLERTHAN',      # Signo de Menor que
    'GREATERTHAN',      # Signo de Mayor que
    'LESSEQUAL',        # Signo de Menor Igual
    'GREATEREQUAL',     # Signo de Mayor Igual

    # Operadores Logicos
    'OR',               # Operador OR
    'AND',              # Operador AND
    'NOT',              # Operador NOT

    # Signos de Agrupacion
    'PARENTHESISOPEN',   # Parentesis Abre
    'PARENTHESISCLOSE',  # Parentesis Cierra
    'COMA',

    # Caracteres de Finalizacion y Encapsulamiento de Sentencias
    'SEMICOLON',        # Punto y Coma para la finalizacion (Puede o no venir)
    'KEYSIGNOPEN',      # Llave que Abre
    'KEYSIGNCLOSE',     # Llave que cierra

    # Declaracion y asignacion de Variables
    'EQUALSYMBOL',      # Simbolo Igual

    # Incremento y Decremento
    'INCREMENT',        # Incremento
    'DECREMENT',        # Decremnto

    # Arreglos
    'CLASPSYMBOLOPEN',   # Corchete abre
    'CLASPSYMBOLCLOSE',  # Corchete cierra

    # Extras
    # Tipos de datos primitivos
    'ENTERO',            # Numero Entero
    'DECIMAL',          # Numero Decimal
    'CARACTER',             # caracter
    'CADENA',           # Cadena
    'ID',               # Identificador (variables, nombres funciones, etc)


] + list(reserved.values())

# Tokens
# Caracteres Especiales
t_TWOPOINTS = r':'

# Operadores Aritmeticos
t_PLUSSIGN = r'\+'
t_SUBTRACTIONSIGN = r'\-'
t_POWERSIGN = r'\*\*'
t_MULTIPLICATIONSIGN = r'\*'
t_DIVISIONSIGN = r'/'
t_MODULESIGN = r'\%'

# Operadores Relacionales
t_EQUALIZATIONSIGN = r'=='
t_DIFFERENTIATIONSIGN = r'=!'
t_SMALLERTHAN = r'<'
t_GREATERTHAN = r'>'
t_LESSEQUAL = r'<='
t_GREATEREQUAL = r'>='

# Operadores Logicos
t_OR = r'\|\|'
t_AND = r'&&'
t_NOT = r'!'

# Signos de Agrupacion
t_PARENTHESISOPEN = r'\('
t_PARENTHESISCLOSE = r'\)'
t_COMA = ','

# Caracteres de Finalizacion y Encapsulamiento de Sentencias
t_SEMICOLON = r';'
t_KEYSIGNOPEN = r'\{'
t_KEYSIGNCLOSE = r'\}'

# Declaracion y asignacion de Variables
t_EQUALSYMBOL = '='

# Incremento y Decremento
t_INCREMENT = r'\+\+'
t_DECREMENT = r'\-\-'

# Arreglos
t_CLASPSYMBOLOPEN = r'\['
t_CLASPSYMBOLCLOSE = r'\]'


def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float Value too large %d", t.value)
        t.value = 0
    return t


def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value.lower(), 'ID')  # revisar en la lista de reservadas
    return t


def t_CADENA(t):
    # r'\"(\\"|.)*?\"'
    r"""\"(\\"|\\'|\\\\|\\n|\\t|\\r|[^\\\'\"])*?\""""
    t.value = t.value[1:-1]  # remover comillas
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\r', '\r')
    t.value = t.value.replace('\\\\', '\\')
    t.value = t.value.replace('\\"', '\"')
    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace("\\'", '\'')
    # if '\\n' in t.value:
    #     t.value = t.value.replace('\\n', '\n')
    # if '\\r' in t.value:
    #     t.value = t.value.replace('\\r', '\r')
    # if '\\\\' in t.value:
    #      t.value = t.value.replace('\\\\', '\\')
    # if '\\"' in t.value:
    #     t.value = t.value.replace('\\"', '\"')
    # if '\\t' in t.value:
    #     t.value = t.value.replace('\\t', '\t')
    # if "\\'" in t.value:
    #     t.value = t.value.replace("\\'", '\'')
    return t


def t_CARACTER(t):
    r""" \'(\\'|\\\\|\\n|\\t|\\r|\\"|.)?\'"""
    t.value = t.value[1:-1]  # remover comillas
    t.value = t.value.replace('\\n', '\n')
    t.value = t.value.replace('\\r', '\r')
    t.value = t.value.replace('\\\\', '\\')
    t.value = t.value.replace('\\"', '\"')
    t.value = t.value.replace('\\t', '\t')
    t.value = t.value.replace("\\'", '\'')
    return t


# Comentario multilineas
def t_COMMENTLINES(t):
    r'\#\*(.|\n)*?\*\#'
    t.lexer.lineno += t.value.count('\n')
    # print('Token multilinea')


# Comentario unilinea
def t_COMMENTUNLINE(t):
    r'\#.*\n'
    t.lexer.lineno += 1
    # print('Token unilinea')


# Caracters ignorados
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Ilegal character '%s'" % t.value[0])
    errors.append(Excepcion("lexico", "Caracter " + t.value[0] + " no pertenece al lenguaje. !!", t.lexer.lineno, find_column(input, t)))
    t.lexer.skip(1)


def find_column(inp, token):
    line_start = inp.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


# Construyendo el analizador lexico
import ply.lex as lex
lexer = lex.lex()

# Asociación de operadores y precedencia
precedence = (
    ('left', 'OR'),  # ||
    ('left', 'AND'),  # &&
    ('right', 'UNOT'),  # !
    ('left', 'EQUALIZATIONSIGN','DIFFERENTIATIONSIGN', 'SMALLERTHAN', 'LESSEQUAL', 'GREATERTHAN', 'GREATEREQUAL'),  # ==, =!, <, <=, >, >=
    ('left', 'PLUSSIGN','SUBTRACTIONSIGN'),  # +  -
    ('left', 'MULTIPLICATIONSIGN', 'DIVISIONSIGN', 'MODULESIGN'),  # /  *  %
    ('left', 'POWERSIGN'),  # **
    ('right', 'UMENOS'),  # -
    ('left', 'INCREMENT', 'DECREMENT'), # ++ --
    )


# --------------------------------------------- DEFINICION DE LA GRAMATICA --------------------------------------------

from Tabla_Simbolo.Tipo import OperadorAritmetico, OperadorRelacional, OperadorLogico, TIPO
from Tabla_Simbolo.Excepcion import Excepcion

from Instrucciones.Imprimir import Imprimir
from Instrucciones.Declaracion import Declaracion
from Instrucciones.Asignacion import Asignacion
from Instrucciones.UnoAUno import UnoAUno
from Instrucciones.If import If
from Instrucciones.While import While
from Instrucciones.Case import Case
from Instrucciones.Switch import Switch
from Instrucciones.For import For
from Instrucciones.Break import Break
from Instrucciones.Main import Main
from Instrucciones.Funcion import Funcion
from Instrucciones.LlamadaFuncion import LlamadaFuncion
from Instrucciones.Return import Return
from Instrucciones.Continue import Continue
from Instrucciones.DeclaracionArreglo import DeclaracionArreglo
from Instrucciones.ModificacionArreglo import ModificarArreglo

from Expresiones.Aritmetica import Aritmetica
from Expresiones.Identificador import Identificador
from Expresiones.Primitivos import Primitivos
from Expresiones.Relacional import Relacional
from Expresiones.Logica import Logica
from Expresiones.Casteo import Casteo
from Expresiones.Read import Read
from Expresiones.AccesoArreglo import AccesoArreglo

from Nativas.ToUpper import ToUpper
from Nativas.ToLower import ToLower
from Nativas.Round import Round
from Nativas.Truncate import Truncate
from Nativas.Length import Length
from Nativas.Typeof import Typeof


#  ------------------------------- PRODUCCION INICIAL ----------------------------------
def p_init(t):
    'init            : instrucciones'
    t[0] = t[1]


def p_instrucciones_instrucciones_instruccion(t):
    'instrucciones    : instrucciones instruccion'
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]


# ------------------------------------------ INSTRUCCIONES ----------------------------------------------

def p_instrucciones_instruccion(t):
    'instrucciones    : instruccion'
    if t[1] == "":
        t[0] = []
    else:
        t[0] = [t[1]]


# ------------------------------------------ INSTRUCCION ------------------------------------------
# instruccion(expresion) print(primitvo)
# var id = expresion                                ID, primitivo,

def p_instruccion(t):
    '''instruccion      : imprimir_instr finins
                        | declarar_instr finins
                        | asignar_instr finins
                        | unoenuno_instr finins
                        | if_instr
                        | while_instr
                        | switch_instr
                        | for_instr
                        | break_instr finins
                        | main_instr
                        | function_instr
                        | llamada_function finins
                        | return_instr finins
                        | continue_instr finins
                        | arreglo_declarar finins
                        | modificar_arreglo finins
    '''

    t[0] = t[1]


#  Produccion para poder finalizar instruccion con punto y coma
def p_finins(t):
    '''finins           : SEMICOLON
                        | '''
    t[0] = None


def p_instruccion_error(t):
    'instruccion        : error SEMICOLON'
    errors.append(
        Excepcion("sintactico", "Error Sintáctico. Instruccion " + str(t[1].value), t.lineno(1), find_column(input, t.slice[1])))
    t[0] = ""

# ------------------------------------------ IMPRIMIR ------------------------------------------

def p_imprimir(t):
    'imprimir_instr     : RPRINT PARENTHESISOPEN expresion PARENTHESISCLOSE'
    t[0] = Imprimir(t[3], t.lineno(1), find_column(input, t.slice[1]))


# ------------------------------------------ DECLARACION ---------------------------------------

def p_declarar_instr(t):
    '''declarar_instr    : declarar_expresion
                         | declarar_nulo'''
    t[0] = t[1]


def p_declarar_nulo(t):
    'declarar_nulo    : RVAR ID'
    t[0] = Declaracion(t[2], t.lineno(2), find_column(input, t.slice[2]), None, TIPO.NULO)


def p_declarar_expresion(t):
    'declarar_expresion  : RVAR ID EQUALSYMBOL expresion'
    t[0] = Declaracion(t[2], t.lineno(2), find_column(input, t.slice[2]), t[4])


# ------------------------------------------ ASIGNACION ----------------------

def p_asignar_instr(t):
    '''asignar_instr    : ID EQUALSYMBOL expresion'''
    t[0] = Asignacion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))


# ------------------------------- INCREMENTO Y DECREMENTO --------------------

def p_unoenuno_instr(t):
    '''unoenuno_instr   : ID INCREMENT
                        | ID DECREMENT'''

    if t[2] == "++":
        t[0] = UnoAUno(t[1], OperadorAritmetico.MASMAS, t.lineno(1), find_column(input, t.slice[1]))
    elif t[2] == "--":
        t[0] = UnoAUno(t[1], OperadorAritmetico.MENOSMENOS, t.lineno(1), find_column(input, t.slice[1]))


# -------------------------------------- IF -----------------------------------

def p_if_simple(t):
    '''if_instr     : RIF PARENTHESISOPEN expresion PARENTHESISCLOSE KEYSIGNOPEN instrucciones KEYSIGNCLOSE'''
    t[0] = If(t[3], t[6], None, None, t.lineno(1), find_column(input, t.slice[1]))


def p_if_else(t):
    '''if_instr     : RIF PARENTHESISOPEN expresion PARENTHESISCLOSE KEYSIGNOPEN instrucciones KEYSIGNCLOSE RELSE KEYSIGNOPEN instrucciones KEYSIGNCLOSE'''
    t[0] = If(t[3], t[6], t[10], None, t.lineno(1), find_column(input, t.slice[1]))


def p_if_elseif(t):
    '''if_instr     : RIF PARENTHESISOPEN expresion PARENTHESISCLOSE KEYSIGNOPEN instrucciones KEYSIGNCLOSE RELSE if_instr'''
    t[0] = If(t[3], t[6], None, t[9], t.lineno(1), find_column(input, t.slice[1]))


# -------------------------------------- SWITCH -----------------------------------
def p_switch_instr1(t):
    '''switch_instr  : RSWITCH PARENTHESISOPEN expresion PARENTHESISCLOSE KEYSIGNOPEN switch_lista_case KEYSIGNCLOSE'''
    t[0] = Switch(t[3], t[6], None, t.lineno(1), find_column(input, t.slice[1]))


def p_switch_instr2(t):
    '''switch_instr  : RSWITCH PARENTHESISOPEN expresion PARENTHESISCLOSE KEYSIGNOPEN switch_default KEYSIGNCLOSE'''
    t[0] = Switch(t[3], None, t[6], t.lineno(1), find_column(input, t.slice[1]))


def p_switch_instr3(t):
    '''switch_instr  : RSWITCH PARENTHESISOPEN expresion PARENTHESISCLOSE KEYSIGNOPEN switch_lista_case switch_default KEYSIGNCLOSE'''
    t[0] = Switch(t[3], t[6], t[7], t.lineno(1), find_column(input, t.slice[1]))


def p_switch_lista_case(t):
    '''switch_lista_case    : switch_lista_case switch_case'''
    if t[2] != "":
        t[1].append(t[2])
    t[0] = t[1]


def p_switch_lista_case2(t):
    '''switch_lista_case    : switch_case'''
    if t[1] == "":
        t[0] = []
    else:
        t[0] = [t[1]]


def p_switch_case(t):
    '''switch_case   : RCASE expresion TWOPOINTS instrucciones'''
    t[0] = Case(t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))


def p_switch_default(t):
    '''switch_default   : RDEFAULT TWOPOINTS instrucciones'''
    t[0] = Case(None, t[3], t.lineno(1), find_column(input, t.slice[1]))


# -------------------------------------- WHILE ----------------------------------
def p_while_instr(t):
    '''while_instr  : RWHILE PARENTHESISOPEN expresion PARENTHESISCLOSE KEYSIGNOPEN instrucciones KEYSIGNCLOSE'''
    t[0] = While(t[3], t[6], t.lineno(1), find_column(input, t.slice[1]))


# -------------------------------------- FOR ------------------------------------
def p_for_instr(t):
    '''for_instr    : RFOR PARENTHESISOPEN declarar_asignar_for SEMICOLON expresion SEMICOLON actualizacion_for PARENTHESISCLOSE KEYSIGNOPEN instrucciones KEYSIGNCLOSE'''
    t[0] = For(t[3], t[5], t[7], t[10], t.lineno(1), find_column(input, t.slice[1]))


def p_declarar_asignar_for(t):
    '''declarar_asignar_for     : declarar_instr
                                | asignar_instr
    '''
    t[0] = t[1]


def p_actualizacion_for(t):
    '''actualizacion_for    : unoenuno_instr
                             | asignar_instr'''
    t[0] = t[1]


# ------------------------------------- BREAK ----------------------------------------
def p_break_instr(t):
    'break_instr     : RBREAK'
    t[0] = Break(t.lineno(1), find_column(input, t.slice[1]))


# ------------------------------------- CONTINUE ----------------------------------------
def p_continue_instr(t):
    'continue_instr     : RCONTINUE'
    t[0] = Continue(t.lineno(1), find_column(input, t.slice[1]))


# ------------------------------------ MAIN ------------------------------------------
def p_main_instr(t):
    '''main_instr   : RMAIN PARENTHESISOPEN PARENTHESISCLOSE KEYSIGNOPEN instrucciones KEYSIGNCLOSE'''
    t[0] = Main(t[5], t.lineno(1), find_column(input, t.slice[1]))


# ------------------------------------ FUNCIONES --------------------------------------
# FUNCION CON PARAMETROS
def p_function_completa(t):
    '''function_instr   : RFUNC ID PARENTHESISOPEN parametros_lista PARENTHESISCLOSE KEYSIGNOPEN instrucciones KEYSIGNCLOSE
    '''
    t[0] = Funcion(t[2], t[4], t[7], t.lineno(1), find_column(input, t.slice[1]))


# FUNCION SIN PARAMETROS
def p_function_simple(t):
    '''function_instr   : RFUNC ID PARENTHESISOPEN PARENTHESISCLOSE KEYSIGNOPEN instrucciones KEYSIGNCLOSE
    '''
    t[0] = Funcion(t[2], [], t[6], t.lineno(1), find_column(input, t.slice[1]))


# LISTA DE PARAMETROS DE FUNCIONES
def p_parametros_lista_1(t):
    '''parametros_lista   :   parametros_lista COMA parametro_simple'''
    t[1].append(t[3])
    t[0] = t[1]


def p_parametros_lista_2(t):
    '''parametros_lista   :   parametro_simple'''
    t[0] = [t[1]]


# PARAMETRO SIMPLE PARA FUNCIONES (TERMINAL)
def p_parametro_simple(t):
    '''parametro_simple    :   tipo_dato ID'''
    t[0] = {'tipo': t[1], 'identificador': t[2]}


def p_parametro_simple_arreglo(t):
    '''parametro_simple    :   tipo_dato lista_dimensiones ID '''
    t[0] = {'tipo': TIPO.ARREGLO, 'identificador': t[3], 'tipo_dato': t[1], 'longitud': t[2]}


# ---------------------------------- LLAMADA DE LAS FUNCIONES ----------------------------------
# LLAMADA DE FUNCIONES SIN PARAMETROS
def p_llamada_function_simple(t):
    '''llamada_function : ID PARENTHESISOPEN PARENTHESISCLOSE'''
    t[0] = LlamadaFuncion(t[1], [], t.lineno(1), find_column(input, t.slice[1]))


# LLAMADA DE FUNCIONES CON PARAMETROS
def p_llamada_function_completa(t):
    '''llamada_function :   ID PARENTHESISOPEN parametros_llamada PARENTHESISCLOSE'''
    t[0] = LlamadaFuncion(t[1], t[3], t.lineno(1), find_column(input, t.slice[1]))


# PARAMETROS DE LLAMADAS (LISTA)
def p_parametros_llamada1(t):
    '''parametros_llamada   :   parametros_llamada COMA parametro_llamada_simple'''
    t[1].append(t[3])
    t[0] = t[1]


def p_parametros_llamada2(t):
    '''parametros_llamada   :   parametro_llamada_simple'''
    t[0] = [t[1]]


# PARAMETROS DE LLAMADA (SIMPLE)
def p_parametro_llamada_simple(t):
    '''parametro_llamada_simple :   expresion'''
    t[0] = t[1]


# ------------------------------------------ RETURN -----------------------------------------
def p_return_instr(t):
    '''return_instr :   RRETURN expresion'''
    t[0] = Return(t[2], t.lineno(1), find_column(input, t.slice[1]))


# ------------------------------------------- DECLARAR ARREGLOS ------------------------------
def p_arreglo_declarar(t):
    '''arreglo_declarar :   tipo_1'''
    t[0] = t[1]


def p_arreglo_tipo_1(t):
    '''tipo_1   :   tipo_dato lista_dimensiones ID EQUALSYMBOL RNEW tipo_dato lista_expresiones'''
    t[0] = DeclaracionArreglo(t[1], t[2], t[3], t[6], t[7], None, t.lineno(3), find_column(input, t.slice[3]))

def p_arreglo_tipo_1_2(t):
    '''tipo_1   :   tipo_dato lista_dimensiones ID EQUALSYMBOL ID'''
    t[0] = DeclaracionArreglo(t[1], t[2], t[3], None, None, t[5], t.lineno(3), find_column(input, t.slice[3]))

def p_lista_dimensiones1(t):
    '''lista_dimensiones    :   lista_dimensiones CLASPSYMBOLOPEN CLASPSYMBOLCLOSE'''
    t[0] = t[1] + 1


def p_lista_dimensiones2(t):
    '''lista_dimensiones    :   CLASPSYMBOLOPEN CLASPSYMBOLCLOSE'''
    t[0] = 1


def p_lista_expresiones1(t):
    '''lista_expresiones    :   lista_expresiones CLASPSYMBOLOPEN expresion CLASPSYMBOLCLOSE'''
    t[1].append(t[3])
    t[0] = t[1]


def p_lista_expresiones2(t):
    '''lista_expresiones    :   CLASPSYMBOLOPEN expresion CLASPSYMBOLCLOSE'''
    t[0] = [t[2]]

# ---------------------------------------- MODIFICACION ARREGLOS ----------------------------
def p_modificar_arreglo(t):
    '''modificar_arreglo    :   ID lista_expresiones EQUALSYMBOL expresion'''
    t[0] = ModificarArreglo(t[1], t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))


# ------------------------------------------ TIPO (DATOS) ------------------------------------
def p_tipo(t):
    '''tipo_dato    :   RINT
                    |   RDOUBLE
                    |   RBOOLEAN
                    |   RCHAR
                    |   RSTRING
                    '''
    if t[1].lower() == 'int':
        t[0] = TIPO.ENTERO
    elif t[1].lower() == 'double':
        t[0] = TIPO.DECIMAL
    elif t[1].lower() == 'boolean':
        t[0] = TIPO.BOOLEANO
    elif t[1].lower() == 'char':
        t[0] = TIPO.CARACTER
    elif t[1].lower() == 'string':
        t[0] = TIPO.CADENA


# ------------------------------------------ EXPRESIONES ------------------------------------------
def p_expresion_binaria(t):
    '''
    expresion : expresion PLUSSIGN expresion
            | expresion SUBTRACTIONSIGN expresion
            | expresion MULTIPLICATIONSIGN expresion
            | expresion DIVISIONSIGN expresion
            | expresion POWERSIGN expresion
            | expresion MODULESIGN expresion
            | expresion EQUALIZATIONSIGN expresion
            | expresion DIFFERENTIATIONSIGN expresion
            | expresion SMALLERTHAN expresion
            | expresion GREATERTHAN expresion
            | expresion LESSEQUAL expresion
            | expresion GREATEREQUAL expresion
            | expresion OR expresion
            | expresion AND expresion
    '''

    if t[2] == '+':
        t[0] = Aritmetica(OperadorAritmetico.MAS, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '-':
        t[0] = Aritmetica(OperadorAritmetico.MENOS, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '**':
        t[0] = Aritmetica(OperadorAritmetico.POT, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '*':
        t[0] = Aritmetica(OperadorAritmetico.POR, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '/':
        t[0] = Aritmetica(OperadorAritmetico.DIV, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '%':
        t[0] = Aritmetica(OperadorAritmetico.MOD, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))

    elif t[2] == '==':
        t[0] = Relacional(OperadorRelacional.IGUALIGUAL, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '=!':
        t[0] = Relacional(OperadorRelacional.DIFERENTE, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<':
        t[0] = Relacional(OperadorRelacional.MENORQUE, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>':
        t[0] = Relacional(OperadorRelacional.MAYORQUE, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '<=':
        t[0] = Relacional(OperadorRelacional.MENORIGUAL, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '>=':
        t[0] = Relacional(OperadorRelacional.MAYORIGUAL, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))

    elif t[2] == '&&':
        t[0] = Logica(OperadorLogico.AND, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == '||':
        t[0] = Logica(OperadorLogico.OR, t[1], t[3], t.lineno(2), find_column(input, t.slice[2]))


def p_expresion_unaria(t):
    '''
        expresion : SUBTRACTIONSIGN expresion %prec UMENOS
                   | NOT expresion %prec UNOT
    '''
    #
    if t[1] == '-':
        t[0] = Aritmetica(OperadorAritmetico.UMENOS, t[2], None, t.lineno(1), find_column(input, t.slice[1]))
    elif t[1] == '!':
        t[0] = Logica(OperadorLogico.NOT, t[2], None, t.lineno(1), find_column(input, t.slice[1]))


def p_expresion_agrupar(t):
    '''expresion : PARENTHESISOPEN expresion PARENTHESISCLOSE'''
    t[0] = t[2]


def p_expresion_unoenuno(t):
    '''
        expresion :  expresion INCREMENT
                  |  expresion DECREMENT
    '''
    # Si es ++
    if t[2] == "++":
        t[0] = Aritmetica(OperadorAritmetico.MASMAS, t[1], None, t.lineno(2), find_column(input, t.slice[2]))
    elif t[2] == "--":
        t[0] = Aritmetica(OperadorAritmetico.MENOSMENOS, t[1], None, t.lineno(2), find_column(input, t.slice[2]))


# --------------------------------------- EXPRESION - LLAMADA ---------------------------------------------
# Expresion para poder realizar un print(llamda)... etc
def p_expresion_llamada(t):
    '''expresion    :   llamada_function'''
    t[0] = t[1]


def p_expresion_identificador(t):
    '''expresion : ID'''
    t[0] = Identificador(t[1], t.lineno(1), find_column(input, t.slice[1]))


# ----------------------------------------- EXPRESION - CASTEO --------------------------------------------
def p_expresion_casteo(t):
    '''expresion    :   PARENTHESISOPEN tipo_dato PARENTHESISCLOSE expresion'''
    t[0] = Casteo(t[2], t[4], t.lineno(1), find_column(input, t.slice[1]))

# ----------------------------------------- EXPRESION - READ ----------------------------------------------
def p_expresion_read(t):
    '''expresion    :   RREAD PARENTHESISOPEN PARENTHESISCLOSE'''
    t[0] = Read(t.lineno(1), find_column(input, t.slice[1]))


# ----------------------------------------- EXPRESION - ARREGLO --------------------------------------------
def p_expresion_arreglo(t):
    '''expresion    :   ID lista_expresiones'''
    t[0] = AccesoArreglo(t[1], t[2], t.lineno(1), find_column(input, t.slice[1]))

#  ---------------------------------------- PRIMITIVOS ----------------------------------
def p_expresion_entero(t):
    '''expresion : ENTERO'''
    t[0] = Primitivos(TIPO.ENTERO, t[1], t.lineno(1), find_column(input, t.slice[1]))


def p_primitivo_decimal(t):
    '''expresion : DECIMAL'''
    t[0] = Primitivos(TIPO.DECIMAL, t[1], t.lineno(1), find_column(input, t.slice[1]))


def p_primitivo_cadena(t):
    '''expresion : CADENA'''
    t[0] = Primitivos(TIPO.CADENA, str(t[1]), t.lineno(1), find_column(input, t.slice[1]))


def p_primitivo_caracter(t):
    '''expresion : CARACTER'''
    t[0] = Primitivos(TIPO.CARACTER, str(t[1]), t.lineno(1), find_column(input, t.slice[1]))


def p_primitivo_true(t):
    '''expresion : RTRUE'''
    t[0] = Primitivos(TIPO.BOOLEANO, True, t.lineno(1), find_column(input, t.slice[1]))


def p_primitivo_false(t):
    '''expresion : RFALSE'''
    t[0] = Primitivos(TIPO.BOOLEANO, False, t.lineno(1), find_column(input, t.slice[1]))


def p_primitivo_null(t):
    '''expresion : RNULL'''
    t[0] = Primitivos(TIPO.NULO, str(t[1]), t.lineno(1), find_column(input, t.slice[1]))


import ply.yacc as yacc
parser = yacc.yacc()


input = ''  # Variable global para encontrar la columna


def getErrores():
    return errors


# FUNCION PARA REALIZAR GRAMTICA
def parse(inp) :
    global errors
    global lexer
    global parser
    errors = []
    lexer = lex.lex()
    parser = yacc.yacc()
    global input
    input = inp
    return parser.parse(inp)


# CREANDO FUNCIONES NATIVAS
def creacion_nativas(ast):
    # Agregando la funcion TOUPPER
    nombreNativa = "toupper"
    parametros = [{'tipo': TIPO.CADENA, 'identificador': 'toUpper##Parametro1'}]
    instrucciones = []
    toUpper = ToUpper(nombreNativa, parametros, instrucciones, -1, -1)
    ast.addFuncion(toUpper)

    # Agregando la funcion TOLOWER
    nombreNativa = "tolower"
    parametros = [{'tipo': TIPO.CADENA, 'identificador': 'toLower##Parametro1'}]
    instrucciones = []
    toLower = ToLower(nombreNativa, parametros, instrucciones, -1, -1)
    ast.addFuncion(toLower)

    # Agregando la funcion LENGTH
    nombreNativa = "length"
    parametros = [{'tipo': TIPO.ENTERO, 'identificador': 'length##Parametro1'}]
    instrucciones = []
    length_n = Length(nombreNativa, parametros, instrucciones, -1, -1)
    ast.addFuncion(length_n)

    # Agregando la funcion TRUNCATE
    nombreNativa = "truncate"
    parametros = [{'tipo': TIPO.ENTERO, 'identificador': 'truncate##Parametro1'}]
    instrucciones = []
    truncate_n = Truncate(nombreNativa, parametros, instrucciones, -1, -1)
    ast.addFuncion(truncate_n)

    # Agregando la funcion ROUND
    nombreNativa = "round"
    parametros = [{'tipo': TIPO.ENTERO, 'identificador': 'round##Parametro1'}]
    instrucciones = []
    round_n = Round(nombreNativa, parametros, instrucciones, -1, -1)
    ast.addFuncion(round_n)

    # Agregando la funcion TYPEOF
    nombreNativa = "typeof"
    parametros = [{'tipo': TIPO.CADENA, 'identificador': 'Typeof##Parametro1'}]
    instrucciones = []
    type_of = Typeof(nombreNativa, parametros, instrucciones, -1, -1)
    ast.addFuncion(type_of)


def realizar_dot(astTree):
    inicio_dot = NodoArbol("RAIZ")
    instruccion_dot = NodoArbol("INSTRUCCIONES")

    for instruccion_ast in astTree.getInstrucciones():
        instruccion_dot.addHijoNodo(instruccion_ast.getNodo())

    inicio_dot.addHijoNodo(instruccion_dot)
    grafo = astTree.getDot(inicio_dot)  # Devuelve el string del grafo

    dirname = os.path.dirname(__file__)
    direcc = os.path.join(dirname, 'ast.dot')
    file = open(direcc, "w+", encoding="utf-8")
    file.write(grafo)
    file.close()
    os.system('dot -T svg -o ast.svg ast.dot')
    os.system('dot -T pdf -o ast.pdf ast.dot')


def grammar_analisis(entrada, txtWidget):
    #  ------------------ EXPORTACIONES ----------------
    from Tabla_Simbolo.Arbol import Arbol
    from Tabla_Simbolo.TablaSimbolos import TablaSimbolos

    '''
    El parse lo que nos devuelve es un arbol con nodos
    Hasta ahora solo hemos hecho el analisis sintactico
    '''
    instrucciones = parse(entrada)      # ARBOL AST
    astTree = Arbol(instrucciones)      # Inicializamos nuestro objeto arbol
    Tabla_Global = TablaSimbolos()      # Inicializamos la tabla de simbolos global
    astTree.setTSglobal(Tabla_Global)
    astTree.setTextoInterfaz(txtWidget) # Agregamos el widget para actualizar el read
    creacion_nativas(astTree)           # Creando funciones nativas

    # CAPTURA DE ERRORES LEXICOS Y SINTACTICOS
    for error in errors:
        astTree.getExcepciones().append(error)
        astTree.updateConsola(error.toString())

    # 1ERA PASADA BUSCANDO (DECLARACIONES , ASIGNACIONES y FUNCIONES)
    for instruccion in astTree.getInstrucciones():
        # Verificando si viene una FUNCION.
        if isinstance(instruccion, Funcion):
            # GUARDAR LA FUNCION EN "MEMORIA" (EN EL ARBOL)
            astTree.addFuncion(instruccion)
        # Verificando si viene una DECLARACION o ASIGNACION
        if isinstance(instruccion, Declaracion) or isinstance(instruccion, Asignacion) or \
                isinstance(instruccion, DeclaracionArreglo) or isinstance(instruccion, ModificarArreglo):
            value_asig_decla = instruccion.interpretar(astTree, Tabla_Global)

            # Si la interpretacion es ERRONEA O BREAK, error
            if isinstance(value_asig_decla, Excepcion):
                astTree.getExcepciones().append(value_asig_decla)
                astTree.updateConsola(value_asig_decla.toString())
            if isinstance(value_asig_decla, Break):
                error_break = Excepcion("Semantico", "BREAK fuera de ciclo.", instruccion.fila, instruccion.columna)
                astTree.getExcepciones().append(error_break)
                astTree.updateConsola(error_break.toString())

    # 2da PASADA PARA EL MAIN
    contador_main = 0
    for instruccion in astTree.getInstrucciones():                                                # 2DA PASADA BUSCANDO MAIN
        if isinstance(instruccion, Main):
            contador_main += 1
            if contador_main >= 2:                                                       # Verificar si no viene 2 veces
                print("entro")
                error_main = Excepcion("Semantico", ">Excepcion MAIN: Existen 2 funciones Main.<", instruccion.fila, instruccion.columna)
                astTree.getExcepciones().append(error_main)
                astTree.updateConsola(error_main.toString())
                break
            value_mainIns = instruccion.interpretar(astTree, Tabla_Global)
            if isinstance(value_mainIns, Excepcion):
                astTree.getExcepciones().append(value_mainIns)
                astTree.updateConsola(value_mainIns.toString())
            if isinstance(value_mainIns, Break):
                err = Excepcion("Semantico", ">Excepcion BREAK: sentencia fuera de ciclo<", instruccion.fila, instruccion.columna)
                astTree.getExcepciones().append(err)
                astTree.updateConsola(err.toString())
            if isinstance(value_mainIns, Return):
                err = Excepcion("Semantico", ">Excepcion RETURN: sentencia no permitida en main.<", instruccion.fila, instruccion.columna)
                astTree.getExcepciones().append(err)
                astTree.updateConsola(err.toString())

    # 3ERA PASADA (SENTENCIAS FUERA DE MAIN)
    for instruccion in astTree.getInstrucciones():
        if not (isinstance(instruccion, Main) or isinstance(instruccion, Declaracion) or
                isinstance(instruccion, Asignacion) or isinstance(instruccion, Funcion) or
                isinstance(instruccion, DeclaracionArreglo) or isinstance(instruccion, ModificarArreglo)):
            err = Excepcion("Semantico", "Sentencias fuera de Main", instruccion.fila, instruccion.columna)
            astTree.getExcepciones().append(err)
            astTree.updateConsola(err.toString())

    print(astTree.getConsola())
    return astTree

# f = open("TestFiles/Prueba_Read1.jpr", "r")
# entrada = f.read()
# grammar_analisis2(entrada)
#
#
# print(float(10))
# print(float('45.6'))
# print(float("458.23"))
# print(float(10))


# import math
# i = math.ceil(10.466)
# print(i)
#
# arreglo = [20]

# print(len(4555))
# i = 10.99999999
# j = int(i)
# print(float(j))
# Pruebas del analizador lexico
# lexer = lex.lex()
# archi1 = open("TestFiles/Prueba1.jpr", "r", encoding="utf-8")
# contenido = archi1.read()
# print(contenido)
# archi1.close()
# lexer.input(contenido)
#
# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print(tok)
#
# cadena = 'cadena\n'
# if '\n' in cadena:
#     print('Si lo contiene')
# print(cadena)