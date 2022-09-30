from PIL import Image
import numpy as np

def get_color_count(np_image):
    colors = {}
    for x in range(np_image.shape[0]):
        for y in range(np_image.shape[1]):
            pixel = np_image[x,y]
            colors[f'{pixel[0]}-{pixel[1]}-{pixel[2]}'] = 1
    return len(colors)

def get_image(file):
    image = Image.open(file) 

    color_count = get_color_count(np.array(image, dtype=np.uint8))

    # Convert to floats instead of the default 8 bits integer coding. Dividing by
    # 255 is important so that plt.imshow behaves works well on float data (need to
    # be in the range [0-1])
    image = np.array(image, dtype=np.uint8)
    return image, color_count