from nca import Automata
import cv2 as cv
import tkinter as tk
from time import perf_counter

nca = Automata()
record = False

#UI
root = tk.Tk()
root.geometry("500x450")
root.title("controls")

heading = tk.Label(text="NCA control panel v1").grid(row=0, column=0, pady=5, sticky="W")

restarts = tk.LabelFrame(root, text="restarts")
restarts.grid(row=1, column=0, padx=15, pady=5, sticky="W")
randintB = tk.Button(restarts, text="randints", padx=10, pady=5, command=nca.randint_canv).grid(row=0, column=0, padx=5, pady=5)
randfloatB = tk.Button(restarts, text="randfloats", padx=10, pady=5, command=nca.randfloat_canv).grid(row=0, column=1, padx=5, pady=5)
centerinitB = tk.Button(restarts, text="center", padx=13, pady=5, command=nca.center).grid(row=1, column=0, padx=5, pady=5)

def setstats(avg, count, isrec):
    countfield.delete(0, tk.END)
    timefield.delete(0, tk.END)
    recordfield.delete(0, tk.END)
    timefield.insert(0, avg)
    countfield.insert(0, count)
    if isrec:
        recordfield.insert(0, "recording")
    else:
        recordfield.insert(0, "not recording")
stats = restarts = tk.LabelFrame(root, text="stats")
stats.grid(row=2, column=1, padx=10, pady=5, sticky="W")
_ = tk.Label(stats, text="avg render time:").grid(row=0, column=0, padx=5, pady=5)
timefield = tk.Entry(stats, width=10)
timefield.grid(row=0, column=1, padx=5, pady=5)
_ = tk.Label(stats, text="render count:").grid(row=1, column=0, padx=5, pady=5)
countfield = tk.Entry(stats, width=10)
countfield.grid(row=1, column=1, padx=5, pady=5)
recordfield = tk.Entry(stats, width=15)
recordfield.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
recordfield.insert(0, "not recording")


def setrecord(x):
    global record
    record = x
recording = tk.StringVar()
recording.set("2")
records = tk.LabelFrame(root, text="recording")
records.grid(row=1, column=1, padx=10, pady=5, sticky="W")
startrecB = tk.Radiobutton(records, text="is recording", padx=5, pady=0, command=lambda: setrecord(True), variable=recording, value="1").grid(row=0, column=0, padx=3, pady=5, sticky="W")
endrecB = tk.Radiobutton(records, text="is not recording", padx=5, pady=0, command=lambda: setrecord(False), variable=recording, value="2").grid(row=1, column=0, padx=3, pady=5, sticky="W")

mode = tk.StringVar()
mode.set("0")
load = tk.LabelFrame(root, text="load")
load.grid(row=2, column=0, padx=15, pady=5, sticky="W")
stars = tk.Radiobutton(load, text="stars", variable=mode, value="1", command=lambda: nca.presetmode("stars")).grid(row=0, column=0, sticky="W")
conways = tk.Radiobutton(load, text="Conway's game of life", variable=mode, value="2", command=lambda: nca.presetmode("conway")).grid(row=1, column=0, sticky="W")
waves = tk.Radiobutton(load, text="waves", variable=mode, value="3", command=lambda: nca.presetmode("waves")).grid(row=2, column=0, sticky="W")
worms = tk.Radiobutton(load, text="worms", variable=mode, value="4", command=lambda: nca.presetmode("worms")).grid(row=3, column=0, sticky="W")
wolfB = tk.Radiobutton(load, text="Wolfram's rule 30", variable=mode, value="5", command=lambda: nca.presetmode("wolf")).grid(row=4, column=0, sticky="W")
pathB = tk.Radiobutton(load, text="paths", variable=mode, value="6", command=lambda: nca.presetmode("paths")).grid(row=5, column=0, sticky="W")

def setident(): nca.activation = "ident"
def setabs(): nca.activation = "abs"

activ = tk.StringVar()
activ.set("0")
setf = tk.LabelFrame(root, text="custom")
setf.grid(row=3, column=0, padx=15, pady=5, sticky="E")
randomB = tk.Button(setf, text="random filter", command=nca.set_rand_filter, padx=5, pady=8).grid(row=0, column=0, sticky="W", padx=5, pady=8, rowspan=3)
active = tk.Label(setf, text="Activation function:").grid(row=0, column=1, pady=5, sticky="W")
identB = tk.Radiobutton(setf, text="identity", variable=activ, value="1", command=setident).grid(row=1, column=1)
absB = tk.Radiobutton(setf, text="absolute", variable=activ, value="2", command=setabs).grid(row=2, column=1)


#record video
fps = 20
video = cv.VideoWriter('render.avi',cv.VideoWriter_fourcc(*'DIVX'), fps, nca.canv_dimensions)

# s is scaling for image
s=1.5
#mainloop starts here
lastrun = perf_counter()
frame = nca.update()
for i in range(frame.shape[0]):
    print(frame[i, :, 1])
print(frame.shape)
print(frame.dtype)
avg = 0
prev = 1
beta = 1 - (1 / 6) # change p in 1 - (1 / p) for precision  
count = 1
while True:
    try:
        #update image
        now = perf_counter()
        if now - lastrun > 0.1:
            time1 = perf_counter()
            frame = nca.update()
            if record:
                video.write(frame)
            time2 = perf_counter()
            #collect state data
            lastrun = now
            avg = beta * prev + (1 - beta) * (time2 - time1)

        res = cv.resize(frame, (int(frame.shape[1] * s), int(frame.shape[0] * s)), interpolation=cv.INTER_AREA)
        cv.imshow("Neural cellular automata", res)

        if cv.waitKey(10) & 0xFF == ord('q'):
            break
        root.update()

        #print state
        setstats(round(avg, 3), count, record)
        count += 1
    except ArithmeticError:
        print("excepted")
        break
cv.destroyAllWindows()
video.release()
# r = threading.Thread(target=run)
# r.start()
# root.mainloop()
