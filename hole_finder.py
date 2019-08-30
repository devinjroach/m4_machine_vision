import os
import numpy as np
import matplotlib.pyplot as plt

from skimage import data, color
from skimage.io import imread
from skimage.transform import hough_circle, hough_circle_peaks
from skimage.feature import canny
from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte
from scipy import ndimage as ndi


def main():
    img = os.path.join(os.getcwd(), 'newstage1.jpg')
    image = imread(img, as_gray=True)
    image = img_as_ubyte(image)
    image = ndi.gaussian_filter(image, 1)

    edges1 = canny(image, sigma=1, low_threshold=10, high_threshold=50)

    hough_radii = np.arange(20, 60, 3)
    hough_res = hough_circle(edges1, hough_radii)

    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                               total_num_peaks=3)

    print(len(radii))

    image = color.gray2rgb(image)

    for center_y, center_x, radius in zip(cy, cx, radii):
        circy, circx = circle_perimeter(center_y, center_x, radius,
                                        shape=image.shape)

        image[circy, circx] = (220, 20, 20)

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 4),
                                   sharex=True, sharey=True)

    ax1.imshow(image, cmap=plt.cm.gray)

    ax2.imshow(edges1, cmap=plt.cm.gray)
    plt.show()


if __name__ == '__main__':
    main()
