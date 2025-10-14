from tkinter import *
from tkinter import messagebox, Toplevel
from Controller import TruyTimKhoBauContronller
from tkinter import ttk
import tkinter.font as tkFont
from PIL import Image, ImageDraw, ImageTk
import math
import pygame
import time
import random
import datetime
import threading

#==============================================================================================
# hiệu ứng màn hình win
class _Firework:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.particles = []
        # tăng số lượng hạt để nhìn hoành tráng hơn
        for _ in range(50):
            ang = random.uniform(0, 2 * math.pi)
            spd = random.uniform(2, 6)  # tốc độ mạnh hơn
            vx, vy = spd * math.cos(ang), spd * math.sin(ang)
            dot = canvas.create_oval(
                x, y, x + 4, y + 4,
                fill=random.choice(["red", "yellow", "orange", "white", "blue", "green", "violet"]),
                outline=""
            )
            # life tăng lên để cháy lâu hơn
            self.particles.append({
                "id": dot,
                "x": x, "y": y,
                "vx": vx, "vy": vy,
                "life": random.randint(50, 80)
            })

    def step(self):
        alive = False
        for p in self.particles[:]:
            p["life"] -= 1
            if p["life"] <= 0:
                self.canvas.delete(p["id"])
                self.particles.remove(p)
                continue
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.1  # trọng lực nhẹ
            self.canvas.coords(p["id"], p["x"], p["y"], p["x"]+4, p["y"]+4)
            alive = True
        return alive
#==============================================================================================

class TruyTimKhoBauView():
    def __init__(self, selected_map="classic"):
        self.selected_map = selected_map
        print(f"🎯 Map được chọn: {self.selected_map}")

        self.cell_size = 40
        self.sound_on = True

        # --- ÂM THANH ---
        pygame.mixer.init()
        self.set_theme()
        # try:
        #     pygame.mixer.music.load("D:/project_nhom_AI/AI_TruyTimKhoBau_2025/sounds/bg_music.mp3")
        #     pygame.mixer.music.play(-1)  # lặp vô hạn
        #     pygame.mixer.music.set_volume(0.5)  # chỉnh âm lượng
        # except Exception as e:
        #     print("Không thể phát nhạc nền:", e)

        self.run_history = []

        self.giaoDien()


    def set_theme(self):
        """Đặt màu sắc, nhạc nền, texture dựa theo bản đồ đã chọn"""
        if self.selected_map == "classic":
            self.bg_color = "#1a1a2e"
            self.grass_color = "#4CAF50"
            self.wall_color = "#8D6E63"
            self.music_path = r"D:/HCMUTE_IT/HK1_2025-2026/Artificial Intelligence/BaoCaoCuoiKy/BaoCaoCK_1/project_nhom_AI/AI_TruyTimKhoBau_2025/sounds/bg_music.mp3"

        elif self.selected_map == "ocean":
            self.bg_color = "#001F3F"
            self.grass_color = "#0097A7"
            self.wall_color = "#006064"
            self.music_path = r"D:/HCMUTE_IT/HK1_2025-2026/Artificial Intelligence/BaoCaoCuoiKy/BaoCaoCK_1/project_nhom_AI/AI_TruyTimKhoBau_2025/sounds/ocean.mp3"  # nhạc sóng biển

        elif self.selected_map == "halloween":
            self.bg_color = "#2E1A47"
            self.grass_color = "#8E24AA"
            self.wall_color = "#BF360C"
            self.music_path = r"D:/HCMUTE_IT/HK1_2025-2026/Artificial Intelligence/BaoCaoCuoiKy/BaoCaoCK_1/project_nhom_AI/AI_TruyTimKhoBau_2025/sounds/halloween.mp3"

        else:
            # fallback
            self.bg_color = "#1a1a2e"
            self.grass_color = "#4CAF50"
            self.wall_color = "#8D6E63"
            self.music_path = r"D:/HCMUTE_IT/HK1_2025-2026/Artificial Intelligence/BaoCaoCuoiKy/BaoCaoCK_1/project_nhom_AI/AI_TruyTimKhoBau_2025/sounds/bg_music.mp3"

        # --- Phát nhạc nền ---
        try:
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
        except Exception as e:
            print("Không thể phát nhạc nền:", e)

#==============================================================================================
# VẼ CÁC ĐỐI TƯỢNG MAP

    def ve_grass(self, size, is_dark=False):
        """Tạo texture cỏ với pattern xen kẽ"""
        #light_green = '#7CB342' if not is_dark else '#689F38'
        #dark_green = '#689F38' if not is_dark else '#558B2F'
        if self.selected_map == "ocean":
            light_green = '#00BCD4' if not is_dark else '#0097A7'
            dark_green = '#00838F' if not is_dark else '#006064'
        elif self.selected_map == "halloween":
            light_green = '#8E24AA' if not is_dark else '#6A1B9A'
            dark_green = '#BF360C' if not is_dark else '#E65100'
        else:
            light_green = '#7CB342' if not is_dark else '#689F38'
            dark_green = '#689F38' if not is_dark else '#558B2F'
        
        img = Image.new('RGB', (size, size), light_green)
        draw = ImageDraw.Draw(img)
        
        # Pattern cỏ
        for i in range(0, size, 6):
            for j in range(0, size, 6):
                if (i + j) % 12 == 0:
                    draw.ellipse([i, j, i+4, j+2], fill=dark_green)
                    draw.ellipse([i+1, j+1, i+5, j+3], fill='#8BC34A')
                elif (i * j) % 15 == 0:
                    draw.ellipse([i, j, i+2, j+4], fill='#9CCC65')
        
        # Texture nhẹ
        for i in range(0, size, 3):
            for j in range(0, size, 3):
                if (i + j) % 9 == 0:
                    draw.rectangle([i, j, i+1, j+1], fill='#AED581')
        
        return ImageTk.PhotoImage(img)

    def ve_wall(self, size):
        """Tạo texture tường gạch"""
        #img = Image.new('RGB', (size, size), '#8D6E63')
        #base = self.wall_color if hasattr(self, "wall_color") else "#8D6E63"
        #img = Image.new('RGB', (size, size), base)
        base = getattr(self, "wall_color", "#8D6E63")
        img = Image.new('RGB', (size, size), base)

        draw = ImageDraw.Draw(img)
        
        brick_h = size // 3
        brick_w = size // 2
        
        for row in range(0, size + brick_h, brick_h):
            offset = brick_w // 2 if (row // brick_h) % 2 else 0
            for col in range(-offset, size + offset, brick_w):
                if col < size and row < size:
                    draw.rectangle([col, row, 
                                  min(col + brick_w - 2, size-1), 
                                  min(row + brick_h - 2, size-1)], 
                                 fill='#A1887F', outline='#6D4C41', width=1)
                    
                    if col + 2 < size and row + 1 < size:
                        draw.rectangle([col + 1, row + 1, 
                                      min(col + brick_w - 3, size-1), row + 2], 
                                     fill='#BCAAA4')
        
        return ImageTk.PhotoImage(img)

    def ve_player(self, size, path=r"D:/HCMUTE_IT/HK1_2025-2026/Artificial Intelligence/BaoCaoCuoiKy/BaoCaoCK_1/project_nhom_AI/AI_TruyTimKhoBau_2025/picture/boy.png"):
        """Load ảnh cậu bé player, tự xóa nền trắng và scale vừa khít ô"""
        from PIL import Image, ImageTk

        try:
            img = Image.open(path).convert("RGBA")

            # --- Tự động loại bỏ nền trắng hoặc nền gần trắng ---
            datas = img.getdata()
            new_data = []
            for item in datas:
                # nếu pixel sáng (trắng hoặc xám nhạt) → làm trong suốt
                if item[0] > 230 and item[1] > 230 and item[2] > 230:
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            img.putdata(new_data)

            # --- Cắt vùng thực để loại bỏ khoảng trống ---
            bbox = img.getbbox()
            if bbox:
                img = img.crop(bbox)

            # --- Resize vừa khít ô ---
            img = img.resize((size, size), Image.Resampling.LANCZOS)

            return ImageTk.PhotoImage(img)

        except Exception as e:
            print("❌ Không thể tải ảnh cậu bé player:", e)
            # fallback nếu lỗi
            fallback = Image.new("RGBA", (size, size), (0, 0, 255, 255))
            draw = ImageDraw.Draw(fallback)
            draw.text((size//3, size//3), "👦", fill="white")
            return ImageTk.PhotoImage(fallback)


    def ve_kho_bau(self, size, path=r"D:/HCMUTE_IT/HK1_2025-2026/Artificial Intelligence/BaoCaoCuoiKy/BaoCaoCK_1/project_nhom_AI/AI_TruyTimKhoBau_2025/picture/treasure.png"):
        """Load hình kho báu từ file và scale vừa khít ô"""
        from PIL import Image, ImageTk

        try:
            img = Image.open(path).convert("RGBA")

            # Xóa nền trắng nếu có
            datas = img.getdata()
            newData = []
            for item in datas:
                if item[0] > 240 and item[1] > 240 and item[2] > 240:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)
            img.putdata(newData)

            # Cắt vùng thực (loại bỏ khoảng trống)
            bbox = img.getbbox()
            if bbox:
                img = img.crop(bbox)

            # Resize vừa khít ô
            img = img.resize((size, size), Image.Resampling.LANCZOS)

            return ImageTk.PhotoImage(img)

        except Exception as e:
            print("❌ Không thể tải ảnh kho báu:", e)
            # Tạo ảnh rỗng để tránh crash
            from PIL import ImageDraw
            fallback = Image.new("RGBA", (size, size), (255, 200, 0, 255))
            draw = ImageDraw.Draw(fallback)
            draw.text((size//3, size//3), "💰", fill="black")
            return ImageTk.PhotoImage(fallback)

    def animate_path(self, path, speed=8):
        """
        Cho cậu bé di chuyển mượt, đúng tâm ô, đè lên đường đi.
        Tự reset khi chạy thuật toán mới.
        """
        if not path or len(path) < 2:
            return

        cell = self.cell_size
        coords = [
            (c * cell + cell / 2, r * cell + cell / 2)
            for (r, c) in path
        ]

        if hasattr(self, "player_image"):
            self.canvas.delete(self.player_image)

        OFFSET_X = 0
        OFFSET_Y = -2

        start_x, start_y = coords[0]
        self.player_image = self.canvas.create_image(
            start_x + OFFSET_X,
            start_y + OFFSET_Y,
            image=self.player_sprite,
            anchor="center"
        )

        def move_step(i=0):
            if i >= len(coords) - 1:
                print("🎯 Cậu bé đã tới kho báu!")
                return

            x1, y1 = coords[i]
            x2, y2 = coords[i + 1]
            dx, dy = x2 - x1, y2 - y1
            dist = (dx**2 + dy**2) ** 0.5
            steps = max(1, int(dist / speed))
            step_dx, step_dy = dx / steps, dy / steps

            def smooth_move(step=0):
                if step <= steps:
                    self.canvas.move(self.player_image, step_dx, step_dy)
                    self.root.after(15, smooth_move, step + 1)
                else:
                    move_step(i + 1)

            smooth_move()

        move_step(0)


#==============================================================================================
# CÁC HÀM XỬ LÝ SỰ KIỆN

    # Xử lý âm thanh - Nút âm thanh
    def toggle_sound(self):
        self.sound_on = not self.sound_on
        if self.sound_on:
            self.btn_sound.config(text="🔊", bg="#4CAF50")
            pygame.mixer.music.play(-1)
        else:
            self.btn_sound.config(text="🔇", bg="#9E9E9E")
            pygame.mixer.music.stop()
            
    # Reset maze, path, status
    def reset(self):
        self.draw_maze(self.original_map)
        self.txt_TextArea.config(state=NORMAL)
        self.txt_TextArea.delete("1.0", END)
        self.txt_TextArea.config(state=DISABLED)
        #
        self.stop_timer()
        self.lbl_TimeValue.config(text="00:00:000")
    
    # Quay laij home - nút home
    def go_home(self):
        """Quay lại màn hình StartScreen"""
        import StartScreen  # import ở đây để tránh circular import
        
        # Đóng cửa sổ hiện tại
        self.root.destroy()

        # Mở lại StartScreen
        start_screen = StartScreen.StartScreen(on_start_callback=self.restart_game)
        start_screen.run()

    # def restart_game(self):
    #     """Callback để chạy lại game từ StartScreen"""
    #     from main import TruyTimKhoBauApp
    #     app = TruyTimKhoBauApp()
    #     app.launch_main_game()

    def restart_game(self):
        """Callback để chạy lại game từ StartScreen"""
        from main import TruyTimKhoBauApp
        app = TruyTimKhoBauApp()
        app.launch()


    def start_timer(self):
        """Khởi động đồng hồ hiển thị song song với đo thời gian thật"""
        self.start_time = time.perf_counter()
        self.timer_running = True

        def update_clock():
            if not self.timer_running:
                return
            elapsed = time.perf_counter() - self.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            milliseconds = int((elapsed * 1000) % 1000)
            self.lbl_TimeValue.config(text=f"{minutes:02d}:{seconds:02d}:{milliseconds:03d}")
            self.root.after(50, update_clock)  # cập nhật mỗi 50ms

        update_clock()

    def stop_timer(self):
        """Dừng đồng hồ"""
        self.timer_running = False

#++++++++++++++++++++++++++++++++
    def giaoDien(self):
        self.root = Tk()
        self.root.title("🏴‍☠️ TREASURE HUNTER - Thám Hiểm Kho Báu")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Gradient background effect - GIỐNG V1
        #self.root.configure(bg="#1a1a2e")
        self.root.configure(bg=self.bg_color)

        
        # Configure grid weights for responsive design - GIỐNG V1
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Custom fonts - GIỐNG V1
        title_font = tkFont.Font(family="Arial Black", size=24, weight="bold")
        header_font = tkFont.Font(family="Arial", size=14, weight="bold")
        text_font = tkFont.Font(family="Arial", size=11)

        # Header frame spanning both columns - GIỐNG V1
        self.frm_Header = Frame(self.root, bg="#16213e", height=80)
        self.frm_Header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10,5))
        self.frm_Header.grid_propagate(False)
        
        # Title with icons - GIỐNG V1
        self.lbl_Title = Label(
            self.frm_Header, 
            text="🏴‍☠️ TREASURE HUNTER 💎",
            font=title_font,
            fg="#ffd700",
            bg="#16213e"
        )
        self.lbl_Title.pack(expand=True)

        # Header buttons frame (top-right)
        self.frm_HeaderButtons = Frame(self.frm_Header, bg="#16213e")
        self.frm_HeaderButtons.place(relx=1.0, rely=0.5, anchor="e")

        # Nút Home
        self.btn_home = Button(
            self.frm_HeaderButtons,
            text="🏠",
            font=("Arial", 16),
            fg="white",
            bg="#1abc9c",
            activebackground="#16a085",
            width=3,
            height=1,
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.go_home  # bạn tạo hàm này
        )
        self.btn_home.pack(side="right", padx=5)

        # Nút Sound
        self.btn_sound = Button(
            self.frm_HeaderButtons,
            text="🔊",
            font=("Arial", 16),
            fg="white",
            bg="#4CAF50",
            activebackground="#388E3C",
            width=3,
            height=1,
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.toggle_sound
        )
        self.btn_sound.pack(side="right", padx=5)

        # Nút Reset
        self.btn_reset = Button(
            self.frm_HeaderButtons,
            text="🔄",
            font=("Arial", 16),
            fg="white",
            bg="#FF9800",
            activebackground="#FB8C00",
            width=3,
            height=1,
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.reset
        )
        self.btn_reset.pack(side="right", padx=5)


        # Get controller and map data
        controller = TruyTimKhoBauContronller(self, self.selected_map)
        arr_Map = controller.getMap()
        self.soHang = controller.getSoHang()
        self.soCot = controller.getSoCot()
        
        # Create textures - TỪSION V2
        self.grass_light = self.ve_grass(self.cell_size, False)
        self.grass_dark = self.ve_grass(self.cell_size, True)
        self.wall_texture = self.ve_wall(self.cell_size)
        #self.player_sprite = self.ve_player(self.cell_size)
        self.player_sprite = self.ve_player(self.cell_size, "D:/HCMUTE_IT/HK1_2025-2026/Artificial Intelligence/BaoCaoCuoiKy/BaoCaoCK_1/project_nhom_AI/AI_TruyTimKhoBau_2025/picture/boy.png")
        #self.treasure_sprite = self.ve_kho_bau(self.cell_size)
        self.treasure_sprite = self.ve_kho_bau(self.cell_size, "D:/HCMUTE_IT/HK1_2025-2026/Artificial Intelligence/BaoCaoCuoiKy/BaoCaoCK_1/project_nhom_AI/AI_TruyTimKhoBau_2025/picture/treasure.png")


        # Main game area frame - GIỐNG V1 NHƯNG CHỨA CANVAS
        self.frm_VungDat = Frame(self.root, bg="#0f3460", bd=3, relief="raised")
        self.frm_VungDat.grid(row=1, column=0, sticky="nsew", padx=(10,5), pady=5)
        
        # Configure frame to be expandable
        self.frm_VungDat.grid_rowconfigure(0, weight=1)
        self.frm_VungDat.grid_columnconfigure(0, weight=1)
        
        # Canvas thay cho grid buttons - FULL SIZE
        self.canvas = Canvas(
            self.frm_VungDat,
            #bg='#4CAF50',
            bg=self.grass_color,  # thay màu nền theo thêm
            highlightthickness=0,
            bd=0
        )
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Bind resize event để canvas tự động scale
        self.canvas.bind('<Configure>', self.on_canvas_resize)

        # Draw initial maze - TỪ VERSION V2
        self.draw_maze(arr_Map)

        # Right panel container - GIỐNG V1
        self.frm_RightPanel = Frame(self.root, bg="#1a1a2e")
        self.frm_RightPanel.grid(row=1, column=1, sticky="nsew", padx=(5,10), pady=5)
        self.frm_RightPanel.grid_rowconfigure(1, weight=1)

        # Control panel - GIỐNG V1
        self.frm_ThongTin = Frame(
            self.frm_RightPanel, 
            bg="#16213e", 
            bd=3, 
            relief="raised"
        )
        self.frm_ThongTin.grid(row=0, column=0, sticky="ew", pady=(0,5))
        self.frm_ThongTin.grid_columnconfigure(0, weight=1)

        # Control panel header - GIỐNG V1
        self.lbl_ThongTin = Label(
            self.frm_ThongTin, 
            text="⚙️ ĐIỀU KHIỂN",
            font=header_font, 
            fg="#ffd700",
            bg="#16213e"
        )
        self.lbl_ThongTin.grid(row=0, column=0, pady=10, sticky="ew")

        # Algorithm selection - GIỐNG V1
        algo_frame = Frame(self.frm_ThongTin, bg="#16213e")
        algo_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=5)
        algo_frame.grid_columnconfigure(1, weight=1)

        self.lbl_ThuatToan = Label(
            algo_frame, 
            text="🧠 Thuật toán:",
            font=text_font, 
            fg="#e94560",
            bg="#16213e"
        )
        self.lbl_ThuatToan.grid(row=0, column=0, sticky="w")

        # Style for combobox - GIỐNG V1
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            'Custom.TCombobox',
            fieldbackground='#0f3460',
            background='#16213e',
            foreground='white',
            arrowcolor='#ffd700'
        )

        self.cbb_ThuatToan = ttk.Combobox(
            algo_frame,
            values=["🏃 Greedy Search", "AStarSearch", "🌲 DFS Search", "BFS Search", "Simulated Annealing", "CSP Backtracking", "And Or Tree", 
                    "MiniMax", "Genetic Algorithms", "PartialObservable Greedy", "ArcConsistency Algorithms", "AlphaBetaPruning"],
            font=text_font,
            state="readonly",
            style='Custom.TCombobox'
        )
        self.cbb_ThuatToan.current(0)
        self.cbb_ThuatToan.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)

        
        # Position info - GIỐNG V1
        pos_frame = Frame(self.frm_ThongTin, bg="#16213e")
        pos_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=10)

        self.lbl_VTBatDau = Label(
            pos_frame,
            text="🚀 Điểm bắt đầu: (0,0)",
            font=text_font,
            fg="#4fc3f7",
            bg="#16213e"
        )
        self.lbl_VTBatDau.pack(anchor="w", pady=2)

        self.lbl_VTKhoBau = Label(
            pos_frame,
            text=f"💰 Kho báu: ({self.soHang-1},{self.soCot-1})",
            font=text_font,
            fg="#4fc3f7",
            bg="#16213e"
        )
        self.lbl_VTKhoBau.pack(anchor="w", pady=2)

        # Start button - GIỐNG V1
        self.btn_BatDau = Button(
            self.frm_ThongTin,
            text="🎮 BẮT ĐẦU PHIÊU LƯU!",
            font=tkFont.Font(family="Arial", size=12, weight="bold"),
            fg="white",
            bg="#e94560",
            activebackground="#ff6b7a",
            activeforeground="white",
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.runAlgorithm
        )
        self.btn_BatDau.grid(row=3, column=0, padx=15, pady=15, sticky="ew")
        
        # Add hover effect - GIỐNG V1
        def on_enter(e):
            self.btn_BatDau.configure(bg="#ff6b7a")
        def on_leave(e):
            self.btn_BatDau.configure(bg="#e94560")
        
        self.btn_BatDau.bind("<Enter>", on_enter)
        self.btn_BatDau.bind("<Leave>", on_leave)

        # Status panel - GIỐNG V1
        self.frm_TrangThai = Frame(
            self.frm_RightPanel, 
            bg="#16213e", 
            bd=3, 
            relief="raised"
        )
        self.frm_TrangThai.grid(row=1, column=0, sticky="nsew")
        self.frm_TrangThai.grid_columnconfigure(0, weight=1)
        self.frm_TrangThai.grid_rowconfigure(1, weight=1)


        # --- Header của khung TRẠNG THÁI + Đồng hồ ---
        header_frame = Frame(self.frm_TrangThai, bg="#16213e")
        header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        header_frame.grid_columnconfigure(0, weight=1)

        # Tiêu đề bên trái
        self.lbl_TrangThai = Label(
            header_frame,
            text="📊 TRẠNG THÁI",
            font=header_font,
            fg="#ffd700",
            bg="#16213e"
        )
        self.lbl_TrangThai.pack(side="left", anchor="w")

        # Đồng hồ bên phải
        self.lbl_TimeValue = Label(
            header_frame,
            text="00:00",
            font=("Consolas", 11, "bold"),
            fg="#ffeb3b",
            bg="#16213e"
        )
        self.lbl_TimeValue.pack(side="right", padx=(5, 0))

        self.lbl_TimeTitle = Label(
            header_frame,
            text="⏱ Thời gian:",
            font=("Arial", 11, "bold"),
            fg="#ffd700",
            bg="#16213e"
        )
        self.lbl_TimeTitle.pack(side="right", padx=(0, 5))

        # Text area with scrollbar - GIỐNG V1
        text_frame = Frame(self.frm_TrangThai, bg="#16213e")
        text_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0,15))
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_rowconfigure(0, weight=1)

        self.txt_TextArea = Text(
            text_frame,
            wrap=WORD,
            bg="#0f3460",
            fg="#ffffff",
            font=text_font,
            bd=0,
            relief="flat",
            insertbackground="#ffd700"
        )
        self.txt_TextArea.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = Scrollbar(text_frame, bg="#16213e", troughcolor="#0f3460")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.txt_TextArea.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.txt_TextArea.yview)

        # Welcome message - GIỐNG V1
        welcome_text = """🎯 Chào mừng đến với Treasure Hunter!

🗺️ Nhiệm vụ: Tìm đường đến kho báu
🚧 Tránh các bức tường 
🏃 Chọn thuật toán và bắt đầu!

Chúc bạn may mắn! 🍀"""
        
        self.txt_TextArea.insert("1.0", welcome_text)
        self.txt_TextArea.config(state=DISABLED)

        self.controller = controller
        self.original_map = [row[:] for row in arr_Map]
        self.path_objects = []

                # --- Nút nổi góc phải dưới ---
        self.frm_FloatingButtons = Frame(self.root, bg="#1a1a2e")
        self.frm_FloatingButtons.place(relx=0.97, rely=0.93, anchor="se")

        # Nút "Lịch sử"
        self.btn_history = Button(
            self.frm_FloatingButtons,
            text="📜 Lịch sử",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#8e44ad",
            activebackground="#9b59b6",
            activeforeground="white",
            width=10,
            height=1,
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.show_history_window
        )
        self.btn_history.pack(pady=(0, 8))

        # Nút "So sánh"
        self.btn_compare = Button(
            self.frm_FloatingButtons,
            text="⚖️ So sánh",
            font=("Arial", 11, "bold"),
            fg="white",
            bg="#16a085",
            activebackground="#1abc9c",
            activeforeground="white",
            width=10,
            height=1,
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self.compare_algorithms
        )
        self.btn_compare.pack()

        
        self.root.mainloop()

    # ================================
    # 📜 HIỂN THỊ CỬA SỔ LỊCH SỬ
    # ================================
    def show_history_window(self):
        if not self.run_history:
            messagebox.showinfo("Lịch sử", "Chưa có lần chạy nào được ghi nhận!")  # ✅ sửa dòng này
            return

        win = Toplevel(self.root)  # ✅ sửa dòng này (bỏ Tk.Toplevel)
        win.title("📜 Lịch sử chạy thuật toán")
        win.geometry("500x300")
        win.config(bg="#2C3E50")

        lbl = Label(win, text="🧠 LỊCH SỬ CHẠY THUẬT TOÁN", font=("Arial", 14, "bold"),
                    fg="#F1C40F", bg="#2C3E50")
        lbl.pack(pady=10)

        tree = ttk.Treeview(win, columns=("algo", "time", "path", "when"), show="headings")
        tree.heading("algo", text="Thuật toán")
        tree.heading("time", text="Thời gian chạy")
        tree.heading("path", text="Độ dài đường đi")
        tree.heading("when", text="Thời điểm")
        tree.column("algo", width=180)
        tree.column("time", width=100, anchor="center")
        tree.column("path", width= 100)
        tree.column("when", width=180)

        for entry in self.run_history:
            tree.insert(
                "", "end",
                values=(
                    entry.get("thuật toán", ""),
                    entry.get("thời gian chạy", ""),
                    entry.get("độ dài đường đi", 0),
                    entry.get("thời điểm", "")
                )
            )

        tree.pack(fill="both", expand=True, padx=10, pady=10)


    def compare_algorithms(self):
        """Chạy tất cả các thuật toán và hiển thị biểu đồ so sánh"""
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        from tkinter import Toplevel, Label, messagebox

        # Danh sách thuật toán muốn so sánh
        algorithms = [
            "BFS", "DFS", "Greedy", "AStarSearch",
            "Simulated Annealing", "CSP Backtracking",
            "And Or Tree", "MiniMax",
            "PartialObservable Greedy", "ArcConsistency Algorithms",
            "AlphaBetaPruning"
        ]

        results = []

        # Chạy lần lượt từng thuật toán
        for algo in algorithms:
            try:
                path, elapsed_ms = self.controller.run_algorithm(algo)
                path_length = int(len(path)) if path else 0
                results.append({
                    "thuật toán": algo,
                    "thời gian chạy": round(elapsed_ms, 2),
                    "độ dài đường đi": path_length
                })
                print(f"✅ {algo}: {elapsed_ms:.2f} ms, path = {path_length}")
            except Exception as e:
                print(f"⚠️ Lỗi khi chạy {algo}: {e}")

        if not results:
            messagebox.showwarning("⚠️", "Không có thuật toán nào chạy thành công!")
            return

        # Tạo cửa sổ hiển thị kết quả
        win = Toplevel(self.root)
        win.title("⚖️ So sánh hiệu suất các thuật toán")
        win.geometry("900x550")
        win.config(bg="#2C3E50")

        Label(
            win,
            text="📊 SO SÁNH HIỆU SUẤT CÁC THUẬT TOÁN",
            font=("Arial", 15, "bold"),
            fg="#F1C40F",
            bg="#2C3E50"
        ).pack(pady=10)

        # Chuẩn bị dữ liệu biểu đồ
        algos = [r["thuật toán"] for r in results]
        times = [r["thời gian chạy"] for r in results]
        lengths = [r["độ dài đường đi"] for r in results]

        # Vẽ biểu đồ
        fig, ax1 = plt.subplots(figsize=(9, 4))
        x = range(len(algos))
        width = 0.35

        bars1 = ax1.bar(
            [i - width / 2 for i in x],
            times,
            width,
            label="⏱ Thời gian (ms)",
            color="#1abc9c"
        )
        bars2 = ax1.bar(
            [i + width / 2 for i in x],
            lengths,
            width,
            label="📏 Độ dài đường đi",
            color="#e67e22"
        )

        # Thêm nhãn & định dạng
        ax1.set_title("So sánh thời gian chạy và độ dài đường đi", fontsize=13, fontweight="bold")
        ax1.set_xlabel("Thuật toán")
        ax1.set_xticks(list(x))
        ax1.set_xticklabels(algos, rotation=30, ha="right")
        ax1.legend()
        ax1.grid(True, linestyle="--", alpha=0.5)

        # --- hiển thị số trên đầu cột ---
        for bar in bars1:  # cột thời gian
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2, height + 2,
                    f"{height:.3f}", ha="center", va="bottom", fontsize=8, color="#16a085")

        for bar in bars2:  # cột độ dài đường đi
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2, height + 1,
                    f"{int(height)}", ha="center", va="bottom", fontsize=8, color="#d35400")

        # Hiển thị biểu đồ trong cửa sổ Tkinter
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()

    def on_canvas_resize(self, event):
        """Handle canvas resize để tự động scale maze"""
        if hasattr(self, 'original_map'):
            # Tính toán cell size mới dựa trên kích thước canvas
            canvas_width = event.width - 20  # Trừ padding
            canvas_height = event.height - 20
            
            # Tính cell size tối ưu
            cell_w = canvas_width // self.soCot
            cell_h = canvas_height // self.soHang
            new_cell_size = min(cell_w, cell_h, 60)  # Max 60px
            
            if new_cell_size != self.cell_size and new_cell_size > 20:
                self.cell_size = new_cell_size
                # Recreate textures với size mới
                self.grass_light = self.ve_grass(self.cell_size, False)
                self.grass_dark = self.ve_grass(self.cell_size, True)
                self.wall_texture = self.ve_wall(self.cell_size)
                self.player_sprite = self.ve_player(self.cell_size)
                self.treasure_sprite = self.ve_kho_bau(self.cell_size)
                
                # Redraw maze
                self.draw_maze(self.original_map)

    def draw_maze(self, arr_map):
        """Vẽ maze với Canvas và textures đẹp - FULL SIZE"""
        self.canvas.delete("all")
        
        # Lấy kích thước canvas hiện tại
        self.canvas.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            # Canvas chưa được render, dùng default
            canvas_width = 600
            canvas_height = 400
        
        # Tính toán để maze nằm giữa canvas
        total_maze_width = self.soCot * self.cell_size
        total_maze_height = self.soHang * self.cell_size
        
        start_x = max(10, (canvas_width - total_maze_width) // 2)
        start_y = max(10, (canvas_height - total_maze_height) // 2)
        
        # Draw checkerboard pattern
        for i in range(self.soHang):
            for j in range(self.soCot):
                x = start_x + j * self.cell_size
                y = start_y + i * self.cell_size
                
                # Checkerboard pattern
                is_dark_square = (i + j) % 2 == 0


                
                if arr_map[i][j] == 0:  # Empty path
                    grass_texture = self.grass_dark if is_dark_square else self.grass_light
                    self.canvas.create_image(x, y, image=grass_texture, anchor="nw")
                
                elif arr_map[i][j] == 1:  # Player start
                    grass_texture = self.grass_dark if is_dark_square else self.grass_light
                    self.canvas.create_image(x, y, image=grass_texture, anchor="nw")
                    self.canvas.create_image(x, y, image=self.player_sprite, anchor="nw")
                
                elif arr_map[i][j] == 2:  # Wall
                    self.canvas.create_image(x, y, image=self.wall_texture, anchor="nw")
                    # 3D shadow effect
                    shadow_offset = 3
                    self.canvas.create_rectangle(
                        x + self.cell_size - shadow_offset, y + shadow_offset, 
                        x + self.cell_size, y + self.cell_size,
                        fill='#424242', outline='', stipple='gray25'
                    )
                
                elif arr_map[i][j] == 5:  # Treasure
                    grass_texture = self.grass_dark if is_dark_square else self.grass_light
                    self.canvas.create_image(x, y, image=grass_texture, anchor="nw")
                    self.canvas.create_image(x, y, image=self.treasure_sprite, anchor="nw")

        # Draw grid lines với position mới
        self.draw_grid(start_x, start_y)

    def draw_grid(self, start_x=10, start_y=10):
        """Vẽ lưới nhẹ với position tùy chỉnh"""
        for i in range(self.soHang + 1):
            y = start_y + i * self.cell_size
            self.canvas.create_line(
                start_x, y, start_x + self.soCot * self.cell_size, y, 
                fill='#2E7D32', width=1, stipple='gray12'
            )
        
        for j in range(self.soCot + 1):
            x = start_x + j * self.cell_size
            self.canvas.create_line(
                x, start_y, x, start_y + self.soHang * self.cell_size, 
                fill='#2E7D32', width=1, stipple='gray12'
            )



    def draw_path_step(self, i, j):
        """Vẽ một bước đường đi (không hiển thị số) và trả về tâm ô để nối tiếp."""
        # Tính lại start position
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        total_maze_width = self.soCot * self.cell_size
        total_maze_height = self.soHang * self.cell_size

        start_x = max(10, (canvas_width - total_maze_width) // 2)
        start_y = max(10, (canvas_height - total_maze_height) // 2)

        x = start_x + j * self.cell_size
        y = start_y + i * self.cell_size
        center_x = x + self.cell_size // 2
        center_y = y + self.cell_size // 2

        # Vẽ marker (oval nhỏ) — nếu muốn chỉ đường không cần marker, có thể bỏ block này
        path_obj = self.canvas.create_oval(
            center_x - max(6, self.cell_size//8),
            center_y - max(6, self.cell_size//8),
            center_x + max(6, self.cell_size//8),
            center_y + max(6, self.cell_size//8),
            fill="#42A5F5", outline="#1976D2", width=2
        )

        # Lưu object (nếu bạn muốn xóa sau này)
        self.path_objects.append(path_obj)

        # Trả về tâm để runAlgorithm có thể nối line từ điểm trước tới điểm này
        return (center_x, center_y)

# đồng dạng format
    def runAlgorithm(self):
        """Chạy thuật toán được chọn, đo thời gian thực tế và hiển thị kết quả"""
        # 🧹 Xóa đường đi cũ
        for obj in self.path_objects:
            self.canvas.delete(obj)
        self.path_objects.clear()
        self.draw_maze(self.original_map)

        algo_name = self.cbb_ThuatToan.get()
        if not algo_name:
            messagebox.showwarning("Chú ý", "Vui lòng chọn thuật toán!")
            return

        self.txt_TextArea.config(state=NORMAL)
        self.txt_TextArea.delete("1.0", END)
        self.txt_TextArea.insert("end", f"🚀 Bắt đầu chạy {algo_name}...\n\n")
        self.txt_TextArea.config(state=DISABLED)
        self.root.update()


        start_dt = datetime.datetime.now()

# 🕒 Bắt đầu đếm và chạy thuật toán
        self.start_timer()
        start_time = time.perf_counter()

        try:
            print("Thuật toán đã chọn: ", algo_name)
            path, elapsed_ms = self.controller.run_algorithm(algo_name)
                        
            if path:
                self.animate_path(path, speed=8)
        finally:
            self.stop_timer()
            end_time = time.perf_counter()
        formatted_time = f"{elapsed_ms:.3f} ms"
        self.lbl_TimeValue.config(text=formatted_time)



        # ✅ Lưu lịch sử với format thống nhất
        path_length = len(path) if path else 0
        self.run_history.append({
            "thuật toán": algo_name,
            "thời gian chạy": f"{elapsed_ms:.3f} ms",
            "độ dài đường đi": len(path) if path else 0,
            "thời điểm": start_dt.strftime("%H:%M:%S %d-%m-%Y")
        })


        # 🔍 Hiển thị kết quả thuật toán
        if not path:
            self.txt_TextArea.config(state=NORMAL)
            self.txt_TextArea.insert("end", "❌ Không tìm thấy đường đi!\n")
            self.txt_TextArea.config(state=DISABLED)
            return

        self.txt_TextArea.config(state=NORMAL)
        self.txt_TextArea.insert("end", f"✅ Đã tìm thấy đường đi! ({len(path)} bước)\n")
        self.txt_TextArea.insert("end", "🎬 Đang hiển thị đường đi...\n\n")
        self.txt_TextArea.config(state=DISABLED)
        self.root.update()

        # 🌀 Animation hiển thị đường đi
        last_center = None
        for step, (i, j) in enumerate(path[1:-1], 1):
            center = self.draw_path_step(i, j)
            if last_center:
                line = self.canvas.create_line(
                    last_center[0], last_center[1],
                    center[0], center[1],
                    width=max(3, self.cell_size // 10),
                    smooth=True, splinesteps=12, fill="#42A5F5"
                )
                self.path_objects.append(line)
            last_center = center

            self.txt_TextArea.config(state=NORMAL)
            self.txt_TextArea.insert("end", f"Bước {step}: ({i}, {j})\n")
            self.txt_TextArea.see("end")
            self.txt_TextArea.config(state=DISABLED)
            self.root.update()
            self.root.after(250)

        # 🏁 Kết thúc - Hiệu ứng chiến thắng
        self.txt_TextArea.config(state=NORMAL)
        self.txt_TextArea.insert("end", "\n🎉 ĐÃ TÌM THẤY KHO BÁU! 💎✨\n")
        self.txt_TextArea.insert("end", "🏆 Chúc mừng bạn!\n")
        self.txt_TextArea.config(state=DISABLED)
        self.txt_TextArea.see("end")

        self.add_victory_effect()
        self.show_win_overlay()



    def add_victory_effect(self):
        """Hiệu ứng chiến thắng với position tùy chỉnh"""
        # Tính lại start position cho victory effect
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        total_maze_width = self.soCot * self.cell_size
        total_maze_height = self.soHang * self.cell_size
        
        start_x = max(10, (canvas_width - total_maze_width) // 2)
        start_y = max(10, (canvas_height - total_maze_height) // 2)
        
        # Find treasure position
        for i in range(self.soHang):
            for j in range(self.soCot):
                if self.original_map[i][j] == 5:
                    x = start_x + j * self.cell_size + self.cell_size // 2
                    y = start_y + i * self.cell_size + self.cell_size // 2
                    
                    # Create sparkles
                    sparkles = []
                    for k in range(8):
                        angle = k * 45
                        radius = self.cell_size // 2 + 10
                        dx = radius * math.cos(math.radians(angle))
                        dy = radius * math.sin(math.radians(angle))
                        
                        sparkle = self.canvas.create_text(
                            x + dx, y + dy, text="✨",
                            font=("Arial", max(12, self.cell_size//3)), fill="#f1c40f"
                        )
                        sparkles.append(sparkle)
                    
                    # Remove sparkles after 2 seconds
                    def remove_sparkles():
                        for sparkle in sparkles:
                            self.canvas.delete(sparkle)
                    
                    self.root.after(2000, remove_sparkles)
                    break



    def show_win_overlay(self):
        """Hiển thị dòng YOU WIN trong suốt ngay trên canvas + nhạc win"""
        import pygame

        # --- TẠM DỪNG NHẠC NỀN ---
        try:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
        except:
            pass

        # --- PHÁT NHẠC WIN ---
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(r"D:/HCMUTE_IT/HK1_2025-2026/Artificial Intelligence/BaoCaoCuoiKy/BaoCaoCK_1/project_nhom_AI/AI_TruyTimKhoBau_2025/sounds/win.wav")
            pygame.mixer.music.play()
        except Exception as e:
            print("Không phát được nhạc chiến thắng:", e)

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        # nền mờ trong suốt
        overlay = self.canvas.create_rectangle(0, 0, w, h, fill="black", stipple="gray50", outline="")

        # chữ YOU WIN
        text_id = self.canvas.create_text(
            w / 2, h / 2,
            text="YOU WIN",
            fill="white",
            font=("Arial Black", 64, "bold")
        )

        # tạo nhiều pháo hoa đẹp hơn
        fireworks = []
        for _ in range(20):
            x = random.randint(int(w * 0.1), int(w * 0.9))
            y = random.randint(int(h * 0.2), int(h * 0.7))
            fireworks.append(_Firework(self.canvas, x, y))

        # animation loop
        def animate():
            alive = False
            for fw in fireworks[:]:
                if not fw.step():
                    fireworks.remove(fw)
                else:
                    alive = True
            if alive:
                self.root.after(50, animate)

        animate()

        # --- CLICK ĐỂ THOÁT ---
        def remove_overlay(event=None):
            self.canvas.delete(overlay)
            self.canvas.delete(text_id)
            for fw in fireworks:
                for p in fw.particles:
                    self.canvas.delete(p["id"])
            self.canvas.unbind("<Button-1>")

            # DỪNG NHẠC WIN
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()

            # PHÁT LẠI NHẠC NỀN
            try:
                pygame.mixer.music.load(r"D:/HCMUTE_IT/HK1_2025-2026/Artificial Intelligence/BaoCaoCuoiKy/BaoCaoCK_1/project_nhom_AI/AI_TruyTimKhoBau_2025/sounds/bg_music.mp3")
                pygame.mixer.music.play(-1)
            except Exception as e:
                print("Không phát được nhạc nền:", e)

        self.canvas.bind("<Button-1>", remove_overlay)


if __name__ == "__main__":
    view = TruyTimKhoBauView()