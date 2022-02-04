from _types.BaseFunction import BaseFunction
from _types.Number import Number
from results.RTResult import RTResult

class Function(BaseFunction):
    def __init__(self, name, expr, arg_names, return_null):
        super().__init__(name)
        self.expr = expr
        self.arg_names = arg_names
        self.return_null = return_null
    def execute(self, args, interpreter):
        res = RTResult()
        ctx = self.make_new_ctx()

        res.register(self.check_and_populate_args(self.arg_names, args, ctx))
        if res.error:
            return res

        value = res.register(interpreter.visit(self.expr, ctx))
        if res.error:
            return res

        return res.success(Number.null if self.return_null else value)
    def copy(self):
        copy = Function(self.name, self.expr, self.arg_names, self.return_null)
        copy.set_ctx(self.ctx)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
    def __repr__(self):
        return f"<function {self.name}>"