import tkinter as tk
from tkinter import ttk
import tkintermapview
import heapq
from PIL import Image, ImageTk
from ctypes import windll

try:
    windll.gdi32.AddFontResourceExW("Minecraft.ttf", 0x10, 0)
except Exception as e:
    print(f"Gagal memuat file font: {e}")

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

edge_graph = [
    ('MB', 'A',   30), ('MB', 'A2',  50), ('MD', 'G',   65),
    ('A',  'A2',  30), ('A',  'B',  120),
    ('A2', 'A3', 100), ('A2', 'A4', 115),
    ('A3', 'A4', 100),
    ('A4', 'B',  160), ('A4', 'B2',  70), ('A4', 'FC1',115),
    ('B',  'B2', 250), ('B',  'D',   95), ('B',  'FC1',130), ('B', 'FC2',175),
    ('B2', 'C1', 105), ('B2', 'F2', 135), ('B2', 'FC1', 60), ('B2','FC2',110),
    ('C1', 'F2',  80), ('C1', 'F3', 150), ('C1', 'FC1',120), ('C1','FC2', 80),
    ('D',  'E',  300), ('D',  'FC1', 80), ('D',  'FC2',100),
    ('E',  'GSG',120), ('E',  'UKM',150),
    ('F',  'F3',  80), ('F',  'G',  130), ('F',  'UKM',105),
    ('F2', 'F3',  90),
    ('G',  'UKM',180),
    ('UKM','GSG', 80),
    ('FC1','FC2', 60),
]

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

# ============================================================
# CLASS GRAPH
# ============================================================

class Graph:
    def __init__(self, directed=False):
        self.graph    = {}
        self.directed = directed

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = {}

    def add_edge(self, u, v, weight=1):
        self.add_node(u); self.add_node(v)
        self.graph[u][v] = weight
        if not self.directed:
            self.graph[v][u] = weight

    def dijkstra(self, start, goal):
        dist = {}
        for node in self.graph:
            dist[node] = float('inf')

        dist[start] = 0

        pred        = {node: None  for node in self.graph}
        pq          = [(0, start)]
        visited     = set()
        visit_order = []

        while pq:
            d, u = heapq.heappop(pq)
            if u in visited: continue
            visited.add(u)
            visit_order.append((u, d))
            if u == goal: break
            for v, w in self.graph[u].items():
                if v not in visited and d + w < dist[v]:
                    dist[v] = d + w
                    pred[v] = u
                    heapq.heappush(pq, (dist[v], v))

        path, cur = [], goal
        while cur:
            path.append(cur)
            cur = pred[cur]

        return dist[goal], path[::-1], visit_order


# ============================================================
# SPLASH SCREEN
# ============================================================

class SplashScreen:
    def __init__(self, root, on_start):
        self.root     = root
        self.on_start = on_start

        self.root.title("E-Parking UNESA")
        self.root.geometry("900x750")
        self.root.configure(bg="#fffbd3")
        self.root.resizable(True, True)

        font_name  = "Minecraft"
        font_title = (font_name, 28, "bold")
        font_sub   = (font_name, 13, "bold")
        font_body  = (font_name, 11)
        font_btn   = (font_name, 14, "bold")

        # ── Spacer atas ──
        tk.Frame(self.root, bg="#fffbd3", height=60).pack()

        # ── Judul ──
        tk.Label(self.root,
                text="🅿  E-PARKING UNESA",
                font=font_title, bg="#fffbd3", fg="#426bae").pack()

        tk.Frame(self.root, bg="#426bae", height=3, width=500).pack(pady=12)

        # ── Subjudul ──
        tk.Label(self.root,
                text="Sistem Pencarian Rute Parkir Tercepat",
                font=font_sub, bg="#fffbd3", fg="#2e7d32").pack()

        tk.Label(self.root,
                text="Menggunakan Algoritma Dijkstra",
                font=(font_name, 11), bg="#fffbd3", fg="#555").pack(pady=(4, 0))

        tk.Frame(self.root, bg="#fffbd3", height=40).pack()

        # ── Card info ──
        card = tk.Frame(self.root, bg="#fff8c5",
                        highlightbackground="#426bae",
                        highlightthickness=2)
        card.pack(padx=120, pady=10, fill="x")

        tk.Label(card, text="Struktur Data dan Algoritma",
                font=(font_name, 12, "bold"),
                bg="#fff8c5", fg="#426bae").pack(pady=(18, 4))

        tk.Label(card, text="S1 Sains Data — FMIPA UNESA",
                font=font_body, bg="#fff8c5", fg="#555").pack(pady=(0, 14))

        tk.Frame(card, bg="#ddd", height=1).pack(fill="x", padx=20)

        tk.Label(card, text="Kelompok :",
                font=(font_name, 11, "bold"),
                bg="#fff8c5", fg="#426bae").pack(pady=(14, 6))

        members = [
            ("257", "Dinda Alifia"),
            ("121", "Maydian Ratu Valencia"),
            ("191", "Syahira Nanda"),
        ]
        for nim, nama in members:
            row = tk.Frame(card, bg="#fff8c5")
            row.pack(pady=3)
            tk.Label(row, text=f"{nim}  —  {nama}",
                    font=font_body, bg="#fff8c5", fg="#333").pack()

        tk.Frame(card, bg="#fffbd3", height=18).pack()

        tk.Frame(self.root, bg="#fffbd3", height=40).pack()

        # ── Tombol MULAI ──
        tk.Button(self.root,
                text="▶   MULAI",
                font=font_btn,
                bg="#426bae", fg="white",
                activebackground="#2e5a8e",
                activeforeground="white",
                relief="flat",
                padx=40, pady=12,
                cursor="hand2",
                command=self.mulai).pack()

        tk.Frame(self.root, bg="#fffbd3", height=20).pack()

        tk.Label(self.root,
                text="Universitas Negeri Surabaya  •  2025/2026",
                font=(font_name, 9),
                bg="#fffbd3", fg="#aaa").pack()

    def mulai(self):
        # Hapus semua widget splash lalu tampilkan GUI utama
        for widget in self.root.winfo_children():
            widget.destroy()
        self.on_start(self.root)


# ============================================================
# GUI UTAMA
# ============================================================

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Rute Tercepat Parkir UNESA')
        self.root.geometry('900x750')
        self.root.configure(bg="#fffbd3")

        self.font_name = "Minecraft"
        self.mc_header = (self.font_name, 24, "bold")
        self.mc_normal = (self.font_name, 12)

        self.g = Graph()
        for node in node_graph: self.g.add_node(node)
        for u, v, w in edge_graph: self.g.add_edge(u, v, w)

        try:
            img = Image.open('image_map.png').resize((35, 35))
            self.custom_icon = ImageTk.PhotoImage(img)
        except:
            self.custom_icon = None

        self.current_path  = None
        self.explore_paths = []
        self.markers       = {}
        self.build_gui()
        self.init_map_markers()

    def build_gui(self):
        tk.Label(self.root, text='RUTE TERCEPAT PARKIR',
                font=self.mc_header, bg='#fffbd3', fg='#426bae').pack(pady=20)

        self.map_widget = tkintermapview.TkinterMapView(
            self.root, width=850, height=450, corner_radius=10)
        self.map_widget.pack(padx=20, pady=10)
        self.map_widget.set_position(-7.314759, 112.726832)
        self.map_widget.set_zoom(17)

        ctrl = tk.Frame(self.root, bg="#fffbd3")
        ctrl.pack(pady=10)

        tk.Label(ctrl, text="MASUK:", font=self.mc_normal,
                bg='#fffbd3', fg="#426bae").grid(row=0, column=0, padx=5)
        self.var_start = tk.StringVar(value='MB')
        ttk.Combobox(ctrl, textvariable=self.var_start,
                    values=list(node_graph.keys()),
                    state='readonly', width=10).grid(row=0, column=1, padx=5)

        tk.Label(ctrl, text="TUJUAN:", font=self.mc_normal,
                bg='#fffbd3', fg='#426bae').grid(row=0, column=2, padx=5)
        self.var_goal = tk.StringVar(value='G')
        ttk.Combobox(ctrl, textvariable=self.var_goal,
                    values=list(node_graph.keys()),
                    state='readonly', width=10).grid(row=0, column=3, padx=5)

        self.btn_cari = tk.Button(ctrl, text='CARI RUTE',
                                font=self.mc_normal, bg='#a6e3a1',
                                command=self.start_animation)
        self.btn_cari.grid(row=0, column=4, padx=10)

        tk.Button(ctrl, text='RESET', font=self.mc_normal,
                bg='#f38ba8', command=self.reset).grid(row=0, column=5, padx=5)

        self.label_result = tk.Label(self.root, text="",
                                    font=self.mc_normal, bg='#fffbd3', fg='#2e7d32')
        self.label_result.pack(pady=5)

        self.label_detail = tk.Label(self.root,
                                    text="PILIH GERBANG DAN TUJUAN",
                                    font=self.mc_normal, bg='#fffbd3', fg='#426bae')
        self.label_detail.pack()

    def init_map_markers(self):
        for code, (lat, lon) in node_pos.items():
            self.markers[code] = self.map_widget.set_marker(
                lat, lon, text=code, icon=self.custom_icon)

    def start_animation(self):
        self.reset()
        start = self.var_start.get()
        goal  = self.var_goal.get()

        if start == goal:
            self.label_result.config(
                text="Titik awal dan tujuan tidak boleh sama!", fg='#f38ba8')
            return

        self.btn_cari.config(state='disabled')
        jarak, rute, visit_order = self.g.dijkstra(start, goal)

        if jarak == float('inf'):
            self.label_result.config(
                text=f"Tidak ada jalur dari {start} ke {goal}!", fg='#f38ba8')
            self.btn_cari.config(state='normal')
            return

        self.animate_dijkstra(visit_order, rute, jarak, 0)

    def animate_dijkstra(self, visit_order, final_rute, total_dist, index):
        if index < len(visit_order):
            node, jarak_node = visit_order[index]
            self.markers[node].set_text(f"✅ {node}")

            if index > 0:
                prev_node = visit_order[index - 1][0]
                path = self.map_widget.set_path(
                    [node_pos[prev_node], node_pos[node]],
                    color="#0c0800", width=3)
                self.explore_paths.append(path)

            self.label_result.config(
                text=f"Dijkstra: Mengunjungi {node_graph[node]} | Jarak sementara: {jarak_node}m",
                fg="#426bae")
            self.root.after(1000, self.animate_dijkstra,
                            visit_order, final_rute, total_dist, index + 1)
        else:
            self.label_result.config(
                text="Eksplorasi selesai. Menampilkan rute terpendek...")
            self.root.after(1000, self.show_result, final_rute, total_dist)

    def show_result(self, rute, jarak):
        for p in self.explore_paths: p.delete()
        self.explore_paths = []
        for code, marker in self.markers.items(): marker.set_text(code)

        path_coords = [node_pos[n] for n in rute]
        self.current_path = self.map_widget.set_path(
            path_coords, color="#f38ba8", width=6)

        self.label_result.config(
            text=f'JARAK TERPENDEK: {jarak} METER', fg='#2e7d32')
        self.label_detail.config(
            text=f"JALUR: {' -> '.join([node_graph[n] for n in rute])}")
        self.btn_cari.config(state='normal')

    def reset(self):
        if self.current_path: self.current_path.delete()
        for p in self.explore_paths: p.delete()
        self.explore_paths = []
        for code, marker in self.markers.items(): marker.set_text(code)
        self.label_result.config(text="", fg='#2e7d32')
        self.label_detail.config(text="PILIH GERBANG DAN TUJUAN")
        self.btn_cari.config(state='normal')


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    root = tk.Tk()
    SplashScreen(root, GUI)
    root.mainloop()