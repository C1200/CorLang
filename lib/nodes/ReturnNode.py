class ReturnNode:
    def __init__(self, to_return, pos_start, pos_end):
        self.to_return = to_return

        self.pos_start = pos_start
        self.pos_end = pos_end