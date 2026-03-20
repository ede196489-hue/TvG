import tkinter as tk
import subprocess
import sys
import os

root = tk.Tk()
root.title("Starting")
root.configure(bg="darkgreen")

# Повний екран одразу
root.attributes('-fullscreen', True)
root.attributes('-topmost', True)

# Отримуємо розміри екрану
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

label = tk.Label(root, text="Starting Menu . . .", font=("Sans", 36), bg="darkgreen", fg="green")
label.place(x=screen_w // 2, y=screen_h // 2, anchor=tk.CENTER)

def open_lobby():
    root.destroy()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    lobby_path = os.path.join(script_dir, "Lobby.py")
    subprocess.Popen([sys.executable, lobby_path])

root.after(3700, open_lobby)
root.mainloop()
