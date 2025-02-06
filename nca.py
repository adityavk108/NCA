from math import pow
import numpy as np


class Automata:
    def __init__(self):
        """
        Initialize the Automata class with default parameters.
        - A 500x500 canvas initialized with zeros.
        - An image representation with three channels.
        - A default filter (3x3 zero matrix).
        """
        self.canv_dimensions = (500, 500)
        self.canvas = np.zeros(self.canv_dimensions, dtype=np.float64)
        self.image = np.zeros((self.canv_dimensions[0], self.canv_dimensions[1], 3))
        self.image_colour = (0, 255, 0)

        self.filter = np.zeros((3, 3))
        self.activation = "abs"

    def update(self):
        """
        Update the canvas by applying convolution and updating the image representation.
        Returns the updated image.
        """
        self.convolve(self.canvas, self.filter)
        self.update_image()
        return self.image

    def update_image(self):
        """
        Convert the canvas into an RGB image representation.
        The green channel is used to visualize the canvas state.
        """
        filler = np.zeros(self.canv_dimensions, dtype=np.float64)
        self.image = np.stack((filler, self.canvas * 255, filler), axis=-1).astype(np.uint8)
    
    def convolve(self, x, filter):
        """
        Apply convolution to the canvas using the given filter.
        Handles edge cases by wrapping values around the borders (toroidal addressing).
        """
        new = x.copy()
        target = np.zeros((3, 3), dtype=np.float64)
        maxrow = x.shape[0] - 1
        maxcol = x.shape[1] - 1
        
        for j in range(x.shape[1]):
            for i in range(x.shape[0]):
                # Handle border conditions with wrapping
                if i == 0 or j == 0 or i == maxrow or j == maxcol:
                    for tr in range(3):
                        for tc in range(3):
                            r = i - 1 + tr
                            c = j - 1 + tc
                            if r < 0:
                                r = maxrow
                            if c < 0:
                                c = maxcol
                            if r > maxrow:
                                r = 0
                            if c > maxcol:
                                c = 0
                            target[tr, tc] = x[r, c]
                else:
                    target = x[i-1:i+2, j-1:j+2]
                
                # Apply filter and activation function
                prod = target * filter
                out = float(self.apply_activation(prod.sum()))
                new[i, j] = out
        
        self.canvas = new 
    
    def presetmode(self, filter):
        """
        Set predefined filter values and activation functions based on mode.
        """
        if filter == "stars":
            self.filter = np.array([[0.565, -0.716, 0.565],
                                    [-0.759, 0.627, -0.759], 
                                    [0.565, -0.716, 0.565]], dtype=np.float64)
            self.activation = "abs"

        elif filter == "conway":
            self.filter = np.ones((3, 3), dtype=np.float64)
            self.filter[1, 1] = 9
            self.activation = "con"

        elif filter == "worms":
            self.filter = np.array([[0.68, -0.9, 0.68], 
                                    [-0.9, -0.66, -0.9], 
                                    [0.68, -0.9, 0.68]], dtype=np.float64)
            self.activation = "invgauss"

        elif filter == "waves":
            self.filter = np.array([[0.565, -0.716, 0.565], 
                                    [-0.716, 0.627, -0.716], 
                                    [0.565, -0.716, 0.565]], dtype=np.float64).T
            self.activation = "2abs"
        
        elif filter == "wolf":
            self.filter = np.array([[4, 2, 1], 
                                    [0, 0, 0], 
                                    [0, 0, 0]])
            self.activation = "wolf"
            self.center()
        
        elif filter == "paths":
            self.filter = np.array([[0, 1, 0], 
                                    [1, 1, 1], 
                                    [0, 1, 0]])
            self.activation = "gauss"

        elif filter == "slime":
            self.filter = np.array([[0.8, -0.85, 0.8], 
                                    [-0.85, -0.2, -0.85], 
                                    [0.8, -0.85, 0.8]])
            self.activation = "slime"
    
    def randfloat_canv(self):
        """Initialize the canvas with random float values between 0 and 1."""
        self.canvas = np.random.rand(self.canv_dimensions[0], self.canv_dimensions[1])
        print("rand float")
        self.update_image()
        
    def randint_canv(self):
        """Initialize the canvas with random integer values (0 or 1)."""
        print("rand int")
        self.canvas = np.random.randint(2, size=self.canv_dimensions).astype("float64")
        self.update_image()
    
    def center(self):
        """Initialize the canvas with a single active cell in the center."""
        print("center")
        self.canvas = np.zeros(self.canv_dimensions, dtype=np.float64)
        self.canvas[int(self.canv_dimensions[0] / 2), int(self.canv_dimensions[0] / 2)] = 1
        self.update_image()
    
    def apply_activation(self, x):
        """Apply the chosen activation function to a given value."""
        if self.activation == "abs":
            return np.abs(x)
        elif self.activation == "ident":
            return x
        elif self.activation == "invgauss":
            return -1./pow(2, (0.6*pow(x, 2.0)))+1.0
        elif self.activation == "2abs":
            return np.abs(1.2 * x)
        elif self.activation == "con":
            if (x == 3.0 or x == 11.0 or x == 12.0):
                return 1.0
            else:
                return 0.0
        elif self.activation == "wolf":
            if (x == 1 or x == 2 or x == 3 or x == 4):
                return 1
            else:
                return 0
        elif self.activation == "gauss":
            b=3.5
            return 1/pow(2.0, (pow(x-b, 2.0)))
        elif self.activation == "slime":
            return -1.0/(0.89*pow(x, 2.0)+1.0)+1.0
        else:
            print("activation error")
            print(self.activation)
            print(x)
    
    def set_rand_filter(self):
        """Generate and set a random 3x3 filter with values in the range [-1, 1]."""
        self.filter = np.random.uniform(-1, 1, (3, 3))
        print("set random filter:")
        print(self.filter)
