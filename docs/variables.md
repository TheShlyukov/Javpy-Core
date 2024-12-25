
# Variables in Javpy

## Overview
Variables in Javpy are dynamically typed and can store different types of values. The language supports both regular variables and constants.

## Variable Declaration
Variables are declared using the following syntax:

variable_name: value


Constants are declared using:

const variable_name: value


## Supported Types
- Numbers (integers and floating-point)
- Strings (enclosed in <<>>)
- Booleans (True/False)

## Examples

```
x: 42 <$> Integer variable <$!>
name: <<John>> <$> String variable <$!>
pi: 3.14 <$> Float variable <$!>
const max: 100 <$> Constant variable <$!>
```


## Rules
1. Variables must be declared before use
2. Variable names must start with a letter or underscore
3. Constants cannot be modified after declaration
4. Variables can be reassigned unless declared as constants

## Error Handling
- Using undeclared variables raises a NameError
- Attempting to modify constants raises a ValueError
- Invalid variable names result in a SyntaxError
