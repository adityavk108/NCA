import numpy as np
from sklearn.linear_model import LinearRegression

class Automata:
    def __init__(self, np_image):

        self.image = np_image[:, :, 0:3].astype(np.float64)
        self.canvshape = np_image.shape[0:2]

        self.anti_decay = 0.3431335897049337 #over 50 frames
        self.convcount = 0

        try:
            self.filter_array = np.load("weights.npy")
            #(image rows, image columns, filter rows, filter columns, color channels)
            self.intercepts = np.load("intercepts.npy")
            #(image rows, image columns, color channels)
        except:
            print("excepting filters to zero")
            self.filter_array = np.zeros((self.canvshape[0], self.canvshape[1], 3, 3, 3), dtype=np.float64)
            self.intercepts = np.zeros((self.canvshape[0], self.canvshape[1], 3), dtype=np.float64)
        self.out = self.create_image()

    def update(self):
        self.convolve()
        if self.convcount % 50 == 0:
            self.correct_decay()
        out = self.create_image()
        return out

    def create_image(self):
        #filler = np.zeros(self.canvshape, dtype=np.float64)
        return (self.image).astype(np.uint8)

    
    #convolution
    """convolves each pixel of the given image with their corresponding filter"""
    def convolve(self):
        x = self.image
        new = x.copy()
        target = np.zeros((3, 3), dtype=np.float64)
        maxrow = x.shape[0] - 1
        maxcol = x.shape[1] - 1
        for channel in range(x.shape[2]):
            for j in range(x.shape[1]):
                for i in range(x.shape[0]):
                    #target matrix extraction
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

                                target[tr, tc] = x[r, c, channel].copy()                         
                    else:
                        target = x[i-1:i+2, j-1:j+2, channel].copy()
                    #computation
                    filter = self.filter_array[i, j, :, :, channel]
                    prod = target * filter
                    out = float(prod.sum())
                    new[i, j, channel] = out
        self.image = new
        self.convcount += 1

    #REGRESSION
    """Computes the filter and bias for each pixel of the image across each channel"""
    def regression(self, inp):
        #extract key value pairs
        x = np.zeros((9))
        x[0:3] = inp[0, :]
        x[3:5] = inp[1, ::2]
        x[5:8] = inp[2, :]
        x[8] = 1
        y = inp[1, 1]

        #train model and extract weights
        model = LinearRegression(fit_intercept=False)
        model.fit([x], [y])
        w = model.coef_
        #assemble theta
        w_ass = np.zeros((3, 3))
        w_ass[0, :] = w[0:3]
        w_ass[1, ::2] = w[3:5]
        w_ass[2, :] =  w[5:8]

        c = inp[1, 1] - np.sum(inp * w_ass)
        return w_ass, c

    """Computes and arranges filter of each pixel across all channels into filter_array"""
    def compute_filters(self):
        x = self.image
        maxrow = x.shape[0] - 1
        maxcol = x.shape[1] - 1
        target = np.zeros((3, 3), dtype=np.float64)
        for channel in range(x.shape[2]):
            for row in range(x.shape[0]):
                for column in range(x.shape[1]):
                    #target matrix extraction
                    if row == 0 or column == 0 or row == maxrow or column == maxcol:
                        for tr in range(3):
                            for tc in range(3):
                                r = row - 1 + tr
                                c = column - 1 + tc
                                if r < 0:
                                    r = maxrow
                                if c < 0:
                                    c = maxcol

                                if r > maxrow:
                                    r = 0
                                if c > maxcol:
                                    c = 0

                                target[tr, tc] = x[r, c, channel].copy()
                    else:
                        target = x[row-1:row+2, column-1:column+2, channel].copy()
                    #compute weights and biases and assign
                    w, c = self.regression(target)
                    self.filter_array[row, column, :, :, channel] = w
                    self.intercepts[row, column, channel] = c
                print(f"row {row+1} channel {channel+1} done")
    
    """Save and manipulate filters"""
    def save_filters(self):
        print("saved filters")
        np.save("weights.npy", self.filter_array)
        np.save("intercepts.npy", self.filter_array)

    def zero_filters(self):
        print("set filters to zero")
        self.filter_array = np.zeros((self.canvshape[0], self.canvshape[1], 3, 3, 3), dtype=np.float64)
        self.intercepts = np.zeros((self.canvshape[0], self.canvshape[1], 3), dtype=np.float64)

    """add noise"""
    def intnoise(self):
        shape = self.canvshape
        clow, chigh = 0.45, 0.55
        rlow, rhigh = 0.45, 0.55
        slice = self.image[int(shape[0] * rlow):int(shape[0] * rhigh), int(shape[1] * clow):int(shape[1] * chigh), :].copy()
        x = np.random.randint(2, size=slice.shape).astype("float64") * 200
        self.image[int(shape[0] * rlow):int(shape[0] * rhigh), int(shape[1] * clow):int(shape[1] * chigh), :] = slice + x
        print("noise added")

    """correct decay from convolution"""
    def correct_decay(self):
        self.image = self.image + self.anti_decay
        print("corrected for decay")
    
#testing

# nca = Automata()
# nca.activation = "invgauss"
# print(nca.apply_activation(-2))

