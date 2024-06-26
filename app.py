from flask import Flask, render_template,flash, request, redirect, url_for, send_file
import os
import time
from functools import reduce
# from werkzeug.utils import secure_filename
import secrets
secret_key = secrets.token_hex(16)
import json
print(secret_key)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/uploads'
app.config['SECRET_KEY'] = secret_key

class HuffmanCoding:
    def __init__(self, path, file, export_file=None):
        self.export_file = export_file
        self.path = path + file
        self.dictionary = None
        self.text = None
        self.current_directory = path
        self.file_name = file[len(file) - file[::-1].index('/'):len(file) - file[::-1].index('.') - 1]
        if self.export_file is None:
            self.export_file = '/encoded/' + \
                            self.file_name + \
                            '_comp.bin'

    def set_dictionary(self):
        self.dictionary = self.frequency_alphabet_init()

    def set_text(self):
        self.text = self.path_to_string()

    def path_to_string(self):
        with open(self.path, "r") as file:
            return reduce(lambda x, y: x + y, file.readlines())

    def frequency_alphabet(self):
        # mengubah teks menjadi list alfabet beserta dengan jumlah frekuensinya yang di zip menjadi list
        self.set_text()
        list_alphabet = dict()
        for letter in self.text:
            if letter in list_alphabet.keys():
                list_alphabet[letter] += 1
            else:
                list_alphabet[letter] = 1
        list_alphabet = list(zip(list_alphabet.keys(), list_alphabet.values()))
        return list_alphabet

    def sorted_alphabet(self, list_alphabet=None):
        # Mengurutkan daftar alfabet berdasarkan frekuensi kemunculan.
        if list_alphabet is None:
            list_alphabet = self.frequency_alphabet()
        list_frequency_values = sorted(list(set([value[1] for value in list_alphabet])), reverse=True)

        list_alphabet_temp_ascii = []
        list_alphabet_temp_other = []
        list_alphabet_final = []

        for value_frequency in list_frequency_values:
            list_alphabet_temp_ascii = sorted(
                [element[0] for element in list_alphabet if element[1] == value_frequency and type(element[0]) == str],
                key=ord, reverse=True)
            list_alphabet_temp_other = [element[0] for element in list_alphabet if
                                        element[1] == value_frequency and not type(element[0]) == str]
            list_alphabet_temp_ascii = [(element, value_frequency) for element in list_alphabet_temp_ascii]
            list_alphabet_temp_other = [(element, value_frequency) for element in list_alphabet_temp_other]
            list_alphabet_final += list_alphabet_temp_ascii
            list_alphabet_final += list_alphabet_temp_other

        # list_alphabet_temp_ascii: Menyimpan karakter ASCII yang diurutkan berdasarkan frekuensi.
        # list_alphabet_temp_other: Menyimpan karakter non-ASCII yang diurutkan berdasarkan frekuensi.
        # list_alphabet_final: Menyimpan daftar akhir yang sudah diurutkan.
        return list_alphabet_final

    def binary_list(self):
        # Pembautan Pohon Huffman
        alphabet = self.sorted_alphabet()
        print(alphabet)

        while len(alphabet) > 2:
            first_part, second_part = alphabet[:-2], alphabet[-2:]
            if len(alphabet) == 2:
                new_node = (second_part, 0)
            else:
                new_node = (second_part, second_part[0][1] + second_part[1][1])
            first_part.append(new_node)
            alphabet = self.sorted_alphabet(first_part)
        return alphabet

    def binary_alphabet(self, binary_list=None, binary_dict=None, binary_code=''):
        if binary_list is None:
            binary_list = self.binary_list()
        if binary_dict is None:
            binary_dict = dict()
        for element in binary_list:
            binary_code_init = binary_code
            print('el',element)
            if not type(element) == int:
                if type(element[1]) == int:
                    binary_value_to_add = str(binary_list.index(element))
                    binary_value_to_add = '1' if binary_value_to_add == '0' else '0'
                else:
                    binary_value_to_add = ''
                if type(element[0]) == str:
                    binary_dict[element[0]] = (binary_code_init + binary_value_to_add)
                else:
                    self.binary_alphabet(element, binary_dict, binary_code_init + binary_value_to_add)
        print(binary_dict)
        return binary_dict

    def encode_file_bin(self, destination=None):
        if destination is None:
            destination = self.current_directory + self.export_file

        binary_alphabet = self.binary_alphabet()
        binary_text = ''

        for letter in self.text:
            binary_text += binary_alphabet[letter]
        length_binary_text = len(binary_text)

        file = open(destination, "wb")
        # merubah teks menjadi biner dan dituliskann ke dalam file destinasi dengan perinta wb / write binary
        index_begin = 0
        while index_begin + 9 <= length_binary_text:
            octet = binary_text[index_begin:index_begin + 8]
            index_begin += 8
            file.write(int(octet, 2).to_bytes(len(octet) // 8, byteorder='big'))
        octet = binary_text[index_begin:] + '0' * (8 - len(binary_text[index_begin:]))
        file.write(int(octet, 2).to_bytes(-(-len(octet) // 8), byteorder='big'))

        file.close()

    def decode(self, encoded_file=None, destination=None):
        if destination is None:
            destination = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + '/encoded/decode.txt'
        if encoded_file is None:
            encoded_file = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + self.export_file
        with open(encoded_file, "rb") as file:
            encoded_text = reduce(lambda x, y: x + y, file.readlines())
            file.close()
        print(encoded_text)
        encoded_text = ''.join(['0' * (8 - len(bin(element)[2:])) + bin(element)[2:] for element in encoded_text])
        encoded_text, last_octet = encoded_text[:-32], encoded_text[-32:]
        file = open(destination, "w")
        dictionary = self.binary_alphabet()
        dictionary = dict(zip(dictionary.values(), dictionary.keys()))
        octet_found = False
        while not octet_found:
            value = last_octet
            while not value == "":
                if value in dictionary.keys():
                    octet_found = True
                    break
                value = value[1:]
            if last_octet == '' or octet_found:
                break
            last_octet = last_octet[:-1]
        encoded_text += last_octet
        while encoded_text:
            if len(encoded_text) < 8:
                break
            for key in list(dictionary.keys()):
                if encoded_text[:len(key)] == key:
                    file.write(dictionary[key])
                    encoded_text = encoded_text[len(key):]
                    break
        file.close()


@app.route('/')
def index():
    encoded_file = None
    decoded_file = None
    if 'encoded_file' in request.args:
        encoded_file = request.args['encoded_file']
    if 'decoded_file' in request.args:
        decoded_file = request.args['decoded_file']
    return render_template('index.html',encoded_file=encoded_file,decoded_file=decoded_file)


@app.route('/encode', methods=['POST'])
def encode():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    file.save(os.path.join('uploads/', file.filename))
    path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
    encoding = HuffmanCoding(path,'/uploads/'+file.filename)
    # Rubah file text menjadi biner
    encoding.encode_file_bin()
    namefile = encoding.export_file
    return redirect(url_for('index',encoded_file=namefile))


@app.route('/decode', methods=['POST'])
def decode():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    file.save(os.path.join('uploads/', file.filename))
    path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')

    encoding = HuffmanCoding(path,'/uploads/'+file.filename)
    encoding.decode(encoded_file=path + '/uploads/'+file.filename)

    return redirect(url_for('index',decoded_file='decode.txt'))

@app.route('/download/<folder>/<filename>')
def download_file(folder,filename):
    return send_file(folder+'/'+filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
