class CallNode:
    def __init__(self, to_call, arg_nodes):
        self.to_call = to_call
        self.arg_nodes = arg_nodes

        self.pos_start = to_call.pos_start
        
        if len(arg_nodes) > 0:
            self.pos_end = arg_nodes[len(arg_nodes) - 1].pos_end
        else:
            self.pos_end = to_call.pos_end