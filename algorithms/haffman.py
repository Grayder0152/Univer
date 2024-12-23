from __future__ import annotations
import heapq
from typing import Optional


class Node:
    def __init__(self, char: Optional[str], freq: int):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other: Node) -> bool:
        return self.freq < other.freq


class HuffmanCoding:
    def __init__(self):
        self.codes = {}
        self.reverse_mapping = {}

    @staticmethod
    def build_frequency_table(text: str) -> dict[str, int]:
        return {char: text.count(char) for char in text}

    @staticmethod
    def build_huffman_tree(freq_table: dict[str, int]) -> Node:
        heap = [Node(char, freq) for char, freq in freq_table.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            merged = Node(None, left.freq + right.freq)
            merged.left = left
            merged.right = right

            heapq.heappush(heap, merged)

        return heap[0]

    def build_codes(self, root, current_code: str = "") -> None:
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char

        self.build_codes(root.left, f"{current_code}0")
        self.build_codes(root.right, f"{current_code}1")

    def encode(self, text: str) -> str:
        return ''.join(self.codes[char] for char in text)

    def decode(self, encoded_text: str) -> str:
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                decoded_text += self.reverse_mapping[current_code]
                current_code = ""

        return decoded_text

    def huffman_encoding(self, text: str) -> tuple[str, Node]:
        freq_table = self.build_frequency_table(text)
        huffman_tree_root = self.build_huffman_tree(freq_table)
        self.build_codes(huffman_tree_root)
        return self.encode(text), huffman_tree_root

    def huffman_decoding(self, encoded_text: str) -> str:
        return self.decode(encoded_text)


if __name__ == "__main__":
    sample_text = "If you still encounter the issue, it might be helpful"

    huffman = HuffmanCoding()
    sample_encoded_text, huffman_tree = huffman.huffman_encoding(sample_text)

    print(f"Original text: {sample_text}")
    print(f"Encoded text: {sample_encoded_text}")

    sample_decoded_text = huffman.huffman_decoding(sample_encoded_text)
    print(f"Decoded text: {sample_decoded_text}")
