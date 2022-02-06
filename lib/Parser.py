from tokentypes import *
from results.ParseResult import ParseResult
from nodes.UnaryOpNode import UnaryOpNode
from nodes.NumberNode import NumberNode
from nodes.StringNode import StringNode
from nodes.BinOpNode import BinOpNode
from nodes.VarAssignNode import VarAssignNode
from nodes.VarAccessNode import VarAccessNode
from nodes.IfNode import IfNode
from nodes.ForNode import ForNode
from nodes.WhileNode import WhileNode
from nodes.FuncDefNode import FuncDefNode
from nodes.CallNode import CallNode
from nodes.ListNode import ListNode
from nodes.ReturnNode import ReturnNode
from nodes.BreakNode import BreakNode
from nodes.ContinueNode import ContinueNode
from errors.SyntaxError import SyntaxError

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = -1
        self.advance()

    def advance(self):
        self.idx += 1
        self.update_current_tok()
        return self.currentToken

    def reverse(self, amount=1):
        self.idx -= amount
        self.update_current_tok()
        return self.currentToken

    def update_current_tok(self):
        if self.idx >= 0 and self.idx < len(self.tokens):
            self.currentToken = self.tokens[self.idx]

    def parse(self):
        res = self.statements()
        if not res.error and self.currentToken.type != TT_EOF:
            return res.failure(SyntaxError(
                self.currentToken.pos_start,
                self.currentToken.pos_end,
                "Expected '+', '-', '*', '/', '^', '==', '!=', '<', '>', <=', '>=', 'and' or 'or'"
            ))
        return res

    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.currentToken.pos_start.copy()

        while self.currentToken.type == TT_NEWLINE:
            res.register_advance()
            self.advance()

        statement = res.register(self.statement())
        if res.error:
            return res
        statements.append(statement)

        more_statements = True
        
        while True:
            newlines = 0
            while self.currentToken.type == TT_NEWLINE:
                res.register_advance()
                self.advance()
                newlines += 1
            if newlines == 0:
                more_statements = False
            if not more_statements:
                break
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.to_reverse)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(ListNode(statements, pos_start, self.currentToken.pos_end.copy()))

    def statement(self):
        res = ParseResult()
        pos_start = self.currentToken.pos_start.copy()

        if self.currentToken.matches(TT_KEYWORD, "return"):
            res.register_advance()
            self.advance()
            
            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse)

            return res.success(ReturnNode(expr, pos_start, self.currentToken.pos_start.copy()))
            
        if self.currentToken.matches(TT_KEYWORD, "break"):
            res.register_advance()
            self.advance()
            return res.success(BreakNode(pos_start, self.currentToken.pos_start.copy()))

        if self.currentToken.matches(TT_KEYWORD, "continue"):
            res.register_advance()
            self.advance()
            return res.success(ContinueNode(pos_start, self.currentToken.pos_start.copy()))

        expr = res.register(self.expr())
        if res.error:
            return res.failure(SyntaxError(
                self.currentToken.pos_start,
                self.currentToken.pos_end,
                "Expected 'var', 'if', 'for', 'while', 'func', 'return', 'continue', 'break', int, float, string, identifier, '+', '-', '(' or '['"
            ))

        return res.success(expr)
        
    def atom(self):
        res = ParseResult()
        tok = self.currentToken

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advance()
            self.advance()
            return res.success(NumberNode(tok))
        elif tok.type == TT_STRING:
            res.register_advance()
            self.advance()
            return res.success(StringNode(tok))
        elif tok.type == TT_IDENTIFIER:
            res.register_advance()
            self.advance()
            return res.success(VarAccessNode(tok))
        elif tok.type == TT_LSQUARE:
            expr = res.register(self.list_expr())
            if res.error:
                return res
            return res.success(expr)
        elif tok.matches(TT_KEYWORD, "if"):
            expr = res.register(self.if_expr())
            if res.error:
                return res
            return res.success(expr)
        elif tok.matches(TT_KEYWORD, "for"):
            expr = res.register(self.for_expr())
            if res.error:
                return res
            return res.success(expr)
        elif tok.matches(TT_KEYWORD, "while"):
            expr = res.register(self.while_expr())
            if res.error:
                return res
            return res.success(expr)
        elif tok.matches(TT_KEYWORD, "func"):
            expr = res.register(self.func_def())
            if res.error:
                return res
            return res.success(expr)
        elif tok.type == TT_LPARENT:
            res.register_advance()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.currentToken.type == TT_RPARENT:
                res.register_advance()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(
                    SyntaxError(self.currentToken.pos_start,
                                self.currentToken.pos_end, "Expected ')'"))
        return res.failure(
            SyntaxError(tok.pos_start, tok.pos_end,
                        "Expected int, float, string, identifier, '+', '-', '(', '[', 'if', 'for', 'while' or 'func'"))

    def power(self):
        return self.bin_op(self.call, (TT_POWER, ), self.factor)

    def call(self):
        res = ParseResult()
        
        atom = res.register(self.atom())
        if res.error:
            return res

        if self.currentToken.type == TT_LPARENT:
            res.register_advance()
            self.advance()

            arg_nodes = []

            if self.currentToken.type == TT_RPARENT:
                res.register_advance()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(SyntaxError(
                        self.currentToken.pos_start,
                        self.currentToken.pos_end,
                        "Expected ')', 'var', 'if', 'for', 'while', 'func', int, float, string, identifier, '+', '-', '(', '[' or 'NOT'"
                    ))

                while self.currentToken.type == TT_COMMA:
                    res.register_advance()
                    self.advance()
                    
                    arg_nodes.append(res.register(self.expr()))
                    if res.error:
                        return res

                if self.currentToken.type != TT_RPARENT:
                    return res.failure(SyntaxError(
                        self.currentToken.pos_start,
                        self.currentToken.pos_end,
                        "Expected ',' or ')'"
                    ))

                res.register_advance()
                self.advance()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)
    
    def factor(self):
        res = ParseResult()
        tok = self.currentToken

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advance()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))
        return self.power()

    def term(self):
        return self.bin_op(self.factor, (TT_MULTIP, TT_DIVIDE, TT_MODULO))

    def comp_expr(self):
        res = ParseResult()

        if self.currentToken.matches(TT_KEYWORD, "not"):
            op_tok = self.currentToken
            res.register_advance()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error:
                return res

            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))
        if res.error:
            return res.failure(SyntaxError(
                self.currentToken.pos_start,
                self.currentToken.pos_end,
                "Expected int, float, string, identifier, '+', '-', '(', '[' or 'not'"
            ))

        return res.success(node)

    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def while_expr(self):
        res = ParseResult()

        if not self.currentToken.matches(TT_KEYWORD, "while"):
            return res.failure(SyntaxError(
                self.currentToken.pos_start,
                self.currentToken.pos_end,
                "Expected 'while'"
            ))

        res.register_advance()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.currentToken.matches(TT_KEYWORD, "then"):
            return res.failure(SyntaxError(
                self.currentToken.pos_start,
                self.currentToken.pos_end,
                "Expected 'then'"
            ))

        res.register_advance()
        self.advance()

        if self.currentToken.type == TT_NEWLINE:
            res.register_advance()
            self.advance()

            statements = res.register(self.statements())
            if res.error:
                return res

            if not self.currentToken.matches(TT_KEYWORD, "end"):
                return res.failure(SyntaxError(
                    self.currentToken.pos_start,
                    self.currentToken.pos_end,
                    "Expected 'end'"
                ))

            res.register_advance()
            self.advance()

            return res.success(WhileNode(condition, statements, True))

        expr = res.register(self.statement())
        if res.error:
            return res

        return res.success(WhileNode(condition, expr, False))

    def if_expr(self):
        res = ParseResult()
        all_cases = res.register(self.if_expr_cases("if"))
        if res.error:
            return res
        cases, else_case = all_cases
        return res.success(IfNode(cases, else_case))

    def elif_expr(self):
        return self.if_expr_cases("elif")

    def else_expr(self):
        res = ParseResult()
        else_case = None

        if self.currentToken.matches(TT_KEYWORD, "else"):
            res.register_advance()
            self.advance()

            if self.currentToken.type == TT_NEWLINE:
                res.register_advance()
                self.advance()

                statements = res.register(self.statements())
                if res.error:
                    return res
                else_case = (statements, True)

                if self.currentToken.matches(TT_KEYWORD, "end"):
                    res.register_advance()
                    self.advance()
                else:
                    return res.failure(SyntaxError(
                        self.currentToken.pos_start,
                        self.currentToken.pos_end,
                        "Expected 'end'"
                    ))
            else:
                expr = res.register(self.statement())
                if res.error:
                    return res
                else_case = (expr, False)

        return res.success(else_case)

    def elif_or_else_expr(self):
        res = ParseResult()
        cases, else_case = [], None

        if self.currentToken.matches(TT_KEYWORD, "elif"):
            all_cases = res.register(self.elif_expr())
            if res.error:
                return res
            cases, else_case = all_cases
        else:
            else_case = res.register(self.else_expr())
            if res.error:
                return res

        return res.success((cases, else_case))
    
    def if_expr_cases(self, keyword):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.currentToken.matches(TT_KEYWORD, keyword):
            return res.failure(SyntaxError(
                self.currentToken.pos_start,
                self.currentToken.pos_end,
                f"Expected '{keyword}'"
            ))

        res.register_advance()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if not self.currentToken.matches(TT_KEYWORD, "then"):
            return res.failure(SyntaxError(
                self.currentToken.pos_start,
                self.currentToken.pos_end,
                "Expected 'then'"
            ))

        res.register_advance()
        self.advance()

        if self.currentToken.type == TT_NEWLINE:
            res.register_advance()
            self.advance()

            statements = res.register(self.statements())
            if res.error:
                return res
            cases.append((condition, statements, True))

            if self.currentToken.matches(TT_KEYWORD, "end"):
                res.register_advance()
                self.advance()
            else:
                all_cases = res.register(self.elif_or_else_expr())
                if res.error:
                    return res
                new_cases, else_case = all_cases
                cases.extend(new_cases)
        else:
            expr = res.register(self.statement())
            if res.error:
                return res
            cases.append((condition, expr, False))

            all_cases = res.register(self.elif_or_else_expr())
            if res.error:
                return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)            

        return res.success((cases, else_case))

    def for_expr(self):
        res = ParseResult()

        if not self.currentToken.matches(TT_KEYWORD, "for"):
            return res.failure(SyntaxError(
                self.currentToken.pos_start,
                self.currentToken.pos_end,
                "Expected 'for'"
            ))

        res.register_advance()
        self.advance()

        if self.currentToken.type != TT_IDENTIFIER:
            return res.failure(SyntaxError(
                self.currentToken.pos_start,
                self.currentToken.pos_end,
                "Expected identifier"
            ))

        var_name = self.currentToken
        res.register_advance()
        self.advance()

        if self.currentToken.type != TT_EQ:
            return res.failure(SyntaxError(
                self.currentToken.pos_start,
                self.currentToken.pos_end,
                "Expected '='"
            ))

        res.register_advance()
        self.advance()

        from_expr = res.register(self.expr())
        if res.error:
            return res

        if not self.currentToken.matches(TT_KEYWORD, "to"):
            return res.failure(SyntaxError(
                self.currentToken.pos_start,
                self.currentToken.pos_end,
                "Expected 'to'"
            ))

        res.register_advance()
        self.advance()
        
        to_expr = res.register(self.expr())
        if res.error:
            return res

        step_expr = None
        if self.currentToken.matches(TT_KEYWORD, "step"):
            res.register_advance()
            self.advance()
            
            step_expr = res.register(self.expr())
            if res.error:
                return res

        if not self.currentToken.matches(TT_KEYWORD, "then"):
            return res.failure(SyntaxError(
                self.currentToken.pos_start,
                self.currentToken.pos_end,
                "Expected 'then'"
            ))

        res.register_advance()
        self.advance()

        if self.currentToken.type == TT_NEWLINE:
            res.register_advance()
            self.advance()

            statements = res.register(self.statements())
            if res.error:
                return res

            if not self.currentToken.matches(TT_KEYWORD, "end"):
                return res.failure(SyntaxError(
                    self.currentToken.pos_start,
                    self.currentToken.pos_end,
                    "Expected 'end'"
                ))

            res.register_advance()
            self.advance()

            return res.success(ForNode(var_name, from_expr, to_expr, step_expr, statements, True))

        expr = res.register(self.statement())
        if res.error:
            return res

        return res.success(ForNode(var_name, from_expr, to_expr, step_expr, expr, False))

    def list_expr(self):
        res = ParseResult()
        pos_start = self.currentToken.pos_start.copy()

        if self.currentToken.type != TT_LSQUARE:
            return res.failure(SyntaxError(
                self.currentToken.pos_start,
                self.currentToken.pos_end,
                "Expected '['"
            ))

        res.register_advance()
        self.advance()

        list_elems = []
        
        if self.currentToken.type == TT_RSQUARE:
            res.register_advance()
            self.advance()
        else:
            list_elems.append(res.register(self.expr()))
            if res.error:
                return res.failure(SyntaxError(
                    self.currentToken.pos_start,
                    self.currentToken.pos_end,
                    "Expected ']', 'var', 'if', 'for', 'while', 'func', int, float, string, identifier, '+', '-', '(', '[' or 'NOT'"
                ))

            while self.currentToken.type == TT_COMMA:
                res.register_advance()
                self.advance()
                    
                list_elems.append(res.register(self.expr()))
                if res.error:
                    return res

            if self.currentToken.type != TT_RSQUARE:
                return res.failure(SyntaxError(
                    self.currentToken.pos_start,
                    self.currentToken.pos_end,
                    "Expected ',' or ']'"
                ))

            res.register_advance()
            self.advance()
        return res.success(ListNode(list_elems, pos_start, self.currentToken.pos_end.copy()))
    
    def expr(self):
        res = ParseResult()

        if self.currentToken.matches(TT_KEYWORD, "var"):
            res.register_advance()
            self.advance()

            if self.currentToken.type != TT_IDENTIFIER:
                res.failure(
                    SyntaxError(self.currentToken.pos_start,
                                self.currentToken.pos_end,
                                "Expected identifier"))

            var_name = self.currentToken
            res.register_advance()
            self.advance()

            if self.currentToken.type != TT_EQ:
                res.failure(
                    SyntaxError(self.currentToken.pos_start,
                                self.currentToken.pos_end, "Expected '='"))

            res.register_advance()
            self.advance()

            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))
        node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, "and"), (TT_KEYWORD, "or"))))
        if res.error:
            return res.failure(SyntaxError(
                self.currentToken.pos_start,
                self.currentToken.pos_end,
                "Expected 'var', 'if', 'for', 'while', 'func', int, float, string, identifier, '+', '-', '(' or '['"
            ))

        return res.success(node)

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())

        if res.error:
            return res

        while self.currentToken.type in ops or (self.currentToken.type, self.currentToken.value) in ops:
            optok = self.currentToken
            res.register_advance()
            self.advance()
            right = res.register(func_b())
            if res.error:
                return res
            left = BinOpNode(left, optok, right)

        return res.success(left)
    def func_def(self):
        res = ParseResult()

        if not self.currentToken.matches(TT_KEYWORD, "func"):
            return res.failure(SyntaxError(
                self.currentToken.pos_start,
                self.currentToken.pos_end,
                "Expected 'func'"
            ))

        res.register_advance()
        self.advance()

        if self.currentToken.type == TT_IDENTIFIER:
            var_name_tok = self.currentToken
            res.register_advance()
            self.advance()
            if self.currentToken.type != TT_LPARENT:
                return res.failure(SyntaxError(
                    self.currentToken.pos_start,
                    self.currentToken.pos_end,
                    "Expected '('"
                ))
        else:
            var_name_tok = None
            if self.currentToken.type != TT_LPARENT:
                return res.failure(SyntaxError(
                    self.currentToken.pos_start,
                    self.currentToken.pos_end,
                    "Expected identifier or '('"
                ))

        res.register_advance()
        self.advance()

        arg_name_toks = []

        if self.currentToken.type == TT_IDENTIFIER:
            arg_name_toks.append(self.currentToken)
            res.register_advance()
            self.advance()

            while self.currentToken.type == TT_COMMA:
                res.register_advance()
                self.advance()

                if self.currentToken.type != TT_IDENTIFIER:
                    return res.failure(SyntaxError(
                        self.currentToken.pos_start,
                        self.currentToken.pos_end,
                        "Expected identifier"
                    ))

                arg_name_toks.append(self.currentToken)
                res.register_advance()
                self.advance()

            if self.currentToken.type != TT_RPARENT:
                return res.failure(SyntaxError(
                    self.currentToken.pos_start,
                    self.currentToken.pos_end,
                    "Expected ',' or ')'"
                ))
        else:
            if self.currentToken.type != TT_RPARENT:
                return res.failure(SyntaxError(
                    self.currentToken.pos_start,
                    self.currentToken.pos_end,
                    "Expected identifier or ')'"
                ))

        res.register_advance()
        self.advance()

        if self.currentToken.type == TT_ARROW:
            res.register_advance()
            self.advance()
    
            to_return = res.register(self.expr())
            if res.error:
                return res
    
            return res.success(FuncDefNode(var_name_tok, arg_name_toks, to_return, True))

        if self.currentToken.type != TT_NEWLINE:
            return res.failure(SyntaxError(
                self.currentToken.pos_start,
                self.currentToken.pos_end,
                "Expected '->' or newline"
            ))

        res.register_advance()
        self.advance()

        statements = res.register(self.statements())
        if res.error:
            return res

        if not self.currentToken.matches(TT_KEYWORD, "end"):
            return res.failure(SyntaxError(
                self.currentToken.pos_start,
                self.currentToken.pos_end,
                "Expected 'end'"
            ))

        res.register_advance()
        self.advance()

        return res.success(FuncDefNode(var_name_tok, arg_name_toks, statements, False))