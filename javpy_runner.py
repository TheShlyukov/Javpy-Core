from javpy_core import JavpyCore

def run_javpy_file(filepath):
    if not filepath.endswith('.jvp'):
        print("Error: Invalid file extension.")
        return
    else:
        try:
            with open(filepath, 'r') as file:
                code = file.read()
        except FileNotFoundError:
            print(f"Error: File '{filepath}' not found.")
            return

        try:
            tokens = JavpyCore.tokenize(code)
            ast = JavpyCore.parse(tokens)
            if ast:
                JavpyCore.interpret(ast)
            else:
                print("Error: No executable code found.")
        except SyntaxError as e:
            print(e)

if __name__ == "__main__":
    run_javpy_file(input("path to file: "))
