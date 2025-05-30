import heapq
import pickle

# ------------- Helper Functions -------------
def int_to_bin(n, bits):
    """Return a binary string of length `bits` for integer n."""
    return format(n, '0{}b'.format(bits))

# ------------- Huffman Coding (Standard) -------------
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequency):
    heap = [Node(ch, freq) for ch, freq in frequency.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    return heap[0]

def build_huffman_codes(root, code, codes):
    if root is None:
        return
    if root.char is not None:
        codes[root.char] = code
    else:
        build_huffman_codes(root.left, code + "0", codes)
        build_huffman_codes(root.right, code + "1", codes)

def huffman_compress(data):
    # data is a string (each character represents one byte)
    freq = {}
    for ch in data:
        freq[ch] = freq.get(ch, 0) + 1
    root = build_huffman_tree(freq)
    codes = {}
    build_huffman_codes(root, "", codes)
    compressed = "".join(codes[ch] for ch in data)
    return compressed, codes

def huffman_decompress(bit_string, codes):
    inv_codes = {v: k for k, v in codes.items()}
    decoded = ""
    temp = ""
    for bit in bit_string:
        temp += bit
        if temp in inv_codes:
            decoded += inv_codes[temp]
            temp = ""
    return decoded

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

def bytes_to_bitstring(b, num_bits):
    # Convert bytes to bitstring with leading zeros to have num_bits length
    return bin(int.from_bytes(b, byteorder='big'))[2:].zfill(num_bits)

# ------------- LZ77 Tokenization and Bit Packing -------------
def lz77_tokenize(data, window_size=255, min_match=3):
    """
    Tokenize data using a simple LZ77 algorithm.
    Returns a list of tokens.
    Each token is a tuple:
      (is_match, offset, length, literal)
    - For a literal token, is_match is False and literal is a character.
    - For a match token, is_match is True; literal is None.
    """
    tokens = []
    i = 0
    n = len(data)
    while i < n:
        best_length = 0
        best_offset = 0
        # Search the window for a match (window size limited to 255)
        start_index = max(0, i - window_size)
        for j in range(start_index, i):
            length = 0
            while i + length < n and data[j + length] == data[i + length]:
                length += 1
                # Ensure we don't match overlapping beyond current position
                if j + length >= i:
                    break
            if length > best_length:
                best_length = length
                best_offset = i - j
        # If a match of at least min_match characters is found, output a match token.
        if best_length >= min_match:
            tokens.append((True, best_offset, best_length, None))
            i += best_length
        else:
            tokens.append((False, 0, 0, data[i]))
            i += 1
    return tokens

def pack_tokens(tokens):
    """
    Convert tokens into a bit string.
    For a literal token: output flag '0' followed by 8 bits of the character.
    For a match token: output flag '1' followed by 8 bits for offset and 8 bits for length.
    """
    bit_str = ""
    for token in tokens:
        if not token[0]:
            # Literal token: flag 0 + literal char (8 bits)
            bit_str += "0" + int_to_bin(ord(token[3]), 8)
        else:
            # Match token: flag 1 + 8-bit offset + 8-bit length
            bit_str += "1" + int_to_bin(token[1], 8) + int_to_bin(token[2], 8)
    return bit_str

def unpack_tokens(bit_str):
    """
    Convert a bit string back into a list of tokens.
    """
    tokens = []
    i = 0
    while i < len(bit_str):
        flag = bit_str[i]
        i += 1
        if flag == "0":
            # Literal token: next 8 bits are the character
            char_bits = bit_str[i:i+8]
            i += 8
            tokens.append((False, 0, 0, chr(int(char_bits, 2))))
        else:
            # Match token: next 8 bits offset, then 8 bits length
            offset = int(bit_str[i:i+8], 2)
            i += 8
            length = int(bit_str[i:i+8], 2)
            i += 8
            tokens.append((True, offset, length, None))
    return tokens

def lz77_decompress_tokens(tokens):
    """
    Reconstruct the original text from the token list.
    """
    output = ""
    for token in tokens:
        if not token[0]:
            output += token[3]
        else:
            offset = token[1]
            length = token[2]
            start = len(output) - offset
            for j in range(length):
                output += output[start+j]
    return output

# ------------- Hybrid Compression/Decompression -------------
def hybrid_compress(input_file, output_file):
    # Read the original text
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        data = f.read()
    # LZ77 tokenization
    tokens = lz77_tokenize(data)
    # Pack tokens into a bit string
    token_bits = pack_tokens(tokens)
    # Pad the bit string to a multiple of 8 bits
    pad = (8 - (len(token_bits) % 8)) % 8
    token_bits_padded = token_bits + "0" * pad
    total_bits = len(token_bits)  # original valid bits count
    # Convert the padded bit string to bytes
    packed_bytes = bitstring_to_bytes(token_bits_padded)
    # Convert these bytes to a string where each byte is a character (for Huffman coding)
    huffman_input = ''.join(chr(b) for b in packed_bytes)
    # Apply Huffman coding on the string
    huff_bit_str, huff_codes = huffman_compress(huffman_input)
    huff_total_bits = len(huff_bit_str)
    huff_bytes = bitstring_to_bytes(huff_bit_str)
    # Store all metadata needed for decompression
    to_store = {
        'huff_codes': huff_codes,
        'huff_total_bits': huff_total_bits,
        'pad': pad,             # padding in the token bitstring
        'packed_token_bits_len': len(token_bits),  # original token bit count
        'compressed_data': huff_bytes
    }
    with open(output_file, 'wb') as f:
        pickle.dump(to_store, f)
    print("Compression complete. Compressed file saved as", output_file)

def hybrid_decompress(input_file, output_file):
    with open(input_file, 'rb') as f:
        stored = pickle.load(f)
    huff_codes = stored['huff_codes']
    huff_total_bits = stored['huff_total_bits']
    pad = stored['pad']
    token_bits_len = stored['packed_token_bits_len']
    huff_bytes = stored['compressed_data']
    # Convert Huffman bytes back to bit string
    huff_bit_str = bytes_to_bitstring(huff_bytes, huff_total_bits)
    # Huffman-decompress to recover the packed token bit string (as a string of characters)
    huffman_output = huffman_decompress(huff_bit_str, huff_codes)
    # Convert the recovered string to bytes
    packed_bytes = bytes([ord(ch) for ch in huffman_output])
    # Convert bytes back to a bit string (padded)
    token_bits_padded = bytes_to_bitstring(packed_bytes, len(packed_bytes)*8)
    # Remove the padding to recover the original token bit string
    token_bits = token_bits_padded[:token_bits_len]
    # Unpack tokens from the bit string
    tokens = unpack_tokens(token_bits)
    # Decompress the tokens to reconstruct the original text
    original_text = lz77_decompress_tokens(tokens)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(original_text)
    print("Decompression complete. Output file saved as", output_file)

# ------------- Main Program -------------
if __name__ == '__main__':
    mode = input("Enter mode (c for compress, d for decompress): ").strip().lower()
    if mode == 'c':
        input_file = input("Enter the path to the file to compress: ")
        output_file = input("Enter the path for the compressed output (e.g., compressed.bin): ")
        hybrid_compress(input_file, output_file)
    elif mode == 'd':
        input_file = input("Enter the path to the compressed file (e.g., compressed.bin): ")
        output_file = input("Enter the path for the decompressed output (e.g., decompressed.txt): ")
        hybrid_decompress(input_file, output_file)
    else:
        print("Invalid mode selected.")
