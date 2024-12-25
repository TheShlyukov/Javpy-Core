import re

TOKEN_SPEC = [
    ("COMMENT_START", r'<\$>'),
    ("COMMENT_END", r'<\$!>'),
    ("PRINT", r'print\b'),
    ("CONST", r'const\b'),
    ("COLON", r':'),
    ("NUMBER", r'\d+(\.\d+)?'),
    ("STRING", r'<<[^>]*>>'),
    ("OPERATOR", r'\*\*|//|\+|\-|\*|/|%|\(|\)'),
    ("IDENT", r'[a-zA-Z_]\w*'),
    ("NEWLINE", r'\n'),
    ("SKIP", r'[ \t]+'),
    ("MISMATCH", r'.'),
]

class JavpyCore:
    JAVPY_CORE_VER = "pre-alpha 0.0.5"
    variables = {}
    constants = set()
    
    class Node:
        def __init__(self, type_, value=None, left=None, right=None):
            self.type = type_
            self.value = value
            self.left = left
            self.right = right

    @staticmethod
    def validate_type(type_, value):
        if type_ == "str":
            return isinstance(value, str)
        elif type_ in ["int", "float", "double"]:
            return isinstance(value, (int, float))
        elif type_ == "bool":
            return isinstance(value, bool)
        return True

    @staticmethod
    def tokenize(code):
        tokens = []
        in_comment = False
        line_num = 1
        pos = 0
        comment_start_line = 0
        
        code_lines = code.split('\n')
        
        if '<$!>' in code and '<$>' not in code:
            error_line_num = code[:code.find('<$!>')].count('\n') + 1
            error_line = code_lines[error_line_num - 1]
            raise SyntaxError(f"Error: Found comment end marker '<$!>' without matching comment start '<$>'\nLine {error_line_num}: {error_line}")
        
        while pos < len(code):
            matched = False
            for tok_type, regex in TOKEN_SPEC:
                match = re.match(regex, code[pos:])
                if match:
                    matched = True
                    lexeme = match.group(0)

                    if tok_type == "COMMENT_START":
                        if in_comment:
                            error_line = code_lines[line_num - 1]
                            raise SyntaxError(f"Error: Nested comment start '<$>' at line {line_num}\nLine {line_num}: {error_line}")
                        in_comment = True
                        comment_start_line = line_num
                    elif tok_type == "COMMENT_END":
                        if not in_comment:
                            error_line = code_lines[line_num - 1]
                            raise SyntaxError(f"Error: Unexpected comment end '<$!>' at line {line_num}\nLine {line_num}: {error_line}")
                        in_comment = False
                    elif not in_comment and tok_type not in ["SKIP", "NEWLINE"]:
                        if tok_type == "STRING":
                            tokens.append((tok_type, lexeme[2:-2]))
                        elif tok_type == "NUMBER" and '.' in lexeme:
                            tokens.append((tok_type, float(lexeme)))
                        else:
                            tokens.append((tok_type, lexeme))

                    pos += len(lexeme)
                    if lexeme == '\n':
                        line_num += 1
                    break

            if not matched:
                if not in_comment:
                    error_line = code_lines[line_num - 1]
                    raise SyntaxError(f"Error: Unknown symbol '{code[pos]}' at line {line_num}, position {pos + 1}\nLine {line_num}: {error_line}")
                pos += 1

        if in_comment:
            error_line = code_lines[comment_start_line - 1]
            raise SyntaxError(f"Error: Unclosed comment starting at line {comment_start_line}\nLine {comment_start_line}: {error_line}")
        return tokens
    @staticmethod
    def parse(tokens):
        if not tokens:
            return None

        def match(expected_type):
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
            
            token_type = tokens[0][0]
            token_value = tokens[0][1]
            
            if token_type == 'NUMBER':
                tokens.pop(0)
                return JavpyCore.Node('Number', float(token_value))
            elif token_type == 'STRING':
                tokens.pop(0)
                return JavpyCore.Node('String', token_value)
            elif token_type == 'IDENT' and token_value in ('True', 'False'):
                tokens.pop(0)
                return JavpyCore.Node('Boolean', token_value == 'True')
            elif token_type == 'IDENT':
                tokens.pop(0)
                return JavpyCore.Node('Identifier', token_value)
            elif token_value == '(':
                tokens.pop(0)
                expr = parse_expression()
                if not tokens or tokens[0][1] != ')':
                    raise SyntaxError("Missing closing parenthesis")
                tokens.pop(0)
                return expr
            
            raise SyntaxError(f"Unexpected token: {token_type}")

        statements = []
        
        while tokens:
            if tokens[0][0] == "PRINT":
                tokens.pop(0)  # consume print
                expr = parse_expression()
                statements.append(JavpyCore.Node("Print", value=expr))
                
            elif tokens[0][0] == "CONST":
                tokens.pop(0)  # consume const
                var_name = tokens.pop(0)[1]  # get variable name
                if tokens.pop(0)[0] != "COLON":
                    raise SyntaxError("Expected ':' after variable name")
                value = parse_expression()
                statements.append(JavpyCore.Node("VarDecl", value=(None, var_name, value, True)))
                
            elif tokens[0][0] == "IDENT":
                var_name = tokens.pop(0)[1]
                if tokens.pop(0)[0] != "COLON":
                    raise SyntaxError("Expected ':' after variable name")
                value = parse_expression()
                statements.append(JavpyCore.Node("VarDecl", value=(None, var_name, value, False)))
            else:
                tokens.pop(0)  # Skip unknown tokens

        return statements
    @staticmethod
    def evaluate(node):
        if not node:
            return None
            
        if node.type == 'Number':
            return node.value
        if node.type == 'String':
            return node.value
        if node.type == 'Identifier':
            if node.value not in JavpyCore.variables:
                raise NameError(f"Variable '{node.value}' is not defined")
            return JavpyCore.variables[node.value]
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

    @staticmethod
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
            elif node.type == "VarDecl":
                _, name, value, is_constant = node.value
                if name in JavpyCore.variables:
                    if name in JavpyCore.constants:
                        raise ValueError(f"Error: Cannot modify constant variable '{name}'")
                evaluated_value = JavpyCore.evaluate(value)
                JavpyCore.variables[name] = evaluated_value
                if is_constant:
                    JavpyCore.constants.add(name)                    
                    JavpyCore.constants.add(name)
