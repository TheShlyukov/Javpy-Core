import re

TOKEN_SPEC = [
    ("PRINT", r'print\b'),
    ("NUMBER", r'\d+'),
    ("IDENT", r'[a-zA-Z_]\w*'),
    ("NEWLINE", r'\n'),
    ("SKIP", r'[ \t]+'),
    ("MISMATCH", r'.'),
]

class Node:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

def tokenize(code):
    tokens = []
    for line in code.splitlines():
        pos = 0
        while pos < len(line):
            for tok_type, regex in TOKEN_SPEC:
                match = re.match(regex, line[pos:])
                if match:
                    lexeme = match.group(0)
                    if tok_type != "SKIP":
                        tokens.append((tok_type, lexeme))
                    pos += len(lexeme)
                    break
    return tokens

def parse(tokens):
    def match(expected_type):
        nonlocal tokens
        if tokens and tokens[0][0] == expected_type:
            return tokens.pop(0)
        return None

    def parse_print():
        match("PRINT")
        value = match("IDENT") or match("NUMBER")
        return Node("Print", value=value[1])

    if tokens[0][0] == "PRINT":
        return parse_print()
    return None

def interpret(ast):
    if ast.type == "Print":
        print(ast.value)

# Пример использования
code = "print 42"
tokens = tokenize(code)
ast = parse(tokens)
interpret(ast)  # Вывод: 42
