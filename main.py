# from StartScreen import StartScreen

# class TruyTimKhoBauApp:
#     def __init__(self):
#         self.game_running = False
    
#     def start_demo(self):
#         start_screen = StartScreen(self.launch_main_game)
#         start_screen.run()
    
#     def launch_main_game(self):
#         self.game_running = True
        
#         try:
#             from View import TruyTimKhoBauView
#             main_game = TruyTimKhoBauView()
#         except Exception as e:
#             print(f"Lỗi khởi động game: {e}")
#             import traceback
#             traceback.print_exc()
    
#     def run(self):
#         self.start_demo()

# if __name__ == "__main__":
#     app = TruyTimKhoBauApp()
#     app.run()


# main.py
# from StartScreen import StartScreen
# from MapSelectionScreen import MapSelectionScreen
# from View import TruyTimKhoBauView


# class TruyTimKhoBauApp:
#     def __init__(self):
#         pass

#     def launch(self):
#         """Bắt đầu bằng màn hình Start"""
#         start_screen = StartScreen(on_start_callback=self.show_map_selection)
#         start_screen.run()

#     def show_map_selection(self):
#         """Hiện màn hình chọn map sau khi bấm 'Bắt đầu'"""
#         map_screen = MapSelectionScreen(on_map_selected_callback=self.launch_game)
#         map_screen.run()

#     def launch_game(self, map_name):
#         """Sau khi chọn map → vào game chính"""
#         print(f"✅ Đang khởi động game với map: {map_name}")
#         view = TruyTimKhoBauView()
#         # Nếu bạn muốn truyền map_name cho view thì có thể mở rộng View sau này


# if __name__ == "__main__":
#     app = TruyTimKhoBauApp()
#     app.launch()


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
