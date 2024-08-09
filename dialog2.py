#!/usr/bin/env python3

from tkinter.messagebox import askyesno, showinfo, showwarning
from tkinter import Tk
import sys

root = Tk()
root.withdraw()
root.attributes('-type', 'dialog')

txt = sys.stdin.read()

if 0:
    x = askyesno("Yes / No", txt)
elif 0:
    x = showinfo("Info", txt)
else:
    x = showwarning("Ug", "Fings getting bad")
if x:
    root.destroy()
    retCode = 0
else:
    root.destroy()
    retCode = 1
    
root.mainloop()
sys.exit(retCode)
