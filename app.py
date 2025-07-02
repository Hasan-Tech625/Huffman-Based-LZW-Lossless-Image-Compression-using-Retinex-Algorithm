import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from HuffmanDataLZW import HuffmanLZWCoding
import LZWImageCompression
import matplotlib.pyplot as plt
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configure upload folders
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
COMPRESS_FOLDER = os.path.join(BASE_DIR, 'static', 'compress')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESS_FOLDER, exist_ok=True)

ALLOWED_TEXT_EXTENSIONS = {'txt'}
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}


def allowed_file(filename, allowed_exts):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_exts



@app.route('/text', methods=['POST'])
def compress_text():
    if 'text_file' not in request.files:
        flash('No text file part')
        return redirect(request.url)

    file = request.files['text_file']
    if file.filename == '':
        flash('No selected text file')
        return redirect(request.url)

    if file and allowed_file(file.filename, ALLOWED_TEXT_EXTENSIONS):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Huffman + LZW compression
        huffman = HuffmanLZWCoding(filepath)
        compressed_path = huffman.compressHuffman()
        decompressed_path = huffman.decompressHuffman(compressed_path)

        # Calculate sizes
        original_size = os.path.getsize(filepath)
        compressed_size = os.path.getsize(compressed_path)

        # Generate size comparison graph
        sizes = [original_size, compressed_size]
        labels = ['Original', 'Compressed']
        plt.figure(figsize=(8,6))
        plt.bar(labels, sizes, color=['blue','green'])
        plt.title('Text Compression Size Comparison')
        plt.ylabel('Size (bytes)')
        graph_path = os.path.join('static', 'graph.png')
        plt.savefig(graph_path)
        plt.close()

        compressed_file_name = os.path.basename(compressed_path)

        return render_template('index.html',
                               text_uploaded=True,
                               original_size=original_size,
                               compressed_size=compressed_size,
                               compressed_file_name=compressed_file_name,
                               graph=True)
    else:
        flash('Invalid file type for text')
        return redirect(url_for('index'))


@app.route('/download/<filename>')
def download_compressed_file(filename):
    # Serve compressed text files
    return send_from_directory(COMPRESS_FOLDER, filename, as_attachment=True)


@app.route('/image', methods=['POST'])
def compress_image():
    if 'image_file' not in request.files:
        flash('No image file part')
        return redirect(request.url)

    file = request.files['image_file']
    if file.filename == '':
        flash('No selected image file')
        return redirect(request.url)

    if file and allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Run compression from your LZWImageCompression.py
        # Clear global pixel dictionary first (important)
        LZWImageCompression.img_pixels.clear()
        pixel_values = LZWImageCompression.getImagePixels(filepath)

        # Convert pixel values to chars string
        pixelString = ''.join(chr(p) for p in pixel_values)

        # Compress image (this writes files into compress folder)
        LZWImageCompression.compressImage(pixelString)

        original_size = os.path.getsize(filepath)
        # Assuming output compress image names are fixed in LZWImageCompression
        compressed_img_name = 'Compress.jpg'
        retinex_img_name = 'retinex_Compress.jpg'
        compressed_path = os.path.join(COMPRESS_FOLDER, compressed_img_name)
        retinex_path = os.path.join(COMPRESS_FOLDER, retinex_img_name)

        compressed_size = os.path.getsize(compressed_path) if os.path.exists(compressed_path) else 0

        # Generate compression size graph
        sizes = [original_size, compressed_size]
        labels = ['Original', 'Compressed']
        plt.figure(figsize=(8,6))
        plt.bar(labels, sizes, color=['blue','green'])
        plt.title('Image Compression Size Comparison')
        plt.ylabel('Size (bytes)')
        graph_path = os.path.join('static', 'graph.png')
        plt.savefig(graph_path)
        plt.close()

        return render_template('index.html',
                               image_uploaded=True,
                               original_size=original_size,
                               compressed_size=compressed_size,
                               original_image=filename,
                               compressed_image=compressed_img_name,
                               retinex_image=retinex_img_name,
                               graph=True)
    else:
        flash('Invalid file type for image')
        return redirect(url_for('index'))


@app.route('/compress/<filename>')
def send_compressed_image(filename):
    return send_from_directory(COMPRESS_FOLDER, filename, as_attachment=True)




@app.route("/signup")
def signup():
    global otp, username, name, email, number, password
    username = request.args.get('user','')
    name = request.args.get('name','')
    email = request.args.get('email','')
    number = request.args.get('mobile','')
    password = request.args.get('password','')
    
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("insert into `info` (`user`,`name`, `email`,`mobile`,`password`) VALUES (?, ?, ?, ?, ?)",(username,name,email,number,password))
    con.commit()
    con.close()
    return render_template("signin.html")

@app.route('/signin')  
def signin():
    user = request.args.get('user','')
    password = request.args.get('password','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(user,password))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")
    
    elif user == str(data[0]) and password == str(data[1]):
        return render_template("index.html")
    else:
        render_template("signin.html")




@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('signin.html')    


if __name__ == '__main__':
    app.run()