# Based on https://scikit-learn.org/stable/auto_examples/cluster/plot_color_quantization.html#color-quantization-using-k-means

import numpy as np
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
from time import time

def run_algorithm(image, n_colors):
    # Load Image and transform to a 2D numpy array.
    w, h, d = tuple(image.shape)
    assert d == 3
    image_array = np.reshape(image, (w * h, d))

    print("Fitting model on a small sub-sample of the data")
    t0 = time()
    image_array_sample = shuffle(image_array, random_state=0, n_samples=1_000)
    kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(image_array_sample)
    print(f"done in {time() - t0:0.3f}s.")

    # Get labels for all points
    print("Predicting color indices on the full image (k-means)")
    t0 = time()
    labels = kmeans.predict(image_array)
    print(f"done in {time() - t0:0.3f}s.")

    def recreate_image(codebook, labels, w, h):
        """Recreate the (compressed) image from the code book & labels"""
        return codebook[labels].reshape(w, h, -1)

    return recreate_image(kmeans.cluster_centers_, labels, w, h)