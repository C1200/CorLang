from results.RTResult import RTResult
from errors.RTError import RTError

class Type:
    def __init__(self):
        self.set_ctx()
        self.set_pos()
    def set_ctx(self, ctx=None):
        self.ctx = ctx
        return self
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    def add(self, other):
        return None, self.illegal_operation(other)
    def minus(self, other):
        return None, self.illegal_operation(other)
    def multiply(self, other):
        return None, self.illegal_operation(other)
    def divide(self, other):
        return None, self.illegal_operation(other)
    def power(self, other):
        return None, self.illegal_operation(other)
    def compare_ee(self, other):
        return None, self.illegal_operation(other)
    def compare_ne(self, other):
        return None, self.illegal_operation(other)
    def compare_lt(self, other):
        return None, self.illegal_operation(other)
    def compare_gt(self, other):
        return None, self.illegal_operation(other)
    def compare_lte(self, other):
        return None, self.illegal_operation(other)
    def compare_gte(self, other):
        return None, self.illegal_operation(other)
    def logic_and(self, other):
       return None, self.illegal_operation(other)
    def logic_or(self, other):
       return None, self.illegal_operation(other)
    def logic_not(self):
        return None, self.illegal_operation()
    def is_true(self):
        return False
    def copy(self):
        raise Exception("No copy method defined")
    def execute(self, args):
        return RTResult().failure(self.illegal_operation())
    def illegal_operation(self, other=None):
        if not other:
            other = self
        return RTError(
            self.pos_start,
            other.pos_end,
            "Illegal operation",
            self.ctx
        )