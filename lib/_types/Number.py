from _types.Type import Type
from errors.RTError import RTError

class Number(Type):
    def __init__(self, value):
        super().__init__()
        self.value = value
    def add(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_ctx(self.ctx), None
        else:
            return None, Type.illegal_operation(self, other)
    def minus(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_ctx(self.ctx), None
        else:
            return None, Type.illegal_operation(self, other)
    def multiply(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_ctx(self.ctx), None
        else:
            return None, Type.illegal_operation(self, other)
    def divide(self, other):
        if isinstance(other, Number):
            if (other.value == 0):
                return None, RTError(
                    other.pos_start,
                    other.pos_end,
                    "Division by zero",
                    self.ctx
                )
            return Number(self.value / other.value).set_ctx(self.ctx), None
        else:
            return None, Type.illegal_operation(self, other)
    def power(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_ctx(self.ctx), None
        else:
            return None, Type.illegal_operation(self, other)
    def modulo(self, other):
        if isinstance(other, Number):
            if (other.value == 0):
                return None, RTError(
                    other.pos_start,
                    other.pos_end,
                    "Division by zero",
                    self.ctx
                )
            return Number(self.value % other.value).set_ctx(self.ctx), None
        else:
            return None, Type.illegal_operation(self, other)
    def compare_ee(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_ctx(self.ctx), None
        else:
            return None, Type.illegal_operation(self, other)
    def compare_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_ctx(self.ctx), None
        else:
            return None, Type.illegal_operation(self, other)
    def compare_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_ctx(self.ctx), None
        else:
            return None, Type.illegal_operation(self, other)
    def compare_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_ctx(self.ctx), None
        else:
            return None, Type.illegal_operation(self, other)
    def compare_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_ctx(self.ctx), None
        else:
            return None, Type.illegal_operation(self, other)
    def compare_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_ctx(self.ctx), None
        else:
            return None, Type.illegal_operation(self, other)
    def logic_and(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_ctx(self.ctx), None
        else:
            return None, Type.illegal_operation(self, other)
    def logic_or(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_ctx(self.ctx), None
        else:
            return None, Type.illegal_operation(self, other)
    def logic_not(self):
        return Number(1 if self.value == 0 else 0).set_ctx(self.ctx), None
    def is_true(self):
        return self.value != 0
    def copy(self):
        copy = Number(self.value)
        copy.set_ctx(self.ctx)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
    def __repr__(self):
        return str(self.value)

Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)