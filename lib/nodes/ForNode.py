class ForNode:
    def __init__(self, var_name_tok, from_expr, to_expr, step_expr, expr):
        self.var_name_tok = var_name_tok
        self.from_expr = from_expr
        self.to_expr = to_expr
        self.step_expr = step_expr
        self.expr = expr

        self.pos_start = var_name_tok.pos_start
        self.pos_end = expr.pos_end