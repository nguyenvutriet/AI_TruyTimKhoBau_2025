import math
from queue import PriorityQueue
import copy

class TruyTimKhoBauModel():
    def __init__(self, controller):
        self.controller = controller
        self.arr_Map = [
            [1, 0, 0, 2, 2, 2, 2, 0, 2, 2],
            [0, 2, 0, 0, 0, 0, 0, 0, 2, 0],
            [0, 2, 0, 2, 2, 2, 0, 2, 0, 0],
            [0, 0, 0, 2, 0, 2, 0, 0, 2, 0],
            [0, 2, 2, 2, 0, 2, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 0, 2, 0, 0, 0],
            [0, 2, 0, 2, 0, 0, 0, 0, 2, 0],
            [0, 0, 0, 0, 0, 2, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 2, 0, 0, 0],
            [0, 2, 0, 2, 0, 0, 0, 0, 2, 5]
        ]
        self.soHang = len(self.arr_Map)
        self.soCot = len(self.arr_Map[0])


    def getMap(self):
        return self.arr_Map
    def getSoHang(self):
        return self.soHang
    def getSoCot(self):
        return self.soCot
    
    def kiemTraTrangThaiDich(self, arr):
        for row in range(self.soHang):
            for col in range(self.soCot):
                if arr[row][col] == 6:
                    return True
        return False

    def PathCost(self, x, y, x_old, y_old):
        chiPhi = math.sqrt((x - x_old)**2+(y - y_old)**2)
        return round(chiPhi,1)
    
    def Herurictics(self, x, y):
        chiPhi = math.sqrt((self.soCot - x)**2+(self.soHang - y)**2)
        return round(chiPhi,1)
    
    def AStarSearch(self):
        pass
        
    def GreedySearch(self):
        queue = PriorityQueue()
        thuTu = 0
        arr = copy.deepcopy(self.arr_Map)
        x_old = 0
        y_old = 0
        chiPhi = self.Herurictics(0,0)
        queue.put((chiPhi, thuTu, arr))
        while queue.qsize() != 0:
            cP, tt, state = queue.get()

            if self.kiemTraTrangThaiDich(state):
                return state
            
            



