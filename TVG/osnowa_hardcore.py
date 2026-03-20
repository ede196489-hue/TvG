import tkinter as tk
import random
import os
import sys
import subprocess

ROWS           = 7
COLS           = 11
CELL_W         = 100
CELL_H         = 70
GRID_X         = 200
GRID_Y         = 130
FPS            = 40
FUEL_START     = 20
FUEL_MAX       = 9999999
FUEL_TICK      = 80
WAVE_DELAY     = 280
WAVE_SIZE_BASE = 10
MAX_WAVES      = 15

USSR_TANKS = {
    "T34": {"name":"T-34", "cost":30, "hp":150, "damage":40,  "range":7,  "fire_cd":28, "img":"Tanks_34.png", "desc":"30", "bullet":"#ffdd00", "bsize":7},
    "BR":  {"name":"BT",   "cost":65, "hp":3500,"damage":120, "range":20, "fire_cd":10, "img":"Mega.png",     "desc":"65", "bullet":"#ffdd00", "bsize":10},
    "T28": {"name":"T-28", "cost":30, "hp":100, "damage":25,  "range":8,  "fire_cd":17, "img":"Tanks.png",   "desc":"30", "bullet":"#ff6600", "bsize":7},
    "T26": {"name":"T-26", "cost":15, "hp":80,  "damage":12,  "range":8,  "fire_cd":23, "img":"T-26.png",    "desc":"15", "bullet":"#ffaa00", "bsize":5},
}

GERMAN_TANKS = {
    "pz2":   {"name":"PZ-2",   "hp":100, "speed":1.8,  "damage":15,  "reward":8,  "img":"pz.png",     "atk_cd":35},
    "nemech":{"name":"Panther","hp":400, "speed":0.9,  "damage":45,  "reward":20, "img":"nemech.png", "atk_cd":45},
    "maus":  {"name":"MAUS",   "hp":900, "speed":0.50, "damage":120, "reward":50, "img":"maus.png",   "atk_cd":55},
}

HP_MUL  = 3.5
SPD_MUL = 2.2

root = tk.Tk()
root.title("HARDCORE")
root.configure(bg="#1a0000")
root.attributes('-fullscreen', True)
root.attributes('-topmost', True)

SW = root.winfo_screenwidth()
SH = root.winfo_screenheight()

canvas = tk.Canvas(root, width=SW, height=SH, bg="#1a0000", highlightthickness=0)
canvas.pack(fill="both", expand=True)

script_dir = os.path.dirname(os.path.abspath(__file__))

images = {}

def load_img(name, factor=2):
    path = os.path.join(script_dir, name)
    if not os.path.exists(path):
        return None
    try:
        img = tk.PhotoImage(file=path)
        if factor > 1:
            img = img.subsample(factor, factor)
        return img
    except Exception:
        return None

for tdef in USSR_TANKS.values():
    images[tdef["img"]] = load_img(tdef["img"], 2)
for edef in GERMAN_TANKS.values():
    images[edef["img"]] = load_img(edef["img"], 2)

state = {
    "fuel":       FUEL_START,
    "wave":       0,
    "wave_timer": WAVE_DELAY // 2,
    "tick":       0,
    "lives":      1,
    "score":      0,
    "selected":   "T34",
    "game_over":  False,
    "victory":    False,
    "paused":     False,
}

grid      = [[None]*COLS for _ in range(ROWS)]
enemies   = []
bullets   = []
particles = []

def cell_center(col, row):
    return GRID_X + col*CELL_W + CELL_W//2, GRID_Y + row*CELL_H + CELL_H//2

def row_y(row):
    return GRID_Y + row*CELL_H + CELL_H//2

def explosion(x, y, n=14):
    for _ in range(n):
        particles.append({
            "x":x, "y":y,
            "dx":random.uniform(-5, 5),
            "dy":random.uniform(-5, 2),
            "life":20,
            "color":random.choice(["#ff4400","#ffaa00","#ffff00","#ff0000","#ffffff"]),
        })

def spawn_wave():
    w     = state["wave"]
    count = WAVE_SIZE_BASE + w * 3
    pool  = (
        ["pz2"]    * max(1, 4 - w) +
        ["nemech"] * (2 + w // 2) +
        ["maus"]   * max(0, w // 2)
    )
    if not pool:
        pool = ["nemech"]
    for i in range(count):
        etype = random.choice(pool)
        edef  = GERMAN_TANKS[etype]
        row   = random.randint(0, ROWS - 1)
        hp    = int(edef["hp"] * HP_MUL * (1 + w * 0.20))
        spd   = edef["speed"] * SPD_MUL * (1 + w * 0.05)
        enemies.append({
            "type":   etype,
            "row":    row,
            "x":      float(SW + 80 + i*100 + random.randint(0, 40)),
            "hp":     hp,
            "max_hp": hp,
            "speed":  spd,
            "damage": int(edef["damage"] * (1 + w * 0.1)),
            "reward": edef["reward"],
            "img":    edef["img"],
            "atk_cd": random.randint(20, edef["atk_cd"]),
        })

def update():
    if state["game_over"] or state["victory"] or state["paused"]:
        draw_frame()
        root.after(FPS, update)
        return

    state["tick"] += 1
    t = state["tick"]

    if t % FUEL_TICK == 0:
        state["fuel"] = min(state["fuel"] + 1, FUEL_MAX)

    state["wave_timer"] -= 1
    if state["wave_timer"] <= 0 and not enemies:
        state["wave"] += 1
        if state["wave"] > MAX_WAVES:
            state["victory"] = True
        else:
            spawn_wave()
            state["wave_timer"] = WAVE_DELAY

    for row in range(ROWS):
        for col in range(COLS):
            tank = grid[row][col]
            if tank is None:
                continue
            tdef = USSR_TANKS[tank["type"]]
            if tank["fire_cd"] > 0:
                tank["fire_cd"] -= 1
                continue
            cx, cy = cell_center(col, row)
            max_x  = cx + tdef["range"] * CELL_W
            target = None
            for e in enemies:
                if e["row"] != row:
                    continue
                if cx < e["x"] <= max_x:
                    if target is None or e["x"] < target["x"]:
                        target = e
            if target:
                tank["fire_cd"] = tdef["fire_cd"]
                bullets.append({
                    "x":     float(cx + 45),
                    "y":     float(cy - 5),
                    "target":target,
                    "dmg":   tdef["damage"],
                    "color": tdef["bullet"],
                    "size":  tdef["bsize"],
                    "speed": 14.0,
                })

    for b in bullets[:]:
        e = b["target"]
        if e not in enemies:
            bullets.remove(b)
            continue
        dx   = e["x"] - b["x"]
        dy   = row_y(e["row"]) - b["y"]
        dist = (dx*dx + dy*dy) ** 0.5
        if dist < b["speed"] + 8:
            e["hp"] -= b["dmg"]
            explosion(e["x"], row_y(e["row"]), 10)
            bullets.remove(b)
        else:
            b["x"] += dx / dist * b["speed"]
            b["y"] += dy / dist * b["speed"]

    for e in enemies[:]:
        row     = e["row"]
        blocked = False
        for col in range(COLS - 1, -1, -1):
            tank = grid[row][col]
            if tank is None:
                continue
            cx, _ = cell_center(col, row)
            if abs(cx - e["x"]) < CELL_W * 0.75:
                blocked = True
                e["atk_cd"] -= 1
                if e["atk_cd"] <= 0:
                    tank["hp"] -= e["damage"]
                    e["atk_cd"] = GERMAN_TANKS[e["type"]]["atk_cd"]
                    explosion(cx, row_y(row), 5)
                    if tank["hp"] <= 0:
                        grid[row][col] = None
                break
        if not blocked:
            e["x"] -= e["speed"] * 2.5
        if e["x"] < GRID_X - 30:
            enemies.remove(e)
            state["lives"] -= 1
            if state["lives"] <= 0:
                state["game_over"] = True
        elif e["hp"] <= 0:
            enemies.remove(e)
            state["fuel"]  = min(state["fuel"] + e["reward"], FUEL_MAX)
            state["score"] += e["reward"]

    for p in particles[:]:
        p["x"] += p["dx"]
        p["y"] += p["dy"]
        p["dy"] += 0.3
        p["life"] -= 1
        if p["life"] <= 0:
            particles.remove(p)

    draw_frame()
    root.after(FPS, update)

def draw_frame():
    canvas.delete("all")

    canvas.create_rectangle(0, 0, SW, GRID_Y-5, fill="#3a1a1a", outline="")
    for cx, cy in [(150,40),(400,60),(750,30),(1100,55),(1500,40),(1800,60)]:
        canvas.create_oval(cx-50,cy-20,cx+50,cy+20, fill="#555", outline="")
        canvas.create_oval(cx-30,cy-35,cx+30,cy+5,  fill="#666", outline="")

    for row in range(ROWS):
        clr = "#2a1010" if row % 2 == 0 else "#251008"
        y1  = GRID_Y + row * CELL_H
        canvas.create_rectangle(0, y1, SW, y1+CELL_H, fill=clr, outline="")

    for row in range(ROWS + 1):
        y = GRID_Y + row * CELL_H
        canvas.create_line(GRID_X, y, GRID_X+COLS*CELL_W, y, fill="#3a1010", width=1)
    for col in range(COLS + 1):
        x = GRID_X + col * CELL_W
        canvas.create_line(x, GRID_Y, x, GRID_Y+ROWS*CELL_H, fill="#3a1010", width=1)

    canvas.create_line(GRID_X, GRID_Y, GRID_X, GRID_Y+ROWS*CELL_H,
                       fill="#ff0000", width=5, dash=(10, 4))
    canvas.create_text(GRID_X-15, GRID_Y+ROWS*CELL_H//2,
                       text="БАЗА", fill="#ff0000", font=("Arial",13,"bold"), angle=90)

    for row in range(ROWS):
        for col in range(COLS):
            t = grid[row][col]
            if t is None:
                continue
            tdef   = USSR_TANKS[t["type"]]
            cx, cy = cell_center(col, row)
            img    = images.get(tdef["img"])
            if img:
                canvas.create_image(cx, cy, image=img, anchor=tk.CENTER)
            else:
                canvas.create_rectangle(cx-45, cy-20, cx+45, cy+20, fill="#4a7a3a", outline="#222", width=2)
            bw    = 85
            ratio = max(t["hp"], 0) / t["max_hp"]
            canvas.create_rectangle(cx-bw//2, cy-38, cx+bw//2, cy-28, fill="#500", outline="")
            canvas.create_rectangle(cx-bw//2, cy-38, cx-bw//2+int(bw*ratio), cy-28, fill="#0c0", outline="")

    for e in enemies:
        ex  = int(e["x"])
        ey  = row_y(e["row"])
        img = images.get(e["img"])
        if img:
            canvas.create_image(ex, ey, image=img, anchor=tk.CENTER)
        else:
            canvas.create_rectangle(ex-45, ey-20, ex+45, ey+20, fill="#7a3a3a", outline="#222", width=2)
        bw    = 85
        ratio = max(e["hp"], 0) / e["max_hp"]
        canvas.create_rectangle(ex-bw//2, ey-40, ex+bw//2, ey-30, fill="#500", outline="")
        canvas.create_rectangle(ex-bw//2, ey-40, ex-bw//2+int(bw*ratio), ey-30, fill="#0c0", outline="")
        canvas.create_text(ex, ey-46, text=GERMAN_TANKS[e["type"]]["name"], fill="#ff6666", font=("Arial",9))

    for b in bullets:
        canvas.create_oval(b["x"]-b["size"], b["y"]-b["size"],
                           b["x"]+b["size"], b["y"]+b["size"], fill=b["color"], outline="")

    for p in particles:
        r = max(1, p["life"] // 5)
        canvas.create_oval(p["x"]-r, p["y"]-r, p["x"]+r, p["y"]+r, fill=p["color"], outline="")

    canvas.create_rectangle(0, 0, SW, GRID_Y-6, fill="#0a0000", outline="")
    canvas.create_text(SW//2, 32, text="💀 HARDCORE — Sssr vs Zombie 💀",
                       fill="#ff2222", font=("Arial",24,"bold"))
    canvas.create_text(25, 18, text=f"Паливо: {state['fuel']}",
                       fill="#ff6644", font=("Arial",17,"bold"), anchor="w")

    wt   = max(0, state["wave_timer"])
    wtxt = f"Хвиля {state['wave']}/{MAX_WAVES}"
    if wt > 0 and not enemies:
        wtxt += f"  |  наступна через {wt // (1000 // FPS)}с"
    canvas.create_text(SW//2, 72, text=wtxt, fill="#ff9999", font=("Arial",15))
    canvas.create_text(SW-25, 18, text=f"Очки: {state['score']}",
                       fill="#ffaa44", font=("Arial",17,"bold"), anchor="e")
    canvas.create_text(SW-25, 52, text="❤️ " * state["lives"] if state["lives"] > 0 else "💀",
                       fill="#ff4444", font=("Arial",15), anchor="e")

    panel_y = GRID_Y + ROWS*CELL_H + 8
    canvas.create_rectangle(0, panel_y, SW, SH, fill="#0a0000", outline="")
    canvas.create_text(22, panel_y+14, text="Вибери танк і клікни на поле:",
                       fill="#ff9999", font=("Arial",13), anchor="w")

    bx = 22
    for key, tdef in USSR_TANKS.items():
        sel = (state["selected"] == key)
        bg  = "#5a1a1a" if sel else "#2a0a0a"
        olc = "#ff4444" if sel else "#663333"
        lw  = 3 if sel else 1
        canvas.create_rectangle(bx, panel_y+28, bx+148, panel_y+90, fill=bg, outline=olc, width=lw)
        img = images.get(tdef["img"])
        if img:
            canvas.create_image(bx+35, panel_y+59, image=img, anchor=tk.CENTER)
        canvas.create_text(bx+90, panel_y+44, text=tdef["name"], fill="#fff", font=("Arial",12,"bold"), anchor="w")
        canvas.create_text(bx+90, panel_y+64, text=tdef["desc"]+" пал", fill="#ff9999", font=("Arial",10), anchor="w")
        bx += 160

    canvas.create_text(SW-20, panel_y+55,
                       text="ЛКМ — поставити  |  ПКМ — продати\nESC — пауза      |  R — рестарт",
                       fill="#663333", font=("Arial",11), anchor="e", justify="right")

    if state["game_over"]:
        canvas.create_rectangle(SW//2-320, SH//2-130, SW//2+320, SH//2+130,
                                 fill="#1a0000", outline="#ff0000", width=5)
        canvas.create_text(SW//2, SH//2-55, text="💀 GAME OVER 💀",
                           fill="#ff0000", font=("Arial",54,"bold"))
        canvas.create_text(SW//2, SH//2+15, text=f"Очки: {state['score']}",
                           fill="white", font=("Arial",24))
        canvas.create_text(SW//2, SH//2+70, text="[R] знову    [ESC] вихід",
                           fill="#aaaaaa", font=("Arial",16))

    if state["victory"]:
        canvas.create_rectangle(SW//2-320, SH//2-130, SW//2+320, SH//2+130,
                                 fill="#001a00", outline="#44ff44", width=5)
        canvas.create_text(SW//2, SH//2-55, text="🏆 НЕМОЖЛИВО... АЛЕ ТИ ВИГРАВ! 🏆",
                           fill="#44ff44", font=("Arial",36,"bold"))
        canvas.create_text(SW//2, SH//2+15, text=f"Очки: {state['score']}",
                           fill="white", font=("Arial",24))
        canvas.create_text(SW//2, SH//2+70, text="[R] знову    [ESC] вихід",
                           fill="#aaaaaa", font=("Arial",16))

    if state["paused"] and not state["game_over"] and not state["victory"]:
        canvas.create_rectangle(SW//2-220, SH//2-55, SW//2+220, SH//2+55,
                                 fill="#000000", outline="#ff4444", width=2)
        canvas.create_text(SW//2, SH//2, text="⏸  ПАУЗА  —  натисни ESC",
                           fill="#ff4444", font=("Arial",22))

def on_click(event):
    if state["game_over"] or state["victory"]:
        return
    mx, my  = event.x, event.y
    panel_y = GRID_Y + ROWS*CELL_H + 8
    bx      = 22
    for key in USSR_TANKS:
        if bx <= mx <= bx+148 and panel_y+28 <= my <= panel_y+90:
            state["selected"] = key
            return
        bx += 160
    col = (mx - GRID_X) // CELL_W
    row = (my - GRID_Y) // CELL_H
    if 0 <= col < COLS and 0 <= row < ROWS:
        if grid[row][col] is None:
            tdef = USSR_TANKS[state["selected"]]
            if state["fuel"] >= tdef["cost"]:
                state["fuel"] -= tdef["cost"]
                grid[row][col] = {
                    "type":    state["selected"],
                    "hp":      tdef["hp"],
                    "max_hp":  tdef["hp"],
                    "fire_cd": 0,
                }

def on_right_click(event):
    col = (event.x - GRID_X) // CELL_W
    row = (event.y - GRID_Y) // CELL_H
    if 0 <= col < COLS and 0 <= row < ROWS:
        t = grid[row][col]
        if t:
            state["fuel"] = min(state["fuel"] + USSR_TANKS[t["type"]]["cost"] // 2, FUEL_MAX)
            grid[row][col] = None

def on_key(event):
    k = event.keysym
    if k == "Escape":
        if state["game_over"] or state["victory"]:
            root.destroy()
            lobby = os.path.join(script_dir, "Lobby.py")
            import subprocess
            subprocess.Popen([sys.executable, lobby])
        else:
            state["paused"] = not state["paused"]
    elif k.lower() in ("r", "к"):
        restart()

def restart():
    global enemies, bullets, particles
    enemies   = []
    bullets   = []
    particles = []
    for r in range(ROWS):
        for c in range(COLS):
            grid[r][c] = None
    state.update({
        "fuel":       FUEL_START,
        "wave":       0,
        "wave_timer": WAVE_DELAY // 2,
        "tick":       0,
        "lives":      1,
        "score":      0,
        "selected":   "T34",
        "game_over":  False,
        "victory":    False,
        "paused":     False,
    })

canvas.bind("<Button-1>", on_click)
canvas.bind("<Button-3>", on_right_click)
root.bind("<KeyPress>", on_key)
canvas.focus_set()

update()
root.mainloop()
