from _types.BaseFunction import BaseFunction
from _types.Number import Number
from results.RTResult import RTResult

class Function(BaseFunction):
    def __init__(self, name, expr, arg_names, auto_return):
        super().__init__(name)
        self.expr = expr
        self.arg_names = arg_names
        self.auto_return = auto_return
    def execute(self, args, interpreter, run):
        res = RTResult()
        ctx = self.make_new_ctx()

        res.register(self.check_and_populate_args(self.arg_names, args, ctx))
        if res.should_return():
            return res

        value = res.register(interpreter.visit(self.expr, ctx))
        if res.should_return() and res.func_return_value == None:
            return res

        return_value = (value if self.auto_return else None) or res.func_return_value or Number.null
        
        return res.success(return_value)
    def copy(self):
        copy = Function(self.name, self.expr, self.arg_names, self.auto_return)
        copy.set_ctx(self.ctx)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
    def __repr__(self):
        return f"<function {self.name}>"