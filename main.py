from nca import Automata
import cv2 as cv
import tkinter as tk
from time import perf_counter
import numpy as np

helptext = """
    Usage Instructions:\n
    Use the 'controls tab' to control the frame, filters, activation, and recording like so: \n
    - restarts: \n\t 
        use restarts to refresh the frame with certain values. \n\t 
        'randints' assigns random values of 1 or 0 to each pixel \n\t 
        'randfloats' assigns random floats \n\t 
        'center' assigns a value of 1 at the center pixel and 0 for all others \n
    - load: \n\t
        Pick a preset simulation to load. You might have to pick a restart to start it.\n
    -recording: \n\t
        click start to start recording generated frames and stop to stop. the video is saved as \n\t render.avi\n
    -custom filters: \n\t
        click on random filters to randomly set the filter. \n\t
        you can also set the activation function. \n
    Caution: the video file may get corrupted if it's too short or the program is stopped abruptly.
    """
nca = Automata()
record = False

#UI
root = tk.Tk()
root.geometry("500x550")
root.title("controls")

heading = tk.Label(text="NCA control panel v1").grid(row=0, column=0, pady=5, sticky="W")

#refresh buttons
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
    recordfield.insert(0, "Recording" if isrec else "Not Recording")

#status display
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

#star/stop recording:
def setrecord(x):
    global record
    record = x

#recording control
recording = tk.StringVar()
recording.set("2")
records = tk.LabelFrame(root, text="recording")
records.grid(row=1, column=1, padx=10, pady=5, sticky="W")
startrecB = tk.Radiobutton(records, text="Start", padx=5, pady=0, command=lambda: setrecord(True), variable=recording, value="1").grid(row=0, column=0, padx=3, pady=5, sticky="W")
endrecB = tk.Radiobutton(records, text="Stop", padx=5, pady=0, command=lambda: setrecord(False), variable=recording, value="2").grid(row=1, column=0, padx=3, pady=5, sticky="W")

#Preset simulations
mode = tk.StringVar()
mode.set("0")
load = tk.LabelFrame(root, text="load")
load.grid(row=2, column=0, padx=15, pady=5, sticky="W", rowspan=2)

conways = tk.Radiobutton(load, text="Conway's game of life", variable=mode, value="1", command=lambda: nca.presetmode("conway")).grid(row=0, column=0, sticky="W")
stars = tk.Radiobutton(load, text="stars", variable=mode, value="2", command=lambda: nca.presetmode("stars")).grid(row=1, column=0, sticky="W")
pathB = tk.Radiobutton(load, text="paths", variable=mode, value="3", command=lambda: nca.presetmode("paths")).grid(row=2, column=0, sticky="W")
pathB = tk.Radiobutton(load, text="slime", variable=mode, value="4", command=lambda: nca.presetmode("slime")).grid(row=3, column=0, sticky="W")
wolfB = tk.Radiobutton(load, text="Wolfram's rule 30", variable=mode, value="5", command=lambda: nca.presetmode("wolf")).grid(row=4, column=0, sticky="W")
waves = tk.Radiobutton(load, text="waves", variable=mode, value="6", command=lambda: nca.presetmode("waves")).grid(row=5, column=0, sticky="W")
worms = tk.Radiobutton(load, text="worms", variable=mode, value="7", command=lambda: nca.presetmode("worms")).grid(row=6, column=0, sticky="W")

#custom functions
def setident(): nca.activation = "ident"
def setabs(): nca.activation = "abs"
def setgauss(): nca.activation = "gauss"
def setinvgauss(): nca.activation = "invgauss"

activ = tk.StringVar()
activ.set("0")
setf = tk.LabelFrame(root, text="custom")
setf.grid(row=4, column=0, padx=15, pady=5, sticky="E")
randomB = tk.Button(setf, text="random filter", command=nca.set_rand_filter, padx=5, pady=8).grid(row=0, column=0, sticky="W", padx=5, pady=8, rowspan=3)
active = tk.Label(setf, text="Activation function:").grid(row=0, column=1, pady=5, sticky="W")
identB = tk.Radiobutton(setf, text="identity", variable=activ, value="1", command=setident).grid(row=1, column=1)
absB = tk.Radiobutton(setf, text="absolute", variable=activ, value="2", command=setabs).grid(row=2, column=1)
gaussB = tk.Radiobutton(setf, text="gaussian", variable=activ, value="3", command=setgauss).grid(row=3, column=1)
invgaussB = tk.Radiobutton(setf, text="inverse gaussian", variable=activ, value="4", command=setinvgauss).grid(row=4, column=1)

# Display filter and activation function
filter_frame = tk.LabelFrame(root, text="Filter & Activation")
filter_frame.grid(row=4, column=1, padx=15, pady=5, sticky="W")
filter_text = tk.Text(filter_frame, height=4, width=20)
filter_text.grid(row=0, column=0, padx=5, pady=5)
activation_label = tk.Label(filter_frame, text=f"Activation: {nca.activation}")
activation_label.grid(row=1, column=0, padx=5, pady=5)

def update_filter_display():
    filter_text.delete("1.0", tk.END)
    filter_matrix = nca.filter if isinstance(nca.filter, np.ndarray) else np.zeros((3, 3))
    filter_text.insert(tk.END, '\n'.join([' '.join(map(lambda x: f"{x:.2f}", row)) for row in filter_matrix]))
    activation_label.config(text=f"Activation: {nca.activation}")

# Help window
def open_help():
    help_window = tk.Toplevel(root)
    help_window.title("Help")
    help_window.geometry("500x500")
    help_label = tk.Label(help_window, text=helptext, justify="left", padx=10, pady=10)
    help_label.pack()

# Exit Button
def exit_app():
    global root
    root.quit()
    root.destroy()
    cv.destroyAllWindows()
    video.release()
    exit()


exit_frame = tk.Frame(root)
exit_frame.grid(row=3, column=1)

tk.Button(exit_frame, text="Help", command=open_help, width=10, height=5).pack(side=tk.RIGHT, padx=5)
tk.Button(exit_frame, text="Exit", command=exit_app, width=10, height=5).pack(side=tk.LEFT, padx=5)

#Video writer
fps = 20
video = cv.VideoWriter('render.avi',cv.VideoWriter_fourcc(*'DIVX'), fps, nca.canv_dimensions)

# Scaling factor for image
s=1.5
#Main loop starts
print("Initializing")
lastrun = perf_counter()
frame = nca.update()
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
        update_filter_display()

        #print state
        setstats(round(avg, 3), count, record)
        count += 1

    except ArithmeticError:
        print("excepted")
        break
    except tk.TclError:
        print("terminated")
        exit()
cv.destroyAllWindows()
video.release()