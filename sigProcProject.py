# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 12:47:05 2017

@author: BobotVFontanilla
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 11:21:21 2017

@author: PepperBurst
"""

import tkinter as tk
import ctypes as ct
import scipy.io.wavfile
from scipy import signal
from tkinter import Scale
from tkinter import Label
from tkinter import Text
from tkinter import Radiobutton
from tkinter import IntVar
import numpy as np

counter = 0
flow = 0
fhigh = 0
 
def Mbox(title, text):
    return ct.windll.user32.MessageBoxW(0, text, title, 1)   
  
def get_values():
    flow = sld_bass.get()
    fhigh = sld_treble.get()
    return flow, fhigh
 
def print_values():
    flow, fhigh = get_values()
    #print(flow)
    #print(fhigh)
    #print(add_wav())
    txt_filename.delete('1.0', 'end')
    return
    
def check_txt():
    #if len(txt_filename.get("end")) == 0:
    if txt_filename.get("1.0", 'end')=="\n":
        Mbox('Warning!', 'Indicate filename!')
        clear_options()
        #set_text('')
    elif(var.get()!=1 and var.get()!=2 and var.get()!=3):
        Mbox('Warning!', 'Choose option!')
        clear_options()
    else:
        #print_values()
        flow, fhigh = get_values()
        filename = txt_filename.get("1.0","end-1c")
        Equalizer(flow, fhigh, add_wav(filename), var.get())
    return
	
def get_wav():
    rate, native_data = scipy.io.wavfile.read('D:\project.wav')
    #print(native_data.dtype)
    data1 = native_data/(32768.)
    data = np.float32(data1)
    #print(data.dtype)
    #rate = 44100
    return rate, data

def add_wav(title):
    title += '.wav'
    return title
        
def clear_options():
    txt_filename.delete('1.0', 'end')
    rbn_bass.select()
    rbn_treble.deselect()
    rbn_both.deselect()
    label.config(text='No Options Selected!')
    return
    
def Equalizer(lowin, highin, filename, option):
    #print(option)
    #print(lowin)
    #print(highin)
    clear_options()
    flow = 0
    fhigh = 0
    if(option==1):
        flow = lowin
        fhigh = 0
    elif(option==2):
        flow = 0
        fhigh = highin
    else:
        flow = lowin
        fhigh = highin
    #print(flow)
    #print(fhigh)
    rate, data = get_wav()
    nyquist_freq = rate/2
    #print(rate)
    if(flow>0):
        b, a = signal.butter(1, flow/nyquist_freq, 'low')
        filteredflow = signal.lfilter(b, a, data)
    else:
        filteredflow = 0
            
    if(fhigh>0):
        b, a = signal.butter(1, fhigh/nyquist_freq, 'high')
        filteredfhigh = signal.lfilter(b, a, data)
    else:
        filteredfhigh = 0
    
    
    finalsound = filteredflow + filteredfhigh
    scipy.io.wavfile.write(filename, rate, finalsound)
    return

root = tk.Tk()
root.title("Equalizer")

def sel():
    if(var.get()==1):
        selection = "Boosting Bass"
        label.config(text = selection)
    elif(var.get()==2):
        selection = "Boosting Treble"
        label.config(text = selection)
    else:
        selection = "Boosting Bass & Treble"
        label.config(text = selection)
    return
	
var = IntVar()
lbl_options = Label (root, text='Equalization options:')
lbl_options.pack(anchor=tk.NW)
rbn_bass = Radiobutton(root, text="Bass", variable=var, value=1, command=sel)
rbn_bass.pack(anchor=tk.NW)
rbn_treble = Radiobutton(root, text="Treble", variable=var, value=2, command=sel)
rbn_treble.pack(anchor=tk.NW)
rbn_both = Radiobutton(root, text="Base & Treble", variable=var, value=3, command=sel)
rbn_both.pack(anchor=tk.NW)
label = Label(root, text='')
label.pack()
sld_bass = Scale (root, from_=31, to=250, length=300, orient='horizontal')
sld_bass.pack()
lbl_bassScale = Label (root, text='Bass Slider')
lbl_bassScale.pack()
sld_treble = Scale (root, from_=2000, to=16000, length=300, orient='horizontal')
sld_treble.pack()
lbl_trebleScale = Label (root, text='Treble Slider')
lbl_trebleScale.pack()

lbl_filename = Label (root, text='Enter Filename',)
lbl_filename.pack()

txt_filename = Text (root, height=1, width=30)
txt_filename.pack()

btn_test= tk.Button (root, text='Equalize', width=25, command=check_txt, bd=5)

btn_test.pack()
btn_exit = tk.Button(root, text='Exit', width=25, command=root.destroy, bd=5)
btn_exit.pack()
root.mainloop()
