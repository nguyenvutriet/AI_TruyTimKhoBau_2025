import tkinter as tk
from tkinter import Label, Button, Frame, Canvas
from PIL import Image, ImageTk
import os


class MapSelectionScreen:
    def __init__(self, on_map_selected_callback):
        self.root = tk.Tk()
        self.root.title("Chọn Map - Treasure Hunter")
        self.root.geometry("1152x768")
        self.root.resizable(False, False)
        
        self.on_map_selected_callback = on_map_selected_callback
        self.selected_map = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        canvas = Canvas(self.root, width=1152, height=768, highlightthickness=0, bg="#1a1a2e")
        canvas.pack(fill="both", expand=True)
        
        # Create gradient background
        for i in range(768):
            color_value = int(26 + (i / 768) * 30)
            color = f"#{color_value:02x}{color_value:02x}{color_value + 20:02x}"
            canvas.create_line(0, i, 1152, i, fill=color)
        
        main_frame = Frame(canvas, bg="#1a1a2e", bd=0)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title with glow effect
        title = Label(
            main_frame,
            text="🗺️ CHỌN BẢN ĐỒ PHIÊU LƯU",
            font=("Arial Black", 42, "bold"),
            fg="#FFD700",
            bg="#1a1a2e"
        )
        title.pack(pady=30)
        
        subtitle = Label(
            main_frame,
            text="Chọn thế giới bạn muốn khám phá",
            font=("Arial", 16),
            fg="#FFFFFF",
            bg="#1a1a2e"
        )
        subtitle.pack(pady=(0, 40))
        
        # Map selection frame
        maps_frame = Frame(main_frame, bg="#1a1a2e")
        maps_frame.pack(pady=20)
        
        maps = [
            {
                "name": "classic",
                "display_name": "🏰 CLASSIC",
                "icon": "🗺️",
                "description": "Bản đồ truyền thống\n⚔️ Phù hợp mọi cấp độ\n🏆 Thử thách cân bằng",
                "color": "#2E7D32",
                "hover_color": "#43A047",
                "accent": "#FFD700",
                "decorations": ["🌳", "🏰", "⚔️", "🗡️"]
            },
            {
                "name": "ocean",
                "display_name": "🌊 ĐẠI DƯƠNG",
                "icon": "⚓",
                "description": "Khám phá đại dương sâu\n🐟 Bí ẩn dưới đáy biển\n💎 Kho báu hải tặc",
                "color": "#0277BD",
                "hover_color": "#0288D1",
                "accent": "#00E5FF",
                "decorations": ["🌊", "🐠", "🐙", "⚓"]
            },
            {
                "name": "halloween",
                "display_name": "🎃 HALLOWEEN",
                "icon": "🦇",
                "description": "Rừng ma quái đêm Halloween\n👻 Thử thách kinh dị\n🕷️ Dành cho người dũng cảm",
                "color": "#D84315",
                "hover_color": "#E64A19",
                "accent": "#FF6F00",
                "decorations": ["🎃", "🦇", "👻", "🕷️"]
            }
        ]
        
        for i, map_info in enumerate(maps):
            self._create_map_card(maps_frame, map_info, i)
    
    def _create_map_card(self, parent, map_info, index):
        card_container = Frame(parent, bg="#1a1a2e", bd=0)
        card_container.grid(row=0, column=index, padx=20, pady=20)
        
        # Decorative top icons
        deco_frame = Frame(card_container, bg="#1a1a2e")
        deco_frame.pack()
        
        for deco in map_info["decorations"]:
            Label(
                deco_frame,
                text=deco,
                font=("Arial", 20),
                bg="#1a1a2e",
                fg=map_info["accent"]
            ).pack(side="left", padx=5)
        
        # Main card
        card = Frame(
            card_container,
            bg=map_info["color"],
            relief="raised",
            bd=0,
            highlightbackground=map_info["accent"],
            highlightthickness=3
        )
        card.pack(pady=10)
        
        # Large icon at top
        icon_label = Label(
            card,
            text=map_info["icon"],
            font=("Arial", 60),
            fg="white",
            bg=map_info["color"],
            pady=20
        )
        icon_label.pack()
        
        # Map name with bold styling
        name_label = Label(
            card,
            text=map_info["display_name"],
            font=("Arial Black", 24, "bold"),
            fg="white",
            bg=map_info["color"],
            pady=10
        )
        name_label.pack()
        
        # Separator line
        separator = Frame(card, bg=map_info["accent"], height=3, width=200)
        separator.pack(pady=10)
        
        # Description with emoji
        desc_label = Label(
            card,
            text=map_info["description"],
            font=("Arial", 12),
            fg="white",
            bg=map_info["color"],
            pady=20,
            justify="left",
            padx=20
        )
        desc_label.pack()
        
        # Select button with glow effect
        select_btn = Button(
            card,
            text="⚡ CHỌN MAP NÀY",
            font=("Arial Black", 14, "bold"),
            fg="white",
            bg="#2D3436",
            activeforeground="white",
            activebackground="#636E72",
            cursor="hand2",
            padx=40,
            pady=15,
            bd=0,
            relief="raised",
            command=lambda: self.select_map(map_info["name"])
        )
        select_btn.pack(pady=25, padx=20)
        
        def on_card_enter(e):
            card.config(bg=map_info["hover_color"], highlightthickness=5)
            icon_label.config(bg=map_info["hover_color"])
            name_label.config(bg=map_info["hover_color"])
            desc_label.config(bg=map_info["hover_color"])
        
        def on_card_leave(e):
            card.config(bg=map_info["color"], highlightthickness=3)
            icon_label.config(bg=map_info["color"])
            name_label.config(bg=map_info["color"])
            desc_label.config(bg=map_info["color"])
        
        def on_btn_enter(e):
            select_btn.config(bg="#636E72", relief="raised", bd=3)
        
        def on_btn_leave(e):
            select_btn.config(bg="#2D3436", relief="raised", bd=0)
        
        # Bind hover events
        card.bind("<Enter>", on_card_enter)
        card.bind("<Leave>", on_card_leave)
        icon_label.bind("<Enter>", on_card_enter)
        icon_label.bind("<Leave>", on_card_leave)
        name_label.bind("<Enter>", on_card_enter)
        name_label.bind("<Leave>", on_card_leave)
        desc_label.bind("<Enter>", on_card_enter)
        desc_label.bind("<Leave>", on_card_leave)
        select_btn.bind("<Enter>", on_btn_enter)
        select_btn.bind("<Leave>", on_btn_leave)
    
    def select_map(self, map_name):
        self.selected_map = map_name
        self.root.destroy()
        if self.on_map_selected_callback:
            self.on_map_selected_callback(map_name)
    
    def run(self):
        self.root.mainloop()


# Test
if __name__ == "__main__":
    def test_callback(map_name):
        print(f"Selected map: {map_name}")
    
    MapSelectionScreen(test_callback).run()
