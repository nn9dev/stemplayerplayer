import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #shhh pygame
import keyboard
import pygame as pg
import time
import json
import glob
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

state=1
stem_list = []
note_objects=[]

root = tk.Tk()
root.title('Stem Player Player')
root.protocol("WM_DELETE_WINDOW", lambda: close_window())

def slider(value):
    i = instrumentals_Scale.get()
    v = vocals_Scale.get()
    b = bass_Scale.get()
    d = drums_Scale.get()

    note_objects[0].set_volume(i)
    note_objects[1].set_volume(v)
    note_objects[2].set_volume(b)
    note_objects[3].set_volume(d)

def open_new():
    pg.mixer.stop()
    global note_objects
    global stem_list
    folder_path = filedialog.askdirectory(initialdir=os.path.normpath("%UserProfile%\Documents"), title="Select Tracks Folder")
    print(folder_path)
    if SPP_CONFIG["MP3_WAV"] == "WAV":
        print("Using WAV...")
        stem_list = glob.glob(folder_path + "/*.wav")
    else:
        stem_list = glob.glob(folder_path + "/*.mp3")
        print("Using MP3...")
    a1Note = pg.mixer.Sound(stem_list[0])
    a2Note = pg.mixer.Sound(stem_list[1])
    a3Note = pg.mixer.Sound(stem_list[2])
    a4Note = pg.mixer.Sound(stem_list[3])
    a1Note.play()
    a2Note.play()
    a3Note.play()
    a4Note.play()
    note_objects = [a1Note, a2Note, a3Note, a4Note]
    


def pause_play():
    global state
    if state==1:
        state=0
        print("Pausing!")
        pg.mixer.pause()
    elif state==0:
        state=1
        print("Unpausing!")
        pg.mixer.unpause()

def close_window():
    pg.mixer.quit()
    pg.quit()
    root.destroy()
    exit()


with open("spp_config.json", encoding="utf-8") as config_file:
    SPP_CONFIG = json.load(config_file)
    KEY_INSTRUMENTALS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_INSTRUMENTALS"])[0]
    KEY_VOCALS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_VOCALS"])[0]
    KEY_BASS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_BASS"])[0]
    KEY_DRUMS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_DRUMS"])[0]


pg.mixer.init()
pg.init()
open_new()


frame = Frame(root, bd=1, relief=None)
frame.pack(pady=5)

instrumentals_label = Label(frame, text="Instrumentals", font=("Times New Roman", 12, "bold"))
instrumentals_label.grid(row=0, column=0)

instrumentals_Scale = Scale(frame, resolution=0.01, from_=0.0, to=1.0, length=210, orient=HORIZONTAL, command=slider)
instrumentals_Scale.grid(row=0, column=1)
instrumentals_Scale.set(1.0)

vocals_label = Label(frame, text="Vocals", font=("Times New Roman", 12, "bold"))
vocals_label.grid(row=1, column=0)

vocals_Scale = Scale(frame, resolution=0.01, from_=0.0, to=1.0, length=210, orient=HORIZONTAL, command=slider)
vocals_Scale.grid(row=1, column=1)
vocals_Scale.set(1.0)

bass_label = Label(frame, text="Bass", font=("Times New Roman", 12, "bold"))
bass_label.grid(row=2, column=0)

bass_Scale = Scale(frame, resolution=0.01, from_=0.0, to=1.0, length=210, orient=HORIZONTAL, command=slider)
bass_Scale.grid(row=2, column=1)
bass_Scale.set(1.0)

drums_label = Label(frame, text="Drums", font=("Times New Roman", 12, "bold"))
drums_label.grid(row=3, column=0)

drums_Scale = Scale(frame, resolution=0.01, from_=0.0, to=1.0, length=210, orient=HORIZONTAL, command=slider)
drums_Scale.grid(row=3, column=1)
drums_Scale.set(1.0)

frame2 = Frame(root, bd=1, relief=None)
frame2.pack(pady=5)

pauseplay = Button(frame2, text="Pause/Play", font=("Times New Roman", 12, "bold"), command=lambda: pause_play())
pauseplay.grid(row=3, column=1, pady=7)

newtrack = Button(frame2, text="New Track", font=("Times New Roman", 12, "bold"), command=lambda: open_new())
newtrack.grid(row=3, column=2, pady=7)


root.mainloop()
