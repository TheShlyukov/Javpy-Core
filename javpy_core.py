import re

TOKEN_SPEC = [
    ("COMMENT_START", r'<\$>'),
    ("COMMENT_END", r'<\$!>'),
    ("PRINT", r'print\b'),
    ("NUMBER", r'\d+(\.\d+)?'),
    ("STRING", r'<<[^>]*>>'),
    ("OPERATOR", r'\*\*|//|\+|\-|\*|/|%|\(|\)'),
    ("IDENT", r'[a-zA-Z_]\w*'),
    ("NEWLINE", r'\n'),
    ("SKIP", r'[ \t]+'),
    ("MISMATCH", r'.'),
]

class JavpyCore:

    JAVPY_CORE_VER = "pre-alpha 0.0.4"

    class Node:
        def __init__(self, type_, value=None, left=None, right=None):
            self.type = type_
            self.value = value
            self.left = left
            self.right = right

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
                        if tok_type == "STRING":
                            # Fix string handling - remove << and >> properly
                            tokens.append((tok_type, lexeme[2:-2]))
                        elif tok_type == "NUMBER" and '.' in lexeme:
                            tokens.append((tok_type, float(lexeme)))
                        else:
                            tokens.append((tok_type, lexeme))

                    pos += len(lexeme)
                    break

            if not matched:
                if not in_comment:
                    raise SyntaxError(f"Error: Unknown symbol '{code[pos]}' at line {line_num}, position {pos + 1}")
                pos += 1

            if pos < len(code) and code[pos - 1] == '\n':
                line_num += 1

        return tokens

    def parse(tokens):
        if not tokens:
            return None

        def match(expected_type):
            nonlocal tokens
            if tokens and tokens[0][0] == expected_type:
                return tokens.pop(0)
            return None

        def parse_expression():
            return parse_addition()

        def parse_addition():
            left = parse_multiplication()
            while tokens and tokens[0][1] in ['+', '-']:
                operator = tokens.pop(0)[1]
                right = parse_multiplication()
                left = JavpyCore.Node('Operation', operator, left, right)
            return left
        def parse_multiplication():
            left = parse_power()
            while tokens and tokens[0][1] in ['*', '/', '//', '%']:
                operator = tokens.pop(0)[1]
                right = parse_power()
                left = JavpyCore.Node('Operation', operator, left, right)
            return left

        def parse_power():
            left = parse_primary()
            while tokens and tokens[0][1] == '**':
                operator = tokens.pop(0)[1]
                right = parse_power()
                left = JavpyCore.Node('Operation', operator, left, right)
            return left


        def parse_primary():
            if not tokens:
                raise SyntaxError("Unexpected end of input")
            
            if tokens[0][0] == 'NUMBER':
                return JavpyCore.Node('Number', float(tokens.pop(0)[1]))
            elif tokens[0][0] == 'STRING':
                return JavpyCore.Node('String', tokens.pop(0)[1])
            elif tokens[0][1] == '(':  # Check for opening parenthesis by value
                tokens.pop(0)  # consume '('
                expr = parse_expression()
                if not tokens or tokens[0][1] != ')':  # Check for closing parenthesis by value
                    raise SyntaxError("Missing closing parenthesis")
                tokens.pop(0)  # consume ')'
                return expr
            
            raise SyntaxError(f"Unexpected token: {tokens[0][0]}")
        def parse_print():
            if match("PRINT"):
                expr = parse_expression()
                return JavpyCore.Node("Print", value=expr)
            return None

        def interpret(ast):
            if not ast:
                return
            for node in ast:
                if node.type == "Print":
                    if isinstance(node.value, JavpyCore.Node):
                        result = JavpyCore.evaluate(node.value)
                        # Format numbers without decimal part if they're whole numbers
                        if isinstance(result, float) and result.is_integer():
                            print(int(result))
                        else:
                            print(result)
                    elif isinstance(node.value, str):
                        print(node.value)
                    else:
                        print(node.value)
        def parse_print():
            if match("PRINT"):
                expr = parse_expression()
                return JavpyCore.Node("Print", value=expr)
            return None

        def parse_statement():
            if not tokens:
                return None
            if tokens[0][0] == "PRINT":
                return parse_print()
            tokens.pop(0)
            return None

        statements = []
        while tokens:
            stmt = parse_statement()
            if stmt:
                statements.append(stmt)

        return statements

    def evaluate(node):
        if node.type == 'Number':
            return node.value
        if node.type == 'String':
            return node.value
        if node.type == 'Operation':
            left = JavpyCore.evaluate(node.left)
            right = JavpyCore.evaluate(node.right)
            if node.value == '+': return left + right
            if node.value == '-': return left - right
            if node.value == '*': return left * right
            if node.value == '/': return left / right
            if node.value == '//': return left // right
            if node.value == '%': return left % right
            if node.value == '**': return left ** right
        return node.value

    def interpret(ast):
        if not ast:
            return
        for node in ast:
            if node.type == "Print":
                result = JavpyCore.evaluate(node.value)
                if isinstance(result, float) and result.is_integer():
                    print(int(result))
                else:
                    print(result)

    def parse_primary(self, tokens):
        if not tokens:
            raise SyntaxError("Unexpected end of input")
        
        token_type = tokens[0][0]
        if token_type == 'NUMBER':
            return JavpyCore.Node('Number', float(tokens.pop(0)[1]))
        elif token_type == 'STRING':
            return JavpyCore.Node('String', tokens.pop(0)[1])
        elif token_type == '(':
            tokens.pop(0)
            expr = self.parse_expression(tokens)
            if not tokens or tokens[0][0] != ')':
                raise SyntaxError("Missing closing parenthesis")
            tokens.pop(0)
            return expr
        
        raise SyntaxError(f"Unexpected token: {token_type}")
