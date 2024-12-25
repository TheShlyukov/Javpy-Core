
# Print Statement in Javpy

The `print` statement in Javpy is used to output values to the console.

## Syntax

print expression


## Features
- Automatically converts integer float values to integers when printing (e.g. 5.0 prints as 5)
- Can print strings, numbers, and results of expressions
- Strings must be enclosed in `<<` and `>>` markers
- Supports arithmetic expressions

## Examples

```
print <<Hello World>> <$> Prints: Hello World <$!>
print 5+3 <$> Prints: 8 <$!>
print 10.0 <$>Prints: 10 <$!>
print 2 * 3 + 4 <$> Prints: 10 <$!>
print True <$> Prints: True <$!>
print x <$> Prints value of variable x <$!>
```


## Notes
- No parentheses needed around the expression
- Each print statement prints on a new line
- Can print variables after they are declared
