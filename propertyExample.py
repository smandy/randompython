class Circle:
    def __init__(self, radius):
        self._radius = radius  # Use a leading underscore to indicate a protected attribute
    
    # Getter for radius
    @property
    def radius(self):
        print("Getting radius")
        return self._radius
    
    # Setter for radius
    @radius.setter
    def radius(self, value):
        print("Setting radius")
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
    
    # Deleter for radius
    @radius.deleter
    def radius(self):
        print("Deleting radius")
        del self._radius
    
    # Read-only property for area
    @property
    def area(self):
        print("Calculating area")
        import math
        return math.pi * (self._radius ** 2)

# Example usage
circle = Circle(5)
print(circle.radius)  # Getting radius -> 5
circle.radius = 10    # Setting radius
print(circle.radius)  # Getting radius -> 10
print(circle.area)    # Calculating area -> 314.1592653589793

try:
    circle.radius = -1  # Setting radius -> ValueError: Radius cannot be negative
except ValueError as e:
    print(e)

del circle.radius      # Deleting radius

try:
    print(circle.radius)  # AttributeError: 'Circle' object has no attribute '_radius'
except AttributeError as e:
    print(e)
