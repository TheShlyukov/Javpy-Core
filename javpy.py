import sys
import argparse
try:
    from javpy_core import JavpyCore
except:
    print()
    print("/"*30)
    print()
    print("Javpy-Core not found.\nShutting down")
    print()
    print("/"*30)
    print()
    exit()

def run_javpy_file(filepath, show_tokens=False, show_content=False):
    if not filepath.endswith('.jvp'):
        print("Error: Invalid file extension. (.jvp extension required)")
        return
    else:
        try:
            with open(filepath, 'r') as file:
                code = file.read()
                
            if show_content:
                print("File content:")
                print()
                print("="*30)
                print(code)
                print("="*30)
                print()
                
            tokens = JavpyCore.tokenize(code)
            if show_tokens:
                print("Tokens:", tokens)
                print()
            
            ast = JavpyCore.parse(tokens)
            if ast:
                JavpyCore.interpret(ast)
            else:
                print("Error: No executable code found.")
        except FileNotFoundError:
            print(f"Error: File '{filepath}' not found.")
        except ValueError as e:
            print("<...>")
            print()
            print("/"*len(str(e)))
            print()
            print(str(e))
            print()
            print("/"*len(str(e)))
        except SyntaxError as e:
            print("<...>")
            print()
            print("/"*len(str(e)))
            print()
            print(e)
            print()
            print("/"*len(str(e)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Javpy file runner')
    parser.add_argument('filepath', help='Path to the .jvp file')
    parser.add_argument('-t', '--tokens', action='store_true', help='Show tokens')
    parser.add_argument('-c', '--content', action='store_true', help='Show file content')
    
    args = parser.parse_args()
    print("-"*40)
    try:
        print("Javpy-Core:", JavpyCore.JAVPY_CORE_VER)
    except:
        print("Javpy-Core (Unknown version)")
    print("Running file:", str(args.filepath))
    print()
    run_javpy_file(args.filepath, args.tokens, args.content)
    print()
    print("-"*40)