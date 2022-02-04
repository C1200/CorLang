from results.RTResult import RTResult
from errors.RTError import RTError
from _types.Number import Number
from _types.Function import Function
from _types.String import String
from _types.List import List
from tokentypes import *

class Interpreter:
    def visit(self, node, ctx):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit)
        return method(node, ctx)
    def no_visit(self, node, ctx):
        raise Exception(f"No visit_{type(node).__name__} method defined")
    def visit_NumberNode(self, node, ctx):
        return RTResult().success(
            Number(node.tok.value).set_ctx(ctx).set_pos(node.pos_start, node.pos_end)
        )
    def visit_StringNode(self, node, ctx):
        return RTResult().success(
            String(node.tok.value).set_ctx(ctx).set_pos(node.pos_start, node.pos_end)
        )
    def visit_VarAccessNode(self, node, ctx):
        res = RTResult();
        var_name = node.var_name_tok.value
        value = ctx.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(
                node.pos_start,
                node.pos_end,
                f"'{var_name}' is not defined",
                ctx
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end).set_ctx(ctx)
        return res.success(value)
    def visit_VarAssignNode(self, node, ctx):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, ctx))
        if res.error:
            return res
        ctx.symbol_table.set(var_name, value)
        return res.success(value)
    def visit_BinOpNode(self, node, ctx):
        res = RTResult()
        
        left = res.register(self.visit(node.left_node, ctx))
        if res.error:
            return res
            
        right = res.register(self.visit(node.right_node, ctx))
        if res.error:
            return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.add(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.minus(right)
        elif node.op_tok.type == TT_MULTIP:
            result, error = left.multiply(right)
        elif node.op_tok.type == TT_DIVIDE:
            result, error = left.divide(right)
        elif node.op_tok.type == TT_POWER:
            result, error = left.power(right)
        elif node.op_tok.type == TT_MODULO:
            result, error = left.modulo(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.compare_ee(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.compare_ne(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.compare_lt(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.compare_gt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.compare_lte(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.compare_gte(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.compare_ee(right)
        elif node.op_tok.matches(TT_KEYWORD, "and"):
            result, error = left.logic_and(right)
        elif node.op_tok.matches(TT_KEYWORD, "or"):
            result, error = left.logic_or(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))
    def visit_UnaryOpNode(self, node, ctx):
        res = RTResult()
        value = res.register(self.visit(node.node, ctx))
        if res.error:
            return res
            
        error = None
        
        if node.op_tok.type == TT_MINUS:
            value, error = value.multiply(Number(-1))
        elif node.op_tok.matches(TT_KEYWORD, "not"):
            value, error = value.logic_not()

        if error:
            return res.failure(error)
        else:
            return res.success(value.set_pos(node.pos_start, node.pos_end))
    def visit_IfNode(self, node, ctx):
        res = RTResult()

        for condition, expr in node.cases:
            condition_value = res.register(self.visit(condition, ctx))
            if res.error:
                return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, ctx))
                if res.error:
                    return res
                return res.success(expr_value)

        if node.else_case:
            else_value = res.register(self.visit(node.else_case, ctx))
            if res.error:
                return res
            return res.success(else_value)

        return res.success(None)
    def visit_WhileNode(self, node, ctx):
        res = RTResult()
        values = []

        while True:
            condition = res.register(self.visit(node.condition_expr, ctx))
            if res.error:
                return res

            if not condition.is_true():
                break

            values.append(res.register(self.visit(node.expr, ctx)))
            if res.error:
                return res

        return res.success(
            List(values).set_ctx(ctx).set_pos(node.pos_start, node.pos_end)
        )
    def visit_ForNode(self, node, ctx):
        res = RTResult()
        values = []

        from_value = res.register(self.visit(node.from_expr, ctx))
        if res.error:
            return res

        to_value = res.register(self.visit(node.to_expr, ctx))
        if res.error:
            return res

        if node.step_expr:
            step_value = res.register(self.visit(node.step_expr, ctx))
            if res.error:
                return res
        else:
            step_value = Number(1)

        i = from_value.value

        if step_value.value >= 0:
            condition = lambda: i < to_value.value
        else:
            condition = lambda: i > to_value.value

        while condition():
            ctx.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value

            values.append(res.register(self.visit(node.expr, ctx)))
            if res.error:
                return res

        return res.success(
            List(values).set_ctx(ctx).set_pos(node.pos_start, node.pos_end)
        )
    def visit_FuncDefNode(self, node, ctx):
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        expr = node.expr
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, expr, arg_names).set_ctx(ctx).set_pos(node.pos_start, node.pos_end)

        if node.var_name_tok:
            ctx.symbol_table.set(func_name, func_value)

        return res.success(func_value)
    def visit_CallNode(self, node, ctx):
        res = RTResult()
        args = []

        to_call = res.register(self.visit(node.to_call, ctx))
        if res.error:
            return res
        to_call = to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, ctx)))
            if res.error:
                return res

        return_value = res.register(to_call.execute(args, Interpreter()))
        if res.error:
            return res
        return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_ctx(ctx)

        return res.success(return_value)
    def visit_ListNode(self, node, ctx):
        res = RTResult()
        list_elems = []

        for list_elem in node.list_elems:
            list_elems.append(res.register(self.visit(list_elem, ctx)))
            if res.error:
                return res

        return res.success(
            List(list_elems).set_ctx(ctx).set_pos(node.pos_start, node.pos_end)
        )