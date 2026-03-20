import tkinter as tk
from tkinter import Button
import os

root = tk.Tk()
root.title("book of tanks")
root.configure(bg="darkblue")
root.attributes('-fullscreen', True)
root.attributes('-topmost', True)

SW = root.winfo_screenwidth()
SH = root.winfo_screenheight()

script_dir = os.path.dirname(os.path.abspath(__file__))

def img(name):
    return tk.PhotoImage(file=os.path.join(script_dir, name))

root.img_maus   = img("maus.png")
root.img_nemech = img("nemech.png")
root.img_pz     = img("pz.png")
root.img_tanks  = img("Tanks.png")
root.img_t34    = img("Tanks_34.png")

tk.Label(root, text="Book of Tanks",
         font=("Arial", 52), fg="cyan", bg="darkblue").place(x=SW//2, y=40, anchor=tk.CENTER)

tk.Label(root, image=root.img_tanks, bg="darkblue").place(x=300, y=200, anchor=tk.CENTER)
tk.Label(root, text="T-26 , Damage = 80 , hp = 400",
         font=("Arial", 15), fg="cyan", bg="darkblue").place(x=300, y=270, anchor=tk.CENTER)

tk.Label(root, image=root.img_t34, bg="darkblue").place(x=300, y=450, anchor=tk.CENTER)
tk.Label(root, text="T-34 , Damage = 150 , hp = 700",
         font=("Arial", 15), fg="cyan", bg="darkblue").place(x=300, y=520, anchor=tk.CENTER)

tk.Label(root, image=root.img_nemech, bg="darkblue").place(x=1000, y=180, anchor=tk.CENTER)
tk.Label(root, text="Panther , Damage = 180 , hp = 800",
         font=("Arial", 15), fg="cyan", bg="darkblue").place(x=1000, y=250, anchor=tk.CENTER)

tk.Label(root, image=root.img_maus, bg="darkblue").place(x=1000, y=420, anchor=tk.CENTER)
tk.Label(root, text="MAUS , Damage = 200 , hp = 1000",
         font=("Arial", 15), fg="cyan", bg="darkblue").place(x=1000, y=490, anchor=tk.CENTER)

tk.Label(root, image=root.img_pz, bg="darkblue").place(x=1000, y=660, anchor=tk.CENTER)
tk.Label(root, text="PZ-2 , Damage = 100 , hp = 300",
         font=("Arial", 15), fg="cyan", bg="darkblue").place(x=1000, y=730, anchor=tk.CENTER)

Button(root, text="EXIT", font=("Arial", 30), fg="black", bg="red",
       command=root.destroy).place(x=SW//2, y=SH-60, anchor=tk.CENTER)

root.mainloop()
