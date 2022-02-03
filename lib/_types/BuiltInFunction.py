from _types.BaseFunction import BaseFunction
from _types.Number import Number
from _types.String import String
from results.RTResult import RTResult

class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)
    def execute(self, args, interpreter):
        res = RTResult()
        ctx = self.make_new_ctx()

        method_name = f"execute_{self.name}"
        method = getattr(self, method_name, self.no_execute)

        res.register(self.check_and_populate_args(method.arg_names, args, ctx))
        if res.error:
            return res

        return_value = res.register(method(ctx))
        if res.error:
            return res

        return res.success(return_value)
    def no_execute(self, node, ctx):
        raise Exception(f"No execute_{self.name} function defined")

    # Start built-in functions
        
    def execute_print(self, ctx):
        print(str(ctx.symbol_table.get("value")))
        return RTResult().success(Number.null)
    execute_print.arg_names = ["value"]

    def execute_input(self, ctx):
        text = input(ctx.symbol_table.get("value"))
        return RTResult().success(String(text))
    execute_input.arg_names = ["value"]

    def execute_input_int(self, ctx):
        while True:
            text = input(ctx.symbol_table.get("value"))
            try:
                num = int(text)
                break
            except:
                print(f"'{text}' could not be converted to int")
        return RTResult().success(Number(num))
    execute_input_int.arg_names = ["value"]

    def execute_type(self, ctx):
        type_of_value = type(ctx.symbol_table.get("value")).__name__
        return RTResult().success(String(type_of_value))
    execute_type.arg_names = ["value"]
    
    # End built-in functions
        
    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_ctx(self.ctx)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
    def __repr__(self):
        return f"<built-in function {self.name}>"

BuiltInFunction.print = BuiltInFunction("print")
BuiltInFunction.input = BuiltInFunction("input")
BuiltInFunction.input_int = BuiltInFunction("input_int")
BuiltInFunction.type = BuiltInFunction("type")