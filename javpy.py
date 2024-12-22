import re

TOKEN_SPEC = [
    ("COMMENT_START", r'<\$>'),  # Move comment tokens to the top
    ("COMMENT_END", r'<\$!>'),
    ("PRINT", r'print\b'),
    ("NUMBER", r'\d+'),
    ("IDENT", r'[a-zA-Z_]\w*'),
    ("NEWLINE", r'\n'),
    ("SKIP", r'[ \t]+'),
    ("MISMATCH", r'.'),
]

class javpy:

    class Node:
        def __init__(self, type_, value=None):
            self.type = type_
            self.value = value

    def tokenize(code):
        tokens = []
        in_comment = False
        line_num = 1

        pos = 0
        while pos < len(code):
            matched = False
            for tok_type, regex in TOKEN_SPEC:
                match = re.match(regex, code[pos:])
                if match:
                    matched = True
                    lexeme = match.group(0)

                    if tok_type == "COMMENT_START":
                        in_comment = True
                    elif tok_type == "COMMENT_END":
                        in_comment = False
                    elif not in_comment and tok_type not in ["SKIP", "NEWLINE"]:
                        tokens.append((tok_type, lexeme))
                    
                    pos += len(lexeme)
                    break
            
            if not matched:
                if not in_comment:
                    raise SyntaxError(f"Error: Unknown symbol '{code[pos]}' at position {pos + 1}")
                pos += 1

        return tokens    
    def parse(tokens):
        if not tokens:
            return None
            
        def match(expected_type):
            nonlocal tokens
            if tokens and tokens[0][0] == expected_type:
                return tokens.pop(0)
            return None

        def parse_print():
            if match("PRINT"):
                value = match("IDENT") or match("NUMBER")
                if value:
                    return javpy.Node("Print", value=value[1])
            return None

        node = None
        if tokens[0][0] == "PRINT":
            node = parse_print()
        return node

    def interpret(ast):
        if ast is None:
            return
        if ast.type == "Print":
            print(ast.value)

if __name__ == "__main__":
    code = """
    <$> This is a single-line comment <$!>
    print 42
    <$>
    This is a 
    multi-line comment
    <$!>
    print 100
    """

    tokens = javpy.tokenize(code)
    print(tokens)
    ast = javpy.parse(tokens)
    if ast:  # Only interpret if we have a valid AST
        javpy.interpret(ast)
    else:
        print("Invalid code")

