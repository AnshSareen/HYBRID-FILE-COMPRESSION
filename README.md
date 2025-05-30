# Hybrid File Compression: Huffman + LZ77

This project demonstrates a hybrid text compression system combining **Huffman coding** and **LZ77 compression** to achieve effective lossless data compression.

---

## 📂 Project Structure

- `HybridCompression.py` – Main script containing compression/decompression logic  
- `test2.txt` – Original uncompressed text (sample input)  
- `comp.bin` – Compressed binary file generated from test2.txt  
- `output1.png` – Output visual (e.g., size comparison chart - optional)  
- `output2.png` – Output visual (e.g., compression ratio or flowchart - optional)  

---

## 🧠 Technologies Used

- **Python 3.8+**
- Huffman Coding
- LZ77 Compression
- Pickle (for serialization)
- Bitwise Manipulation

---

## 💡 How It Works

### 1. LZ77 Compression
- The input text is tokenized using LZ77-style references.
- Tokens are encoded into a bit string.

### 2. Huffman Coding
- The token bit string is then compressed using Huffman encoding.
- Results in further reduction by encoding frequent patterns with shorter codes.

### 3. Decompression
- Huffman decoding is performed first.
- Then LZ77 decoding reconstructs the original content.

---

## 🛠️ Usage

> Run from terminal or command prompt:

### 🔹 Compression

```bash
python HybridCompression.py
# Then enter:
# Enter mode (c for compress, d for decompress): c
# Enter the path to the file to compress: test2.txt
# Enter the path for the compressed output (e.g., comp.bin): comp.bin
```
### 🔹 DEcompression
```bash
python HybridCompression.py
# Then enter:
# Enter mode (c for compress, d for decompress): d
# Enter the path to the compressed file (e.g., comp.bin): comp.bin
# Enter the path for the decompressed output (e.g., output.txt): output.txt
```
---

## 📊 Results

- **Original File Size:** `test2.txt` → **~92 KB**
- **Compressed File Size:** `comp.bin` → **~71 KB**
- **Size Reduction:** ✅ ~23% achieved using the hybrid compression model

> 📈 Check the following visuals for more insights:
- `output1.png` – Size comparison
- `output2.png` – ratio visualization

---

## ✅ Features

- ✅ **Lossless Compression**
- ✅ **Hybrid of LZ77 + Huffman for better optimization**
- ✅ **Supports large text files**
- ✅ **Simple CLI interface for compression and decompression**

---

## 📌 Notes

- The file `test2.txt` contains educational content used for compression testing.
- For best results, ensure your custom input file is in **UTF-8** format and contains readable text data.
- The script ignores unsupported characters during file reading if encoding issues arise.

---

## 📚 References

- Huffman, D. A. (1952). *A Method for the Construction of Minimum-Redundancy Codes*.
- Lempel, A., & Ziv, J. (1977). *A Universal Algorithm for Sequential Data Compression*.
- Python Standard Library modules:
  - [`heapq`](https://docs.python.org/3/library/heapq.html)
  - [`pickle`](https://docs.python.org/3/library/pickle.html)
  - [`os`](https://docs.python.org/3/library/os.html)

---
