def linear_search(iterable, key):
    for item in iterable:
        if item == key:
            return True
    return False


def binary_search(sequence, key):
    low = 0
    high = len(sequence) - 1
    while low <= high:
        mid = (low + high) //2
        if sequence[mid] < key:
            low = mid + 1
        elif sequence[mid] > key:
            high = mid - 1
        else : 
            return True
    return False


class Stack():
    def __init__(self):
        self._container = []
    
    @property
    def empty(self):
        return not self._container

    def push(self, item):
        self._container.append(item)

    def pop(self):
        return self._container.pop()

    def __repr__(self):
        return repr(self._container)


class Node():
    def __init__(self, state, parent, cost = 0.0, heuristic = 0.0):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def dfs(initial, goal_test, successors):
    frontier = Stack()
    frontier.push(Node(initial, None))
    explored = {initial}

    while not frontier.empty:
        current_node = frontier.pop()
        current_state = current_node.state
        if goal_test(current_state):
            return current_node
        for child in successors(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
    return None


def bfs():
    return 0


def astar():
    return 0


def node_to_path(node):
    path = [node.state]
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path


if __name__ == "__main__":
    print(linear_search([1,2,3,4,5,6,7,8,9,10],8))
    print(binary_search([1,2,3,4,5,6,7,8,9,10],8))
    print(binary_search([1,2,3,4,5,6,7,8,9,10],99))
