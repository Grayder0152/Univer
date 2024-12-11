class PreTreeNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class PreTree:
    def __init__(self):
        self.root = PreTreeNode()

    def insert(self, word: str):
        """
        Вставка слова в дерево.
        :param word: Слово для вставки.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = PreTreeNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """
        Перевірка наявності слова в дереві.
        :param word: Слово для пошуку.
        :return: True, якщо слово є в дереві, інакше False.
        """
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """
        Перевірка, чи існує слово в дереві з певним префіксом.
        :param prefix: Префікс для перевірки.
        :return: True, якщо є хоча б одне слово з таким префіксом.
        """
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def search_with_prefix(self, prefix: str) -> list:
        """
        Пошук усіх слів, які починаються з заданого префікса.
        :param prefix: Префікс для пошуку.
        :return: Список слів із заданим префіксом.
        """

        def dfs(node, path, results):
            if node.is_end_of_word:
                results.append("".join(path))
            for char, child_node in node.children.items():
                dfs(child_node, path + [char], results)

        node = self.root
        for char in prefix:
            if char not in node.children:
                return []  # Якщо префікс не знайдено
            node = node.children[char]

        results = []
        dfs(node, list(prefix), results)
        return results

    def delete(self, word: str) -> bool:
        """
        Видалення слова з дерева.
        :param word: Слово для видалення.
        :return: True, якщо слово успішно видалено, інакше False.
        """

        def _delete(node, word, depth):
            if depth == len(word):
                if not node.is_end_of_word:
                    return False
                node.is_end_of_word = False
                return len(node.children) == 0

            char = word[depth]
            if char not in node.children:
                return False

            can_delete_child = _delete(node.children[char], word, depth + 1)
            if can_delete_child:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end_of_word

            return False

        return _delete(self.root, word, 0)


if __name__ == '__main__':
    tree = PreTree()

    tree.insert("apple")
    tree.insert("app")
    tree.insert("bat")
    tree.insert("ball")

    print(tree.search("app"))
    print(tree.search("appl"))

    print(tree.starts_with("app"))
    print(tree.starts_with("bat"))
    print(tree.starts_with("cat"))

    tree.delete("app")
    print(tree.search("app"))
    print(tree.search("apple"))

    print(tree.search_with_prefix("app"))
    print(tree.search_with_prefix("ba"))
    print(tree.search_with_prefix("cat"))