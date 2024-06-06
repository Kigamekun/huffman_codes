import heapq
import os
from collections import defaultdict, Counter

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freq_dict):
    heap = [HuffmanNode(char, freq) for char, freq in freq_dict.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)

    return heap[0]

def build_huffman_code(node, prefix="", codebook={}):
    if node:
        if node.char is not None:
            codebook[node.char] = prefix
        build_huffman_code(node.left, prefix + "0", codebook)
        build_huffman_code(node.right, prefix + "1", codebook)
    return codebook

def huffman_encode(data):
    freq_dict = Counter(data)
    huffman_tree = build_huffman_tree(freq_dict)
    huffman_code = build_huffman_code(huffman_tree)
    encoded_data = ''.join(huffman_code[char] for char in data)
    return encoded_data, huffman_tree

def huffman_decode(encoded_data, huffman_tree):
    decoded_data = []
    current_node = huffman_tree
    for bit in encoded_data:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right
        if current_node.char:
            decoded_data.append(current_node.char)
            current_node = huffman_tree
    return ''.join(decoded_data)
