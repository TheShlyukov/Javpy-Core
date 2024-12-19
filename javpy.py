import re

TOKEN_SPEC = [
    ("PRINT", r'print\b'),
    ("NUMBER", r'\d+'),
    ("IDENT", r'[a-zA-Z_]\w*'),
    ("NEWLINE", r'\n'),
    ("SKIP", r'[ \t]+'),
    ("MISMATCH", r'.'),
]

TOKEN_SPEC.append(("COMMENT_START", r'<\$>'))
TOKEN_SPEC.append(("COMMENT_END", r'<\$!>'))

class Node:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

def tokenize(code):
    tokens = []
    in_comment = False  # Track if inside a comment
    line_num = 1  # Track line numbers for error messages

    for line in code.splitlines():
        pos = 0
        while pos < len(line):
            for tok_type, regex in TOKEN_SPEC:
                match = re.match(regex, line[pos:])
                if match:
                    lexeme = match.group(0)

                    # Start of a comment
                    if tok_type == "COMMENT_START":
                        if in_comment:
                            raise SyntaxError(f"Error: Comment already opened at line {line_num}")
                        in_comment = True
                        pos += len(lexeme)
                        break

                    # End of a comment
                    elif tok_type == "COMMENT_END":
                        if not in_comment:
                            raise SyntaxError(f"Error: Closing comment <$!> without opening at line {line_num}")
                        in_comment = False
                        pos += len(lexeme)
                        break

                    # Ignore everything inside a comment
                    elif in_comment:
                        pos += 1
                        break

                    # Other tokens
                    elif tok_type != "SKIP" and not in_comment:
                        tokens.append((tok_type, lexeme))

                    pos += len(lexeme)
                    break
            else:  # If no token matches
                raise SyntaxError(f"Error: Unknown symbol '{line[pos]}' at line {line_num}, position {pos + 1}")
        line_num += 1

    # Check for unclosed comment
    if in_comment:
        raise SyntaxError(f"Error: Unclosed comment started at line {line_num - 1}")

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

code = """
<$> This is a single-line comment <$!>
print 42
<$>
This is a 
multi-line comment
<$!>
print 100
"""

tokens = tokenize(code)
print(tokens)
ast = parse(tokens)
interpret(ast)


