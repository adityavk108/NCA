from rnca import Automata
import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from time import perf_counter
import time
record = False
filename = ""

#UI
root = tk.Tk()
root.geometry("500x450")
root.title("controls")

#get file directory
runwind = True
def insert_im():
    global runwind, filename
    runwind = False
    filename = filedialog.askopenfilename()
def default_dir():
    global runwind, filename
    runwind = False
    filename = r"C:\newprojects\NCA_project\r_nca\default.png"
iframe = tk.LabelFrame(root)
iframe.grid(row=1, column=0, padx=185, pady=175)
insertman = tk.Label(iframe, text="insert image")
insertman.pack(padx=10, pady=10)
insertB = tk.Button(iframe, text="insert", command = lambda: insert_im(), padx=5, pady=5).pack(padx=10, pady=10)#.grid(row=1, column=0)
defB = tk.Button(iframe, text="default", command = lambda: default_dir(), padx=5, pady=5).pack(padx=10, pady=5)
while runwind:
    root.update()

#got file dir here
print(filename)
iframe.grid_forget()

#UI- stats
heading = tk.Label(root, text="R_NCA control panel v1").grid(row=0, column=0, pady=5, sticky="W")
def setstats(avg, count, status):
    countfield.delete(0, tk.END)
    timefield.delete(0, tk.END)
    recordfield.delete(0, tk.END)
    timefield.insert(0, avg)
    countfield.insert(0, count)
    recordfield.insert(0, status)
    root.update()
    
def resetstats():
    global avg, count
    avg, count = 0, 0
stats = restarts = tk.LabelFrame(root, text="stats")
stats.grid(row=1, column=0, padx=10, pady=5, sticky="W")
_ = tk.Label(stats, text="avg render time:").grid(row=0, column=0, padx=5, pady=5)
timefield = tk.Entry(stats, width=10)
timefield.grid(row=0, column=1, padx=5, pady=5)
_ = tk.Label(stats, text="render count:").grid(row=1, column=0, padx=5, pady=5)
countfield = tk.Entry(stats, width=10)
countfield.grid(row=1, column=1, padx=5, pady=5)
recordfield = tk.Entry(stats, width=15)
recordfield.grid(row=2, column=0, columnspan=1, padx=10, pady=10, sticky="W")
recordfield.insert(0, "not recording")
resetB = tk.Button(stats, text="reset", command=lambda: resetstats()).grid(row=2, column=1)

#UI- render
def render_once(record):
    global frame, video, avg
    time1 = perf_counter()
    frame = nca.update()
    if record:
        video.write(frame)
    time2 = perf_counter()
    #collect state data
    avg = beta * prev + (1 - beta) * (time2 - time1)

rendermode = tk.IntVar()
rends = tk.LabelFrame(root, text="rendering")
rends.grid(row=2, column=0, padx=10, pady=5, sticky="W")
singlerendB = tk.Button(rends, text="render \n once", padx=5, pady=8, command= lambda: render_once(record)).grid(row=0, column=0, padx=8, pady=8, sticky="W", rowspan=3)
_ = tk.Label(rends, text="continous rendering:").grid(row=0, column=1, padx=8, pady=1, sticky="W", columnspan=2)
rendtoggle1 = tk.Radiobutton(rends, text="off", variable=rendermode, value=0).grid(row=1, column=1, padx=8, pady=1, sticky="W")
rendtoggle2 = tk.Radiobutton(rends, text="on", variable=rendermode, value=1).grid(row=1, column=2, padx=8, pady=1, sticky="W")
rendermode.set(0)


#UI - compute
def create_filter():
    global avg, count
    setstats(avg, count, "computing")
    nca.compute_filters()

apply = tk.LabelFrame(root, text="regression")
apply.grid(row=2, column=1)
regressB = tk.Button(apply, text="apply \n regression", padx=5, pady=8, command= lambda: create_filter()).grid(row=0, column=0, padx=8, pady=8)

#UI- record
def setrecord(x):
    global record
    record = x
def setscale():
    global s
    s = scaler.get() / 10
recording = tk.StringVar()
recording.set("2")
records = tk.LabelFrame(root, text="recording/viewing")
records.grid(row=1, column=1, padx=10, pady=5, sticky="W")
startrecB = tk.Radiobutton(records, text="is recording", padx=5, pady=0, command=lambda: setrecord(True), variable=recording, value="1").grid(row=0, column=0, padx=1, pady=5, sticky="W")
endrecB = tk.Radiobutton(records, text="is not recording", padx=5, pady=0, command=lambda: setrecord(False), variable=recording, value="2").grid(row=1, column=0, padx=1, pady=5, sticky="W")
# _ = tk.Label(records, text="window:").grid(row=3, column=0)
scaler = tk.Scale(records, from_=1, to=30, orient=tk.HORIZONTAL)
scaler.grid(row=4, column=0)
scaler.set(10)

#nca inst
np_image = np.asarray(Image.open(filename))
nca = Automata(np_image)

#record video
fps = 20
video = cv.VideoWriter('render_rnca.avi',cv.VideoWriter_fourcc(*'DIVX'), fps, (nca.image.shape[0], nca.image.shape[1]))

# s is scaling for image
s = 10
#mainloop starts here
lastrun = perf_counter()
frame = nca.image

avg = 0
prev = 1
beta = 1 - (1 / 6) # change p in 1 - (1 / p) for precision  
count = 1
while True:
    try:
        #update image
        if rendermode.get():
            time1 = perf_counter()
            frame = nca.update()
            if record:
                video.write(frame)
            time2 = perf_counter()
            #collect state data
            avg = beta * prev + (1 - beta) * (time2 - time1)

        #display image
        s = scaler.get() / 10
        res = cv.resize(frame, (int(frame.shape[1] * s), int(frame.shape[0] * s)), interpolation=cv.INTER_AREA)
        cv.imshow("Neural cellular automata", res)

        #print state
        setstats(round(avg, 3), count, "recording" if record else "not recording")
        count += 1

        #exit key
        if cv.waitKey(10) & 0xFF == ord('q'):
            break
        root.update()

    except:
        print("excepted")
        break
cv.destroyAllWindows()
video.release()
