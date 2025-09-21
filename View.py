from tkinter import *
from Controller import TruyTimKhoBauContronller
from tkinter import ttk

class TruyTimKhoBaoView():
    btns = [[0 for _ in range(20)] for _ in range(20)]  # ma trận 20x20 để lưu button

    def __init__(self):
        self.giaoDien()

    def giaoDien(self):
        self.root = Tk()
        self.root.title("Truy tìm kho báu")
        self.root.geometry("775x490")
        #self.root.resizable(False, False)

        # Frame vùng đất
        self.frm_VungDat = Frame(self.root, bg="#A0522D", height=700)
        self.frm_VungDat.grid(row = 0, column= 0, rowspan=2)

        # Vùng đất tìm kho báu
        controller = TruyTimKhoBauContronller(self)
        arr_Map = controller.getMap()
        soHang = controller.getSoHang()
        soCot = controller.getSoCot()
        self.VungDat(arr_Map, soHang, soCot)

        # Frame thông tin
        self.frm_ThongTin = Frame(self.root, bg="#A0522D", height=250, width=300)
        self.frm_ThongTin.grid(row = 0, column= 1)
        self.frm_ThongTin.grid_propagate(False)
        self.lbl_ThongTin = Label(self.frm_ThongTin, text="Thông Tin", font=("Times New Roman", 16,"bold"), fg="white",bg="#A0522D")
        self.lbl_ThongTin.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.lbl_ThuatToan = Label(self.frm_ThongTin, text="Chọn thuật toán: ", font=("Times New Roman", 16, "normal"), fg="white",bg="#A0522D")
        self.lbl_ThuatToan.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.cbb_ThuaToan = ttk.Combobox(self.frm_ThongTin, values=["Greedy Search", "A* Search"], font=("Times New Roman", 16, "normal"), state="readonly", width=8)
        self.cbb_ThuaToan.current(0) # Mặc đinh hiển thị là Greedy Search
        self.cbb_ThuaToan.grid(row=1, column=1, padx=5, pady=5)
        self.lbl_VTBatDau = Label(self.frm_ThongTin, text="Vị trí bắt đầu: (0,0)", font=("Times New Roman", 16, "normal"), fg="white",bg="#A0522D")
        self.lbl_VTBatDau.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.lbl_VTKhoBau = Label(self.frm_ThongTin, text="Vị trí kho báu: ("+str(soHang)+","+str(soCot)+")", font=("Times New Roman", 16, "normal"), fg="white",bg="#A0522D")
        self.lbl_VTKhoBau.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        self.btn_BatDau = Button(self.frm_ThongTin, text="Bắt Đầu", font=("Times New Roman", 16, "normal"), fg="white", bg="blue")
        self.btn_BatDau.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="e")


        # Frame trang thái
        self.frm_TrangThai = Frame(self.root, bg="#A0522D", height=240, width=300)
        self.frm_TrangThai.grid(row = 1, column= 1)
        self.frm_TrangThai.grid_propagate(False)
        self.lbl_TrangThai = Label(self.frm_TrangThai, text="Trạng Thái", font=("Times New Roman", 16,"bold"), fg="white",bg="#A0522D")
        self.lbl_TrangThai.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.scrollbar = Scrollbar(self.frm_TrangThai)
        #self.scrollbar.pack(side=RIGHT, fill=Y)
        self.txt_TextArea = Text(self.frm_TrangThai, wrap=WORD, yscrollcommand=self.scrollbar.set, width=35, height=10)
        self.txt_TextArea.grid(row=1, column=0, padx=5, pady=5, sticky="nesw")

        self.root.mainloop()

    def VungDat(self, arr, soHang, soCot):
        for i in range(soHang):
            for j in range(soCot):
                if arr[i][j] == 0:
                    text = ""
                    color = "#54E77E"   # nền đất
                elif arr[i][j] == 1:
                    text = "😄"         # người thám hiểm
                    color = "#54E77E"
                elif arr[i][j] == 2:
                    text = "🧱"         # tường
                    color = "#C1440E"   # đổi nền cho dễ nhìn (nâu gạch)
                elif arr[i][j] == 5:
                    text = "💰"         # kho báu
                    color = "#FFD700"   # vàng
                self.btns[i][j] = Label(
                    self.frm_VungDat,
                    text=text,
                    bg=color,
                    font=("Segoe UI Symbol", 24, "bold"),  # font to hơn
                    relief="flat",
                    borderwidth=1
                )
                self.btns[i][j].grid(row=i, column=j, sticky="nsew")


if __name__ == "__main__":
    view = TruyTimKhoBaoView()
