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
    mandelbrot_grid = np.zeros((height, width))

    for i in range(height):
        for j in range(width):
            mandelbrot_grid[i, j] = mandelbrot(complex(x[j], y[i]), max_iter)

    return mandelbrot_grid

def plot_mandelbrot(xmin, xmax, ymin, ymax, max_iter, width, height):
    mandelbrot_grid = mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter)
    plt.imshow(mandelbrot_grid, extent=(xmin, xmax, ymin, ymax), cmap='inferno', origin='lower')
    plt.xlabel('Re(c)')
    plt.ylabel('Im(c)')
    plt.title('Mandelbrot Set')
    plt.gca().set_aspect('equal')

def on_click(event):
    global xmin, xmax, ymin, ymax, width, height
    x_center, y_center = event.xdata, event.ydata
    zoom_factor = 0.5  # Zoom factor

    # Calculate new limits
    x_range = (xmax - xmin) * zoom_factor
    y_range = (ymax - ymin) * zoom_factor
    xmin_new = x_center - x_range / 2
    xmax_new = x_center + x_range / 2
    ymin_new = y_center - y_range / 2
    ymax_new = y_center + y_range / 2

    # Update global limits
    xmin, xmax, ymin, ymax = xmin_new, xmax_new, ymin_new, ymax_new
    
    # Update width and height for higher resolution
    width *= 2
    height *= 2
    
    # Clear the current plot and plot the Mandelbrot set with higher resolution
    plt.clf()
    plot_mandelbrot(xmin, xmax, ymin, ymax, max_iter, width, height)
    plt.draw()

# Define parameters
xmin, xmax = -2, 2
ymin, ymax = -2, 2
max_iter = 100
width, height = 800, 800

# Plot Mandelbrot set
plot_mandelbrot(xmin, xmax, ymin, ymax, max_iter, width, height)

# Connect mouse click event for zooming
plt.gcf().canvas.mpl_connect('button_press_event', on_click)

plt.show()
