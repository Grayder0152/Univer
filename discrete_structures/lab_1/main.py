from deque import Deque

if __name__ == '__main__':
    print('Init deque')
    deq = Deque([1, 2, 3])
    print(deq)

    print('Add 4 to the front')
    deq.add_front(4)
    print(deq)

    print('Add 0 to the back')
    deq.add_back(0)
    print(deq)

    print('Reverse')
    deq.reverse()
    print(deq)

    print('Delete front item')
    deq.remove_front()
    print(deq)

    print('Delete back item')
    deq.remove_back()
    print(deq)

    print(f'Front item: {deq.get_front_item()}')
    print(f'Back item: {deq.get_back_item()}')
    print(f'Is empty: {deq.is_empty()}')
    print(f'Length: {deq.size()}')
    print(f'5 is in: {deq.is_contain(5)}')
    print(f'3 is in: {deq.is_contain(3)}')

    print('Swap front to back')
    deq.swap_front_and_back()
    print(deq)

    print('Clear')
    deq.clear()
    print(deq)
