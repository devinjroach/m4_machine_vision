import os
import numpy as np
import matplotlib.pyplot as plt

from skimage import data, color
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte


def main():
    img = os.path.join(os.getcwd(), 'newstage1.bmp')

    image = img_as_ubyte(img)
    edges = canny(image, sigm=3, low_threshold=10, high_threshold=50)

    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 4))
    image = color.gray2rgb(image)

    ax.imshow(image, cmap=plt.cm.gray)
    plt.show()


if __name__ == '__main__':
    main()
