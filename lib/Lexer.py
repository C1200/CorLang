from string import ascii_letters
from tokentypes import *
from Token import Token
from errors.InvalidCharError import InvalidCharError
from errors.ExpectedCharError import ExpectedCharError
from Position import Position

ALPHA = ascii_letters
NUMERIC = "0123456789"
ALPHANUMERIC = ALPHA + NUMERIC
KEYWORDS = [
    "var",  "and",   "or",
    "not",  "if",    "then",
    "elif", "else",  "for",
    "to",   "while", "step",
    "func", "exit",  "end"
]

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.currentChar = None
        self.advance()
    def advance(self):
        self.pos.advance(self.currentChar)
        if self.pos.idx < len(self.text):
            self.currentChar = self.text[self.pos.idx]
        else:
            self.currentChar = None
    def tokenize(self):
        tokens = []

        while self.currentChar != None:
            if self.currentChar in " \t":
                self.advance()
            elif self.currentChar in ";\n":
                tokens.append(Token(TT_NEWLINE, pos_start=self.pos))
                self.advance()
            elif self.currentChar in NUMERIC:
                tokens.append(self.make_number())
            elif self.currentChar in ALPHANUMERIC:
                tokens.append(self.make_identifier())
            elif self.currentChar in "\"'":
                tok, error = self.make_string(self.currentChar)
                if error:
                    return [], error
                tokens.append(tok)
            elif self.currentChar == "+":
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.currentChar == "-":
                tokens.append(self.make_minus())
                self.advance()
            elif self.currentChar == "*":
                tokens.append(Token(TT_MULTIP, pos_start=self.pos))
                self.advance()
            elif self.currentChar == "/":
                tokens.append(Token(TT_DIVIDE, pos_start=self.pos))
                self.advance()
            elif self.currentChar == "^":
                tokens.append(Token(TT_POWER, pos_start=self.pos))
                self.advance()
            elif self.currentChar == "%":
                tokens.append(Token(TT_MODULO, pos_start=self.pos))
                self.advance()
            elif self.currentChar == "(":
                tokens.append(Token(TT_LPARENT, pos_start=self.pos))
                self.advance()
            elif self.currentChar == ")":
                tokens.append(Token(TT_RPARENT, pos_start=self.pos))
                self.advance()
            elif self.currentChar == "[":
                tokens.append(Token(TT_LSQUARE, pos_start=self.pos))
                self.advance()
            elif self.currentChar == "]":
                tokens.append(Token(TT_RSQUARE, pos_start=self.pos))
                self.advance()
            elif self.currentChar == ",":
                tokens.append(Token(TT_COMMA, pos_start=self.pos))
                self.advance()
            elif self.currentChar == "=":
                tokens.append(self.make_equals())
                self.advance()
            elif self.currentChar == "<":
                tokens.append(self.make_lt())
                self.advance()
            elif self.currentChar == ">":
                tokens.append(self.make_gt())
                self.advance()
            elif self.currentChar == "!":
                tok, error = self.make_not_equals()
                if error:
                    return [], error
                tokens.append(tok)
            else:
                pos_start = self.pos.copy()
                char = self.currentChar
                self.advance()
                return [], InvalidCharError(pos_start, self.pos, f"'{char}'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None
    def make_number(self):
        pos_start = self.pos.copy()
        dp = 0
        number_str = ""

        while self.currentChar != None and self.currentChar in NUMERIC + ".":
            if self.currentChar == ".":
                if dp == 1: break
                dp += 1
                number_str += "."
            else:
                number_str += self.currentChar
            self.advance()

        if dp == 0:
            return Token(TT_INT, int(number_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(number_str), pos_start, self.pos)
    def make_string(self, quote_type):
        pos_start = self.pos.copy()
        string = ""
        escape_char = False
        self.advance()

        escape_chars = {
            "n": "\n",
            "t": "\t"
        }
        
        while self.currentChar != None and (self.currentChar != quote_type or escape_char):
            if escape_char:
                string += escape_chars.get(self.currentChar, self.currentChar)
                escape_char = False
            else:
                if self.currentChar == "\\":
                    escape_char = True
                else:
                    string += self.currentChar
            self.advance()

        self.advance()
        return Token(TT_STRING, string, pos_start, self.pos), None
    def make_identifier(self):
        pos_start = self.pos.copy()
        identifier = ""

        while self.currentChar != None and self.currentChar in ALPHANUMERIC + "_":
            identifier += self.currentChar
            self.advance()

        if identifier in KEYWORDS:
            return Token(TT_KEYWORD, identifier, pos_start, self.pos)
        else:
            return Token(TT_IDENTIFIER, identifier, pos_start, self.pos)
    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.currentChar == "=":
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None

        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "Expected '=' after '!'")
    def make_equals(self):
        tok_type = TT_EQ
        pos_start = self.pos.copy()
        self.advance()

        if self.currentChar == "=":
            self.advance()
            tok_type = TT_EE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
    def make_lt(self):
        tok_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()

        if self.currentChar == "=":
            self.advance()
            tok_type = TT_LTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
    def make_gt(self):
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()

        if self.currentChar == "=":
            self.advance()
            tok_type = TT_GTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)
    def make_minus(self):
        tok_type = TT_MINUS
        pos_start = self.pos.copy()
        self.advance()

        if self.currentChar == ">":
            tok_type = TT_ARROW
            self.advance()

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)