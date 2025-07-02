import io
from PIL import Image
import numpy as np
import cv2
from collections import defaultdict
import os

img_pixels = defaultdict(list)
global height
global width

def huffmanCompress(compressed_image):
    dictionary_size = 256
    dictionary_arr = {i: chr(i) for i in range(dictionary_size)}
    results = io.StringIO()
    pixel = chr(compressed_image.pop(0))
    results.write(pixel)

    for m in compressed_image:
        if m in dictionary_arr:
            entry_pixel = dictionary_arr[m]
        elif m == dictionary_size:
            entry_pixel = pixel + pixel[0]
        else:
            raise ValueError(f'Bad compression m: {m}')
        results.write(entry_pixel)
        dictionary_arr[dictionary_size] = pixel + entry_pixel[0]
        dictionary_size += 1
        pixel = entry_pixel
    return results.getvalue()

def huffmanCompressDict(uncompressed_image):
    dictionary_size = 256
    dictionary_arr = {chr(i): i for i in range(dictionary_size)}
    pixel = ""
    results = []

    for chars in uncompressed_image:
        pixel_chars = pixel + chars
        if pixel_chars in dictionary_arr:
            pixel = pixel_chars
        else:
            results.append(dictionary_arr[pixel])
            dictionary_arr[pixel_chars] = dictionary_size
            dictionary_size += 1
            pixel = chars

    if pixel:
        results.append(dictionary_arr[pixel])
    return results

def Retinex(image, gamma_value=0.5):
    inv_Gamma = 1.0 / gamma_value
    lookup_table = np.array([((i / 255.0) ** inv_Gamma) * 255 for i in np.arange(0, 256)], dtype="uint8")
    return cv2.LUT(image, lookup_table)

def LZWEncodeImage(codes, image_name, retinex_image):
    pixel_list = [ord(code) for code in codes]
    img_array = np.asarray(pixel_list).reshape(height, width)

    orig = np.zeros((height, width, 3))
    for i in range(width):
        for j in range(height):
            value = int(img_array[j, i])
            values = img_pixels.get(f"{i},{j}")
            if values:
                r, g, b = values[0]
                orig[j, i] = [b, g, r]

    cv2.imwrite(image_name, orig, [cv2.IMWRITE_JPEG_QUALITY, 35])
    img = cv2.imread(image_name)
    img = Retinex(img)
    cv2.imwrite(retinex_image, img, [cv2.IMWRITE_JPEG_QUALITY, 45])


def compressImage(uncompress_image):
    compressed_image = huffmanCompressDict(uncompress_image)
    compressed_image = huffmanCompress(compressed_image)

    compress_path = os.path.join("static", "compress", "Compress.jpg")
    retinex_path = os.path.join("static", "compress", "retinex_Compress.jpg")
    LZWEncodeImage(compressed_image, compress_path, retinex_path)


def getImagePixels(image_path):
    global height
    global width
    input_image = Image.open(image_path)
    pixels = input_image.load()
    width, height = input_image.size
    pixels_arr = []

    for i in range(width):
        for j in range(height):
            color_pixel = pixels[i, j]
            gray_value = int(round(sum(color_pixel) / float(len(color_pixel))))
            img_pixels[f"{i},{j}"].append(color_pixel)
            pixels_arr.append(gray_value)

    return pixels_arr

def huffmanImageCompression(input_image):
    img_pixels.clear()
    pixel_values = getImagePixels(input_image)
    pixel_string = ''.join(chr(f) for f in pixel_values)
    compressImage(pixel_string)
