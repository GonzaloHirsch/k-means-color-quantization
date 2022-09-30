import math
import numpy as np
from datetime import datetime
import argparse
from bitstring import BitArray
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# File formatting is
# |2 bytes - width|2 bytes - height|2 bytes - color count|1 byte - index size|
# |Variable - colors (3 bytes per color)|Variable - data|


def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

def bytes_to_bitstring(s):
    return bin(int.from_bytes(s, "big"))

# Storing the image in a custom file format


def store_image(image, color_count):
    image_shape = image.shape
    # Get the variables in proper shapes
    width, height = np.uint16(image_shape[1]), np.uint16(image_shape[0])
    colors = np.uint16(color_count)
    color_size = math.ceil(math.log2(color_count))
    # Compute all the colors and the map and create the resulting array
    color_map = {}
    color_index = {}
    index = 0
    result = []
    for row in range(image_shape[0]):
        for col in range(image_shape[1]):
            # Compute the key
            color_key = f'{image[row,col][0]}-{image[row,col][1]}-{image[row,col][2]}'
            # Compute the index
            if not color_key in color_map:
                # Store in map
                color_map[color_key] = index
                color_index[index] = [np.uint8(image[row, col][0]),
                                      np.uint8(image[row, col][1]),
                                      np.uint8(image[row, col][2])]
                index += 1
            # Compute the image result
            result.append(color_map[color_key])
    # Adding width & height
    data = np.binary_repr(width, 16) + np.binary_repr(height, 16)
    # Adding color count & size
    data += np.binary_repr(colors, 16) + np.binary_repr(color_size, 8)
    # Add color data
    for i in range(color_count):
        data += np.binary_repr(color_index[i][0], 8) + np.binary_repr(
            color_index[i][1], 8) + np.binary_repr(color_index[i][2], 8)
    # Add pixel data
    for pixel in result:
        data += np.binary_repr(pixel, color_size)
    # Store the data
    byte_data = bitstring_to_bytes(data)
    with open(f"sample/result-{int(datetime.timestamp(datetime.now()))}.gonza", "wb") as binary_file:
        binary_file.write(byte_data)

def restore_image(file):
    binary_arr = BitArray(bytes=open(file, 'rb').read())
    # Get basic properties
    print("BUILDING VARIABLES...")
    index = 0
    width = binary_arr[index:index + 16].uint
    index += 16
    height = binary_arr[index:index + 16].uint
    index += 16
    color_count = binary_arr[index:index + 16].uint
    index += 16
    index_size = binary_arr[index:index + 8].uint
    index += 8
    # Read color data
    print("BUILDING COLORS...")
    color_index = {}
    for i in range(color_count):
        # build the color
        arr = [None] * 3
        for j in range(3):
            arr[j] = binary_arr[index:index + 8].uint
            index += 8
        arr = np.array(arr)
        # Add to the index
        color_index[i] = arr
    # Read the pixel data
    print("BUILDING IMAGE...")
    raw_image = []
    total_pixels = width * height
    for i in range(total_pixels):
        # Get the index
        c_index = binary_arr[index:index + index_size].uint
        # Get the color and add it
        raw_image.append(color_index[c_index])
        index += index_size
        print(f"READING PIXEL {i}/{total_pixels}...", end="\r")
    raw_image = np.array(raw_image).reshape((height, width, 3))/255
    fig, ax = plt.subplots(figsize=(12,7))
    ax.set_title(f'Compressed Image ({color_count} Colors)')
    ax.xaxis.set_major_locator(ticker.NullLocator())
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.imshow(raw_image)
    plt.show()

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="K-Means Color Quantization - Restore Image")

    # Add arguments
    parser.add_argument('-f', dest='file', required=True)    # Path to file
    args = parser.parse_args()

    restore_image(args.file)

    
if __name__ == '__main__':
    main()
