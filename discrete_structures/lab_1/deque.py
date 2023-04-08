from typing import Any, Optional


class Deque:
    def __init__(self, items: Optional[list[Any]] = None):
        self.items: list[Any] = items or []

    def __repr__(self) -> str:
        return f"Deque elements: [{', '.join(map(str, self.items))}]\n"

    def __contains__(self, item: Any) -> bool:
        return item in self.items

    def __len__(self) -> int:
        return len(self.items)

    def is_empty(self):
        return self.items == []

    def add_front(self, item: Any):
        self.items.append(item)

    def add_back(self, item: Any):
        self.items.insert(0, item)

    def remove_front(self) -> Any:
        return self.items.pop()

    def remove_back(self) -> Any:
        return self.items.pop(0)

    def size(self) -> int:
        return len(self)

    def get_item(self, position: int) -> Any:
        if not isinstance(position, int):
            raise TypeError(f'Position type must be int not {type(position)}')
        return self.items[position]

    def get_front_item(self) -> Any:
        return self.get_item(-1)

    def get_back_item(self) -> Any:
        return self.get_item(0)

    def swap_front_and_back(self):
        self.items[0], self.items[-1] = self.items[-1], self.items[0]

    def reverse(self):
        self.items.reverse()

    def is_contain(self, item: Any) -> bool:
        return item in self

    def clear(self):
        self.items.clear()
