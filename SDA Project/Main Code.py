#import library
import tkinter as tk
from tkinter import ttk
import tkintermapview
import heapq
import customtkinter as ctk
from PIL import Image, ImageTk
from ctypes import windll

#import font
try:
    windll.gdi32.AddFontResourceExW("Font use/SpaceGrotesk-Regular.ttf", 0x10, 0)
    windll.gdi32.AddFontResourceExW("Font use/SpaceGrotesk-Medium.ttf", 0x10, 0)
    windll.gdi32.AddFontResourceExW("Font use/SpaceGrotesk-SemiBold.ttf", 0x10, 0)
    windll.gdi32.AddFontResourceExW("Font use/SpaceGrotesk-Bold.ttf", 0x10, 0)
    windll.gdi32.AddFontResourceExW("Font use/SpaceGrotesk-Bold.ttf", 0x10, 0)
except Exception as e:
    print(f"Gagal memuat file font: {e}")
    
# Palet warna
BG_MAIN      = "#f3eeff"   # bg utama
BG_CARD      = "#e8d8ff"   # bg card
ACCENT_LIGHT = "#d4b8ff"   # aksen terang
ACCENT_MAIN  = "#7c5cbf"   # aksen utama (tombol)
ACCENT_DARK  = "#5a3d9c"   # aksen gelap (header)
SUCCESS      = "#c8f7c5"   # sukses / rute
ERROR        = "#ffd6d6"   # error / reset
INFO         = "#fff4cc"   # info / langkah
WHITE        = "#ffffff"   # tabel / putih
TEXT_DARK    = "#4a4a6a"   # teks gelap

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# DATA GRAF

node_graph = {
    'MD' : 'Pintu Depan',
    'MB' : 'Pintu Belakang',
    'A'  : 'Area Teknik Informatika',
    'A2' : 'Area Pend. Tata Rias',
    'A3' : 'Gedung Teknik Utama',
    'A4' : 'Teknik Elektro, Sipil',
    'B'  : 'Fakultas FMIPA',
    'B2' : 'Sains Data',
    'C1' : 'Fakultas Hukum',
    'D'  : 'Danau',
    'E'  : 'Fakultas Vokasi',
    'F'  : 'Fakultas Ekonomi dan Bisnis',
    'F2' : 'Area FEB Tengah',
    'F3' : 'Area FEB Belakang',
    'G'  : 'Fisipol',
    'UKM': 'UKM Center',
    'GSG': 'Gedung Serba Guna',
    'FC1': 'Food Court Baru',
    'FC2': 'Food Court Lama',
}

#jarak antar graf
edge_graph = [
    ('MB', 'A',   30), 
    ('MB', 'A2',  50), 
    ('MD', 'G',   65),
    ('A',  'A2',  30), 
    ('A',  'B',  120),
    ('A2', 'A3', 100), 
    ('A2', 'A4', 115),
    ('A3', 'A4', 100),
    ('A4', 'B',  160), 
    ('A4', 'B2',  70), 
    ('A4', 'FC1',115),
    ('B',  'B2', 250), 
    ('B',  'D',   95), 
    ('B',  'FC1',130), 
    ('B', 'FC2',175),
    ('B2', 'C1', 105), 
    ('B2', 'F2', 135), 
    ('B2', 'FC1', 60), 
    ('B2','FC2',110),
    ('C1', 'F2',  80), 
    ('C1', 'F3', 150), 
    ('C1', 'FC1',120), 
    ('C1','FC2', 80),
    ('D',  'E',  300), 
    ('D',  'FC1', 80), 
    ('D',  'FC2',100),
    ('E',  'GSG',120), 
    ('E',  'UKM',150),
    ('F',  'F3',  80), 
    ('F',  'G',  130), 
    ('F',  'UKM',105),
    ('F2', 'F3',  90),
    ('G',  'UKM',180),
    ('UKM','GSG', 80),
    ('FC1','FC2', 60),
]

#koordinat tkinterviewmap
node_pos = {
    'MB' : (-7.317247, 112.725369),
    'MD' : (-7.311469, 112.729386),
    'A'  : (-7.316933, 112.725169),
    'A2' : (-7.316911, 112.725775),
    'A3' : (-7.317158, 112.726392),
    'A4' : (-7.316264, 112.726475),
    'B'  : (-7.315169, 112.725278),
    'B2' : (-7.315506, 112.727031),
    'C1' : (-7.314622, 112.727436),
    'D'  : (-7.314156, 112.726025),
    'E'  : (-7.311519, 112.727061),
    'F'  : (-7.313267, 112.728903),
    'F2' : (-7.314656, 112.728194),
    'F3' : (-7.313978, 112.728644),
    'G'  : (-7.312217, 112.729519),
    'UKM': (-7.312817, 112.727778),
    'GSG': (-7.312569, 112.727428),
    'FC1': (-7.315075, 112.726458),
    'FC2': (-7.314503, 112.726722),
}


# CLASS GRAPH

class Graph: #class inisialisasi graph
    def __init__(self, directed=False): #constructor graph tidak berarah "false"
        self.graph    = {} #menyimpan adjacency list graph
        self.directed = directed 

    def add_node(self, node): #penambahan node ke graph
        if node not in self.graph:
            self.graph[node] = {}

    def add_edge(self, u, v, weight=1): #penambahan edge ke graph dengan bobot tertentu
        self.add_node(u); self.add_node(v)
        self.graph[u][v] = weight
        if not self.directed:
            self.graph[v][u] = weight

    def dijkstra_steps(self, start, goal): #algoritma dijkstra dengan langkah-langkah eksplorasi
        # dist: jarak terpendek ke setiap node, node > infinity
        dist = {} 
        for node in self.graph: #merubah seluruh node ke infinity
            dist[node] = float('inf')

        dist[start] = 0 #titik start selalu 0

        #predecessor mencatat asal node ditemukan (jalur)
        pred = {}
        for node in self.graph:
            pred[node] = None #tempat semua node yg ditemuin

        pq      = [(0, start)] #tuple (jarak, node) 
        visited = set() #list final node
        steps   = [] #list rekam setiap langkah (visualisasi)

        while pq: #loop utama use prioprity queue
            d, u = heapq.heappop(pq) #menggunakan heapmin untuk jalur terpendek
            if u in visited:
                continue
            visited.add(u)

            for v, w in self.graph[u].items(): #ketika tetangga belum visited
                if v not in visited:
                    if d + w < dist[v]: #apakah jalur u lebih pendek
                        dist[v] = d + w
                        pred[v] = u #jika iya update
                        heapq.heappush(pq, (dist[v], v)) #masukkan jalur baru ke priority queue

            steps.append({ #rekam semua langkah eksplorasi untuk visualisasi
                'current' : u,
                'dist'    : dict(dist),
                'pred'    : dict(pred),
                'visited' : set(visited),
                'desc'    : f"Langkah {len(steps)+1}: Memproses node [{u}] — {node_graph[u]}",
                'detail'  : (
                    f"Jarak terpendek ke {u} = {dist[u]} m"
                    + (f" (lewat {pred[u]} ({node_graph[pred[u]]}))" if pred[u] else " (titik awal)")
                ),
            })

            #rekontruksi jalur
            if u == goal:
                break

        path, cur = [], goal #kembalikan jalur dari goal ke start menggunakan pred
        while cur:
            path.append(cur)
            cur = pred[cur]
        path = path[::-1] #jalur dihitung kembali goal - start jadi start - goal

        return dist[goal], path, steps


# SPLASH SCREEN

class SplashScreen:
    def __init__(self, root, on_start):
        self.root     = root
        self.on_start = on_start

        self.root.title("Shortest Path UNESA - Dijkstra Algorithm")
        self.root.geometry("860x720")
        self.root.configure(bg=BG_MAIN)
        self.root.resizable(True, True)

        font_name  = "Orbitron"
        font_title = (font_name, 26, "bold")
        font_sub   = (font_name, 12, "bold")
        font_body  = (font_name, 11)

        # ── Top spacer ──
        ctk.CTkFrame(self.root, fg_color=BG_MAIN, height=30).pack()

        # ── Badge header kecil ──
        badge = ctk.CTkFrame(self.root, fg_color=ACCENT_DARK,
                            corner_radius=8)
        badge.pack(padx=60, pady=(0, 6), fill="x")

        ctk.CTkLabel(badge,
                    text="SHORTEST PATH UNESA",
                    font=(font_name, 26, "bold"),
                    text_color=WHITE).pack(pady=(16, 2))

        ctk.CTkLabel(badge,
                    text="Sistem Pencarian Rute Antar Gedung Tercepat",
                    font=(font_name, 12, "bold"),
                    text_color=ACCENT_LIGHT).pack(pady=(0, 4))

        ctk.CTkLabel(badge,
                    text="Menggunakan Algoritma Dijkstra",
                    font=(font_name, 11),
                    text_color=SUCCESS).pack(pady=(0, 14))

        # ── Card info kelompok ──
        card = ctk.CTkFrame(self.root, fg_color=BG_CARD,
                            corner_radius=14,
                            border_width=2, border_color=ACCENT_LIGHT)
        card.pack(padx=80, pady=14, fill="x")

        ctk.CTkLabel(card,
                    text="Mata Kuliah Struktur Data dan Algoritma",
                    font=(font_name, 12, "bold"),
                    text_color=ACCENT_DARK).pack(pady=(18, 2))

        ctk.CTkLabel(card,
                    text="S1 Sains Data  —  2025 A",
                    font=font_body,
                    text_color=TEXT_DARK).pack(pady=(0, 10))

        # Divider
        ctk.CTkFrame(card, fg_color=ACCENT_LIGHT, height=2).pack(fill="x", padx=24)

        ctk.CTkLabel(card,
                    text="Kelompok :",
                    font=(font_name, 11, "bold"),
                    text_color=ACCENT_MAIN).pack(pady=(14, 4))

        anggota = [
            ("257", "Dinda Alifia"),
            ("121", "Maydian Ratu Valencia"),
            ("191", "Syahira Nanda"),
        ]
        for nim, nama in anggota:
            row_frame = ctk.CTkFrame(card, fg_color="transparent")
            row_frame.pack(pady=3)

            ctk.CTkLabel(row_frame,
                        text=f"{nim}",
                        font=(font_name, 11, "bold"),
                        text_color=ACCENT_DARK,
                        width=40).pack(side="left", padx=(10, 4))

            ctk.CTkLabel(row_frame,
                        text="—",
                        font=font_body,
                        text_color=TEXT_DARK).pack(side="left", padx=4)

            ctk.CTkLabel(row_frame,
                        text=nama,
                        font=font_body,
                        text_color=TEXT_DARK).pack(side="left", padx=4)

        ctk.CTkFrame(card, fg_color="transparent", height=14).pack()

        # ── Universitas label ──
        ctk.CTkLabel(self.root,
                    text="Universitas Negeri Surabaya  •  2025/2026",
                    font=(font_name, 9),
                    text_color=TEXT_DARK).pack(pady=(8, 0))

        ctk.CTkFrame(self.root, fg_color=BG_MAIN, height=20).pack()

        # ── Tombol MULAI ──
        ctk.CTkButton(self.root,
                    text="✦  MULAI  ✦",
                    font=(font_name, 14, "bold"),
                    fg_color=ACCENT_MAIN,
                    hover_color=ACCENT_DARK,
                    text_color=WHITE,
                    corner_radius=10,
                    width=220, height=48,
                    command=self.mulai).pack(pady=(4, 0))

        ctk.CTkFrame(self.root, fg_color=BG_MAIN, height=16).pack()

    def mulai(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.on_start(self.root)


# GUI UTAMA

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Shortest Path UNESA - Dijkstra Algorithm")
        self.root.geometry("920x960")
        self.root.configure(bg=BG_MAIN)

        self.font_name = "Orbitron"
        self.mc_header = (self.font_name, 20, "bold")
        self.mc_normal = (self.font_name, 11)
        self.mc_small  = (self.font_name, 10)

        self.g = Graph()
        for node in node_graph: self.g.add_node(node)
        for u, v, w in edge_graph: self.g.add_edge(u, v, w)

        try:
            img = Image.open('image_map.png').resize((35, 35))
            self.custom_icon = ImageTk.PhotoImage(img)
        except:
            self.custom_icon = None

        # State step-by-step
        self.steps        = []
        self.current_step = 0
        self.final_path   = []
        self.total_dist   = 0

        # State peta
        self.current_path  = None
        self.explore_paths = []
        self.markers       = {}

        self.build_gui()
        self.init_map_markers()

    # BUILD GUI
    def build_gui(self):
        # ── Header bar ──
        header_bar = ctk.CTkFrame(self.root, fg_color=ACCENT_DARK,
                                corner_radius=0, height=56)
        header_bar.pack(fill="x")
        header_bar.pack_propagate(False)

        ctk.CTkLabel(header_bar,
                    text="SHORTEST PATH ANTAR GEDUNG UNESA",
                    font=(self.font_name, 18, "bold"),
                    text_color=WHITE).pack(expand=True)

        # ── Peta ──
        content = ctk.CTkFrame(
        self.root,
    fg_color="transparent"
)
        content.pack(
    fill="both",
    expand=True,
    padx=18,
    pady=12
)
        # ── Tabel dist[] ──
        tbl_outer = ctk.CTkFrame(
            self.root,
            fg_color=BG_CARD,
            corner_radius=12,
            border_width=1,
            border_color=ACCENT_LIGHT
        )

        tbl_outer.pack(
            fill="x",
            padx=18,
            pady=(0,12)
        )

        ctk.CTkLabel(tbl_outer,
                    text="  Tabel Jarak Terpendek  dist[ ]",
                    font=(self.font_name, 11, "bold"),
                    text_color=ACCENT_DARK,
                    anchor="w").pack(anchor="w", padx=8, pady=(6, 2))

        tbl_frame = tk.Frame(tbl_outer, bg=BG_CARD)
        tbl_frame.pack(fill="x", padx=8, pady=(0, 8))

        xscroll = ttk.Scrollbar(tbl_frame, orient="horizontal")
        xscroll.pack(side="bottom", fill="x")

        self.dist_table = ttk.Treeview(
    tbl_frame,
    xscrollcommand=xscroll.set,
    height=4
)
        xscroll.config(command=self.dist_table.xview)

        node_keys = list(node_graph.keys())
        self.dist_table['columns'] = node_keys
        self.dist_table['show']    = 'headings'
        for col in node_keys:
            self.dist_table.heading(col, text=col)
            self.dist_table.column(
    col,
    width=85,
    anchor='center',
    minwidth=70
)
        self.dist_table.pack(fill='x')


        left_panel = ctk.CTkFrame(
    content,
    width=340,
    fg_color=BG_CARD,
    corner_radius=15,
    border_width=1,
    border_color=ACCENT_LIGHT
)

        left_panel.pack(
    side="left",
    fill="y",
    expand=True,
    padx=(0,5)
)

        left_panel.pack_propagate(False)

# PANEL KONTROL KIRI

        ctk.CTkLabel(
            left_panel,
            text="KONTROL RUTE",
            font=(self.font_name, 16, "bold"),
            text_color=ACCENT_DARK
        ).pack(pady=(15,10))

        # MASUK
        ctk.CTkLabel(
            left_panel,
            text="Start",
            font=self.mc_small,
            text_color=TEXT_DARK
        ).pack(anchor="w", padx=15)

        self.var_start = tk.StringVar(value="MB")

        cb_start = ttk.Combobox(
            left_panel,
            textvariable=self.var_start,
            values=list(node_graph.keys()),
            state="readonly"
        )
        cb_start.pack(fill="x", padx=15, pady=(0,10))

        # TUJUAN
        ctk.CTkLabel(
            left_panel,
            text="Tujuan",
            font=self.mc_small,
            text_color=TEXT_DARK
        ).pack(anchor="w", padx=15)

        self.var_goal = tk.StringVar(value="G")

        cb_goal = ttk.Combobox(
            left_panel,
            textvariable=self.var_goal,
            values=list(node_graph.keys()),
            state="readonly"
        )
        cb_goal.pack(fill="x", padx=15, pady=(0,15))

        # TOMBOL CARI
        self.btn_cari = ctk.CTkButton(
            left_panel,
            text="🔍 Cari Rute",
            fg_color=ACCENT_MAIN,
            hover_color=ACCENT_DARK,
            command=self.cari_rute
        )
        self.btn_cari.pack(fill="x", padx=15, pady=3)

        # TOMBOL NEXT
        self.btn_next = ctk.CTkButton(
            left_panel,
            text="Next Step",
            fg_color="#fff4cc",
            text_color=TEXT_DARK,
            state="disabled",
            command=self.next_step
        )
        self.btn_next.pack(fill="x", padx=15, pady=3)

        # TOMBOL RESET
        self.btn_reset = ctk.CTkButton(
            left_panel,
            text="Reset",
            fg_color="#ffd6d6",
            text_color="#c0392b",
            command=self.reset
        )
        self.btn_reset.pack(fill="x", padx=15, pady=(3,10))

        # COUNTER LANGKAH
        self.label_langkah = ctk.CTkLabel(
            left_panel,
            text="",
            font=self.mc_small,
            text_color=TEXT_DARK
        )
        self.label_langkah.pack(pady=(0,10))

        right_panel = ctk.CTkFrame(
    content,
    fg_color=BG_CARD,
    corner_radius=15,
    border_width=1,
    border_color=ACCENT_LIGHT
)

        right_panel.pack(
    side="left",
    fill="both",
    expand=True
)

        self.map_widget = tkintermapview.TkinterMapView(
    right_panel,
    corner_radius=10
)

        self.map_widget.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)
        self.map_widget.set_position(-7.314759, 112.726832)
        self.map_widget.set_zoom(17)
        

        # ── Label hasil & detail ──
        hasil_card = ctk.CTkFrame(
    left_panel,
    fg_color="#f7f2ff",
    corner_radius=12,
    border_width=1,
    border_color=ACCENT_LIGHT
)
        hasil_card.pack(fill="x", padx=12, pady=(10,0),ipady=15)

        ctk.CTkLabel(
        hasil_card,
    text="HASIL PENCARIAN",
    font=(self.font_name, 12, "bold"),
    text_color=ACCENT_DARK
).pack(anchor="w", padx=12, pady=(10,5))

        self.label_result = ctk.CTkLabel(
    hasil_card,
    text="",
    font=(self.font_name, 11, "bold"),
    text_color="#2e7d32",
    wraplength=240,
    justify="left"
)
        self.label_result.pack(fill="x", padx=12)

        self.label_detail = ctk.CTkLabel(
    hasil_card,
    text="PILIH GERBANG DAN TUJUAN",
    font=(self.font_name, 9),
    text_color=TEXT_DARK,
    wraplength=240,
    justify="left"
)
        self.label_detail.pack(fill="x", padx=12, pady=(5,12))



        # Style tabel
        style = ttk.Style()
        style.configure("Treeview.Heading",
                        font=(self.font_name, 10, "bold"),
                        background=WHITE,
                        foreground=ACCENT_DARK,
                        relief="flat",
                        padding=4)
        style.map("Treeview.Heading",
                background=[("active", WHITE),
                            ("pressed", WHITE)],
                foreground=[("active", ACCENT_DARK),
                            ("pressed", ACCENT_DARK)],
                relief=[("active", "flat"),
                        ("pressed", "flat")])
        style.configure("Treeview",
                        font=(self.font_name, 10),
                        rowheight=26,
                        background=BG_MAIN,
                        fieldbackground=BG_MAIN)
        style.map("Treeview",
                background=[("selected", ACCENT_LIGHT)])

        self._refresh_table({n: float('inf') for n in node_graph})


    # MAP MARKER
    def init_map_markers(self):
        for code, (lat, lon) in node_pos.items():
            self.markers[code] = self.map_widget.set_marker(
                lat, lon, text=code, icon=self.custom_icon)

    # CARI RUTE
    def cari_rute(self):
        self.reset()
        start = self.var_start.get()
        goal  = self.var_goal.get()

        if start == goal:
            self.label_result.configure(
                text="Titik awal dan tujuan tidak boleh sama!",
                text_color="#c0392b")
            return

        jarak, path, steps = self.g.dijkstra_steps(start, goal)

        if jarak == float('inf'):
            self.label_result.configure(
                text=f" Tidak ada jalur dari {start} ke {goal}!",
                text_color="#c0392b")
            return

        self.steps        = steps
        self.final_path   = path
        self.total_dist   = jarak
        self.current_step = 0

        self.btn_cari.configure(state='disabled')
        self.btn_next.configure(state='normal')

        init_dist = {n: float('inf') for n in node_graph}
        init_dist[start] = 0
        self._refresh_table(init_dist)

        self.label_langkah.configure(text=f"0 / {len(self.steps)}")
        self.label_result.configure(
            text=f"Siap! Klik 'Next Step' untuk mulai eksplorasi dari {node_graph[start]}.",
            text_color=ACCENT_MAIN)
        jalur = " → ".join(
    [node_graph[n] for n in self.final_path]
)

        self.label_detail.configure(
    text=f"JALUR:\n{jalur}"
)

    # NEXT STEP
    def next_step(self):
        if self.current_step >= len(self.steps):
            return

        step = self.steps[self.current_step]
        self.current_step += 1

        node = step['current']
        dist = step['dist']
        pred = step['pred']

        self.markers[node].set_text(f"✅ {node}")

        if pred[node]:
            prev = pred[node]
            path_line = self.map_widget.set_path(
                [node_pos[prev], node_pos[node]],
                color="#5a3d9c", width=3)
            self.explore_paths.append(path_line)

        self.label_langkah.configure(
            text=f"{self.current_step} / {len(self.steps)}")
        self.label_result.configure(
            text=step['desc'], text_color=ACCENT_MAIN)
        self.label_detail.configure(
            text=step['detail'])

        self._refresh_table(dist, step['visited'])

        if self.current_step >= len(self.steps):
            self._show_final()

    # TAMPILKAN HASIL AKHIR
    def _show_final(self):
        for p in self.explore_paths:
            p.delete()
        self.explore_paths = []

        for code in self.markers:
            self.markers[code].set_text(code)

        path_coords = [node_pos[n] for n in self.final_path]
        self.current_path = self.map_widget.set_path(
            path_coords, color="#7c5cbf", width=6)

        self.btn_next.configure(state='disabled')
        self.btn_cari.configure(state='normal')

        self.label_result.configure(
            text=f"✅  JARAK TERPENDEK: {self.total_dist} METER",
            text_color="#2e7d32")
        self.label_detail.configure(
            text=f"JALUR: {' → '.join([node_graph[n] for n in self.final_path])}")

    # REFRESH TABEL dist[]
    def _refresh_table(self, dist, visited=None):
        for row in self.dist_table.get_children():
            self.dist_table.delete(row)

        node_keys = list(node_graph.keys())
        visited = visited or set()
        values = []
        for k in node_keys:
            v = dist.get(k, float('inf'))
            values.append("∞" if v == float('inf') else str(v))

        self.dist_table.insert('', 'end', values=values, tags=('dist',))
        self.dist_table.tag_configure('dist', background=WHITE, foreground=TEXT_DARK)

        style = ttk.Style()
        for k in node_keys:
            if k in visited:
                self.dist_table.heading(k, text=k)
                style.configure(f"Treeview.Heading", background=ACCENT_DARK)
            if k in visited:
                self.dist_table.heading(k, text=f"✓{k}")
            else:
                self.dist_table.heading(k, text=k)

    # RESET
    def reset(self):
        if self.current_path:
            self.current_path.delete()
            self.current_path = None
        for p in self.explore_paths:
            p.delete()
        self.explore_paths = []

        for code in self.markers:
            self.markers[code].set_text(code)

        for k in node_graph.keys():
            self.dist_table.heading(k, text=k)

        self.steps        = []
        self.current_step = 0
        self.final_path   = []
        self.total_dist   = 0

        self.btn_cari.configure(state='normal')
        self.btn_next.configure(state='disabled')
        self.label_langkah.configure(text="")
        self.label_result.configure(text="", text_color=ACCENT_MAIN)
        self.label_detail.configure(text="PILIH GERBANG DAN TUJUAN")
        self._refresh_table({n: float('inf') for n in node_graph})

if __name__ == '__main__':
    root = ctk.CTk()
    SplashScreen(root, GUI)
    root.mainloop() 