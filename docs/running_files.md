# Running Javpy Files

## Overview
Javpy is a programming language interpreter that processes `.jvp` files using a two-part system: javpy.py (runner) and javpy_core.py (core interpreter).

## Functionality

### Main Components
1. File Runner (javpy.py)
   - Handles command-line arguments
   - Reads and processes .jvp files
   - Provides debugging options (show tokens, show content)
   - Manages error handling and display

2. Core Interpreter (javpy_core.py)
   - Tokenizes source code
   - Parses tokens into AST
   - Evaluates expressions
   - Manages variables and constants
   - Handles arithmetic operations

### Command Line Usage

python javpy.py filename.jvp [-t] [-c]

Options:
- `-t, --tokens`: Display tokenization results
- `-c, --content`: Show file contents before execution

### Features
- Variable declaration and assignment
- Constant declarations
- Basic arithmetic operations (`+`, `-`, `*`, `/`, `//`, `%`, `**`)
- String support
- Print statements
- Comments (using `<$>` and `<$!>`)
- Error handling with detailed messages

### Supported Data Types
- Numbers (integers and floats)
- Strings (enclosed in `<<>>`)
- Booleans (True/False)

### Error Handling
- Syntax errors
- Variable reference errors
- Constant modification errors
- File handling errors
- Invalid token errors
- Comment parsing errors

javpy.py output example:

`$ python javpy.py example.jvp --tokens --content`

```
----------------------------------------
Javpy-Core: pre-alpha 0.0.5
Running file: example.jvp

File content:

==============================
<$> This is a comment <$!>

print 42

<$>
This is a 
multi-line comment
<$!>

print 100

<$> String test <$!>
print <<Hello World!>>

<$> Decimal test <$!>
print 3.14

print <<>>

<$> Expressions test <$!>
print (((2+2)*2)/2)**2

<$>Variables test<$!>

<$> String <$!>
a: <<Variables!>>
print a

<$> Number <$!>
b: 12
print b

<$> Decemal <$!>
c: 3.14
print c

<$> Evaluation <$!>
d: (((2+2)*2)/2)**2
print d

<$> Boolean <$!>
e: False
print e

<$> Constants <$!>
const Truth: True
print Truth
==============================

Tokens: [('PRINT', 'print'), ('NUMBER', '42'), ('PRINT', 'print'), ('NUMBER', '100'), ('PRINT', 'print'), ('STRING', 'Hello World!'), ('PRINT', 'print'), ('NUMBER', 3.14), ('PRINT', 'print'), ('STRING', ''), ('PRINT', 'print'), ('OPERATOR', '('), ('OPERATOR', '('), ('OPERATOR', '('), ('NUMBER', '2'), ('OPERATOR', '+'), ('NUMBER', '2'), ('OPERATOR', ')'), ('OPERATOR', '*'), ('NUMBER', '2'), ('OPERATOR', ')'), ('OPERATOR', '/'), ('NUMBER', '2'), ('OPERATOR', ')'), ('OPERATOR', '**'), ('NUMBER', '2'), ('IDENT', 'a'), ('COLON', ':'), ('STRING', 'Variables!'), ('PRINT', 'print'), ('IDENT', 'a'), ('IDENT', 'b'), ('COLON', ':'), ('NUMBER', '12'), ('PRINT', 'print'), ('IDENT', 'b'), ('IDENT', 'c'), ('COLON', ':'), ('NUMBER', 3.14), ('PRINT', 'print'), ('IDENT', 'c'), ('IDENT', 'd'), ('COLON', ':'), ('OPERATOR', '('), ('OPERATOR', '('), ('OPERATOR', '('), ('NUMBER', '2'), ('OPERATOR', '+'), ('NUMBER', '2'), ('OPERATOR', ')'), ('OPERATOR', '*'), ('NUMBER', '2'), ('OPERATOR', ')'), ('OPERATOR', '/'), ('NUMBER', '2'), ('OPERATOR', ')'), ('OPERATOR', '**'), ('NUMBER', '2'), ('PRINT', 'print'), ('IDENT', 'd'), ('IDENT', 'e'), ('COLON', ':'), ('IDENT', 'False'), ('PRINT', 'print'), ('IDENT', 'e'), ('CONST', 'const'), ('IDENT', 'Truth'), ('COLON', ':'), ('IDENT', 'True'), ('PRINT', 'print'), ('IDENT', 'Truth')]

42
100
Hello World!
3.14

16
Variables!
12
3.14
16
False
True

----------------------------------------
```
