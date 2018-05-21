from btnode import Node


class Tree:
    def __init__(self, root):
        self.data = root
        self.childs = []

    def print_all(self):
        for child in self.childs:
            if len(child.childs) == 0:
                print(child.data)
                print()
                continue

    def add_node(self, new_node):
        self.childs.append(new_node)
