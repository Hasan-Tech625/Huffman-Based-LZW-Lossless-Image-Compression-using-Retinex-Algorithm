import heapq
import os
from functools import total_ordering

@total_ordering
class TreeNode:
    def __init__(self, chars, frequency):
        self.chars = chars
        self.frequency = frequency
        self.leftNode = None
        self.rightNode = None

    def __lt__(self, othernode):
        return self.frequency < othernode.frequency

    def __eq__(self, othernode):
        if othernode is None:
            return False
        if not isinstance(othernode, TreeNode):
            return False
        return self.frequency == othernode.frequency


class HuffmanLZWCoding:
    def __init__(self, filepath):
        self.filepath = filepath
        self.heap_arr = []
        self.codes_arr = {}
        self.reverse_mapping_arr = {}

    # Functions for compression:

    def huffman_dict(self, text_char):
        frequency_arr = {}
        for character in text_char:
            frequency_arr[character] = frequency_arr.get(character, 0) + 1
        return frequency_arr

    def addNode(self, frequency_arr):
        for key in frequency_arr:
            treenode = TreeNode(key, frequency_arr[key])
            heapq.heappush(self.heap_arr, treenode)

    def mergeNodes(self):
        while len(self.heap_arr) > 1:
            node1 = heapq.heappop(self.heap_arr)
            node2 = heapq.heappop(self.heap_arr)

            merged_node = TreeNode(None, node1.frequency + node2.frequency)
            merged_node.leftNode = node1
            merged_node.rightNode = node2

            heapq.heappush(self.heap_arr, merged_node)

    def createCode(self, rootnode, currentcode):
        if rootnode is None:
            return

        if rootnode.chars is not None:
            self.codes_arr[rootnode.chars] = currentcode
            self.reverse_mapping_arr[currentcode] = rootnode.chars
            return

        self.createCode(rootnode.leftNode, currentcode + "0")
        self.createCode(rootnode.rightNode, currentcode + "1")

    def addCodes(self):
        rootnode = heapq.heappop(self.heap_arr)
        self.createCode(rootnode, "")

    def LZW_encoded_text(self, textdata):
        return ''.join([self.codes_arr[char] for char in textdata])

    def LZWpad_encoded_text(self, encodedtext):
        extrapadding = 8 - len(encodedtext) % 8
        paddedinfo = f"{extrapadding:08b}"
        encodedtext += "0" * extrapadding
        return paddedinfo + encodedtext

    def LZW_byte_array(self, paddedencoded_text):
        if len(paddedencoded_text) % 8 != 0:
            print("Encoding text data not properly padded")
            exit(0)

        byte_arr = bytearray()
        for i in range(0, len(paddedencoded_text), 8):
            byte = paddedencoded_text[i:i+8]
            byte_arr.append(int(byte, 2))
        return byte_arr

    def compressHuffman(self):
        input_file, file_extension = os.path.splitext(self.filepath)
        outputpath = "compress/compress.bin"

        with open(self.filepath, 'r+') as file, open(outputpath, 'wb') as output:
            textdata = file.read().rstrip()

            frequency_arr = self.huffman_dict(textdata)
            self.addNode(frequency_arr)
            self.mergeNodes()
            self.addCodes()

            encodedText = self.LZW_encoded_text(textdata)
            paddedencoded_text = self.LZWpad_encoded_text(encodedText)
            byte_arr = self.LZW_byte_array(paddedencoded_text)
            output.write(bytes(byte_arr))

        print("Compression Completed")
        return outputpath

    """ Functions for decompression: """

    def removePadding(self, paddedencoded_text):
        padded_info = paddedencoded_text[:8]
        extraPadding = int(padded_info, 2)
        paddedencoded_text = paddedencoded_text[8:]
        return paddedencoded_text[:-extraPadding]

    def textDecode(self, encodedText):
        currentCode = ""
        decodedText = ""

        for bit in encodedText:
            currentCode += bit
            if currentCode in self.reverse_mapping_arr:
                decodedText += self.reverse_mapping_arr[currentCode]
                currentCode = ""

        return decodedText

    def decompressHuffman(self, inputPath):
        outputPath = "compress/decompress.txt"
        with open(inputPath, 'rb') as file, open(outputPath, 'w') as output:
            bitStrings = ""
            bytes_data = file.read(1)
            while len(bytes_data) > 0:
                bytes_data = ord(bytes_data)
                bit = bin(bytes_data)[2:].rjust(8, '0')
                bitStrings += bit
                bytes_data = file.read(1)

            encodedText = self.removePadding(bitStrings)
            decompressedText = self.textDecode(encodedText)
            output.write(decompressedText)

        print("Decompression Process Completed")
        return outputPath
