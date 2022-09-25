import argparse
from slider import build_slider
from image import get_image

def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="K-Means Color Quantization")

    # Add arguments
    parser.add_argument('-f', dest='file', required=True)    # Path to file
    args = parser.parse_args()

    # Open the iamge only once
    image, color_count = get_image(args.file)
    # Build the slider
    build_slider(image, color_count)
    
if __name__ == '__main__':
    main()
