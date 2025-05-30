🚀 Hybrid File Compression using Huffman Coding & LZ77
This project implements a hybrid text compression system that combines LZ77 tokenization with Huffman Coding to achieve efficient, lossless file compression. It’s designed to reduce file sizes while preserving the integrity of the original data — perfect for text-based file optimization.

📄 Files Included
File Name	Description
HybridCompression.py	Main Python script implementing the compression & decompression logic.
test2	Sample text file used as input for compression. (92 KB)
comp.bin	Binary file output after compression. (71 KB)

📌 Features
✅ Lossless compression using LZ77 + Huffman hybrid method

✅ Handles any text file (.txt, .log, .csv, etc.)

✅ Saves compressed binary format using pickle

✅ Full decompression support with integrity retention

🛠️ How It Works
🔁 Compression Flow:
LZ77 identifies repeated patterns in the input.

Matches and literals are encoded into a compact token bitstring.

The bitstring is then further compressed using Huffman Coding.

All necessary metadata (codes, padding, etc.) are stored in the final .bin output.

🔁 Decompression Flow:
Huffman decoding restores the LZ77 token bitstring.

Tokens are unpacked and decompressed to reconstruct the original file.

▶️ How to Run
bash
Copy
Edit
# Run the script
python HybridCompression.py
You’ll be prompted to choose:

c – Compress a file

d – Decompress a file

📷 Sample Output

📉 Compression Results
Input File	Size
test2	92 KB
comp.bin	71 KB
➡️ Reduction	~22.8%

