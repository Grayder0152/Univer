class binomial_tree:
    def __init__(self, key):
        self.key = key
        self.children = []
        self.order = 0

    def add_at_end(self, t):
        self.children.append(t)
        self.order = self.order + 1


my_tree = []
print('Menu')
print('create <key>')
print('combine <index1> <index2>')
print('exit')
while True:
    option = input('What do you wish like to do? ').split()
    operation = option[0].strip().lower()
    if operation == 'create':
        key = int(option[1])
        b_tree = binomial_tree(key)
        my_tree.append(b_tree)
        print('Binomial tree has been created.')
    elif operation == 'combine':
        index_1 = int(option[1])
        index_2 = int(option[2])
        if my_tree[index_1].order == my_tree[index_2].order:
            my_tree[index_1].add_at_end(my_tree[index_2])
            del my_tree[index_2]
            print('Binomial trees have been combined.')
        else:
            print('Order of trees need to be the same to combine them.')
    elif operation == 'exit':
        print("Exit")
        break
    print('{:>8}{:>12}{:>8}'.format('Index', 'Root key', 'Order'))
    for index, t in enumerate(my_tree):
        print('{:8d}{:12d}{:8d}'.format(index, t.key, t.order))
