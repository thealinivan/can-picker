import sqlite3
import tkinter as tk
from tkinter import *

data = tk.Tk()
data.geometry("400x250")
con = sqlite3.connect('TinTrackingDB.db')
cur = con.cursor()
cur.execute("select * from TinHistory where Status ='Invalid Consignment' ")
#Selecting all Tin History 
resultdata = cur.fetchall()
rows = cur.fetchall()

for row in rows:
    print (row)
#print(resultdata)
i=0 
for tin in resultdata:
    for j in range (len(tin)):
        e = Entry(data, width=10, fg='blue')
        e.grid(row=i, column=j)
        e.insert(END,tin[j])
    i=i+1
data.mainloop()