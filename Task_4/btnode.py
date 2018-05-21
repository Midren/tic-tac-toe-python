class Node(object):
    """
    Represents a node for a tree.
    """

    def __init__(self, data):
        self.data = data
        self.childs = []
