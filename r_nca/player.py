from faulthandler import disable
import numpy as np
import cv2 as cv
from tkinter import filedialog
import tkinter as tk
from time import perf_counter
import time

#UI
root = tk.Tk()
root.geometry("500x450")
root.title("player")

#get file directory
runwind = True
def insert_im():
    global runwind, filename
    runwind = False
    filename = filedialog.askopenfilename()
def default_dir():
    global runwind, filename
    runwind = False
    filename = r"video.npy"
frame = tk.LabelFrame(root)
frame.grid(row=1, column=0, padx=185, pady=175)
insertman = tk.Label(frame, text="insert npy im")
insertman.pack(padx=5, pady=5)
insertB = tk.Button(frame, text="insert", command = lambda: insert_im(), padx=5, pady=5).pack(padx=10, pady=10)
defB = tk.Button(frame, text="default", command = lambda: default_dir(), padx=5, pady=5).pack(padx=10, pady=5)
while runwind:
    root.update()

#got file dir here
print(filename)
video = np.load("video.npy")

frame.grid_forget()
frame = tk.LabelFrame(root)
frame.grid(row=1, column=0, padx=135, pady=175)

def disable(_):
    global move
    move = False
def play():
    global play
    play = True
def pause():
    global play
    play = False
def replay():
    global framecount
    framecount = 1

media = tk.LabelFrame(frame)
media.grid(row=1, column=0)
playb = tk.Button(media, text="▶", command=play , padx=5, pady=5).grid(row=1, column=0, sticky="E")
pauseb = tk.Button(media, text="||", command=pause, padx=7, pady=5).grid(row=1, column=1, sticky="E")
replayb = tk.Button(media, text="🔄", command=replay, padx=7, pady=5).grid(row=1, column=2, sticky="E")
videobar = tk.Scale(frame, from_=1, to=video.shape[3], orient=tk.HORIZONTAL, length=300, command= disable)
videobar.grid(row=0, column=0, columnspan=5)
videobar.set(1)

def setscale():
    global s
    s = scaler.get() / 10
scaler = tk.Scale(frame, from_=1, to=30, orient=tk.HORIZONTAL, length=60)
scaler.grid(row=2, column=4)
scaler.set(10)

def fpsup():
    global fps
    fps += 3
def fpsdown():
    global fps
    if fps > 4:
        fps -= 3
fpsset = tk.LabelFrame(frame)
fpsset.grid(row=1, column=2)
fpupB = tk.Button(fpsset, text="↑", command=fpsup).grid(row=0, column=0)
fpdownB = tk.Button(fpsset, text="↓", command=fpsdown).grid(row=0, column=1)

fpsdisp = tk.Label(frame, text="fps:")
fpsdisp.grid(row=1, column=1)


play = False
move = True
fps = 15
framecount = 0
prev = perf_counter()
diff = 0
frametime = 1/ fps
s = 10
while True:
    #video player mechanism and fps regulator:
    if diff >= frametime:
        if move:
            if play:
                framecount += 1
        else:
            x = videobar.get()
            framecount = x
        move = True
        videobar.set(framecount)
        prev = perf_counter()
    diff = perf_counter() - prev
    frametime = 1/ fps
    #video fetching
    vidframe = video[:, :, :, framecount]
    #video display:
    s = scaler.get() / 10
    res = cv.resize(vidframe, (int(vidframe.shape[1] * s), int(vidframe.shape[0] * s)), interpolation=cv.INTER_AREA)
    cv.imshow("nca player", res)
    #fps setting
    fpsdisp.config(text=f"fps: {fps}")
    
    root.update()