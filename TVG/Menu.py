import tkinter as tk
import subprocess
import sys
import os
from tkinter import Button

root = tk.Tk()
root.title("Starting")
root.configure(bg="darkgreen")

# Повний екран одразу
root.attributes('-fullscreen', True)
root.attributes('-topmost', True)

# Отримуємо розміри екрану
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

label = tk.Label(root, text="Menu of the mods", font=("Sans", 36), bg="orange", fg="yellow")
label.place(x=screen_w // 2, y=screen_h // 5, anchor=tk.CENTER)
def launch(script):
    path = os.path.join(script)
    subprocess.Popen([sys.executable, path])

Button(root, text="Hardcore",    font=("Arial", 34), fg="red", bg="white",
    command=lambda: launch("osnowa_hardcore")).place(x=180, y=455, anchor=tk.CENTER)

Button(root, text="Endless",    font=("Arial", 34), fg="orange", bg="black",
    command=lambda: launch("osnowa_endless.py")).place(x=500, y=455, anchor=tk.CENTER)

Button(root, text="Hard",    font=("Arial", 34), fg="white", bg="red",
    command=lambda: launch("osnowa_hard.py")).place(x=1000, y=455, anchor=tk.CENTER)

Button(root, text="Normal",    font=("Arial", 34), fg="Yellow", bg="green",
    command=lambda: launch("osnowa.py")).place(x=1320, y=455, anchor=tk.CENTER)




root.mainloop()
