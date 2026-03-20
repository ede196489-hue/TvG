import subprocess
import tkinter as tk
from tkinter import Button
import sys
import os

root = tk.Tk()
root.title("start")
root.configure(bg="darkred")
root.attributes('-fullscreen', True)
root.attributes('-topmost', True)

SW = root.winfo_screenwidth()
SH = root.winfo_screenheight()

script_dir = os.path.dirname(os.path.abspath(__file__))

def launch(script):
    path = os.path.join(script_dir, script)
    subprocess.Popen([sys.executable, path])

tk.Label(root, text="Tanks vs Guys",
         font=("Arial", 52), fg="purple", bg="darkred").place(x=SW//2, y=80, anchor=tk.CENTER)

root.logo_img = tk.PhotoImage(file=os.path.join(script_dir, "logo.png"))
tk.Label(root, image=root.logo_img, bg="darkred").place(x=SW//2, y=SH//2, anchor=tk.CENTER)

Button(root, text="PLAY",    font=("Arial", 30), fg="black", bg="green",
       command=lambda: launch("Menu.py")).place(x=180, y=455, anchor=tk.CENTER)

Button(root, text="BOOK",    font=("Arial", 30), fg="black", bg="yellow",
       command=lambda: launch("book.py")).place(x=180, y=550, anchor=tk.CENTER)

Button(root, text="SETTING", font=("Arial", 15), fg="black", bg="grey",
       command=lambda: launch("Setting.py")).place(x=180, y=625, anchor=tk.CENTER)

Button(root, text="QUIT",    font=("Arial", 15), fg="black", bg="red",
       command=root.destroy).place(x=180, y=680, anchor=tk.CENTER)

label = tk.Label(root, text="0.0.1 made by Denus Skhidnytskyi", font=("Arial", 10), bg="darkred", fg="red")
label.place(x=SW-10, y=SH-10, anchor=tk.SE)
label.pack()

root.mainloop()
