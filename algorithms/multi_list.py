from __future__ import annotations
from typing import Any, Optional


class Node:
    def __init__(self, value: Any = None):
        self.value = value
        self.next: Optional[Node] = None
        self.sublist: Optional[MultiList] = None


class MultiList:
    def __init__(self):
        self.head: Optional[Node] = None

    def add_element(self, value: Any) -> None:
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def add_sublist(self, index: int, values: list[Any]) -> None:
        current = self.head
        for i in range(index):
            if current:
                current = current.next
            else:
                return None

        if current:
            sublist = MultiList()
            for value in values:
                sublist.add_element(value)
            current.sublist = sublist

    def remove_element(self, value: Any) -> None:
        current = self.head
        previous = None
        while current:
            if current.value == value:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next
                return
            previous = current
            current = current.next

    def remove_sublist(self, index: int) -> None:
        current = self.head
        for i in range(index):
            if current:
                current = current.next
            else:
                return None

        if current and current.sublist:
            current.sublist = None

    def clear(self) -> None:
        self.head = None

    def copy(self) -> MultiList:
        new_list = MultiList()
        current = self.head
        while current:
            new_list.add_element(current.value)
            if current.sublist:
                sublist_copy = current.sublist.copy()
                new_list.add_sublist(new_list.size() - 1, sublist_copy.to_list())
            current = current.next
        return new_list

    def size(self) -> int:
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def to_list(self) -> list:
        result = []
        current = self.head
        while current:
            if current.sublist:
                result.append([current.value, current.sublist.to_list()])
            else:
                result.append(current.value)
            current = current.next
        return result


def main():
    multi_list = MultiList()

    print("Welcome to MultiList Manager!")
    while True:
        print("\nAvailable commands:")
        print("1 - Add element")
        print("2 - Add sublist")
        print("3 - Remove element")
        print("4 - Remove sublist")
        print("5 - Clear list")
        print("6 - Copy list")
        print("7 - Show list")
        print("8 - Exit")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            value = int(input("Enter the value to add: "))
            multi_list.add_element(value)
            print(f"Element {value} added.")
        elif choice == '2':
            index = int(input("Enter the index where to add the sublist: "))
            values = input("Enter values for sublist separated by space: ")
            sublist_values = [int(v) for v in values.split()]
            multi_list.add_sublist(index, sublist_values)
            print(f"Sublist {sublist_values} added at index {index}.")
        elif choice == '3':
            value = int(input("Enter the value to remove: "))
            multi_list.remove_element(value)
            print(f"Element {value} removed.")
        elif choice == '4':
            index = int(input("Enter the index of the element to remove sublist from: "))
            multi_list.remove_sublist(index)
            print(f"Sublist at index {index} removed.")
        elif choice == '5':
            multi_list.clear()
            print("MultiList cleared.")
        elif choice == '6':
            new_list = multi_list.copy()
            print("List copied. New list:")
            print(new_list.to_list())
        elif choice == '7':
            print("Current MultiList:")
            print(multi_list.to_list())
        elif choice == '8':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == '__main__':
    main()
    # multi_list = MultiList()
    # multi_list.add_element(1)
    # multi_list.add_element(2)
    # multi_list.add_sublist(1, [3, 4, 5])
    # multi_list.add_element(6)
    #
    # print(multi_list.to_list())
