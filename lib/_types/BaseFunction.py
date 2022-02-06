from _types.Type import Type
from Context import Context
from SymbolTable import SymbolTable
from results.RTResult import RTResult
from errors.RTError import RTError

class BaseFunction(Type):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"
    def make_new_ctx(self):
        ctx = Context(self.name, self.ctx, self.pos_start)
        ctx.symbol_table = SymbolTable(ctx.parent.symbol_table)
        return ctx
    def check_args(self, arg_names, args):
        res = RTResult()
        
        if len(args) != len(arg_names):
            return res.failure(RTError(
                self.pos_start,
                self.pos_end,
                f"Function '{self.name}' expected {len(arg_names)} arguments, instead got {len(args)}",
                self.ctx
            ))

        return res.success(None)
    def populate_args(self, arg_names, args, ctx):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_ctx(ctx)
            ctx.symbol_table.set(arg_name, arg_value)
    def check_and_populate_args(self, arg_names, args, ctx):
        res = RTResult()
        res.register(self.check_args(arg_names, args))
        if res.should_return():
            return res
        self.populate_args(arg_names, args, ctx)
        return res.success(None)