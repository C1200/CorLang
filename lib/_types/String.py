from _types.Type import Type
from _types.Number import Number

class String(Type):
    def __init__(self, value):
        super().__init__()
        self.value = value
    def add(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_ctx(self.ctx), None
        else:
            return None, Type.illegal_operation(self, other)
    def multiply(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_ctx(self.ctx), None
        else:
            return None, Type.illegal_operation(self, other)
    def compare_ee(self, other):
        if isinstance(other, String):
            return Number(int(self.value == other.value)).set_ctx(self.ctx), None
        else:
            return None, Type.illegal_operation(self, other)
    def compare_ne(self, other):
        if isinstance(other, String):
            return Number(int(self.value != other.value)).set_ctx(self.ctx), None
        else:
            return None, Type.illegal_operation(self, other)
    def logic_and(self, other):
        if isinstance(other, String):
            return Number(int(self.is_true() and other.is_true())).set_ctx(self.ctx), None
        else:
            return None, Type.illegal_operation(self, other)
    def logic_or(self, other):
        if isinstance(other, String):
            return Number(int(self.is_true() or other.is_true())).set_ctx(self.ctx), None
        else:
            return None, Type.illegal_operation(self, other)
    def logic_not(self):
        return Number(int(not self.is_true())).set_ctx(self.ctx), None
    def is_true(self):
        return self.value != ""
    def copy(self):
        copy = String(self.value)
        copy.set_ctx(self.ctx)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
    def __str__(self):
        return f"{self.value}"
    def __repr__(self):
        return f"\"{self.value}\""