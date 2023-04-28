#ID: 28900057
#Name: Chong Kah Ying

import sys
from bitarray import bitarray

ERROR_0 = False
ERROR_CANTDECODE = "UNABLE TO DECODE!"
ABORT = "ABORT"

class Node:
    def __init__(self):
        self.isLeaf = False
        self.zero = None
        self.one = None
        self.character = ""

class HuffmanTree:
    def __init__(self):
        self.root = Node()

    def add(self,code,character):
        current = self.root
        for bit in code:
            if bit == 1:
                if current.one == None:
                    current.one = Node()
                current = current.one
            else:
                if current.zero == None:
                    current.zero = Node()
                current = current.zero 
        
        current.isLeaf = True
        current.character = character

    def getChar(self,encoding):
        # returns encoding that will continue to be decoded 
        # and the character that corresponds to the huffman encoding 
        current = self.root
        while True:
            char = encoding.pop(0)
            if char == 0:
                current = current.zero
            else:
                current = current.one
            if current.isLeaf:
                break
            
        return current.character, encoding

def get_encoded_data(filename):
    binary_encoded_text = bitarray()
    with open(filename, 'rb') as fh:
        binary_encoded_text.fromfile(fh)

    return binary_encoded_text

def binary_to_integer(binary_bytes):
    sum = 0
    for i in range(len(binary_bytes)):
        bit = binary_bytes[i]
        # if the bit equals to 1, add 2^digit to existing sum 
        if bit == 1:
            power = len(binary_bytes)-1-i
            value = 2**power
            sum += value
    return sum

def decode_elias(binary):
    current = bitarray()
    current.append(binary.pop(0))
    while True:
        if current[0] == 0:
            current[0] = 1     
            read_next_n_bits = binary_to_integer(current)
            current = bitarray()
            if read_next_n_bits+1 < len(binary):
                for _ in range(read_next_n_bits+1):
                    current.append(binary.pop(0))
            else:
                return ERROR_0,ERROR_CANTDECODE 
        else:
            break
    return binary_to_integer(current)-1, binary

def decode_header(encoded_header):
    # decode length of input filename to delete <length> ascii value of characters in the original filenaem 
    # in the original file name
    length_of_asc_filename, encoded_header = decode_elias(bitarray(encoded_header))
    #stop decoding subsequent bits if there is an error
    if encoded_header == ERROR_CANTDECODE:
        return ABORT
    # strip off bits with length = 8*length of the original filename 
    for _ in range(length_of_asc_filename):
        for _ in range(8):
            encoded_header.pop(0)
    
    # number of characters in the file 
    number_of_characters, encoded_header = decode_elias(encoded_header)

    if encoded_header == ERROR_CANTDECODE:
        return ABORT

    # number of unique characters the file contains 
    number_of_unique_chars, encoded_header = decode_elias(encoded_header)
    if encoded_header == ERROR_CANTDECODE:
        return ABORT

    huffman_tree = HuffmanTree()
    for _ in range(number_of_unique_chars):
        # the huffman code is encoded by the ascii of the character that corresponds to the huffman code
        # and the length of the huffman code itself 
        ascii_letter = bitarray()
        for _ in range(8):
            ascii_letter.append(encoded_header.pop(0))
        character = chr(binary_to_integer(ascii_letter))
        length_of_huffman_code, encoded_header = decode_elias(encoded_header)
        if encoded_header == ERROR_CANTDECODE:
            return ABORT
        huffman_code = bitarray()

        # add the huffman and the corresponding character to the huffman tree 
        for _ in range(length_of_huffman_code):
            huffman_code.append(encoded_header.pop(0))
        huffman_tree.add(huffman_code,character)
    return huffman_tree, number_of_characters, encoded_header

def decode_data(huffman_tree, number_of_characters, encoded_text):
    recovered_text = ""
    # once currently recovered characters reach the specified number of characters,
    # stop decoding encoded text even if there are remaining characters in it 
    while len(recovered_text) < number_of_characters:
        # encoded data is in the form <offset, length, character>
        # 1) get the offset value 
        offset, encoded_text = decode_elias(encoded_text)
        if encoded_text == ERROR_CANTDECODE:
            return False
        # 2) get the length value 
        length, encoded_text = decode_elias(encoded_text)        
        if encoded_text == ERROR_CANTDECODE:
            return False
        
        # from the current position, go to the offset position and copy <length> characters
        # starting from the offset position and add to recovered text 
        starting_index = len(recovered_text)-offset
        i = starting_index
        while length > 0:
            recovered_text += recovered_text[i]
            i += 1
            length -= 1
        character, encoded_text = huffman_tree.getChar(encoded_text)
        recovered_text += character

    return recovered_text

def recover_text_from_encoding(encoded_header_text):
    # first decode the header
    # output empty string to text file if unable to decode header
    returned_information = decode_header(encoded_header_text)
    if returned_information == ABORT:
        return ""
    else:
        huffman_tree = returned_information[0] 
        number_of_characters = returned_information[1]
        encoded_text = returned_information[2]
    # try and recover original text if header is successfully decoded 
    recovered_text = decode_data(huffman_tree, number_of_characters, encoded_text)
    # return empty text if unable to recover original text 
    if recovered_text == False:
        return ""
    return recovered_text

def output_recovered_text_to_file(inputfilename,recovered_text):
    outputFileName = inputfilename.split(".bin")[0]
    f = open(outputFileName, "w")
    f.write(recovered_text)
    f.close()

def main(inputfilename):
    encoded_text = get_encoded_data(inputfilename)
    recovered_text = recover_text_from_encoding(encoded_text)
    output_recovered_text_to_file(inputfilename,recovered_text)
    
if __name__ == "__main__":
    inputfilename = sys.argv[1]
    main(inputfilename)
    

