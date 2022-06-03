from math import pow
import numpy as np


class Automata:
    def __init__(self):
        self.canv_dimensions = (500, 500)
        self.canvas = np.zeros(self.canv_dimensions, dtype=np.float64)
        self.image = np.zeros((self.canv_dimensions[0], self.canv_dimensions[1], 3))
        self.image_colour = (0, 255, 0)

        self.filter = np.zeros((3, 3))
        self.activation = "abs"

    def update(self):
        self.convolve(self.canvas, self.filter)
        self.update_image()
        return self.image

    def update_image(self):
        filler = np.zeros(self.canv_dimensions, dtype=np.float64)
        self.image = np.stack((filler, self.canvas * 255, filler), axis=-1).astype(np.uint8)
    
    #convolution
    def convolve(self, x, filter):
        new = x.copy()
        target = np.zeros((3, 3), dtype=np.float64)
        maxrow = x.shape[0] - 1
        maxcol = x.shape[1] - 1
        for j in range(x.shape[1]):
            for i in range(x.shape[0]):
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
                prod = target * filter
                out = float(self.apply_activation(prod.sum()))
                new[i, j] = out
        self.canvas = new 
    
    def presetmode(self, filter):
        if filter == "stars":
            self.filter = np.array([[0.565, -0.716, 0.565], [-0.759, 0.627, -0.759], [0.565, -0.716, 0.565]], dtype=np.float64)
            self.activation = "abs"

        if filter == "conway":
            self.filter = np.ones((3, 3), dtype=np.float64)
            self.filter[1, 1] = 9
            self.activation = "con"

        if filter == "worms":
            self.filter = np.array([[0.68, -0.9, 0], [0, -0.66, 0], [0, 0, 0]], dtype=np.float64)
            self.activation = "invgauss"

        if filter == "waves":
            self.filter = np.array([[0.565, -0.716, 0.565], [-0.716, 0.627, -0.716], [0.565, -0.716, 0.565]], dtype=np.float64)
            self.activation = "2abs"
        
        if filter == "wolf":
            self.filter = np.array([[4, 2, 1], [0, 0, 0], [0, 0, 0]])
            self.activation = "wolf"
            self.center()
        
        if filter=="paths":
            self.filter = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
            self.activation = "gauss"

    #initialisation
    def randfloat_canv(self):
        self.canvas = np.random.rand(self.canv_dimensions[0], self.canv_dimensions[1])
        print("rand float")
        self.update_image()
        
    def randint_canv(self):
        print("rand int")
        self.canvas = np.random.randint(2, size=self.canv_dimensions).astype("float64")
        self.update_image()
    
    def center(self):
        print("center")
        self.canvas = np.zeros(self.canv_dimensions, dtype=np.float64)
        self.canvas[int(self.canv_dimensions[0] / 2), int(self.canv_dimensions[0] / 2)] = 1
        self.update_image()
    
    #activation functions
    def apply_activation(self, x):
        if self.activation == "abs":
            return np.abs(x)
        elif self.activation == "ident":
            return x
        elif self.activation == "invgauss":
            return -1./pow(2, (0.6*pow(x, 2)))+1
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
            b=1.35
            return 1/pow(2, (pow(x-b, 2)))
        else:
            print("activation error")
            print(self.activation)
            print(x)
    #custom filters
    def set_rand_filter(self):
        self.filter = np.random.uniform(-1, 1, (3, 3))
        print("set random filter:")
        print(self.filter)
#testing

# nca = Automata()
# nca.activation = "invgauss"
# print(nca.apply_activation(-2))

