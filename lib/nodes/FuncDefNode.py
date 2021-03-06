class FuncDefNode:
    def __init__(self, var_name_tok, arg_name_toks, expr, auto_return):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.expr = expr
        self.auto_return = auto_return

        if var_name_tok:
            self.pos_start = var_name_tok.pos_start
        elif len(arg_name_toks) > 0:
            self.pos_start = arg_name_toks[0].pos_start
        else:
            self.pos_start = expr.pos_start
            
        self.pos_end = expr.pos_end