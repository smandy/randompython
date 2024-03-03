import numpy as np
import matplotlib.pyplot as plt

def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z**2 + c
        n += 1
    return n

def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    mandelbrot_grid = np.zeros((width, height))

    for i in range(width):
        for j in range(height):
            mandelbrot_grid[i, j] = mandelbrot(complex(x[i], y[j]), max_iter)

    return mandelbrot_grid

def plot_mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter):
    mandelbrot_grid = mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter)
    plt.imshow(mandelbrot_grid.T, extent=(xmin, xmax, ymin, ymax))
    plt.xlabel('Re(c)')
    plt.ylabel('Im(c)')
    plt.title('Mandelbrot Set')
    plt.show()

# Define parameters
xmin, xmax = -2, 2
ymin, ymax = -2, 2
width, height = 800, 800
max_iter = 100

# Plot Mandelbrot set
plot_mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter)
