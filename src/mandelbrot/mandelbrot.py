# draw a mandelbrot set
from typing import Tuple

import numpy as np
import matplotlib.pyplot as plt

def mandelbrot(c: complex, max_iter: int) -> int:
    """determine if a complex number is in the mandelbrot set"""

    z = c
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def mandelbrot_set(xmin: float, xmax: float, ymin: float, ymax: float, width: int, height: int, max_iter: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """create a mandelbrot set image"""

    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width, height))
    for i in range(width):
        for j in range(height):
            # n3[i, j] is the number of iterations before z becomes unbounded
            n3[i, j] = mandelbrot(r1[i] + 1j*r2[j], max_iter)
    return (r1, r2, n3)

def display(xmin, xmax, ymin, ymax, width, height, max_iter):
    dpi = 72
    img_width = width
    img_height = height
    x_min = xmin
    x_max = xmax
    y_min = ymin
    y_max = ymax
    n3 = mandelbrot_set(x_min, x_max, y_min, y_max, img_width, img_height, max_iter)
    # save the image
    plt.figure(figsize=(img_width/dpi, img_height/dpi), dpi=dpi)
    plt.imshow(n3[2], extent=(x_min, x_max, y_min, y_max))
    plt.set_cmap('Pastel1')
    # plt.colorbar()
    plt.savefig('mandelbrot.png')

if __name__ == '__main__':
    display(-2.0, 0.5, -1.25, 1.25, 1000, 1000, 100)
