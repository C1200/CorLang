import __main__
import os.path as path
from _types.BaseFunction import BaseFunction
from _types.Number import Number
from _types.String import String
from _types.List import List
from results.RTResult import RTResult
from errors.RTError import RTError

class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)
    def execute(self, args, interpreter, run):
        res = RTResult()
        ctx = self.make_new_ctx()
        self.run = run

        method_name = f"execute_{self.name}"
        method = getattr(self, method_name, self.no_execute)

        res.register(self.check_and_populate_args(method.arg_names, args, ctx))
        if res.should_return():
            return res

        return_value = res.register(method(ctx))
        if res.should_return():
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

    def execute_import(self, ctx):
        res = RTResult()
        fn = ctx.symbol_table.get("fn")
        
        if isinstance(fn, String):
            fn = fn.value

            if fn.startswith("std."):
                fn = path.join(path.abspath(path.dirname(__main__.__file__)), "std", fn[4:] + ".cor")
            
            try:
                with open(fn, "r") as f:
                    text = f.read()
            except Exception as e:
                return res.failure(RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Unable to load file \"{fn}\"\n" + str(e),
                    ctx
                ))

            _, error = self.run(fn, text)

            if error:
                return res.failure(RTError(
                    self.pos_start,
                    self.pos_end,
                    f"Encountered error while loading \"{fn}\"" + error.to_string(),
                    ctx
                ))

            return res.success(Number.null)
        else:
            return res.failure(RTError(
                self.pos_start,
                self.pos_end,
                "Argument 'fn' must be a string",
                ctx
            ))
    execute_import.arg_names = ["fn"]

    def execute_len(self, ctx):
        value = ctx.symbol_table.get("value")
        
        if isinstance(value, String):
            return RTResult().success(Number(len(value.value)))
        elif isinstance(value, List):
            return RTResult().success(Number(len(value.values)))
        else:
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                f"Cannot get length of a {type(value).__name__}",
                ctx
            ))
    execute_len.arg_names = ["value"]

    def execute_throw(self, ctx):
        errorText = ctx.symbol_table.get("error")
        if isinstance(errorText, String):
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                errorText,
                ctx
            ))
        else:
            return RTResult().failure(RTError(
                self.pos_start,
                self.pos_end,
                "Error text must be a string",
                ctx
            ))
    execute_throw.arg_names = ["error"]
    
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
BuiltInFunction._import = BuiltInFunction("import")
BuiltInFunction.len = BuiltInFunction("len")
BuiltInFunction.throw = BuiltInFunction("throw")