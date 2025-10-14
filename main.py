
# main.py
from StartScreen import StartScreen
from MapSelectionScreen import MapSelectionScreen
from View import TruyTimKhoBauView


class TruyTimKhoBauApp:
    def __init__(self):
        pass

    def launch(self):
        StartScreen(self.show_map_selection).run()

    def show_map_selection(self):
        MapSelectionScreen(self.launch_game).run()

    def launch_game(self, map_name):
        """Khi người dùng chọn xong map, mở game chính với theme tương ứng"""
        print(f"🗺️ Đã chọn map: {map_name}")
        TruyTimKhoBauView(selected_map=map_name)  # truyền map_name vào game


if __name__ == "__main__":
    app = TruyTimKhoBauApp()
    app.launch()
