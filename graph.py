import matplotlib.pyplot as plt
import os

def generate_graph(original_size, compress_size, title="Compression Comparison"):
    bars = ['Original', 'Compressed']
    sizes = [original_size, compress_size]
    plt.figure(figsize=(6, 4))
    plt.bar(bars, sizes, color=['blue', 'green'])
    plt.title(title)
    plt.ylabel('File Size (bytes)')
    plt.tight_layout()
    plt.savefig(os.path.join('static', 'graph.png'))
    plt.close()
