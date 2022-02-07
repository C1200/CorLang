---
layout: docs
title: Modules & Imports
order: 7
---

## Modules & Imports

### Importing Modules

To import modules use the `import` function.

```corlang
import("mymodule.cor")

# If a module is in a different folder use:
import("myfolder/mymodule.cor")
```

### Reserved Module Names

*\* is used as a wildcard.*

| File Name | Use                                   |
|-----------|---------------------------------------|
| std.*     | [Standard Library](#standard-library) |
| lib.*     | Reserved for future                   |

### Standard Library

#### std.list

##### list_join(list, separator)

Joins list items (must be a list of strings), separated by the separator string.

```corlang
list_join(["Eggs", "Bread", "Milk"], ", ") # Outputs: "Eggs, Bread, Milk"
```