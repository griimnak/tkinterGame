try:
    # Python 2 fallback
    import Tkinter as tk
except ImportError:
    import tkinter as tk
import sys
import time
import threading
import random

# Game defaults
CONF = {}
CONF["canvas_w"] = 800
CONF["canvas_h"] = 600
CONF["stat_hp"] = 1000
CONF["stat_ap"] = 50
CONF["currency_rare"] = 0
CONF["currency_common"] = 10
CONF["stat_death"] = False
CONF["npc_moved"] = False

CONF["frame_rate_list"] = []
CONF["frame_rate"] = 100
CONF["frame_delay"] = 12

# Cursor
X1 = Y1 = CONF["canvas_w"] // 2


class Window(tk.Frame):
    """ Window Object
            Sets up tkinter elements and base window.
    """
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        sys.stdout = self
        """ Logs print() output to game client window. """
        self.log_area = tk.Text(self, height=7, width=40)
        self.log_vsb = tk.Scrollbar(self, orient="vertical", command=self.log_area.yview)

        self.log_area.configure(yscrollcommand=self.log_vsb.set)

        self.log_vsb.pack(side="right", fill="y")
        self.log_area.pack(side="left", fill="both", expand=True)

    def write(self, txt):
        """ log_area write() """
        self.log_area.insert("end", str(txt))
        self.log_area.see("end")
    
    def flush(self):
        """ log_area flush() """
        pass


class Controller:
    """Controller Object
            Game controller.
    """
    def __init__(self):
        print("(Controller mounted) Use WASD to run into the blue wall.")
    def key_w(self, event):
        global Y1
        self.del_rect()
        Y1 -= 10
        self.draw_rect()

    def key_a(self, event):
        global X1
        if X1 < 40:
            pass
        else:
            self.del_rect()
            X1 -= 10
            self.draw_rect()

    def key_s(self, event):
        global Y1
        if Y1 > 560:
            pass
        else:
            self.del_rect()
            Y1 += 10
            self.draw_rect()

    def key_d(self, event=""):
        global X1
        if X1 > 760:
            pass
        else:
            self.del_rect()
            X1 += 10
            self.draw_rect()

    def draw_rect(self):      
        canvas.create_rectangle(X1, Y1, X1 + 10, Y1 + 10, fill="#fff")

    def del_rect(self):
        canvas.create_rectangle(X1, Y1, X1 + 10, Y1 + 10, fill="#000")


def run_npc():
    CONF["npc_moved"] = True
    
    chance = random.randint(1,10)
    if chance > 5:
        print("(Red NPC decides to move)")
        num = random.randint(40,580)
        numx = random.randint(40,680)
        canvas.coords(npc, numx, num, numx+10, num+10)
    time.sleep(3)
    run_npc()

def update():
    global CONF
    timer = time.time()
    root.title("idkgame   FPS:" + str(CONF["frame_rate"])[0:6])

    # Update HUD with any changes
    if CONF["stat_hp"] < 200:
        canvas.itemconfigure(_hp, text=f"HP: {CONF['stat_hp']}", fill="red")
    elif CONF["stat_hp"] < 700:
        canvas.itemconfigure(_hp, text=f"HP: {CONF['stat_hp']}", fill="orange")
    else:
        canvas.itemconfigure(_hp, text=f"HP: {CONF['stat_hp']}")
    canvas.itemconfigure(_ap, text=f"AP: {CONF['stat_ap']}")

    # Check death status
    if CONF["stat_hp"] < 1:
        CONF["stat_hp"] = 0
        CONF["stat_death"] = True

    if CONF["stat_death"] == True:
        print("Game over.")

    # npc demo **
    if CONF["npc_moved"] is False:
        threading.Thread(target=run_npc).start()

    # Wall demo **
    if X1 == 40:
        controller.key_d()
        CONF["stat_hp"] = CONF["stat_hp"] - 30
        print(f"[{time.ctime()}] *hits wall* -30 ==> {CONF['stat_hp']}")

    # Last
    timer_end = time.time()
    root.after(CONF["frame_delay"], update)
    CONF["frame_rate_list"].append(float(timer_end - timer))
    if len(CONF["frame_rate_list"]) == 30:
        try:
            CONF["frame_rate"] = str(1 / (sum(CONF["frame_rate_list"]) / 30))
        except:
            CONF["frame_rate"] = 1000
        else:
            CONF["frame_rate_list"] = []


root = tk.Tk()
window = Window(root)

# Game screen
canvas = tk.Canvas(root, bg="#000", width=CONF["canvas_w"], height=CONF["canvas_h"])

# Binds
controller = Controller()
canvas.bind_all('<KeyPress-W>', controller.key_w)  # ^
canvas.bind_all('<KeyPress-w>', controller.key_w)  # |

canvas.bind_all('<KeyPress-A>', controller.key_a)  # <-
canvas.bind_all('<KeyPress-a>', controller.key_a)  # <-

canvas.bind_all('<KeyPress-S>', controller.key_s)  # |
canvas.bind_all('<KeyPress-s>', controller.key_s)  # v

canvas.bind_all('<KeyPress-D>', controller.key_d)  # ->
canvas.bind_all('<KeyPress-d>', controller.key_d)  # ->

canvas.create_rectangle(X1, Y1, X1 + 10, Y1 + 10, fill="#fff")
canvas.create_rectangle(40, 500, 40 + 10, 40 + 10, fill="blue")
npc = canvas.create_rectangle(110, 60, 60 + 60, 60 + 10, fill="red")
#canvas.bind_all("<Key>", Controller)
canvas.pack(fill="both", expand=True)

_hp = canvas.create_text((10,15),text=f"HP: 1000", fill="green", anchor="w")
_ap = canvas.create_text((10,35), text=f"AP:  50", fill="#fff", anchor="w")

window.pack(fill="both", expand=True)

while True:
    """Game loop
            Here begins the game loop
    """
    update()
    root.mainloop()
