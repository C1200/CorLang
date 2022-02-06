---
layout: docs
title: Functions
order: 6
---

## Functions

### Calling functions

Functions are called by typing the function name followed by a set of brackets.
Functions can optionally be passed arguments inside the brackets, separated by commas.

Example:
```corlang
this_function_takes_no_args()
this_function_takes_args("an argument")
```

### Defining functions

Functions are usually defined using the `func` keyword, followed by a function name and a
set of brackets.
Between the brackets you can optionally take arguments by putting argument names inside the
brackets, separated by commas.
Functions can use multiline or singleline. In v0.0.3 and below, only singleline functions
can return data but that will change in the future. Since v0.0.4, both types can return
data (multiline needs to use return).

Example:
```corlang
func add(a, b) -> a + b

func multiline(name)
    print("Hello, " + name)
    print("This is a multiline function")
    return "I can return stuff"
end
```