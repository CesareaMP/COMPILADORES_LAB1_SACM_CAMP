import re
from math import e


def tokenize(expression):
    # Define los patrones para los diferentes tipos de tokens
    token_specification = [
        ('bint', r'0b[01]+'),  # Binario
        ('hint', r'0x[0-9A-Fa-f]+'),  # Hexadecimal
        ('oint', r'0o[0-7]+'),  # Octal
        ('int', r'[0-9]+'),  # Decimal
        ('var', r'[A-Za-z_][A-Za-z0-9_]*'),  # Variables
        ('plus', r'\+'),  # Operador +
        ('minus', r'-'),  # Operador -
        ('mul', r'\*'),  # Operador *
        ('div', r'/'),  # Operador /
        ('equals', r'='),  # signo igual
        ('lparen', r'\('),  # Paréntesis izquierdo
        ('rparen', r'\)'),  # Paréntesis derecho
        ('skip', r'[ \t]+'),  # Espacios y tabuladores (ignorar)
    ]

    # Compila la expresión regular combinada
    tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})'
                         for pair in token_specification)
    get_token = re.compile(tok_regex).match

    # Almacena los tokens encontrados
    tokens = []
    line = expression
    pos = 0
    mo = get_token(line)

    while mo is not None:
        typ = mo.lastgroup
        if typ != 'skip':  # Ignorar los espacios en blanco
            tokens.append((typ, mo.group(typ)))
        pos = mo.end()
        mo = get_token(line, pos)

    return tokens


# Ejemplos de uso:
#expr1 = "(1010 + 111) - 11"
expr3 = "Truski = 1123"
expr4 = "(Truski *2) + 23"
#tokens1 = tokenize(expr1)
tokens3 = tokenize(expr3)
tokens4 = tokenize(expr4)
#print(tokens1)

#print(tokens4)

G = {
    "S": ["var = Y T", "U"],
    "Y": ["bint", "int", "hint", "oint"],
    "T": ["S", "U", "ϵ"],
    "U": ["A X"],
    "X": ["U", "ϵ"],
    "A": ["B C"],
    "C": ["+ B C", "- B C", "ϵ"],
    "B": ["D E"],
    "E": ["* D E", "/ D E", "ϵ"],
    "D": ["var", "Y", "( A )"],
}



def found_terminals(productions_dict):
    terminals = set()

    for productions in productions_dict.values():
        for actual in productions:
            words = actual.split()
            for wactual in words:
                if wactual.islower() and wactual != 'ϵ':
                    terminals.add((wactual, wactual, 'ϵ'))

    return list(terminals)

    return terminals


def found_not_terminals(productions_dict):
    not_terminals = []

    for key, productions in productions_dict.items():
        for actual_prod in productions:
            not_terminals.append(('ϵ', key, actual_prod))

    return not_terminals

def sintactic_verifier(inputs):
    stack = ["S"]
    while len(inputs) != 0:
        top = stack.pop()
        lookahead = inputs[0]
        if top == "S":
            if lookahead == "var":
                stack.append("T")
                stack.append("Y")
                stack.append("equals")
                stack.append("var")
            else:
                stack.append("U")

        elif top == "Y":
            if lookahead == "bint":
                stack.append("bint")
            elif lookahead == "int":
                stack.append("int")
            elif lookahead == "oint":
                stack.append("oint")
            elif lookahead == "hint":
                stack.append("hint")

        elif top == "T":
            if lookahead == "var":
                stack.append("S")
            elif lookahead == "var" or lookahead == "lparen":
                stack.append("U")
            elif lookahead == "ϵ":
                inputs.pop(0)

        elif top == "U":
            stack.append("A")
            stack.append("X")

        elif top == "X":
            if lookahead == "ϵ":
                inputs.pop(0)
            else:
                stack.append("U")

        elif top == "A":
            stack.append("C")
            stack.append("B")

        elif top == "C":
            if lookahead == "plus":
                stack.append("C")
                stack.append("B")
                stack.append("plus")
            elif lookahead == "minus":
                stack.append("C")
                stack.append("B")
                stack.append("minus")

        elif top == "B":
            stack.append("E")
            stack.append("D")

        elif top == "E":
            if lookahead == "mul":
                stack.append("E")
                stack.append("D")
                stack.append("mul")
            elif lookahead == "div":
                stack.append("E")
                stack.append("D")
                stack.append("div")
            elif lookahead == "ϵ":
                inputs.pop(0)

        elif top == "D":
            if lookahead == "var":
                stack.append("var")
            elif lookahead == "lparen":
                stack.append("rparen")
                stack.append("A")
                stack.append("lparen")
            else:
                stack.append("Y")
        else:
            if lookahead in ["var","equals","bint","int","hint","oint","plus","minus","mul","div","lparen","rparen"]:
                inputs.pop(0)
                if(len(inputs) == 0):
                    inputs.append("ϵ")
    if (len(stack) == 0 and len(inputs) == 0):
        return "ACEPTADA"
    else:
        return "RECHAZADA"

evalu = 'S'
while evalu == 'S':
    
    print("Gramática G:")
    for key, value in G.items():
        consola = f"{key} = "
        for actual in value:
            consola += actual + " | "
        print(consola[:len(consola)-2])
    
    valor = input("Ingrese la operacion a evaluar en base a la Grámatica G:\n")
    tokens = tokenize(valor)
    print("Su operacion se tokenizó: ",tokens)
    print("La operacion ingresada fue: ", sintactic_verifier([token[0] for token in tokens]))
    
    evalu = input("Ingrese 'S' para continuar evaluando\n")