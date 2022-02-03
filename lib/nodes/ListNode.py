class ListNode:
    def __init__(self, list_elems, pos_start, pos_end):
        self.list_elems = list_elems

        self.pos_start = pos_start
        self.pos_end = pos_end

    def __repr__(self):
        return f'{self.list_elems}'