class WhileNode:
    def __init__(self, condition_expr, expr, return_null):
        self.condition_expr = condition_expr
        self.expr = expr
        self.return_null = return_null

        self.pos_start = condition_expr.pos_start
        self.pos_end = expr.pos_end