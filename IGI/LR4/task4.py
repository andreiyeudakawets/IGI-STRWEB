
from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
from inputs import input_float, input_color, try_input_int as input_int


class Figure(ABC):
    @abstractmethod
    def calculate_area(self):
        """
        Abstract method to calculate the area of the geometric shape.
        """
        pass


class ChangeSizeMixin:
    def change(self, size):
        self.a = size


class FigureColor:
    def __init__(self):
        self._color = "red"

    @property
    def color(self):
        """Get the color."""
        return self._color
    
    @color.setter
    def color(self, value):
        """Set the color"""
        self._color = value
    

class Fiveangler(Figure, ChangeSizeMixin):
    """
    The Pentagon class represents a pentagon and extends the Shape class.
    """

    name = "pentagon"

    def __init__(self, a, color):
        #super().__init__()
        #self.name = name
        self.a = a
        self.col = FigureColor()
        self.col.color = color


    @property
    def a(self):
        """
        Getter for the side length.
        """
        return self._a
    
    @a.setter
    def a(self, value):
        """
        Setter for the side length.
        """
        if not isinstance(value, int) or value <= 0:
           value = 1
        self._a = value    


    def calculate_area(self):
        return ((5*self.a**2)/(4*np.tan(np.pi/5)))
    
    def get_name(self):
        return self.name

    def describe(self):
        """
        Возвращаем строку с параметрами фигуры, ее цветом и площадью
        """
        
        return "Shape: {0}, Color: {1}, Area: {2:.2f}".format(self.__class__.__name__, self.col.color, self.calculate_area())

    def draw(self):

        x_A = 10
        y_A = 10

        x_B = x_A + self.a 
        y_B = y_A

        x_C = x_B + self.a * np.sin(np.pi / 10)
        y_C = y_B - self.a * np.cos(np.pi / 10)
        
        x_D = x_C - self.a * np.cos(2*np.pi / 10)
        y_D = y_C - self.a * np.sin(2*np.pi / 10)

        x_E = x_D - self.a * np.cos(2*np.pi / 10)
        y_E = y_D + self.a * np.sin(2*np.pi / 10)

        x_F = x_E + self.a * np.sin(np.pi / 10)
        y_F = y_E + self.a * np.cos(np.pi / 10)

        x_coords = [x_A, x_B, x_C, x_D, x_E, x_F]
        y_coords = [y_A, y_B, y_C, y_D, y_E, y_F]

        plt.plot(x_coords,  y_coords, self.col.color)

        plt.fill(x_coords, y_coords, self.col.color, alpha=0.5)

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(self.get_name())
        plt.grid(True)
        plt.axis("equal")
        plt.savefig(r'C:\Users\Andrei\PycharmProjects\IGI4\fourth.png', dpi=300)
        plt.show()


def task4():
    """
    performs the fourth task
    """
    colors = ['red', 'green', 'yellow', 'black', 'grey', 'blue', 'purple']

    c = input_color(colors)
    size = input_float("Size")
    a = Fiveangler(size, c)
    a.name = input("Name: ")
    
    print(a.describe())
    a.draw()

    print("Do you want to change size of figure? (1 - yes, other - no)\n")
    while True:
        option = input("choose the option")
        if option == '1':
            size = input_float("Size")
            a.change(size)
            a.draw()
            break
        else:
            break

