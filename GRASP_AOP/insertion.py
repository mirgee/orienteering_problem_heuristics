class Insertion(object):
    """Insertion candidate"""
    def __init__(self, arc, start_position, end_position, hval=None):
        self.arc = arc
        self.hval = hval
        self.add_cost = 0
        # This is position of the first node of the arc in the node list
        self.start_position = start_position
        self.end_position = end_position

    def __repr__(self):
        return str(self.arc[0], self.arc[1])