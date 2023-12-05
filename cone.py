from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

# Define the base and height of the cone
r = 1
h = 3

# Define the x and y coordinates of the base circle
theta = np.linspace(0, 2*np.pi, 100)
x = r * np.cos(theta)
y = r * np.sin(theta)

# Define the z coordinates of the cone
z = np.linspace(0, h, 50)

# Create a 3D axes object
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the cone using the plot_surface function
X, Y = np.meshgrid(x, y)
Z = np.sqrt(X**2 + Y**2) * h / r
ax.plot_surface(X, Y, Z, alpha=0.5)

# Set the limits and labels of the plot
ax.set_xlim(-r, r)
ax.set_ylim(-r, r)
ax.set_zlim(0, h)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Enable interactive rotation and zooming
ax.view_init(elev=30, azim=30)
ax.mouse_init()

# Display the plot
plt.show()
