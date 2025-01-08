from typing import Tuple
from PIL import Image

import matplotlib.animation as manim
import numpy as np
import matplotlib.pyplot as plt


def mandelbrot(c: complex, max_iter: int) -> int:
    """
    determine if a complex number is in the mandelbrot set

    Args:
        c: complex number to test, verify if it is in the mandelbrot set
        max_iter: maximum number of iterations to test if c is in the mandelbrot set boundaries

    Returns:
        int: number of iterations before the sequence becomes unbounded, its purpose is to determine if
        c is in the mandelbrot set and if not how fast it diverges
        resulting on changing the color of the pixel in the mandelbrot set image
    """

    z = c
    for n in range(max_iter):
        # if abs(z) > 2, then the sequence will diverge to infinity it is not in the mandelbrot set
        if abs(z) > 2:
            return n

        # update the sequence based on the mandelbrot set formula
        # z(n+1) = z(n)^2 + c
        z = z * z + c
    return max_iter


def mandelbrot_set(xmin: float, xmax: float, ymin: float, ymax: float, width: int, height: int, max_iter: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    compute the mandelbrot image over the given range
    xmin, xmax, ymin, ymax define the rectangular region in the complex plane to compute the mandelbrot set

    Args:
        xmin: minimum value of the x-axis
        xmax: maximum value of the x-axis
        ymin: minimum value of the y-axis
        ymax: maximum value of the y-axis
        width: width of the image in pixels
        height: height of the image in pixels
        max_iter: maximum number of iterations to test if a complex number is in the mandelbrot set
    """

    # r1 and r2 are 1-D arrays representing the real and imaginary parts of the complex numbers
    # the points are evenly spaced along the real and imaginary axes
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)

    # store the number of iterations before the sequence becomes unbounded (max_iter meaning it is in the mandelbrot set)
    n3 = np.empty((width, height))
    for i in range(width):
        for j in range(height):
            # n3[i, j] is the number of iterations before z becomes unbounded
            n3[i, j] = mandelbrot(r1[i] + 1j * r2[j], max_iter)
    return (r1, r2, n3)


def display(xmin: float, xmax: float, ymin: float, ymax: float, width: int, height: int, max_iter: int, name: str = 'mandelbrot.png') -> Image.Image:
    """
    display the mandelbrot set
    """

    dpi = 72
    img_width = width
    img_height = height
    x_min = xmin
    x_max = xmax
    y_min = ymin
    y_max = ymax

    # get the mandelbrots set
    n3 = mandelbrot_set(x_min, x_max, y_min, y_max, img_width, img_height, max_iter)

    # create the plot without saving intermediate images
    fig, ax = plt.subplots(figsize=(img_width / dpi, img_height / dpi), dpi=dpi)
    ax.imshow(n3[2], extent=(x_min, x_max, y_min, y_max))
    plt.set_cmap('hot')
    plt.axis('off')

    # plt.savefig(name)
    plt.close(fig)

    # convert to image
    img = Image.open(name)
    return img

if __name__ == '__main__':
    frames = []

    # create a gif of the mandelbrot set
    for i in range(100):
        frames.append(display(-2.0, 0.5, -1.25, 1.25, 1000, 1000, i, f'mandelbrot_{i}.png'))

    # create the gif
    frames[0].save('mandelbrot.gif', save_all=True, append_images=frames[1:], optimize=False, duration=40, loop=0)
