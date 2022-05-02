import sys
import os
from tkinter import *

window=Tk()

window.title("Running Python Script")
window.geometry('550x200')

def run():
    os.system('python3 main.py')
def Stoprun():
    sys.exit()
def Validtins():
    os.system('python3 validTins.py')
def InvalidTins():
    os.system('python3 invalidTins.py')
def TinHistory():
    print("Coming soon...")
    #os.system('python3 tinHistory.py')

btn = Button(window, text="Start System", bg="pink", fg="black",command=run)
btn.grid(column=1, row=0)
btn = Button(window, text="Stop System", bg="pink", fg="black",command=Stoprun)
btn.grid(column=3, row=0)
btn = Button(window, text="Valid Tins", bg="pink", fg="black",command=Validtins)
btn.grid(column=5, row=0)
btn = Button(window, text="InValid Tins", bg="pink", fg="black",command=InvalidTins)
btn.grid(column=7, row=0)
btn = Button(window, text="Tin History", bg="pink", fg="black",command=TinHistory)
btn.grid(column=9, row=0)
window.mainloop()