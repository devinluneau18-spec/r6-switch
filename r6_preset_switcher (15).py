import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os, re, glob, time, threading, json

# ─── Optional automation imports ───────────────────────────────────────────────
try:
    import pyautogui
    import pygetwindow as gw
    AUTOGUI_AVAILABLE = True
except ImportError:
    AUTOGUI_AVAILABLE = False

# ─── Calibration file ──────────────────────────────────────────────────────────
CALIB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ghub_calibration.json")

def load_calibration():
    try:
        with open(CALIB_FILE, "r") as f:
            return json.load(f)
    except:
        return None

def save_calibration(data):
    with open(CALIB_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ─── Calibration steps definition ─────────────────────────────────────────────
CALIB_STEPS = [
    {
        "key":   "hamburger",
        "title": "Step 1 of 5 — Profile Menu Button",
        "instruction": (
            "Go to GHub and find your R6 Siege profile.\n\n"
            "Hover your mouse over the  ☰  three-line menu icon\n"
            "on that profile card, then press START."
        ),
        "label": "Capturing: ☰ profile hamburger menu",
    },
    {
        "key":   "create_lua",
        "title": "Step 2 of 5 — Create Lua Script",
        "instruction": (
            "Click the ☰ menu on your profile to open it,\n"
            "then scroll to the bottom of the options.\n\n"
            "Hover your mouse over  'Create Lua Script'  and press START."
        ),
        "label": "Capturing: Create Lua Script option",
    },
    {
        "key":   "script_menu",
        "title": "Step 3 of 5 — Script Menu",
        "instruction": (
            "The script editor should now be open.\n\n"
            "Hover your mouse over the  'Script'  menu\n"
            "in the top menu bar of the editor, then press START."
        ),
        "label": "Capturing: Script menu in editor",
    },
    {
        "key":   "save_run",
        "title": "Step 4 of 5 — Save & Run",
        "instruction": (
            "Click  'Script'  in GHub to open the dropdown,\n"
            "then hover your mouse over  'Save & Run'  in the list.\n\n"
            "Hold still and press START."
        ),
        "label": "Capturing: Save & Run option",
    },
    {
        "key":   "back_arrow",
        "title": "Step 5 of 5 — Back Arrow",
        "instruction": (
            "Finally, hover your mouse over the  ← back arrow\n"
            "in GHub that returns you to the profiles menu.\n\n"
            "Hold still and press START."
        ),
        "label": "Capturing: ← back arrow to profiles",
    },
]

# ─── Presets ───────────────────────────────────────────────────────────────────
PRESETS = [
    ("Ace","ace"),("Amaru","amaru"),("Ash","ash"),("Brava","brava"),
    ("Buck","buck"),("Deimos","deimos"),("Dokkaebi","dokkaebi"),
    ("Finka","Finka"),("Fuze","Fuze"),("Glaz","Glaz"),
    ("Gridlock","Gridlock"),("Grim","grim"),("Hibana","Hibana"),
    ("Iana","Iana"),("IQ","IQ"),("Jackal","Jackal"),("Lion","lion"),
    ("Maverick","maverick"),("Nokk","nokk"),("Nomad","nomad"),
    ("Osa","Osa"),("Ram","ram"),("Rauora","Rauora"),("Sens","Sens"),
    ("Sledge","Sledge"),("Thatcher","thatcher"),("Thermite","thermite"),
    ("Twitch","twitch"),("Ying","Ying"),("Zero","Zero"),("Zofia","Zofia"),
    ("Alibi","alibi"),("Aruni","aruni"),("Azami","azami"),
    ("Bandit","bandit"),("Castle","Castle"),("Doc","doc"),
    ("Denari","denari"),("Echo","echo"),("Ela","ela"),
    ("Fenrir","fenrir"),("Goyo","goyo"),("Jager","jager"),
    ("Kaid","kaid"),("Kapkan","kapkan"),("Lesion","lesion"),
    ("Maestro","maestro"),("Melusi","melusi"),("Mira","mira"),
    ("Mozzie","mozzie"),("Mute","mute"),("Oryx","Oryx"),
    ("Pulse","Pulse"),("Rook","Rook"),("Smoke","Smoke"),
    ("Solis","Solis"),("Thorn","Thorn"),("Thunderbird","Thunderbird"),
    ("Tubarao","tubarao"),("Valkyrie","valkyrie"),("Vigil","Vigil"),
    ("Wamai","Wamai"),("Warden","Warden"),("Frost","frost"),
]

PRESET_STATS = {
    "ace":(29,-1),"amaru":(12,0),"ash":(29,-1),"brava":(17,-1),
    "frost":(8,-1),"buck":(25,-1),"deimos":(17,0),"dokkaebi":(24,1),
    "Finka":(12,0),"Fuze":(19,-1),"Glaz":(12,0),"Gridlock":(13,0),
    "grim":(18,0),"Hibana":(8,-1),"Iana":(14,0),"IQ":(13,0),
    "Jackal":(30,12),"lion":(17,0),"maverick":(22,-2),"nokk":(25,0),
    "nomad":(17,-1),"Osa":(50,20),"ram":(29,-1),"Rauora":(10,6),
    "Sens":(20,8),"Sledge":(10,0),"thatcher":(16,0),"thermite":(16,0),
    "twitch":(43,0),"Ying":(45,18),"Zero":(50,20),"Zofia":(14,1),
    "alibi":(15,1),"aruni":(8,-1),"azami":(11,-1),"bandit":(12,1),
    "Castle":(30,12),"doc":(10,0),"denari":(14,0),"echo":(9,0),
    "ela":(14,0),"fenrir":(12,1),"goyo":(14,0),"jager":(12,-1),
    "kaid":(35,0),"kapkan":(10,0),"lesion":(11,0),"maestro":(13,0),
    "melusi":(10,0),"mira":(14,0),"mozzie":(11,2),"mute":(19,0),
    "Oryx":(9,0),"Pulse":(15,6),"Rook":(6,0),"Smoke":(19,0),
    "Solis":(30,12),"Thorn":(7,0),"Thunderbird":(40,16),"tubarao":(10,0),
    "valkyrie":(12,0),"Vigil":(15,1),"Wamai":(10,4),"Warden":(15,1),
}

def get_recoil_label(vert, horiz):
    if vert <= 10:   return "Low",       "#4ade80"
    elif vert <= 20: return "Medium",    "#facc15"
    elif vert <= 30: return "High",      "#fb923c"
    else:            return "Very High", "#f87171"

# ─── File helpers ───────────────────────────────────────────────────────────────
def find_ghub_script():
    appdata = os.environ.get("LOCALAPPDATA", "")
    patterns = [
        os.path.join(appdata, "LGHUB", "scriptfiles", "*.lua"),
        os.path.join(appdata, "LGHUB", "profiles", "**", "*.lua"),
        os.path.join(os.path.expanduser("~"), "AppData", "Local", "LGHUB", "**", "*.lua"),
    ]
    candidates = []
    for p in patterns:
        candidates.extend(glob.glob(p, recursive=True))
    for path in candidates:
        name = os.path.basename(path).lower()
        if "r6" in name or "recoil" in name or "siege" in name:
            return path
    for path in candidates:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            if 'Preset = "' in content and "VerticalStrength" in content:
                return path
        except:
            pass
    return None

def read_current_preset(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        m = re.search(r'Preset\s*=\s*"([^"]+)"', content)
        if m:
            return m.group(1)
    except:
        pass
    return None

def write_preset(filepath, value):
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        new = re.sub(r'(Preset\s*=\s*)"[^"]+"', f'\\1"{value}"', content, count=1)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new)
        return True
    except Exception as e:
        return str(e)

# ─── GHub automation ───────────────────────────────────────────────────────────
def ghub_save_and_run(calib, status_cb=None):
    """
    Full sequence:
      1. Focus GHub
      2. Click ☰ hamburger on the profile
      3. Click 'Create Lua Script' (forces reload of file from disk)
      4. Wait for editor to open
      5. Click Script menu
      6. Click Save & Run
    """
    if not AUTOGUI_AVAILABLE:
        return False, "pyautogui not installed."
    if not calib:
        return False, "⚠  Not calibrated — click '⊕ CALIBRATE GHUB' first."

    # Find and focus GHub
    ghub_win = None
    for title in gw.getAllTitles():
        if "lghub" in title.lower() or "g hub" in title.lower() or "logitech" in title.lower():
            wins = gw.getWindowsWithTitle(title)
            if wins:
                ghub_win = wins[0]
                break

    if ghub_win is None:
        return False, "⚠  GHub window not found — is GHub open?"

    if status_cb: status_cb("⟳  Focusing GHub...")
    try:
        if ghub_win.isMinimized:
            ghub_win.restore()
        ghub_win.activate()
    except:
        pass
    time.sleep(0.3)

    # Step 1 — Click the ☰ hamburger menu on the profile
    if status_cb: status_cb("⟳  Opening profile menu...")
    pyautogui.click(calib["hamburger_x"], calib["hamburger_y"])
    time.sleep(0.3)   # wait for dropdown to fully appear

    # Step 2 — Move mouse into the open dropdown and scroll to the bottom
    # so that "Create Lua Script" becomes visible regardless of menu length
    if status_cb: status_cb("⟳  Scrolling menu to bottom...")
    menu_x = calib["hamburger_x"]
    menu_y = calib["hamburger_y"] + 80  # move cursor into the body of the open menu
    pyautogui.moveTo(menu_x, menu_y, duration=0.05)
    time.sleep(0.05)
    for _ in range(20):
        pyautogui.scroll(-20)  # rapid repeated scrolls = faster scroll speed
        time.sleep(0.01)
    time.sleep(0.1)         # wait for scroll animation to fully settle

    # Step 3 — Click "Create Lua Script" which is now scrolled into view
    if status_cb: status_cb("⟳  Clicking 'Create Lua Script'...")
    pyautogui.click(calib["create_lua_x"], calib["create_lua_y"])
    time.sleep(0.6)   # wait for the script editor to open/reload

    # Step 3 — Click the Script menu in the editor top bar
    if status_cb: status_cb("⟳  Clicking Script menu...")
    pyautogui.click(calib["script_menu_x"], calib["script_menu_y"])
    time.sleep(0.2)   # wait for dropdown

    # Step 4 — Click Save & Run
    if status_cb: status_cb("⟳  Clicking Save & Run...")
    pyautogui.click(calib["save_run_x"], calib["save_run_y"])
    time.sleep(0.2)

    # Step 5 — Click the back arrow to return to profiles menu (ready for next change)
    if status_cb: status_cb("⟳  Returning to profiles menu...")
    pyautogui.click(calib["back_arrow_x"], calib["back_arrow_y"])
    time.sleep(0.3)

    return True, "✓  GHub reloaded and 'Save & Run' triggered."

def ghub_save_and_run_async(calib, status_cb=None, done_cb=None):
    def worker():
        ok, msg = ghub_save_and_run(calib, status_cb)
        if done_cb:
            done_cb(ok, msg)
    threading.Thread(target=worker, daemon=True).start()


# ─── Calibration Window ────────────────────────────────────────────────────────
class CalibrationWindow:
    """
    4-step wizard — captures mouse position for each GHub click target.
    User hovers their mouse over the target, presses START, then has 3 seconds
    to switch to GHub and position their cursor before it captures.
    """
    def __init__(self, parent, existing_calib, on_complete):
        self.parent      = parent
        self.on_complete = on_complete
        self.step        = 0
        self.coords      = dict(existing_calib) if existing_calib else {}

        self.win = tk.Toplevel(parent)
        self.win.title("Calibrate GHub")
        self.win.configure(bg="#0d0f14")
        self.win.geometry("540x320")
        self.win.resizable(False, False)
        self.win.grab_set()
        self.win.protocol("WM_DELETE_WINDOW", self._cancel)

        # Header
        tk.Label(self.win, text="GHUB CALIBRATION",
                 font=("Courier New", 13, "bold"),
                 bg="#0d0f14", fg="#e8b84b", pady=14).pack()

        self.title_lbl = tk.Label(self.win, text="",
                                  font=("Courier New", 10, "bold"),
                                  bg="#0d0f14", fg="#7dc4e4")
        self.title_lbl.pack()

        self.instruction = tk.Label(self.win, text="",
                                    font=("Courier New", 9),
                                    bg="#0d0f14", fg="#c8cdd8",
                                    wraplength=490, justify="center")
        self.instruction.pack(padx=20, pady=(6, 0))

        self.countdown_lbl = tk.Label(self.win, text="",
                                      font=("Courier New", 30, "bold"),
                                      bg="#0d0f14", fg="#e8b84b")
        self.countdown_lbl.pack(pady=6)

        self.step_lbl = tk.Label(self.win, text="",
                                 font=("Courier New", 8),
                                 bg="#0d0f14", fg="#5a6070")
        self.step_lbl.pack()

        btn_row = tk.Frame(self.win, bg="#0d0f14")
        btn_row.pack(pady=14)

        self.start_btn = tk.Button(btn_row, text="START",
                                   font=("Courier New", 10, "bold"),
                                   bg="#e8b84b", fg="#0d0f14",
                                   relief="flat", bd=0,
                                   padx=20, pady=8, cursor="hand2",
                                   command=self._begin_step)
        self.start_btn.pack(side="left", padx=6)

        tk.Button(btn_row, text="CANCEL",
                  font=("Courier New", 10),
                  bg="#1e2230", fg="#c8cdd8",
                  relief="flat", bd=0,
                  padx=20, pady=8, cursor="hand2",
                  command=self._cancel).pack(side="left", padx=6)

        self._show_step()

    def _show_step(self):
        s = CALIB_STEPS[self.step]
        self.title_lbl.configure(text=s["title"])
        self.instruction.configure(text=s["instruction"])
        self.step_lbl.configure(text=s["label"])
        self.countdown_lbl.configure(text="")
        self.start_btn.configure(
            text=f"START  (step {self.step + 1} of {len(CALIB_STEPS)})",
            state="normal"
        )

    def _begin_step(self):
        self.start_btn.configure(state="disabled")
        self._countdown(3)

    def _countdown(self, n):
        if n > 0:
            self.countdown_lbl.configure(text=str(n))
            self.win.after(1000, lambda: self._countdown(n - 1))
        else:
            self.countdown_lbl.configure(text="📍")
            self.win.after(150, self._capture)

    def _capture(self):
        x, y = pyautogui.position()
        key  = CALIB_STEPS[self.step]["key"]
        self.coords[f"{key}_x"] = x
        self.coords[f"{key}_y"] = y

        self.countdown_lbl.configure(text=f"✓  ({x}, {y})")

        if self.step < len(CALIB_STEPS) - 1:
            self.step += 1
            self.win.after(900, self._show_step)
        else:
            self.win.after(600, self._finish)

    def _finish(self):
        save_calibration(self.coords)
        self.win.destroy()
        self.on_complete(self.coords)

    def _cancel(self):
        self.win.destroy()


# ─── Main App ──────────────────────────────────────────────────────────────────
class R6PresetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("R6 Recoil — Preset Switcher")
        self.root.geometry("820x700")
        self.root.resizable(True, True)
        self.root.configure(bg="#0d0f14")

        self.script_path    = tk.StringVar()
        self.search_var     = tk.StringVar()
        self.current_preset = None
        self.calibration    = load_calibration()
        self.active_tab     = "attacker"   # "attacker" or "defender"

        self.search_var.trace("w", self.filter_presets)
        self._build_ui()

        found = find_ghub_script()
        if found:
            self.script_path.set(found)
            self._refresh_active_preset()
        else:
            self.status_var.set("⚠  Script not auto-detected — use Browse to locate it.")

    def _build_ui(self):
        # ── Top bar ──────────────────────────────────────────────────────────────
        topbar = tk.Frame(self.root, bg="#0d0f14")
        topbar.pack(fill="x", padx=18, pady=(18, 0))

        tk.Label(topbar, text="R6", font=("Courier New", 22, "bold"),
                 bg="#0d0f14", fg="#e8b84b").pack(side="left")
        tk.Label(topbar, text=" RECOIL SWITCHER", font=("Courier New", 14, "bold"),
                 bg="#0d0f14", fg="#c8cdd8").pack(side="left", pady=(6, 0))

        self.calib_badge = tk.Label(topbar, font=("Courier New", 8, "bold"), bg="#0d0f14")
        self.calib_badge.pack(side="right", pady=(8, 0))
        self._update_calib_badge()

        tk.Button(topbar, text="⊕ CALIBRATE GHUB",
                  font=("Courier New", 8, "bold"),
                  bg="#1e2230", fg="#7dc4e4",
                  relief="flat", bd=0, padx=10, pady=4, cursor="hand2",
                  command=self._open_calibration
                  ).pack(side="right", padx=(0, 10), pady=(6, 0))

        # ── File path bar ─────────────────────────────────────────────────────────
        pathbar = tk.Frame(self.root, bg="#161920")
        pathbar.pack(fill="x", padx=18, pady=(14, 0))

        tk.Label(pathbar, text="SCRIPT PATH", font=("Courier New", 8, "bold"),
                 bg="#161920", fg="#5a6070", padx=10, pady=6).pack(side="left")

        tk.Entry(pathbar, textvariable=self.script_path,
                 font=("Courier New", 9), bg="#1e2230", fg="#7dc4e4",
                 insertbackground="#7dc4e4", relief="flat", bd=0,
                 highlightthickness=0
                 ).pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 4))

        tk.Button(pathbar, text="BROWSE", font=("Courier New", 8, "bold"),
                  bg="#e8b84b", fg="#0d0f14", relief="flat", bd=0,
                  padx=12, cursor="hand2",
                  command=self._browse_file
                  ).pack(side="right", ipadx=4, ipady=8)

        tk.Button(pathbar, text="↺", font=("Courier New", 11, "bold"),
                  bg="#1e2230", fg="#7dc4e4", relief="flat", bd=0,
                  padx=10, cursor="hand2",
                  command=self._refresh_active_preset
                  ).pack(side="right", ipadx=4, ipady=6)

        # ── Active preset banner ──────────────────────────────────────────────────
        banner = tk.Frame(self.root, bg="#1a1f2e")
        banner.pack(fill="x", padx=18, pady=(10, 0))

        self.active_label = tk.Label(banner, text="Active Preset: —",
                                     font=("Courier New", 11, "bold"),
                                     bg="#1a1f2e", fg="#e8b84b",
                                     padx=14, pady=10, anchor="w")
        self.active_label.pack(side="left", fill="x", expand=True)

        self.recoil_badge = tk.Label(banner, text="",
                                     font=("Courier New", 9, "bold"),
                                     bg="#1a1f2e", fg="#0d0f14", padx=10, pady=4)
        self.recoil_badge.pack(side="right", padx=10)

        # ── Attacker / Defender tabs ──────────────────────────────────────────────
        tabbar = tk.Frame(self.root, bg="#0d0f14")
        tabbar.pack(fill="x", padx=18, pady=(14, 0))

        self.tab_var = tk.StringVar(value="attacker")

        self.atk_btn = tk.Button(tabbar, text="⚔  ATTACKERS",
                                 font=("Courier New", 10, "bold"),
                                 bg="#e8b84b", fg="#0d0f14",
                                 relief="flat", bd=0, padx=20, pady=8,
                                 cursor="hand2",
                                 command=lambda: self._switch_tab("attacker"))
        self.atk_btn.pack(side="left")

        self.def_btn = tk.Button(tabbar, text="🛡  DEFENDERS",
                                 font=("Courier New", 10, "bold"),
                                 bg="#1e2230", fg="#5a6070",
                                 relief="flat", bd=0, padx=20, pady=8,
                                 cursor="hand2",
                                 command=lambda: self._switch_tab("defender"))
        self.def_btn.pack(side="left", padx=(4, 0))

        # ── Search bar ────────────────────────────────────────────────────────────
        searchbar = tk.Frame(self.root, bg="#0d0f14")
        searchbar.pack(fill="x", padx=18, pady=(10, 0))

        tk.Label(searchbar, text="🔍", font=("Segoe UI Emoji", 11),
                 bg="#0d0f14", fg="#5a6070").pack(side="left")

        se = tk.Entry(searchbar, textvariable=self.search_var,
                      font=("Courier New", 10), bg="#161920", fg="#c8cdd8",
                      insertbackground="#e8b84b", relief="flat", bd=0,
                      highlightthickness=1, highlightbackground="#2a2f3e",
                      highlightcolor="#e8b84b")
        se.pack(side="left", fill="x", expand=True, ipady=7, padx=(6, 0))
        se.bind("<FocusIn>",  lambda e: se.configure(highlightbackground="#e8b84b"))
        se.bind("<FocusOut>", lambda e: se.configure(highlightbackground="#2a2f3e"))

        # ── Scrollable preset grid ────────────────────────────────────────────────
        container = tk.Frame(self.root, bg="#0d0f14")
        container.pack(fill="both", expand=True, padx=18, pady=(12, 0))

        canvas = tk.Canvas(container, bg="#0d0f14", highlightthickness=0, bd=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.grid_frame = tk.Frame(canvas, bg="#0d0f14")
        cw = canvas.create_window((0, 0), window=self.grid_frame, anchor="nw")

        self.grid_frame.bind("<Configure>",
                             lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(cw, width=e.width))
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        # ── Status bar ────────────────────────────────────────────────────────────
        statusbar = tk.Frame(self.root, bg="#0a0c10", height=32)
        statusbar.pack(fill="x", side="bottom")
        statusbar.pack_propagate(False)
        self.status_var = tk.StringVar(value="Ready.")
        tk.Label(statusbar, textvariable=self.status_var,
                 font=("Courier New", 9), bg="#0a0c10", fg="#5a6070",
                 anchor="w", padx=14).pack(fill="both", expand=True)

        self.all_buttons = {}
        self._build_preset_buttons(PRESETS[:32])

    def _update_calib_badge(self):
        if self.calibration and all(
            f"{s['key']}_x" in self.calibration for s in CALIB_STEPS
        ):
            self.calib_badge.configure(text="● CALIBRATED", fg="#4ade80")
        else:
            self.calib_badge.configure(text="○ NOT CALIBRATED", fg="#f87171")

    # ── Calibration ───────────────────────────────────────────────────────────────
    def _open_calibration(self):
        if not AUTOGUI_AVAILABLE:
            messagebox.showerror("Missing Package",
                "Please install pyautogui first:\n\npip install pyautogui pygetwindow")
            return
        CalibrationWindow(self.root, self.calibration, self._on_calibration_done)

    def _on_calibration_done(self, coords):
        self.calibration = coords
        self._update_calib_badge()
        self.status_var.set("✓  Calibration saved! All 4 positions captured.")

    def _switch_tab(self, tab):
        self.active_tab = tab
        self.search_var.set("")  # clear search when switching tabs
        if tab == "attacker":
            self.atk_btn.configure(bg="#e8b84b", fg="#0d0f14")
            self.def_btn.configure(bg="#1e2230", fg="#5a6070")
            self._build_preset_buttons(PRESETS[:32])
        else:
            self.atk_btn.configure(bg="#1e2230", fg="#5a6070")
            self.def_btn.configure(bg="#e8b84b", fg="#0d0f14")
            self._build_preset_buttons(PRESETS[32:])

    # ── Preset grid ───────────────────────────────────────────────────────────────
    def _build_preset_buttons(self, presets):
        for w in self.grid_frame.winfo_children():
            w.destroy()
        self.all_buttons = {}

        COLS = 4
        for i, (label, value) in enumerate(presets):
            row, col = divmod(i, COLS)
            stats = PRESET_STATS.get(value)
            vert  = stats[0] if stats else "?"
            horiz = stats[1] if stats else "?"
            _, color = get_recoil_label(vert, 0) if isinstance(vert, int) else (None, "#5a6070")

            cell = tk.Frame(self.grid_frame, bg="#161920",
                            highlightbackground="#252a38", highlightthickness=1)
            cell.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            self.grid_frame.columnconfigure(col, weight=1)

            tk.Frame(cell, bg=color, width=3).pack(side="left", fill="y")

            inner = tk.Frame(cell, bg="#161920")
            inner.pack(side="left", fill="both", expand=True, padx=(8, 6), pady=6)

            name_lbl = tk.Label(inner, text=label.upper(),
                                font=("Courier New", 9, "bold"),
                                bg="#161920", fg="#c8cdd8", anchor="w")
            name_lbl.pack(fill="x")

            stats_lbl = tk.Label(inner,
                                 text=f"V:{vert}  H:{horiz}" if isinstance(vert, int) else "",
                                 font=("Courier New", 7),
                                 bg="#161920", fg="#5a6070", anchor="w")
            stats_lbl.pack(fill="x")

            apply_btn = tk.Button(cell, text="SET",
                                  font=("Courier New", 8, "bold"),
                                  bg="#1e2230", fg="#e8b84b",
                                  relief="flat", bd=0, padx=10, cursor="hand2",
                                  command=lambda v=value, l=label: self._apply_preset(v, l))
            apply_btn.pack(side="right", padx=6, pady=6, ipady=4)

            self.all_buttons[value] = (cell, apply_btn)

            def on_enter(e, c=cell, b=apply_btn):
                c.configure(highlightbackground="#e8b84b")
                b.configure(bg="#e8b84b", fg="#0d0f14")

            def on_leave(e, c=cell, b=apply_btn, v=value):
                if v != self.current_preset:
                    c.configure(highlightbackground="#252a38")
                    b.configure(bg="#1e2230", fg="#e8b84b")

            for w in [cell, inner, name_lbl, stats_lbl, apply_btn]:
                w.bind("<Enter>", on_enter)
                w.bind("<Leave>", on_leave)

        self._highlight_active()

    def _highlight_active(self):
        for value, (cell, btn) in self.all_buttons.items():
            if value == self.current_preset:
                cell.configure(highlightbackground="#e8b84b", highlightthickness=2, bg="#1e2230")
                btn.configure(bg="#e8b84b", fg="#0d0f14", text="✓ ON")
                for w in cell.winfo_children():
                    try: w.configure(bg="#1e2230")
                    except: pass
            else:
                cell.configure(highlightbackground="#252a38", highlightthickness=1, bg="#161920")
                btn.configure(bg="#1e2230", fg="#e8b84b", text="SET")
                for w in cell.winfo_children():
                    try: w.configure(bg="#161920")
                    except: pass

    # ── Apply preset ──────────────────────────────────────────────────────────────
    def _apply_preset(self, value, label):
        path = self.script_path.get().strip()
        if not path or not os.path.isfile(path):
            messagebox.showerror("Error", "Script file not found.\nCheck the path or use Browse.")
            return

        result = write_preset(path, value)
        if result is not True:
            messagebox.showerror("Write Error", f"Could not write to file:\n{result}")
            return

        self.current_preset = value
        self._update_active_banner(label, value)
        self._highlight_active()

        if not AUTOGUI_AVAILABLE:
            self.status_var.set(
                f"✓  Preset saved as '{label}'. "
                "Run:  pip install pyautogui pygetwindow  to enable GHub automation."
            )
            return

        if not self.calibration or not all(
            f"{s['key']}_x" in self.calibration for s in CALIB_STEPS
        ):
            self.status_var.set(
                f"✓  Preset saved as '{label}'. "
                "Click '⊕ CALIBRATE GHUB' to enable automatic Save & Run."
            )
            return

        self.status_var.set(f"✓  Preset saved — triggering GHub...")

        def on_status(msg):
            self.root.after(0, lambda: self.status_var.set(msg))

        def on_done(ok, msg):
            self.root.after(0, lambda: self.status_var.set(msg))

        ghub_save_and_run_async(self.calibration, status_cb=on_status, done_cb=on_done)

    # ── Helpers ───────────────────────────────────────────────────────────────────
    def _refresh_active_preset(self):
        path = self.script_path.get().strip()
        if path and os.path.isfile(path):
            self.current_preset = read_current_preset(path)
            if self.current_preset:
                label = next((l for l, v in PRESETS if v == self.current_preset), self.current_preset)
                self._update_active_banner(label, self.current_preset)
                self._highlight_active()
                self.status_var.set(f"↺  Refreshed — current preset: {label}")
            else:
                self.status_var.set("⚠  Could not read preset from file.")
        else:
            self.status_var.set("⚠  No valid script path set.")

    def _update_active_banner(self, label, value):
        stats = PRESET_STATS.get(value)
        if stats:
            vert, horiz = stats
            rl, color = get_recoil_label(vert, horiz)
            self.active_label.configure(
                text=f"Active Preset: {label.upper()}   │   V: {vert}   H: {horiz}")
            self.recoil_badge.configure(
                text=f" {rl.upper()} RECOIL ", bg=color, fg="#0d0f14")
        else:
            self.active_label.configure(text=f"Active Preset: {label.upper()}")
            self.recoil_badge.configure(text="")

    def _browse_file(self):
        path = filedialog.askopenfilename(
            title="Select GHub Lua Script",
            filetypes=[("Lua Files", "*.lua"), ("All Files", "*.*")],
            initialdir=os.path.join(os.environ.get("LOCALAPPDATA", ""), "LGHUB"))
        if path:
            self.script_path.set(path)
            self._refresh_active_preset()

    def filter_presets(self, *args):
        q = self.search_var.get().lower().strip()
        pool = PRESETS[:32] if self.active_tab == "attacker" else PRESETS[32:]
        filtered = [(l, v) for l, v in pool if q in l.lower() or q in v.lower()] if q else pool
        self._build_preset_buttons(filtered)


# ─── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Vertical.TScrollbar",
                    background="#1e2230", troughcolor="#0d0f14",
                    arrowcolor="#5a6070", bordercolor="#0d0f14")
    R6PresetApp(root)
    root.mainloop()
