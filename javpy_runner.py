import sys
import argparse
from javpy_core import JavpyCore

def run_javpy_file(filepath, show_tokens=False):
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
            if show_tokens:
                print("Tokens:", tokens)
                print()
            
            ast = JavpyCore.parse(tokens)
            if ast:
                JavpyCore.interpret(ast)
            else:
                print("Error: No executable code found.")
        except SyntaxError as e:
            print(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Javpy file runner')
    parser.add_argument('filepath', help='Path to the .jvp file')
    parser.add_argument('-t', '--tokens', action='store_true', help='Show tokens')
    
    args = parser.parse_args()
    print("--------------------")
    try:
        print("Javpy-core", JavpyCore.JAVPY_CORE_VER)
    except:
        print("Javpy-Core (Unknown version)")
    print("Runnig:", str(args.filepath))
    print()
    run_javpy_file(args.filepath, args.tokens)
    print()
    print("--------------------")
