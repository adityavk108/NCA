import numpy as np


class Automata:
    def __init__(self):
        self.canv_dimensions = (500, 500)
        self.canvas = np.zeros(self.canv_dimensions, dtype=np.float64)
        self.image = np.zeros((self.canv_dimensions[0], self.canv_dimensions[1], 3))
        self.image_colour = (0, 255, 0)

        self.filter = np.array([[4, 2, 1], [0, 0, 0], [0, 0, 0]])

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
        self.canvas += new

    #initialisation
    def center(self):
        print("center")
        self.canvas = np.zeros(self.canv_dimensions, dtype=np.float64)
        self.canvas[int(self.canv_dimensions[0] / 2), int(self.canv_dimensions[0] / 2)] = 1
        self.update_image()
    
    #activation functions
    def apply_activation(self, x):
        if (x == 1 or x == 2 or x == 3 or x == 4):
            return 1
        else:
            return 0
#testing

# nca = Automata()
# nca.activation = "invgauss"
# print(nca.apply_activation(-2))


##########################################################################################################################################################################
import cv2 as cv
from time import perf_counter


nca = Automata()
nca.center()

#record video
fps = 20
video = cv.VideoWriter('wolfram.avi',cv.VideoWriter_fourcc(*'DIVX'), fps, nca.canv_dimensions)

# s is scaling for image
s=1.5
#mainloop starts here
lastrun = perf_counter()
frame = nca.update()

tsum = 0.0
count = 1
while True:
    try:
        #update image
        now = perf_counter()
        if now - lastrun > 0.1:
            time1 = perf_counter()
            frame = nca.update()
            video.write(frame)
            time2 = perf_counter()
            #collect state data
            tsum += round(time2 - time1, 3)
            lastrun = now

        res = cv.resize(frame, (int(frame.shape[1] * s), int(frame.shape[0] * s)), interpolation=cv.INTER_AREA)
        cv.imshow("Neural cellular automata", res)

        if cv.waitKey(10) & 0xFF == ord('q'):
            break

        #print state
        avg = round(tsum / count, 3)
        print(f"average time:{avg} count:{count}")
        count += 1

    except:
        print("excepted")
        break
cv.destroyAllWindows()
video.release()
# r = threading.Thread(target=run)
# r.start()
# root.mainloop()
