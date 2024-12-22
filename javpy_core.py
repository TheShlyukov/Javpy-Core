import re

TOKEN_SPEC = [
    ("COMMENT_START", r'<\$>'),
    ("COMMENT_END", r'<\$!>'),
    ("PRINT", r'print\b'),
    ("NUMBER", r'\d+'),
    ("IDENT", r'[a-zA-Z_]\w*'),
    ("NEWLINE", r'\n'),
    ("SKIP", r'[ \t]+'),
    ("MISMATCH", r'.'),
]

class JavpyCore:

    class Node:
        def __init__(self, type_, value=None):
            self.type = type_
            self.value = value

    @staticmethod
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
                    raise SyntaxError(f"Error: Unknown symbol '{code[pos]}' at line {line_num}, position {pos + 1}")
                pos += 1

            if pos < len(code) and code[pos - 1] == '\n':
                line_num += 1

        if in_comment:
            raise SyntaxError(f"Error: Unclosed comment starting at line {line_num}")

        return tokens    

    @staticmethod
    def parse(tokens):
        if not tokens:
            return None

        def match(expected_type):
            nonlocal tokens
            if tokens and tokens[0][0] == expected_type:
                return tokens.pop(0)
            return None

        def parse_statement():
            if tokens and tokens[0][0] == "PRINT":
                return parse_print()
            return None

        def parse_print():
            if match("PRINT"):
                value = match("IDENT") or match("NUMBER")
                if value:
                    return JavpyCore.Node("Print", value=value[1])
                raise SyntaxError("Error: Missing value after 'print'")
            return None

        statements = []
        while tokens:
            stmt = parse_statement()
            if stmt:
                statements.append(stmt)
            else:
                raise SyntaxError(f"Error: Unexpected token {tokens[0]}")

        return statements

    @staticmethod
    def interpret(ast):
        if not ast:
            return
        for node in ast:
            if node.type == "Print":
                print(node.value)