from string_with_arrows import string_with_arrows

class Error:
    def __init__(self, pos_start, pos_end, name, details):
        self.name = name
        self.details = details
        self.pos_start = pos_start
        self.pos_end = pos_end
    def to_string(self):
        result = f"{self.name}: {self.details}\n"
        result += f"File {self.pos_start.fn}, line {self.pos_start.ln + 1}\n\n"
        result += string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result