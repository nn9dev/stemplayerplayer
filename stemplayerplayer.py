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

with open("spp_config.json", encoding="utf-8") as config_file:
    SPP_CONFIG = json.load(config_file)
    KEY_INSTRUMENTALS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_INSTRUMENTALS"])[0]
    KEY_VOCALS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_VOCALS"])[0]
    KEY_BASS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_BASS"])[0]
    KEY_DRUMS = keyboard.key_to_scan_codes(SPP_CONFIG["KEY_DRUMS"])[0]

root = tk.Tk()
root.withdraw()

folder_path = filedialog.askdirectory(initialdir=os.path.normpath("%UserProfile%\Documents"), title="Select Tracks Folder")
print(folder_path)
stem_list = glob.glob(folder_path + "/*.mp3")

pg.mixer.init()
pg.init()
"""
pg.display.set_caption('Stem Player Player')
window = pg.display.set_mode((300, 300))
image = pg.image.load('stemplayer.png')
image = pg.transform.scale(image, (300, 300))
window.blit(image, (0, 0))
"""


a1Note = pg.mixer.Sound(stem_list[0])
a2Note = pg.mixer.Sound(stem_list[1])
a3Note = pg.mixer.Sound(stem_list[2])
a4Note = pg.mixer.Sound(stem_list[3])

#pg.mixer.set_num_channels(50)

a1Note.play()
a2Note.play()
a3Note.play()
a4Note.play()

#print (pg.mixer.get_busy())

while pg.mixer.get_busy() == True:
    #print(a1Note.get_volume())
    #print(a2Note.get_volume())
    #print(a3Note.get_volume())
    #print(a4Note.get_volume())
    
    if keyboard.is_pressed(KEY_INSTRUMENTALS):
        print ("1")
        if a1Note.get_volume() == 1.0:
            a1Note.set_volume(0.0)
        elif a1Note.get_volume() == 0.0:
            a1Note.set_volume(1.0)
        print(a1Note.get_volume())
        while keyboard.is_pressed(KEY_INSTRUMENTALS):
            keyboard.block_key(KEY_INSTRUMENTALS)
        keyboard.unhook_all()
            
    if keyboard.is_pressed(KEY_VOCALS):
        print ("2")
        if a2Note.get_volume() == 1.0:
            a2Note.set_volume(0.0)
        elif a2Note.get_volume() == 0.0:
            a2Note.set_volume(1.0)
        print(a2Note.get_volume())
        while keyboard.is_pressed(KEY_VOCALS):
            keyboard.block_key(KEY_VOCALS)
        keyboard.unhook_all()
            
    if keyboard.is_pressed(KEY_BASS):
        print("3")
        if a3Note.get_volume() == 1.0:
            a3Note.set_volume(0.0)
        elif a3Note.get_volume() == 0.0:
            a3Note.set_volume(1.0)
        print(a3Note.get_volume())
        while keyboard.is_pressed(KEY_BASS):
            keyboard.block_key(KEY_BASS)
        keyboard.unhook_all()
            
    if keyboard.is_pressed(KEY_DRUMS):
        print("4")
        if a4Note.get_volume() == 1.0:
            a4Note.set_volume(0.0)
        elif a4Note.get_volume() == 0.0:
            a4Note.set_volume(1.0)
        print(a4Note.get_volume())
        while keyboard.is_pressed(KEY_DRUMS):
            keyboard.block_key(KEY_DRUMS)
        keyboard.unhook_all()

##hello :)
    
