# Huffman-Based-LZW-Lossless-Image-Compression-using-Retinex-Algorithm
A hybrid image compression system that enhances images using Retinex for better visual clarity and then compresses them losslessly using a combination of LZW (Lempel–Ziv–Welch) and Huffman encoding. This project is aimed at achieving efficient storage and transmission of high-quality images.

🚀 Features
✅ Image enhancement using Single Scale Retinex (SSR)

✅ LZW (Dictionary-based) Compression

✅ Huffman Encoding for entropy optimization

✅ Supports Grayscale and RGB images

✅ Lossless compression with high PSNR

✅ Easy-to-use Python script for processing

🧠 Algorithms Used
Retinex Algorithm (SSR)
Enhances image illumination and contrast to simulate human perception of color constancy.

LZW Compression
Builds a dictionary of input data sequences for compression without losing any information.

Huffman Coding
Further compresses the output of LZW using variable-length codes based on symbol frequency.

🛠️ Tech Stack
Python 3.8+

NumPy

OpenCV

Matplotlib

PIL (Pillow)

Custom implementations of LZW & Huffman

📂 Project Structure
graphql
Copy
Edit
├── retinex.py             # Image enhancement using Retinex
├── lzw_compression.py     # LZW compression and decompression
├── huffman.py             # Huffman coding implementation
├── main.py                # Main script for execution
├── test_images/           # Sample images for testing
├── output/                # Compressed and decompressed outputs
├── README.md              # This file
🧪 How to Run (Tutorial)
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/your-username/huffman-lzw-retinex-compression.git
cd huffman-lzw-retinex-compression
2. Install Required Libraries
Use pip:

bash
Copy
Edit
pip install -r requirements.txt
Or install manually:

bash
Copy
Edit
pip install numpy opencv-python matplotlib pillow
3. Run the Main Script
bash
Copy
Edit
python main.py
You’ll be prompted (or can modify) to:

Choose the input image (test_images/your_image.jpg)

Perform Retinex enhancement

Compress using LZW

Encode using Huffman

Save compressed file

Decompress and compare

4. Outputs
Compressed file saved in /output/

Decompressed image saved as /output/decompressed_image.png

Logs and stats like original vs. compressed size, PSNR, etc.

📊 Example Results
Metric	Original Image	Compressed
File Size	512 KB	178 KB
PSNR	47.3 dB	47.3 dB
Compression Ratio	2.87:1	—

📸 Sample Images
Images used for testing are located in the test_images/ folder. You can replace them with your own.

📈 Future Enhancements
Add GUI using Tkinter or Streamlit

Support batch image processing

Extend to video compression

Integrate Adaptive Retinex

👨‍💻 Author
MD HASAN MEHDI
B.Tech in Information Technology, Muffakham Jah College of Engineering and Technology


📝 License
This project is open-source and free to use under the MIT License.
