from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import os
from werkzeug.utils import secure_filename
from image_compression import huffmanImageCompression
from text_compression import HuffmanLZWCoding
from graph import generate_graph
import uuid
import logging

logging.basicConfig(level=logging.DEBUG)

UPLOAD_FOLDER = 'static/uploads'
COMPRESS_FOLDER = 'static/compress'
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png'}
ALLOWED_TEXT_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COMPRESS_FOLDER'] = COMPRESS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESS_FOLDER, exist_ok=True)

def allowed_file(filename, filetype='image'):
    ext = filename.rsplit('.', 1)[1].lower()
    return (filetype == 'image' and ext in ALLOWED_IMAGE_EXTENSIONS) or \
           (filetype == 'text' and ext in ALLOWED_TEXT_EXTENSIONS)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/text', methods=['POST'])
def upload_text():
    file = request.files.get('text_file')
    if not file or file.filename == '' or not allowed_file(file.filename, 'text'):
        flash('Please upload a valid .txt file.', 'error')
        return redirect(url_for('home'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        coder = HuffmanLZWCoding(filepath)
        unique_name = f"compress_{uuid.uuid4().hex}.bin"
        output_path = os.path.join(app.config['COMPRESS_FOLDER'], unique_name)
        compress_path = coder.compressHuffman(output_path)
        coder.decompressHuffman(compress_path)
    except Exception as e:
        flash(f'Compression error: {str(e)}', 'error')
        return redirect(url_for('home'))

    original_size = os.path.getsize(filepath)
    compressed_size = os.path.getsize(compress_path)
    generate_graph(original_size, compressed_size, "Text Compression Comparison")

    return render_template('index.html',
                           text_uploaded=True,
                           original_size=original_size,
                           compressed_size=compressed_size,
                           graph=True,
                           compressed_file_name=os.path.basename(compress_path))

@app.route('/image', methods=['POST'])
def upload_image():
    file = request.files.get('image_file')
    if not file or file.filename == '' or not allowed_file(file.filename, 'image'):
        flash('Please upload a valid image file.', 'error')
        return redirect(url_for('home'))

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        compressed_path, retinex_path, original_size, compressed_size = huffmanImageCompression(filepath)
    except Exception as e:
        flash(f'Image compression error: {str(e)}', 'error')
        return redirect(url_for('home'))

    generate_graph(original_size, compressed_size, "Image Compression Comparison")

    return render_template('index.html',
                           image_uploaded=True,
                           original_image=filename,
                           compressed_image=os.path.basename(compressed_path),
                           retinex_image=os.path.basename(retinex_path),
                           original_size=original_size,
                           compressed_size=compressed_size,
                           graph=True)

@app.route('/download/<filename>')
def download_compressed_file(filename):
    path = os.path.join(app.config['COMPRESS_FOLDER'], filename)
    return send_file(path, as_attachment=True) if os.path.exists(path) else ("File not found", 404)

@app.route('/send_compressed_image/<filename>')
def send_compressed_image(filename):
    path = os.path.join(app.config['COMPRESS_FOLDER'], filename)
    return send_file(path, mimetype='image/jpeg', as_attachment=True) if os.path.exists(path) else ("File not found", 404)

if __name__ == '__main__':
    app.run(debug=True)
