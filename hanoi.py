class Stack():

    def __init__(self):
        self._container = []

    
    def push(self, item):
        self._container.append(item)
    

    def pop(self):
        return self._container.pop()
    

    def __repr__(self):
        return repr(self._container)
    

disc = 3

tower_a = Stack()
tower_b = Stack()
tower_c = Stack()
##initialize
for i in range(1, disc + 1):
    tower_a.push(i)

    
def hanoi(begin, end, temp, n):
    if n == 1:
        end.push(begin.pop())
    else:
        hanoi(begin, temp, end, n-1)
        hanoi(begin, end, temp, 1)    
        hanoi(temp, end, begin, n-1)


if __name__ == "__main__":
    print('A:' + str(tower_a))
    print('B:' + str(tower_b))
    print('C:' + str(tower_c))
    hanoi(tower_a, tower_c, tower_b, disc)
    print('A:' + str(tower_a))
    print('B:' + str(tower_b))
    print('C:' + str(tower_c))
