#ID: 28900057
#Name: Chong Kah Ying
import heapq
import sys
from bitarray import bitarray

from numpy import empty
EIGHT = 8

def z_algo(txt):
    '''
    param: string input 
    function: computes the z-value for each character of the string input, 
    and adds it to a list that will always have the same length as the given 
    string input
    return: a list of z-values 
    '''
    n = len(txt)

    z_values = [n] #because z value is always the length of provided pattern 
    #represents the left and right end indices of the latest z_box that occurs before index i. 
    left_i = -1
    right_i = -1
    i = 1
    #start comparison from the 2nd letter onwards, which is index = 1 in 0 indexing
    while i < n:
        z_i = 0
  
        if i > right_i:
        #manually compare characters when current index(i) is larger than the right side of the 
        # latest z-box
            for j in range(n-i):
                if txt[i+j] == txt[j]:
                    z_i += 1
                else:
                    #stop comparison when there is a mismatch 
                    break
            
        else:
            if z_values[i-left_i] >= right_i - i + 1:
                #start a loop to manually compare characters from outside the z-box 
                z_i = z_values[i-left_i]
                if i + z_i < n:
                    for j in range(z_i,n):
                        if txt[i+j] != txt[j]:
                            break
                        else:
                            z_i += 1

            else:
                #copy z[i-beginning index of the z-box] when i is within the latest z-box
                z_i = z_values[i-left_i]
            
        z_values.append(z_i)

        #update latest z-box
        if z_i > 0:
            left_i = i
            right_i = left_i + z_i - 1
        
        #when z[1] == q, the next q-1 characters is the same as txt[0] and txt[1]
        #so add the respective values into the z-values list without needing to 
        #compare the characters manually at each iteration
        #if text has more characters than q+2, the z-value of txt[q+2] will be 0 
        #only use the z-algo cases above after skipping unneeded iterations which is updated
        #here using i += 1 
        if len(z_values) == 2 and z_i > 0:
            for z in range(z_values[-1]-1,0,-1):
                z_values.append(z)
                i += 1
            if len(z_values) < len(txt):
                z_values.append(0)
                i += 1
        i += 1
    return z_values

def search(text, pattern,stop):
    n = len(text)
    m = len(pattern)
    z_values = z_algo(pattern)
    i = 0
    right_i = -1
    max = (-1,0)
    if n < m:
        if n < stop:
            stop = n
    while i < stop:
        z_i = 0
        if i > right_i:
        #manually compare characters when current index(i) is larger than the right side of the 
        # latest z-box
            if n < m:
                length = n
            else:
                length = m
            for j in range(length):
                if text[i+j] == pattern[j]:
                    z_i += 1
                else:
                    #stop comparison when there is a mismatch 
                    break

        else:
            if z_values[i-left_i] >= right_i - i + 1:
                #start a loop to manually compare characters from outside the z-box 
                z_i = z_values[i-left_i]
                if n < m:
                    length = n
                else:
                    length = m
                for j in range(z_i,length):
                    if i+j > length-1 or text[i+j] != pattern[j]:
                        break
                    else:
                        z_i += 1

            else:
                #copy z[i-beginning index of the z-box] when i is within the latest z-box
                z_i = z_values[i-left_i]
            
        #update latest z-box
        if z_i > 0:
            if z_i >= max[1]:
                max = (i,z_i)
            left_i = i
            right_i = left_i + z_i - 1
        
        i += 1
    return max

def int_to_bin(integer):
    quotient = integer
    binary = bitarray()
    while quotient > 0:
        quotient,remainder = divmod(quotient,2)
        if remainder == 0:
            binary.append(0)
        else:
            binary.append(1)
    binary.reverse()
    return binary

def elias_encoding(integer):
    binary = int_to_bin(integer+1)
    full = binary
    length_binary = len(binary)
    # stop encoding when length of previous length - 1 is 0 
    while length_binary - 1 > 0:
        length_binary = int_to_bin(length_binary-1) 
        length_binary[0] = 0
        full = length_binary + full
        length_binary = len(length_binary)
    return full
        
def huffman(word):
    ascii_freq = [ 0 for _ in range(256)] 
    char_huffmancode = [bitarray() for _ in range(256)]
    set_freq = []
    for char in word:
        ascii_freq[ord(char)] += 1
        set_freq.append(ord(char))
    unique_ascii = list(set(set_freq))

    unique_ascii_freq = unique_ascii.copy()
    # create list of [(frequency of character, character), (frequency of character2, character2),.... ]
    for i in range(len(unique_ascii_freq)):
        unique_ascii_freq[i] = (ascii_freq[unique_ascii_freq[i]],chr(unique_ascii_freq[i]))
    heapq.heapify(unique_ascii_freq)
    #maintain min heap 
    #first item in tuple will take order precedence
    while True:
        a = None
        b = None
        a = heapq.heappop(unique_ascii_freq)
        if len(unique_ascii_freq) > 0:
            b = heapq.heappop(unique_ascii_freq)

        sum = 0
        combined_string = ""
        freq = a[0]
        chars = a[1]
        combined_string += chars 
        for char in chars:
            char_huffmancode[ord(char)].append(0)

        sum += freq

        if b != None:
            freq = b[0]
            chars = b[1]
            for char in chars:
                char_huffmancode[ord(char)].append(1)
            sum += freq
            combined_string += chars
        if len(unique_ascii_freq) == 0:
            break
        else:
            heapq.heappush(unique_ascii_freq, (sum,combined_string))
            
    char_huffmancode_non_zero = [] 
    for char in unique_ascii:
        char_huffmancode[char].reverse()
        huffman_code = char_huffmancode[char]
        char_huffmancode_non_zero.append((char,huffman_code))
    return char_huffmancode_non_zero, char_huffmancode

def constructHeader(filename,text):
    n = len(filename)
    length_inputname = elias_encoding(n)
    header = length_inputname
    #get ascii letters values in the file name:
    for char in filename:
        ascii_bin = int_to_bin(ord(char))
        for _ in range(EIGHT-len(ascii_bin)):
            header.append(0)
        header += ascii_bin
    #length of text in the file
    header += elias_encoding(len(text))
    return header

def lz77_encode(word,search_window_size,buffer_size, ascii_table):
    i = 1
    pattern = ""
    data = bitarray()

    data += elias_encoding(0) + elias_encoding(0) + ascii_table[ord(word[0])]

    # start and end is always <0,0,char>
    # loop until 2nd last char in word 
    while i < len(word)-1:
        #set end point of pattern
        end = -1
        if i + buffer_size > len(word)-1:
            end = len(word)-1
        else:
            end = i+buffer_size 

        pattern = word[i:end]
        text = ""  
        start = -1
        stop = -1

        #set start and end point of text to compare with pattern in look ahead buffer
        if i < search_window_size:
            start = 0
            text = word[start:i+search_window_size-1]
            stop = i
        else:
            text_end = -1
            if i + search_window_size -1 >= len(word)-1:
                text_end = len(word)-1
            else:
                text_end = i + search_window_size - 1

            start = i-buffer_size
            text = word[start:text_end]
            if start == 0:
                stop = i
            else:
                stop = i-start
        #set stop point to avoid comparing text that starts where the look ahead window starts 
        index_length = search(text,pattern,stop)
        
        index = index_length[0]
        if start != 0 and index != -1:
            #rescale index of text for when buffer is beyond index 0 
            index += start
        length = index_length[1]
        
        if index == -1:
            offset = 0
        else:
            offset = i-index
        data += elias_encoding(offset) + elias_encoding(length) 
        if length > 0:
            # force followup character to be second last character of word 
            # even if pattern up till that point matches a portion of buffer text + pattern
            # by reducing the length 
            if i+length-1 == len(word)-2:
                length -= 1
                character = word[len(word)-2]
                huffman_character = ascii_table[ord(character)]
            else:
                character = word[i+ length]
                huffman_character = ascii_table[ord(character)]
                data += huffman_character
        else:
            # no overlapping for both text and pattern <0,0,pattern[0]>
            character = word[i]
            huffman_character = ascii_table[ord(character)]
            data += huffman_character

        if length > 0:  
            i += length + 1
        else:
            i += 1

    last_char = word[-1]
    data += elias_encoding(0) + elias_encoding(0) + ascii_table[ord(last_char)]
    return data

def ascii_to_binary(text,filename,search_window_size,look_ahead_buffer_size):
    full = constructHeader(filename,text)
    if len(text) > 0:
        huffman_codes, all_ascii = huffman(text)
        #elias of the number of unique letters in the text 
        huffman_bytes = elias_encoding(len(huffman_codes))

        #encode all huffman codes
        for code in huffman_codes:
            ascii_value = code[0]
            huffman_code = code[1]
            ascii_binary = int_to_bin(ascii_value)  
            for _ in range(EIGHT-len(ascii_binary)):
                huffman_bytes.append(0)
            huffman_bytes += ascii_binary
            elias_length_codeword = elias_encoding(len(huffman_code))
            huffman_bytes += elias_length_codeword
            huffman_bytes += huffman_code
        full += huffman_bytes

        lz77 = lz77_encode(text,search_window_size,look_ahead_buffer_size,all_ascii)
        full += lz77

        #length of the entire encoding in binary has to be a multiple of 8 
        #pad remainder of the current length/8 number of zeroes at the back
        remainder = len(full) % EIGHT
        for _ in range(8-remainder):
            full.append(0)

    return full

def readContentOfFile(filename):
    f = open(filename, "r",encoding="utf-8")
    text = f.readline()
    f.close()
    return text

def writeToFile(filename, encoding):
    with open(filename+'.bin', 'wb') as fo:
        encoding.tofile(fo)

def main(filename):
    search_window_size =  int(sys.argv[2])
    look_ahead_buffer_size =  int(sys.argv[3])
    text = readContentOfFile(filename)   
    binary = ascii_to_binary(text,filename,search_window_size,look_ahead_buffer_size)
    writeToFile(filename,binary)

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)

    

    