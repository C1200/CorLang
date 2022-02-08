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

##### list_map(list, function)

Returns a new list populated with the results of calling the supplied function on each
element in the supplied list.
The function should take in the element and the index.

```corlang
func square(elem, idx)
    return elem ^ 2
end
list_map([1, 2, 3, 4], square) # Outputs: [1, 2, 9, 16]
```

##### list_indexof(list, value)

Finds the supplied value in the list. If the item is found, the index of the item is returned.
Otherwise, -1 is returned.

```corlang
list_indexof([1, 2, 3, 4], 3) # Outputs: 2
list_indexof([1, 2, 3, 4], 5) # Outputs: -1
```