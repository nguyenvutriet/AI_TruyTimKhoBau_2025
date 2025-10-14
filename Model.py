from collections import deque
import math
from queue import PriorityQueue
import copy
import random


class TruyTimKhoBauModel():
    def __init__(self, controller, loaiMap):
        self.controller = controller
        self.theloai = loaiMap

        print("Thể loại map: ", self.theloai)

        if self.theloai == "classic":
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
        elif self.theloai == "ocean":
            self.arr_Map = [
                [1, 0, 0, 0, 0, 2, 0, 0, 0, 0],
                [0, 2, 0, 0, 0, 0, 2, 0, 2, 0],
                [0, 2, 2, 2, 2, 0, 0, 0, 2, 0],
                [0, 0, 0, 0, 2, 0, 2, 0, 0, 0],
                [0, 2, 2, 0, 0, 0, 2, 2, 0, 0],
                [0, 0, 0, 0, 2, 0, 0, 0, 2, 0],
                [2, 0, 0, 0, 0, 0, 2, 0, 0, 0],
                [0, 0, 2, 2, 0, 0, 0, 2, 0, 0],
                [0, 2, 0, 0, 0, 2, 0, 0, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 5]
            ]

        elif self.theloai == "halloween":
            self.arr_Map = [
                [1, 0, 2, 0, 2, 2, 2, 0, 2, 2],
                [0, 0, 0, 0, 0, 0, 2, 0, 0, 2],
                [2, 2, 2, 2, 0, 2, 2, 2, 0, 2],
                [0, 0, 0, 0, 0, 2, 0, 0, 0, 2],
                [0, 2, 2, 2, 0, 0, 0, 2, 0, 0],
                [0, 2, 0, 0, 0, 2, 0, 0, 2, 5],
                [0, 2, 0, 2, 0, 2, 2, 0, 2, 0],
                [0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
                [2, 2, 0, 2, 0, 2, 2, 2, 0, 0],
                [0, 0, 0, 0, 0, 2, 0, 0, 2, 0]
            ]

        self.soHang = len(self.arr_Map)
        self.soCot = len(self.arr_Map[0])

    # MỘT SỐ HÀM PHỤ
    #1. Lấy map
    def getMap(self):
        return self.arr_Map
    
    #2. Lấy số hàng
    def getSoHang(self):
        return self.soHang
    
    #3. Lấy số cột
    def getSoCot(self):
        return self.soCot

    #4. Tính chi phí path cost
    def PathCost(self, x, y, x_old, y_old):
        chiPhi = math.sqrt((x - x_old)**2+(y - y_old)**2)
        return round(chiPhi,1)
    
    #4. ước lượng chi phí 
    def Herurictics(self, x, y):
        chiPhi = math.sqrt((self.soCot - x)**2+(self.soHang - y)**2)
        return round(chiPhi,1)
    
    #5. Lấy ra vị trí ban đầu
    def getStart(self):
        # Tìm vị trí bắt đầu (giá trị = 1)
        for i in range(self.soHang):
            for j in range(self.soCot):
                if self.arr_Map[i][j] == 1:
                    return (i, j)
        return None

    #6. Lấy ra vị trí kho báu
    def getGoal(self):
        # Tìm vị trí kho báu (giá trị = 5)
        for i in range(self.soHang):
            for j in range(self.soCot):
                if self.arr_Map[i][j] == 5:
                    return (i, j)
        return None

    # Nhóm 1: TÌM KIẾM KHÔNG CÓ THÔNG TIN
    # 1. Depth First Search
    def DFS(self):
        start = self.getStart()
        goal = self.getGoal()
        if not start or not goal:
            return None

        stack = [(start, [start])]
        visited = set()

        step = 0  # đếm bước duyệt

        while stack:
            (x, y), path = stack.pop()
            step += 1
            # kiểm tra vị trí có phải kho báu không
            if (x, y) == goal:
                return path
            # đanh dấu đã thăm
            if (x, y) in visited:
                continue
            visited.add((x, y))
            # di chuyển 4 hướng
            for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:  # 4 hướng
                nx, ny = x+dx, y+dy
                if 0 <= nx < self.soHang and 0 <= ny < self.soCot:
                    if self.arr_Map[nx][ny] != 2 and (nx, ny) not in visited:
                        stack.append(((nx, ny), path+[(nx, ny)]))
        return None

    # 2. Breadth First Search
    def BFS(self):
        start = self.getStart()
        goal = self.getGoal()
        if not start or not goal:
            return None
        
        queue = deque([(start, [start])])
        visited = set()

        while queue:
            (x,y) , path = queue.popleft()
            # kiểm tra vị trí có phải kho báu không
            if (x,y) == goal:
                return path
            # đanh dấu đã thăm
            if (x,y) in visited:
                continue
            visited.add((x,y))
             # di chuyển 4 hướng
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x+dx, y+dy
                if 0<=nx<self.soHang and 0 <= ny < self.soCot:
                    if self.arr_Map[nx][ny] != 2 and (nx, ny) not in visited:
                        queue.append(((nx, ny), path + [(nx, ny)]))
        return None

    # Nhóm 2: TÌM KIẾM KHÔNG CÓ THÔNG TIN
    # 1. A* Search
    def AStarSearch(self):
        start = self.getStart()
        goal = self.getGoal()
        if not start or not goal:
            return None
        queue = PriorityQueue()
        queue.put((0 + self.Herurictics(*start), 0, start, [start]))  
        visited = set()
        while not queue.empty():
            f, g, (x, y), path = queue.get()
            # kiểm tra vị trí có phải kho báu không
            if (x, y) == goal:
                return path  # trả về danh sách tọa độ
            # đanh dấu đã thăm
            if (x, y) in visited:
                continue
            visited.add((x, y))
            # 4 hướng
            for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < self.soHang and 0 <= ny < self.soCot:
                    if self.arr_Map[nx][ny] != 2 and (nx, ny) not in visited: 
                        gn = g + self.PathCost(nx, ny, x, y)
                        hn = self.Herurictics(nx, ny)
                        fn = gn + hn
                        queue.put((fn, gn, (nx, ny), path+[(nx, ny)]))
        return None
 
    # 2. Greedy Search
    def GreedySearch(self):
        start = self.getStart()
        goal = self.getGoal()
        if not start or not goal:
            return None

        queue = PriorityQueue()
        queue.put((self.Herurictics(*start), start, [start]))  # (heuristic, vị trí hiện tại, đường đi)

        visited = set()
        while not queue.empty():
            h, (x, y), path = queue.get()
            # kiểm tra vị trí có phải kho báu không
            if (x, y) == goal:
                return path  # trả về danh sách tọa độ
            # đanh dấu đã thăm
            if (x, y) in visited:
                continue
            visited.add((x, y))
            # 4 hướng
            for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < self.soHang and 0 <= ny < self.soCot:
                    if self.arr_Map[nx][ny] != 2 and (nx, ny) not in visited: # tránh tường
                        hn = self.Herurictics(nx, ny)
                        queue.put((hn, (nx, ny), path+[(nx, ny)]))
        return None
 

    # Nhóm 3: LOCAL SEARCH
    # 1. Genetic Algorithm
    def khoiTaoQuanThe(self):
        quanT = []
        soLuong = 6
        huong = [(0,1),(1,0),(0,-1),(-1,0)]
        while len(quanT) < soLuong:
            bandau = self.getStart()
            caThe = [bandau]
            for i in range(18):
                x, y = caThe[-1]
                index = random.randint(0, 3)
                dx, dy = huong[index]
                nx, ny = x+dx, y+dy
                if nx >=0 and nx < self.soHang and ny >= 0 and ny < self.soCot:
                    if self.arr_Map[nx][ny] == 0:
                        caThe.append((nx, ny))
            if caThe not in quanT:
                doFitness = self.fitness(caThe)
                quanT.append((caThe, doFitness))
                soLuong -= 1
        return quanT
    
    def fitness(self, caThe):
        x, y = caThe[-1]
        goal = self.getGoal()
        doFitness = (math.sqrt(self.soHang**2 + self.soCot**2)) - (math.sqrt((goal[0] - x)**2 + (goal[1] - y)**2))
        return round(doFitness,2)
                
    def ChonLoc(self, quanThe):
        chonLocQT = []
        # Chọn 2 cá thể tốt nhất
        quanThe.sort(key=lambda x: x[1], reverse=True) 
        chonLocQT.append(quanThe[0])
        chonLocQT.append(quanThe[1]) 
        
        # Chọn 1 cá thể ngẫu nhiên trong số 4 cá thể còn lại
        index = random.randint(2, len(quanThe)-1)
        chonLocQT.append(quanThe[index])

        return chonLocQT

    def GeneticAlgorithms(self):
        # Khởi tạo quần thể 
        quanThe = self.khoiTaoQuanThe()
        maGen = 10000
        while maGen > 0:
            maGen -= 1
            # Chọn lọc cá thể: chọn 3 cá thể trong đó có 2 cả thể tốt và 1 cá thể ngẫn nhiên trong 4 cá thể còn lại
            quanTheChonLoc = self.ChonLoc(quanThe)

            # Lai ghép: tạo 3 cá thể mới từ 3 cá thể đã chọn lọc
            quanTheMoi = []
            huong = [(0,1),(1,0),(0,-1),(-1,0)]
            Flag = False
            for i in range(len(quanTheChonLoc)): 
                caTheCha = copy.deepcopy(quanTheChonLoc[i])
                for j in range(i+1, len(quanTheChonLoc)):
                    caTheMe = copy.deepcopy(quanTheChonLoc[j])
                    tiLeLai = 0.65
                    # Phép lại đồng nhất với tỉ lệ 65%
                    for k in range(1, min(len(caTheCha[0]), len(caTheMe[0]))):
                        tiLeRandom = random.random()
                        if tiLeRandom < tiLeLai:
                            Temp = caTheCha[0][k]
                            caTheCha[0][k] = caTheMe[0][k]
                            caTheMe[0][k] = Temp
                    # Phép đột biến với tỉ lệ 5%
                    tiLeDotBien = 0.05
                    for k in range(1, len(caTheCha[0])):
                        tiLeRandom = random.random()
                        if  tiLeRandom < tiLeDotBien:
                            index = random.randint(0, 3)
                            dx, dy = huong[index]
                            x, y = caTheCha[0][k]
                            nx, ny = x+dx, y+dy
                            if nx >=0 and nx < self.soHang and ny >= 0 and ny < self.soCot:
                                if self.arr_Map[nx][ny] == 0:
                                    caTheCha[0][k] = (nx, ny)
                    for k in range(1, len(caTheMe[0])):
                        tiLeRandom = random.random()
                        if  tiLeRandom < tiLeDotBien:
                            index = random.randint(0, 3)
                            dx, dy = huong[index]
                            x, y = caTheMe[0][k]
                            nx, ny = x+dx, y+dy
                            if nx >=0 and nx < self.soHang and ny >= 0 and ny < self.soCot:
                                if self.arr_Map[nx][ny] == 0:
                                    caTheMe[0][k] = (nx, ny)
                    doFitnessCha = self.fitness(caTheCha[0])
                    doFitnessMe = self.fitness(caTheMe[0])
                    quanTheMoi.append((caTheCha[0], doFitnessCha))
                    quanTheMoi.append((caTheMe[0], doFitnessMe))
                    if len(quanTheMoi) == 6:
                        Flag = True
                        break
                if Flag:
                    quanThe = copy.deepcopy(quanTheMoi)
                    break
            for caThe in quanTheMoi:
                if self.getGoal() in caThe[0]:
                    return caThe[0]
                
        return None  

    # 2. Simulated Annealing
    def SimulatedAnnealing(self):
        start = self.getStart()
        goal = self.getGoal()
        if not start or not goal:
            return None

        # --- Tham số ---
        T = 10.0         # Nhiệt độ ban đầu
        Tmin = 1e-3      # Nhiệt độ dừng
        alpha = 0.995    # Tốc độ giảm nhiệt
        max_steps = 5000 # Số vòng lặp tối đa

        def heuristic(x, y):
            gx, gy = goal
            # Manhattan distance vì di chuyển 4 hướng
            return abs(gx - x) + abs(gy - y)

        # tập các đường di chuyển tiếp theo hợp lệ từ vị trí x,y
        def get_neighbors(x, y):
            dirs = [(0,1),(1,0),(0,-1),(-1,0)]
            return [
                (x+dx, y+dy)
                for dx, dy in dirs
                if 0 <= x+dx < self.soHang and 0 <= y+dy < self.soCot and self.arr_Map[x+dx][y+dy] != 2
            ]

        # --- Khởi tạo ---
        current = start
        current_cost = heuristic(*current)
        best = current
        best_cost = current_cost
        path = [current]
        visited = set([current])

        for step in range(max_steps):
            if current == goal:
                return path

            neighbors = [n for n in get_neighbors(*current) if n not in visited]
            if not neighbors:
                neighbors = get_neighbors(*current)  # cho phép quay lại nếu bế tắc
            if not neighbors:
                break

            # Tính heuristic của tất cả neighbor
            scored = [(heuristic(x, y), (x, y)) for x, y in neighbors]
            scored.sort(key=lambda s: s[0])  # sắp xếp theo heuristic tăng dần

            # --- ƯU TIÊN: chọn neighbor tốt hơn hiện tại ---
            better_neighbors = [n for h, n in scored if h < current_cost]

            if better_neighbors:
                # chọn neighbor tốt nhất
                nx, ny = better_neighbors[0]
                next_cost = heuristic(nx, ny)
                current = (nx, ny)
                current_cost = next_cost
                path.append(current)
                visited.add(current)

                if next_cost < best_cost:
                    best, best_cost = current, next_cost

            else:
                # --- Nếu không có neighbor tốt hơn → chọn random neighbor tệ hơn theo xác suất SA ---
                worse_h, (nx, ny) = random.choice(scored)
                next_cost = worse_h
                delta = next_cost - current_cost
                p = math.exp(-delta / T)

                if random.random() < p:
                    current = (nx, ny)
                    current_cost = next_cost
                    path.append(current)
                    visited.add(current)

            # --- Giảm nhiệt độ ---
            T *= alpha
            if T < Tmin:
                break

        return path

    # Nhóm 4: MÔ TRƯỜNG PHỨC TẠP
    # 1. And-Or Tree Search
    def and_or_tree_search(self):
        start = self.getStart()
        goal = self.getGoal()
        if not start or not goal:
            return None

        def goal_test(state):
            return state == goal

        def actions(state):
            x, y = state
            dirs = [(0,1), (1,0), (0,-1), (-1,0)]
            valid = []
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.soHang and 0 <= ny < self.soCot:
                    if self.arr_Map[nx][ny] != 2:
                        valid.append((nx, ny))
            return valid

        def result(state, action):
            return action

        def or_search(state, path):
            if goal_test(state):
                return [state]
            if state in path:  # tránh vòng lặp
                return None

            for action in actions(state):
                plan = and_search(result(state, action), path + [state])
                if plan is not None:
                    return [state] + plan
            return None

        def and_search(state, path):
            subplan = or_search(state, path)
            if subplan is None:
                return None
            return subplan

        plan = or_search(start, [])
        if plan is None:
            print("⚠️ Không tìm thấy đường đi bằng AND–OR Tree Search.")
        return plan


    # 2. Tìm kiếm trong môi trường nhìn thấy một phần (vị trí (1,3))
    def chiPhiHerurictics_Partial(self, niemTin, FlagVT):
        chPhi = 0
        goal = self.getGoal()
        batBuoc = (1, 3)
        for path, arr in niemTin:
            vtCuoi = path[-1]
            # Càng ra xa vị trí (1, 3) thì chi phí càng lớn
            if FlagVT == False:
                chPhi += (50 +  math.sqrt((vtCuoi[0] - batBuoc[0])**2 + (vtCuoi[1] - batBuoc[1])**2))
            else:
                chPhi += math.sqrt((vtCuoi[0] - goal[0])**2 + (vtCuoi[1] - goal[1])**2)

        return round(chPhi,1)


    def PartialObservable_Greedy(self):
        # tại vị trí  (1,3) có đường đi đến kho báu
        start = self.getStart()
        goal = self.getGoal()
        niemTinBanDau = []
        if self.theloai == "classic":
            niemTinBanDau.append(([start], copy.deepcopy(self.arr_Map)))
            arr = copy.deepcopy(self.arr_Map)
            arr[0][1] = 1
            niemTinBanDau.append(([start, (0,1)], arr))
            arr2 = copy.deepcopy(self.arr_Map)
            arr2[1][0] = 1
            niemTinBanDau.append(([start, (1,0)], arr2))
        elif self.theloai == "ocean":
            niemTinBanDau.append(([start], copy.deepcopy(self.arr_Map)))
            arr = copy.deepcopy(self.arr_Map)
            arr[0][1] = 1
            niemTinBanDau.append(([start, (0,1)], arr))
            arr2 = copy.deepcopy(self.arr_Map)
            arr2[1][0] = 1
            niemTinBanDau.append(([start, (1,0)], arr2))
             # 🔹 Thêm niềm tin về hướng đi (1,3)
            arr3 = copy.deepcopy(self.arr_Map)
            arr3[1][3] = 1
            niemTinBanDau.append(([start, (1,0), (1,1), (1,2), (1,3)], arr3))
        elif self.theloai == "halloween":
            niemTinBanDau.append(([start], copy.deepcopy(self.arr_Map)))
            arr = copy.deepcopy(self.arr_Map)
            arr[0][1] = 1
            niemTinBanDau.append(([start, (0,1)], arr))
            arr2 = copy.deepcopy(self.arr_Map)
        
        priorityQueue = PriorityQueue()
        priorityQueue.put((self.chiPhiHerurictics_Partial(niemTinBanDau, False), niemTinBanDau))
        diQuaFix = False

        # Gia đoạn 1: đi đến 1,3
        while not priorityQueue.empty():
            h, niemTin = priorityQueue.get()
            Flag = True
            for i in range(len(niemTin)):
                if niemTin[i][0][-1] == (1, 3):
                    Flag = True
                    break
            if Flag:
                diQuaFix = True
                priorityQueue.queue.clear()
                priorityQueue.put((h, niemTin))
                break    
                
            hanhDong = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dx, dy in hanhDong:
                state = []
                for i in range(len(niemTin)):
                    vtCuoi = copy.deepcopy(niemTin[i][0])
                    x, y = vtCuoi[len(vtCuoi) - 1][0], vtCuoi[len(vtCuoi) - 1][1]
                    nx = dx + x
                    ny = dy + y
                    arrCopy = copy.deepcopy(niemTin[i][1])
                    if nx >= 0 and nx < self.soHang and ny >= 0 and ny < self.soCot and arrCopy[nx][ny] == 0:
                        arrCopy[nx][ny] = 1
                        duongDi = copy.deepcopy(niemTin[i][0])
                        duongDi.append((nx, ny))
                        state.append((duongDi, arrCopy))
                if len(state) > 0:
                    priorityQueue.put((self.chiPhiHerurictics_Partial(state, diQuaFix), state))

        # Gia đoạn 2: đi đến kho báu
        while not priorityQueue.empty():
            h, niemTin = priorityQueue.get()
            Flag = True

            for i in range(len(niemTin)):
                if niemTin[i][0][-1] != goal:
                    Flag = False
                    break
            if Flag:
                return niemTin[0][0]
                
            hanhDong = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dx, dy in hanhDong:
                state = []
                for i in range(len(niemTin)):
                    vtCuoi = copy.deepcopy(niemTin[i][0])
                    x, y = vtCuoi[len(vtCuoi) - 1][0], vtCuoi[len(vtCuoi) - 1][1]
                    nx = dx + x
                    ny = dy + y
                    arrCopy = copy.deepcopy(niemTin[i][1])
                    if nx == goal[0] and ny == goal[1]: 
                        S = copy.deepcopy(niemTin[i][0])
                        S.append((nx, ny))
                        state.append((S, arrCopy))
                    if nx >= 0 and nx < self.soHang and ny >= 0 and ny < self.soCot and arrCopy[nx][ny] == 0:
                        arrCopy[nx][ny] = 1
                        duongDi = copy.deepcopy(niemTin[i][0])
                        duongDi.append((nx, ny))
                        state.append((duongDi, arrCopy))
                if len(state) > 0:
                    priorityQueue.put((self.chiPhiHerurictics_Partial(state, diQuaFix), state))

        return None

    # Nhóm 5: Tìm kiếm thõa mãn ràng buộc
    def ArcConsistencyAlgorithms(self):
        # tập biến và miền giá trị
        tapBien = []
        Dx, Dy = self.mienGiaTri()
        tapBien.append((1, Dx))
        tapBien.append((2, Dy))
        # tập rằng buộc: loại bỏ hướng đi của người chơi nếu có 3 hướng di chuyển đều là tường, nếu 2 hướng là tường và một hướng còn lại là ngoài mê cung, 2 hướng tường và một hướng đã bị xóa khỏi miền giá trị trước đó. 
        tapBienRG = self.AC3(tapBien)
        start = self.getStart()
        result = self.BackTracking(tapBienRG, [start], start, copy.deepcopy(self.arr_Map))
        return result

    def mienGiaTri(self):
        duongDi = []
        tuong = []
        
        for i in range(self.soHang):
            for j in range(self.soCot):
                if self.arr_Map[i][j] == 0:
                    duongDi.append((i, j))
                elif self.arr_Map[i][j] == 2:
                    tuong.append((i, j))

        return duongDi, tuong
    def AC3(self, tapBien):
        queue = deque()
        tapBienNew = []
        for i in tapBien:
            for j in tapBien:
                if i != j:
                    tapBienNew.append(i)
                    queue.append((i, j))
        
        while len(queue) > 0:
            x, y = queue.popleft()
            flag, mienGT = self.revise(x, y)
            if flag:
                if len(mienGT) == 0:
                    return False
                
                xBien = copy.deepcopy(x[0])
                xcopy = [(xBien, mienGT)]
                for bien in tapBienNew:
                    if bien[0] == xBien and len(mienGT) < len(bien[1]):
                        bien[1] = mienGT

                for k in tapBien:
                    if k != x and k != y:
                        queue.append((k, xcopy))

        return tapBienNew
    def revise(self, x, y):
        revised = False
        arrDelete = []
        arr = copy.deepcopy(self.arr_Map)

        if x[0] == 1:
            for i in x[1]:
                tichLuy = 0
                huong = [(0, 1), (1, 0), (0, -1), (-1, 0)]
                for dx, dy in huong:
                    nx = i[0] + dx
                    ny = i[1] + dy
                    if (nx, ny) in y[1]:
                        tichLuy += 1
                    elif nx > 9 or ny > 9 or nx < 0 or ny < 0:
                        tichLuy += 1
                    elif arr[i[0]][i[1]] == -1:
                        tichLuy += 1
                if tichLuy >= 3:
                    revised = True
                    arrDelete.append(i)
                    arr[i[0]][i[1]] = -1
            # Xóa các giá trị bên trong miền giá trị
            for j in arrDelete:
                x[1].remove(j)
            return revised, x[1]
        return revised, None
    
    def BackTracking(self, tapB, vt, start: tuple, arr):
        if vt[len(vt)-1] == self.getGoal():
            return vt
        if len(tapB[0][1]) == 0:
            return None
        huong = [(1, 0), (0, 1), (0, -1), (-1, 0)]
        for dx, dy in huong:
            x = start[0] + dx
            y = start[1] + dy 
            if (x, y) == self.getGoal():
                vtNew = copy.deepcopy(vt)
                vtNew.append((x, y))
                return vtNew 
            if (x, y) in tapB[0][1]:
                arrCopy = copy.deepcopy(arr)
                if arrCopy[x][y] == 0:
                    arrCopy[x][y] = -1
                    vtNew = copy.deepcopy(vt)
                    vtNew.append((x, y))
                    tapBNew = copy.deepcopy(tapB)
                    tapBNew[0][1].remove((x, y))
                    result = self.BackTracking(tapBNew, vtNew, (x, y), arrCopy)
                    if result is not None: 
                        return result
                    arrCopy[x][y] = 0
                    tapBNew[0][1].append((x, y))
            
        return None

    # 2. CSP sử dụng với Backtracking
    def CSP_Backtracking(self):
        start = self.getStart()
        goal = self.getGoal()
        if not start or not goal:
            return None

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # phải, xuống, trái, lên

        # ------------------------
        # Khởi tạo domain cho mỗi ô
        # ------------------------
        domain = {
            (x, y): [
                (x + dx, y + dy)
                for dx, dy in directions
                if 0 <= x + dx < self.soHang and 0 <= y + dy < self.soCot
                and self.arr_Map[x + dx][y + dy] != 2
            ]
            for x in range(self.soHang)
            for y in range(self.soCot)
            if self.arr_Map[x][y] != 2
        }

        path = []
        visited = set()

        # ------------------------
        # Hàm kiểm tra ràng buộc
        # ------------------------
        def is_consistent(pos):
            """Kiểm tra ô có hợp lệ không (không ra ngoài map, không vào tường, không trùng)"""
            x, y = pos
            return (
                0 <= x < self.soHang and
                0 <= y < self.soCot and
                self.arr_Map[x][y] != 2 and
                pos not in visited
            )

        # ------------------------
        # Hàm quay lui (backtracking)
        # ------------------------
        def backtrack(current):
            path.append(current)
            visited.add(current)

            if current == goal:
                return True

            # Sắp xếp domain theo khoảng cách tới goal (heuristic)
            gx, gy = goal
            next_moves = sorted(
                domain[current],
                key=lambda p: abs(p[0] - gx) + abs(p[1] - gy)
            )

            for next_pos in next_moves:
                if is_consistent(next_pos):
                    if backtrack(next_pos):
                        return True

            # Quay lui nếu không thành công
            path.pop()
            visited.remove(current)
            return False

        # ------------------------
        # Bắt đầu giải
        # ------------------------
        if backtrack(start):
            # print("🎯 Tìm thấy đường đi bằng CSP Backtracking!")
            return path
        else:
            # print("⚠️ Không tìm được đường thỏa mãn ràng buộc.")
            return None



    # NHÓM 6: ĐỐI KHÁNG 
    # 1. Alpha-Beta Pruning
    def AlphaBetaPruning(self):
        huong = [(0, -1), (-1, 0), (1, 0), (0, 1)]
        start = self.getStart()
        self.soTT = 0
        bestScore = -math.inf
        bestSate = None
        for dx, dy in huong:
            x = dx + start[0]
            y = dy + start[1]
            if x >= 0 and x < self.soHang and y >= 0 and y < self.soCot:
                arrCopy = copy.deepcopy(self.arr_Map)
                if arrCopy[x][y] == 0:
                    arrCopy[x][y] = 1
                    vtNew = [start, (x, y)]
                    newState = (vtNew, arrCopy)
                    p, v = self.MaxValue_AB(newState, -math.inf, math.inf)
                    if bestScore < p:
                        bestScore = p
                        bestSate = v
        goal = self.getGoal()
        if goal not in bestSate: 
            return None
        return bestSate

    def MaxValue_AB(self, state: tuple, alpha, beta):
        path, arr = state
        if self.TerminalTest(path, arr):
            return self.Utility(path), path
        v = -math.inf
        VT = None
        huong = [(0, -1), (-1, 0), (1, 0), (0, 1) ]
        for dx, dy in huong:
            stateNew = self.Result(state, dx, dy)
            if stateNew is None:
                continue
            point, vt = self.MinValue_AB(stateNew, alpha, beta)
            if point >= v:
                v = point
                VT = vt
            if v >= beta:
                return v, VT
            alpha = max(v, alpha)
        return v, VT

    def MinValue_AB(self, state: tuple, alpha, beta):
        path, arr = state
        if self.TerminalTest(path, arr):
            return self.Utility(path), path

        v = math.inf
        VT = None
        huong = [(0, -1), (-1, 0), (1, 0), (0, 1) ]
        for dx, dy in huong:
            stateNew = self.Result(state, dx, dy)
            if stateNew is None:
                continue
            point, vt = self.MaxValue_AB(stateNew , alpha, beta)
            if point <= v:
                v = point
                VT = vt
            if v <= alpha:
                return v, VT
            beta = min(v, beta)
        return v, VT

    def Result(self, state: tuple, dx, dy):
        path, arr = state
        vtCuoi = path[-1]
        x = dx + vtCuoi[0]
        y = dy + vtCuoi[1]
        if x >= 0 and x < self.soHang and y >= 0 and y < self.soCot:
            if arr[x][y] == 0 or arr[x][y] == 5:
                arrCopy = copy.deepcopy(arr)
                if arr[x][y] != 5:
                    arrCopy[x][y] = 1
                vtNew = copy.deepcopy(path)
                vtNew.append((x, y))
                self.soTT += 1
                return (vtNew, arrCopy)
        return None
        
    # kiểm tra điều kiện
    def TerminalTest(self, state, arr):
        goal = self.getGoal()
        x = state[-1][0]
        y = state[-1][1]
        
        if (x, y) == goal:
            return True
    
        for dx, dy in [(0,-1), (-1,0), (1,0), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.soHang and 0 <= ny < self.soCot:
                if arr[nx][ny] == 0 or arr[nx][ny] == 5:
                    return False
        return True 

    # Tính giá trị đánh giá
    def Utility(self, path):
        goal = self.getGoal()
        x, y = path[-1]
        if (x, y) == goal:
            return 1000
        # Càng gần kho báu điểm càng cao
        distance = math.sqrt((x - goal[0])**2 + (y - goal[1])**2)
        return 100 - distance

    # 2. MiniMax
    # Giải thuật MiniMax
    def MiniMax(self):
        huong = [(0, -1), (-1, 0), (1, 0), (0, 1)]
        start = self.getStart()
        self.soTT = 0
        bestScore = -math.inf
        bestState = None

        for dx, dy in huong:
            result = self.Result(([start], copy.deepcopy(self.arr_Map)), dx, dy)
            if result is None:
                continue

            score, path = self.MaxValue(result)
            if score > bestScore:
                bestScore = score
                bestState = path

        goal = self.getGoal()
        if bestState is None or goal not in bestState:
            print("Không tìm thấy đường đi hợp lệ.")
            return None

        print("✅ Tìm thấy đường đi:", bestState)
        print("Số trạng thái duyệt:", self.soTT)
        return bestState


    def MaxValue(self, state):
        path, arr = state
        if self.TerminalTest(path, arr):
            return self.Utility(path), path

        v = -math.inf
        bestPath = None
        huong = [(0, -1), (-1, 0), (1, 0), (0, 1)]
        for dx, dy in huong:
            newState = self.Result(state, dx, dy)
            if newState is None:
                continue
            score, p = self.MinValue(newState)
            if score > v:
                v = score
                bestPath = p
        return v, bestPath


    def MinValue(self, state):
        path, arr = state
        if self.TerminalTest(path, arr):
            return self.Utility(path), path

        v = math.inf
        bestPath = None
        huong = [(0, -1), (-1, 0), (1, 0), (0, 1)]
        for dx, dy in huong:
            newState = self.Result(state, dx, dy)
            if newState is None:
                continue
            score, p = self.MaxValue(newState)
            if score < v:
                v = score
                bestPath = p
        return v, bestPath