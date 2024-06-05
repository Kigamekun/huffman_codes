from flask import Flask, render_template, request, send_file
import heapq
from collections import Counter
from PIL import Image
import io
import base64

app = Flask(__name__)

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    freq = Counter(text)
    heap = [HuffmanNode(char, freq) for char, freq in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

def generate_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}
    if node.char is not None:
        codebook[node.char] = prefix
    else:
        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)
    return codebook

def huffman_encode(text):
    root = build_huffman_tree(text)
    codebook = generate_codes(root)
    encoded_text = ''.join(codebook[char] for char in text)
    return codebook, encoded_text

# Simple image compression (resizing)
def compress_image(image_file, quality=20):
    image = Image.open(image_file)
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG", quality=quality)
    return buffered

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    text = request.form['text']
    codebook, encoded_text = huffman_encode(text)
    return render_template('index.html', encoded_text=encoded_text, codebook=codebook)

@app.route('/compress_image', methods=['POST'])
def compress_image_route():
    image_file = request.files['image']
    compressed_image_io = compress_image(image_file)
    compressed_image_io.seek(0) 
    image_name = "compressed_image.jpg"
    with open(image_name, "wb") as f:
        f.write(compressed_image_io.read())
    compressed_image_io.seek(0) 
    compressed_image_base64 = base64.b64encode(compressed_image_io.read()).decode()
    return render_template('index.html', compressed_image=compressed_image_base64, image_name=image_name)

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
