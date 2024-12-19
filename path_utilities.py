class Node:
    def __init__(self, parent, state, action):
        self.parent = parent
        self.state = state
        self.action = action
        self.cost = 0


class StackFrontier:
    def __init__(self):
        self.frontier = list()
        self.explored = set()

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("Empty frontier.")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier.")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node