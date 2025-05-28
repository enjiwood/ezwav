from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile, asksaveasfile

root = Tk()
root.geometry('200x100')

def inputfile():
    file = askopenfile(mode='r', filetypes=[('mp3 files', '*.mp3')], title="Select an mp3 file")
    return file

def outputfile():
    file = asksaveasfile(mode='w', filetypes=[('wav files', '*.wav')], title="Save wav file as")
    return file