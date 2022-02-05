---
layout: docs
title: Types
order: 3
---

## Types

### Number

A number is either an integer or a float.

```corlang
print(6)
print(3.141)
```

See also:
[Operations](https://c1200.js.org/CorLang/docs/operations.html#number-operations)

### String

A string is a series of characters surrounded by quotes (either single or double).

```corlang
print("Hello World!")
print('Hello Reader!')
```
See also:
[Operations](https://c1200.js.org/CorLang/docs/operations.html#string-operations)

### List

A list is a set of comma separated values.

```corlang
print([ true, "truthy", 3.141, 6 ])
```
See also:
[Operations](https://c1200.js.org/CorLang/docs/operations.html#list-operations)

### Function

A function is a block of CorLang code that runs when it's called.

```corlang
func my_func() -> "this is the return"
print(my_func())
```

See also:
[Functions](https://c1200.js.org/CorLang/docs/functions.html)

### Built-in Function

A built-in function executes "native" Python code when called.

```corlang
print()
```

See also:
[Built-ins](https://c1200.js.org/CorLang/docs/builtins.html)