import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import os


class StartScreen:
    def __init__(self, on_start_callback):
        self.root = tk.Tk()
        self.root.title("Treasure Hunter")
        self.root.geometry("1152x768")
        self.root.resizable(False, False)

        self.on_start_callback = on_start_callback

        self.background("D:/HCMUTE_IT/HK1_2025-2026/Artificial Intelligence/BaoCaoCuoiKy/BaoCaoCK_1/project_nhom_AI/AI_TruyTimKhoBau_2025/picture/demo.png")
        self._create_play_button()

    def background(self, image_path):
        if os.path.exists(image_path):
            bg_image = Image.open(image_path).resize((1152, 768), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = Label(self.root, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            self.root.configure(bg="#2F4F4F")

    def _create_play_button(self):
        self.play_button = Button(
            self.root,
            text="🚀 BẮT ĐẦU",
            font=("Arial Black", 20, "bold"),
            fg="white",
            bg="#FF6B35",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            padx=40,
            pady=15,
            command=self.start_game,
        )
        self.play_button.place(relx=0.5, rely=0.9, anchor="center")

        # Hover effects
        self.play_button.bind("<Enter>", self._on_hover)
        self.play_button.bind("<Leave>", self._on_leave)

    def _on_hover(self, _):
        self.play_button.config(bg="#FF8555", relief="raised", bd=3)

    def _on_leave(self, _):
        self.play_button.config(bg="#FF6B35", relief="flat", bd=0)

    def start_game(self):
        self.root.destroy()
        if self.on_start_callback:
            self.on_start_callback()

    def run(self):
        self.root.mainloop()


# Test riêng StartScreen
if __name__ == "__main__":
    def test_callback():
        pass
    
    StartScreen(test_callback).run()
