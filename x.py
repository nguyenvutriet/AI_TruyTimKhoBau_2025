import tkinter as tk
from tkinter import Canvas, Frame, Label

class GameKhoBauUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Treasure Hunter")
        self.root.geometry("950x820")
        self.root.configure(bg="#A0522D")  

        # Bien game
        self.kich_thuoc = 12
        self.o_size = 55

        # Vi tri
        self.nguoi_choi = (1, 1)       
        self.kho_bau = (8, 9)     
        self.ke_thu = [(1, 2), (3, 3), (3, 8)]
        self.tuong = self.lay_vi_tri_tuong()

        self.tao_giao_dien()

    def lay_vi_tri_tuong(self):
        tuong = set()
        # Tuong vien
        for i in range(self.kich_thuoc):
            tuong.add((i, 0))
            tuong.add((i, self.kich_thuoc - 1))
            tuong.add((0, i))
            tuong.add((self.kich_thuoc - 1, i))

        # Tuong ben trong
        tuong_trong = [
            (5, 2),
            (8, 3), (10, 3),
            (5, 4), (8, 5), (10, 5),
            (2, 6), (8, 6), (10, 6),
            (2, 7), (5, 8), (8, 8), (10, 8),
            (2, 9), (10, 10)
        ]
        for w in tuong_trong:
            tuong.add(w)

        return tuong

    def tao_giao_dien(self):
        # Tieu de
        frame_tieu_de = Frame(self.root, bg="#A0522D", height=100)
        frame_tieu_de.pack(fill="x", pady=(20, 5))  # giảm khoảng cách dưới

        # Dau lau ben trai
        dau_trai = Label(frame_tieu_de, text="☠", font=("Arial", 28, "bold"),
                           fg="white", bg="#4A2C2A", width=3, height=1)
        dau_trai.pack(side="left", padx=20)

        label_tieu_de = Label(frame_tieu_de, text="TREASURE HUNTER",
                            font=("Arial", 36, "bold"),
                            fg="#FFD700", bg="#A0522D")
        label_tieu_de.pack(side="left", expand=True)

        # Dau lau ben phai
        dau_phai = Label(frame_tieu_de, text="☠", font=("Arial", 28, "bold"),
                            fg="white", bg="#4A2C2A", width=3, height=1)
        dau_phai.pack(side="right", padx=20)

        # Bang choi
        frame_chinh = Frame(self.root, bg="#3B2A1C", bd=8, relief="ridge")
        frame_chinh.pack(pady=10)  

        rong = self.kich_thuoc * self.o_size
        cao = self.kich_thuoc * self.o_size
        self.canvas = Canvas(frame_chinh, width=rong, height=cao,
                             bg="#2F1B14", highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)

        self.ve_luoi()

    def ve_luoi(self):
        self.canvas.delete("all")
        for hang in range(self.kich_thuoc):
            for cot in range(self.kich_thuoc):
                x1 = cot * self.o_size
                y1 = hang * self.o_size
                x2 = x1 + self.o_size
                y2 = y1 + self.o_size

                mau, ky_hieu = self.lay_thuoc_tinh_o(cot, hang)

                # O vuong
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=mau, outline="#3B2A1C", width=1
                )

                if ky_hieu:
                    cx, cy = x1 + self.o_size // 2, y1 + self.o_size // 2
                    size_chu = 20 if ky_hieu == "🧱" else 28
                    self.canvas.create_text(
                        cx, cy, text=ky_hieu, font=("Arial", size_chu, "bold"),
                        fill="white" if ky_hieu == "☠" else "black"
                    )

    def lay_thuoc_tinh_o(self, cot, hang):
        if (cot, hang) == self.nguoi_choi:
            return "#4169E1", "☠"     # Nguoi choi
        elif (cot, hang) == self.kho_bau:
            return "#FFD700", "💰"    # Kho bau
        elif (cot, hang) in self.ke_thu:
            return "#8B2635", "👹"    # Ke thu
        elif (cot, hang) in self.tuong:
            return "#CD853F", "🧱"    # Tuong
        else:
            return "#2F1B14", None    # Trong

    def chay(self):
        self.root.mainloop()


if __name__ == "__main__":
    ui = GameKhoBauUI()
    ui.chay()
