from _types.Type import Type
from _types.Number import Number
from errors.RTError import RTError

class List(Type):
    def __init__(self, values):
        super().__init__()
        self.values = values
    # append to list
    def add(self, other):
        new_list = self.copy()
        new_list.values.append(other)
        return new_list, None
    # remove from list
    def minus(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.values.pop(other.value)
                return new_list, None
            except:
                return None, RTError(
                    other.pos_start,
                    other.pos_end,
                    f"Element at position {other.value} does not exist",
                    self.ctx
                )
        else:
            return None, Type.illegal_operation(self, other)
    # concat lists
    def compare_lte(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.values.extend(other.values)
            return new_list, None
        else:
            return None, Type.illegal_operation(self, other)
    # get element
    def compare_gt(self, other):
        if isinstance(other, Number):
            try:
                return self.values[other.value], None
            except:
                return None, RTError(
                    other.pos_start,
                    other.pos_end,
                    f"Element at position {other.value} does not exist",
                    self.ctx
                )
        else:
            return None, Type.illegal_operation(self, other)
    def copy(self):
        copy = List(self.values)
        copy.set_ctx(self.ctx)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
    def __repr__(self):
        x = ", ".join([str(repr(value)) for value in self.values])
        return f"[ {x} ]"