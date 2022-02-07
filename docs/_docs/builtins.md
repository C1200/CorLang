---
layout: docs
title: Built-Ins
order: 2
---

## Built-In Variables

| Variable  | Type            | Info                                   |
|-----------|-----------------|----------------------------------------|
| null      | Number          | Equal to 0                             |
| true      | Number          | Equal to 1                             |
| false     | Number          | Equal to 0                             |

## Built-In Functions

### print(text)
Prints input to the screen.

```corlang
print("Hello, World!")
```

### input(text)
Prompts user for string input.

```corlang
var my_input = input("Input some text: ")
print("Got some input: " + my_input)
```

### input_int(text)
Prompts user for integer input.

```corlang
var a = input_int("Input a number: ")
var b = input_int("Input another number: ")
print(a + b)
```

### type(value)
Returns type of input.

```corlang
type("a string") # Output: "String"
type([true, "truthy", 3.141, 10]) # Output: "List"
```

### import(file)
![Version >= 0.0.4](https://img.shields.io/badge/Version-%3E%3D%200.0.4-blue?style=flat-square)

Imports exteral file.

```corlang
import("std.list")
import("mymodule.cor")
```

See also:
[Modules & Imports](https://c1200.js.org/CorLang/docs/modules-imports.html)

### len(value)
![Version >= 0.0.4](https://img.shields.io/badge/Version-%3E%3D%200.0.4-blue?style=flat-square)

Returns the length of a list or string.

```corlang
len("Hello") # Outputs: 5
len(["this", "has", "4", "elements"]) # Outputs: 4
```

### throw(text)
![Version >= 0.0.4](https://img.shields.io/badge/Version-%3E%3D%200.0.4-blue?style=flat-square)

Throws a runtime error.

```corlang
throw("An error occurred")
```