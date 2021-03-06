import os
import re
from os.path import expanduser
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #shhh pygame
import subprocess
import keyboard
import pygame as pg
import json
import glob
import tkinter as tk
import tkinter.messagebox
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
from pydub import AudioSegment

homedir = os.path.expanduser("~")

state=1
stem_list = []
note_objects=[]
mutevols=[0,0,0,0]
merging = False

root = tk.Tk()
startstop_bridge = tk.IntVar()
startstop_bridge.set(0)
root.title('Stem Player Player')
root.protocol("WM_DELETE_WINDOW", lambda: close_window())

def create_config():
    import platform
    if not os.path.exists(homedir + "/stemplayerplayer_config.json"): ##create config if doesn't exist
        default_config = {
        "KEY_INSTRUMENTALS": "1",
        "KEY_VOCALS": "2",
        "KEY_BASS": "3",
        "KEY_DRUMS": "4",
        "KEYBINDS_ENABLED": 0,
        }
        if 'SPP_HOME' not in default_config:
            if platform.system() == 'Windows':
                default_config["SPP_HOME"] = homedir + "\\stemplayer"
            else:
                default_config["SPP_HOME"] = homedir + "/stemplayer"
        tempjson = json.dumps(default_config, indent=2)
        with open(homedir + "/stemplayerplayer_config.json", "w") as jsonfile:
            jsonfile.write(tempjson)
        tempjson.close()

create_config()
#load config
with open(homedir + "/stemplayerplayer_config.json", encoding="utf-8") as config_file:
    SPP_CONFIG = json.load(config_file)
    KEY_INSTRUMENTALS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_INSTRUMENTALS"])[0]
    KEY_VOCALS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_VOCALS"])[0]
    KEY_BASS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_BASS"])[0]
    KEY_DRUMS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_DRUMS"])[0]
    KEYBINDS_ENABLED = SPP_CONFIG["KEYBINDS_ENABLED"]
    SPP_HOME = SPP_CONFIG["SPP_HOME"]
    if not os.path.exists(SPP_HOME):
        os.makedirs(SPP_HOME)

from stembridge import *

def open_config():
    import platform
    global KEY_INSTRUMENTALS, KEY_VOCALS, KEY_BASS, KEY_DRUMS
    if platform.system() == 'Windows':
        subprocess.Popen("notepad.exe " + homedir + "/stemplayerplayer_config.json", creationflags=0x08000000) #flag for CREATE_NO_WINDOW
    elif platform.system() == 'Linux':
        subprocess.Popen("xdg-open " + homedir + "/stemplayerplayer_config.json")
    elif platform.system() == 'Darwin':
        subprocess.Popen("open " + homedir + "/stemplayerplayer_config.json")

    '''
    with open(homedir + "/stemplayerplayer_config.json", encoding="utf-8") as config_file: #reimport keybinds
        SPP_CONFIG = json.load(config_file)
        KEY_INSTRUMENTALS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_INSTRUMENTALS"])[0]
        KEY_VOCALS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_VOCALS"])[0]
        KEY_BASS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_BASS"])[0]
        KEY_DRUMS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_DRUMS"])[0]
        SPP_HOME = SPP_CONFIG["SPP_HOME"]
    '''
        

def slider(value):
    i = instrumentals_Scale.get()
    v = vocals_Scale.get()
    b = bass_Scale.get()
    d = drums_Scale.get()

    if note_objects:    #suppress stupid error
        note_objects[0].set_volume(i)
        note_objects[1].set_volume(v)
        note_objects[2].set_volume(b)
        note_objects[3].set_volume(d)

def open_new():
    pg.mixer.stop()
    global note_objects
    global stem_list
    stem_list=[]
    folder_path = filedialog.askdirectory(title="Select Tracks Folder")
    print(folder_path)
    if not folder_path:
        return
    elif glob.glob(folder_path + "/*.flac"):
        print("Using FLAC...")
        stem_list = glob.glob(folder_path + '/*[0-9].flac')
    elif glob.glob(folder_path + "/*.wav"):
        print("Using WAV...")
        stem_list = glob.glob(folder_path + '/*[0-9].wav')
    elif glob.glob(folder_path + "/*.mp3"):
        print("Using MP3...")
        stem_list = glob.glob(folder_path + '/*[0-9].mp3')
        
    a1Note = pg.mixer.Sound(stem_list[0])
    a2Note = pg.mixer.Sound(stem_list[1])
    a3Note = pg.mixer.Sound(stem_list[2])
    a4Note = pg.mixer.Sound(stem_list[3])
    if merging == False:
        a1Note.play()
        a2Note.play()
        a3Note.play()
        a4Note.play()
    note_objects = [a1Note, a2Note, a3Note, a4Note]

def merge_stems():
    global stem_list
    stem_list = []
    global merging
    from shutil import which
    print(which('ffmpeg'))
    if which('ffmpeg') is not None:
        merging = True
        open_new()
        merging = False
        if stem_list:
            text = stem_list[0]
            soundformat = re.split('[1-4]\.', text)[1]
            startname = re.split('[1-4]\.', text)[0]
            print(soundformat)
            print(startname)
            print(stem_list[0])
            print(re.split('[1-4]\.', text)[0] + "." + soundformat)
            if os.path.exists(os.path.normpath(startname + "." + soundformat)):
                os.remove(os.path.normpath(startname + "." + soundformat))
            
            stem1 = AudioSegment.from_file(os.path.normpath(stem_list[0]))
            stem2 = AudioSegment.from_file(os.path.normpath(stem_list[1]))
            stem3 = AudioSegment.from_file(os.path.normpath(stem_list[2]))
            stem4 = AudioSegment.from_file(os.path.normpath(stem_list[3]))
            overlay = stem1.overlay(stem2.overlay(stem3.overlay(stem4)))
            file_handle = overlay.export(startname + "." + soundformat, format=soundformat)
            file_handle.flush()
            file_handle.close()
            
    else:
         tk.messagebox.showerror(title="ffmpeg not found", message="ffmpeg not found on your system. Please install ffmpeg and make sure it is added to your PATH.")
    
def toggle_keybinds():
    print(onoff.get())

def check_keybinds():
    ##hell keybinds
    if keyboard.is_pressed(KEY_INSTRUMENTALS) and onoff.get() == 1:
        toggle_channel(1)
                
    if keyboard.is_pressed(KEY_VOCALS)and onoff.get() == 1:
        toggle_channel(2)

    if keyboard.is_pressed(KEY_BASS) and onoff.get() == 1:
        toggle_channel(3)
            
    if keyboard.is_pressed(KEY_DRUMS) and onoff.get() == 1:
        toggle_channel(4)
    root.after(1, check_keybinds)

def toggle_channel(toToggle):
    #print("hello from togglechannel")
    if note_objects:  #suppress stupid error pt 2
        if toToggle == 1:
            print ("1")
            if note_objects[0].get_volume() != 0.0:
                mutevols[0] = note_objects[0].get_volume()
                note_objects[0].set_volume(0.0)
            elif note_objects[0].get_volume() == 0.0:
                note_objects[0].set_volume(mutevols[0])
            print(note_objects[0].get_volume())
            while keyboard.is_pressed(KEY_INSTRUMENTALS):
                keyboard.block_key(KEY_INSTRUMENTALS)
            keyboard.unhook_all()
        elif toToggle == 2:
            print ("2")
            if note_objects[1].get_volume() != 0.0:
                mutevols[1] = note_objects[1].get_volume()
                note_objects[1].set_volume(0.0)
            elif note_objects[1].get_volume() == 0.0:
                note_objects[1].set_volume(mutevols[1])
            print(note_objects[1].get_volume())
            while keyboard.is_pressed(KEY_VOCALS):
                keyboard.block_key(KEY_VOCALS)
            keyboard.unhook_all()
        elif toToggle == 3:
            print ("3")
            if note_objects[2].get_volume() != 0.0:
                mutevols[2] = note_objects[2].get_volume()
                note_objects[2].set_volume(0.0)
            elif note_objects[2].get_volume() == 0.0:
                note_objects[2].set_volume(mutevols[2])
            print(note_objects[2].get_volume())
            while keyboard.is_pressed(KEY_BASS):
                keyboard.block_key(KEY_BASS)
            keyboard.unhook_all()
        elif toToggle == 4:
            print ("4")
            if note_objects[3].get_volume() != 0.0:
                mutevols[3] = note_objects[3].get_volume()
                note_objects[3].set_volume(0.0)
            elif note_objects[3].get_volume() == 0.0:
                note_objects[3].set_volume(mutevols[3])
            print(note_objects[3].get_volume())
            while keyboard.is_pressed(KEY_DRUMS):
                keyboard.block_key(KEY_DRUMS)
            keyboard.unhook_all()
    else:
        return
        

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
    global onoff
    with open(homedir + "/stemplayerplayer_config.json") as json_file:
        jsontemp = json.load(json_file)
    jsontemp['KEYBINDS_ENABLED'] = onoff.get()
    
    with open(homedir + "/stemplayerplayer_config.json", 'w') as json_file:
        json.dump(jsontemp, json_file)
    pg.mixer.quit()
    pg.quit()
    root.destroy()
    exit()


pg.mixer.init()

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

###commands
frame2 = Frame(root, bd=1, relief=None)
frame2.pack(pady=5)

pauseplay = Button(frame2, text="Pause/Play", font=("Times New Roman", 12, "bold"), command=lambda: pause_play())
pauseplay.grid(row=3, column=1, sticky=E)

newtrack = Button(frame2, text="New Track", font=("Times New Roman", 12, "bold"), command=lambda: open_new())
newtrack.grid(row=3, column=2)

keybindsbutton = Button(frame2, text="Edit config", font=("Times New Roman", 12, "bold"), command=lambda: open_config())
keybindsbutton.grid(row=3, column=3, sticky=W)

mergebutton = Button(frame2, text="Merge Stems", font=("Times New Roman", 12, "bold"), command=lambda: merge_stems())
mergebutton.grid(row=4, column=2, pady=2)

#startbridge = Button(frame2, text="Bridge on/off", font=("Times New Roman", 12, "bold"), command=lambda: start_bridge())
#startbridge.grid(row=4, column=2, pady=2)


startbridge = tk.Checkbutton(root,
                             text='Bridge Enabled',
                             command=lambda: start_bridge(startstop_bridge.get()),
                             font=("Times New Roman", 12, "bold"),
                             variable=startstop_bridge,
                             onvalue=1,
                             offvalue=0)
startbridge.pack()



onoff = tk.IntVar()         #Keybinds toggle box
onoff.set(KEYBINDS_ENABLED)
tgkb = tk.Checkbutton(root,
                      text='Keybinds Enabled',
                      command=toggle_keybinds,
                      font=("Times New Roman", 12, "bold"),
                      variable=onoff,
                      onvalue=1,
                      offvalue=0)
tgkb.pack()

root.after(1, check_keybinds)
root.mainloop()
