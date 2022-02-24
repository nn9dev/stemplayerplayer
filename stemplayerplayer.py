import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #shhh pygame
import keyboard
import pygame as pg
import time
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

folder_path = filedialog.askdirectory(initialdir=os.path.normpath("%UserProfile%\Documents"), title="Select Track Folder")
print(folder_path)

pg.mixer.init()
#pg.init()

a1Note = pg.mixer.Sound(folder_path + "\\1.mp3")
a2Note = pg.mixer.Sound(folder_path + "\\2.mp3")
a3Note = pg.mixer.Sound(folder_path + "\\3.mp3")
a4Note = pg.mixer.Sound(folder_path + "\\4.mp3")

#pg.mixer.set_num_channels(50)

a1Note.play()
a2Note.play()
a3Note.play()
a4Note.play()

print (pg.mixer.get_busy())

while pg.mixer.get_busy() == True:
    #print(a1Note.get_volume())
    #print(a2Note.get_volume())
    #print(a3Note.get_volume())
    #print(a4Note.get_volume())
    
    if keyboard.is_pressed('1'):
        print ("1")
        if a1Note.get_volume() == 1.0:
            a1Note.set_volume(0.0)
        elif a1Note.get_volume() == 0.0:
            a1Note.set_volume(1.0)
        print(a1Note.get_volume())
        while keyboard.is_pressed('1'):
            keyboard.block_key('1')
        keyboard.unhook_all()
            
    if keyboard.is_pressed('2'):
        print ("2")
        if a2Note.get_volume() == 1.0:
            a2Note.set_volume(0.0)
        elif a2Note.get_volume() == 0.0:
            a2Note.set_volume(1.0)
        print(a2Note.get_volume())
        while keyboard.is_pressed('2'):
            keyboard.block_key('2')
        keyboard.unhook_all()
            
    if keyboard.is_pressed('3'):
        print("3")
        if a3Note.get_volume() == 1.0:
            a3Note.set_volume(0.0)
        elif a3Note.get_volume() == 0.0:
            a3Note.set_volume(1.0)
        print(a3Note.get_volume())
        while keyboard.is_pressed('3'):
            keyboard.block_key('3')
        keyboard.unhook_all()
            
    if keyboard.is_pressed('4'):
        print("4")
        if a4Note.get_volume() == 1.0:
            a4Note.set_volume(0.0)
        elif a4Note.get_volume() == 0.0:
            a4Note.set_volume(1.0)
        print(a4Note.get_volume())
        while keyboard.is_pressed('4'):
            keyboard.block_key('4')
        keyboard.unhook_all()
