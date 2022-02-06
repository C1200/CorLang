from Lexer import Lexer
from Parser import Parser
from Interpreter import Interpreter
from Context import Context
from SymbolTable import SymbolTable
from _types.Number import Number
from _types.BuiltInFunction import BuiltInFunction

global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number.null)
global_symbol_table.set("true", Number.true)
global_symbol_table.set("false", Number.false)
global_symbol_table.set("print", BuiltInFunction.print)
global_symbol_table.set("input", BuiltInFunction.input)
global_symbol_table.set("input_int", BuiltInFunction.input_int)
global_symbol_table.set("type", BuiltInFunction.type)
global_symbol_table.set("import", BuiltInFunction._import)
global_symbol_table.set("len", BuiltInFunction.len)
global_symbol_table.set("throw", BuiltInFunction.throw)

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.tokenize()
    if error:
        return None, error
    
    if len(tokens) == 1: # if only token is EOF
        return None, None
    
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error
    
    interpreter = Interpreter(run)
    ctx = Context("<program>")
    ctx.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, ctx)
    
    return result.value, result.error