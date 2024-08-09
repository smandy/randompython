#!/usr/bin/env python3

#from tkinter.messagebox import askyesno, showerror, showwarning, showinfo
from tkinter.messagebox import askyesno
#from tkinter import Button, X, mainloop
from tkinter import Tk
import sys

root = Tk()
root.withdraw()
root.attributes('-type', 'dialog')

# def answer():
#     showerror("Answer", "Sorry, no answer available")
# def callback():
#     if askyesno('Verify', 'Really quit?'):
#         showwarning('Yes', 'Not yet implemented')
#     else:
#         showinfo('No', 'Quit has been cancelled')

#Button(text='Quit', command=callback).pack(fill=X)
#Button(text='Answer', command=answer).pack(fill=X)
#showinfo("No", "Omanapadmion")

x = askyesno("Doit", "Quot")
if x:
    print("Yes selected")
    root.destroy()
    retCode = 0
else:
    print("No selected")
    root.destroy()
    retCode = 1

root.mainloop()
sys.exit(retCode)
