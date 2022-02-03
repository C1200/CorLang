class WhileNode:
    def __init__(self, condition_expr, expr):
        self.condition_expr = condition_expr
        self.expr = expr

        self.pos_start = condition_expr.pos_start
        self.pos_end = expr.pos_end