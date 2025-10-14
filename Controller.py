from Model import TruyTimKhoBauModel
import time

class TruyTimKhoBauContronller:
    def __init__(self, view, loaiMap):
        self.view = view
        self.model = TruyTimKhoBauModel(self, loaiMap)

    def getMap(self):
        return self.model.getMap()

    def getSoHang(self):
        return self.model.getSoHang()

    def getSoCot(self):
        return self.model.getSoCot()

    def run_algorithm(self, name):
        """Chạy thuật toán và đo thời gian chạy chính xác"""
        start_time = time.perf_counter()
        print("Thuật toán bên trong controller: ", name)

        if "AStarSearch" in name:
            result = self.model.AStarSearch()
        elif "BFS" in name:
            result = self.model.BFS()
        elif "DFS" in name:
            result = self.model.DFS()
        elif "Greedy" in name:
            result = self.model.GreedySearch()
        elif "Simulated Annealing" in name:
            result = self.model.SimulatedAnnealing()
        elif "CSP Backtracking" in name:
            result = self.model.CSP_Backtracking()
        elif "And Or Tree" in name:
            result = self.model.and_or_tree_search()
        elif "MiniMax" in name:
            result = self.model.minimax()
        elif "Genetic Algorithms" in name:
            result = self.model.GeneticAlgorithms()
        elif "PartialObservable Greedy" in name:
            print("Bạn đã vô đây")
            result = self.model.PartialObservable_Greedy()
        elif "ArcConsistency Algorithms" in name:
            result = self.model.ArcConsistencyAlgorithms()
        elif "AlphaBetaPruning" in name:
            result = self.model.AlphaBetaPruning()
        else:
            print("⚠️ Thuật toán không hợp lệ:", name)
            return None, 0.0

        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000

        print(f"⏱ Thời gian chạy {name}: {elapsed_ms:.3f} ms")
        print(f"[DEBUG] Raw time: {end_time - start_time} (seconds)")
        
        return result, elapsed_ms


