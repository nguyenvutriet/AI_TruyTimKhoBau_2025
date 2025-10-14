# Báo Cáo Cuối Kỳ
- **GVHD: Phan Thị Huyền Trang**

| STT | Sinh viên thực hiện  | MSSV      |
|-----|----------------------|-----------|
| 1   | Nguyễn Vũ Triết      | 23110161  |
| 2   | Phan Thị Thanh Trà   | 23110159  |

# Trò chơi Truy Tìm Kho Báu 
## Giới thiệu
- Trò chơi được xây dựng nhằm mục đích đánh giá một số thuật toán trong 6 nhóm thuật toán: tìm kiếm không có thông tin, tìm kiếm có thông tin, tìm kiếm local search, tìm kiếm trong  môi trường phức tạp, tìm kiếm thõa mãn ràng buộc, tìm kiếm đối kháng. 
- Phân tích PEAS của bài toán: 
\- Performance: tìm kiếm đường đến kho báu nhanh nhất, số bước đi và thời gian ít nhất có thể, tránh cái vật cản trong quá trình tìm kiếm.
\- Enviroment: lưu bảng đồ bằng ma trận, có các vật cản, kho báu, nhân vật tìm kiếm kho báu. Loại môi trường: môi trường có thể quan sát, môi trường tĩnh, rời rạc, môi trường xác định, môi trường quan sát toàn phần.
\- Actuators: di chuyển sang trái, phải, lên, xuống.
\- Ensors: vị trí xuất phát, vị trí kho báu đang ở, 4 hướng di chuyển là vật cản hay ô có thể di được.

## Các nhóm thuật toán
### Nhóm 1: tìm kiếm không có thônng tin.
#### Breadth First Search
- Thuật toán tìm kiếm theo chiều rộng sử dụng cấu trúc Queue để lưu trữ các trạng thái sinh ra. Queue sẽ hoạt động theo cơ chế FIFO. Nếu theo cấu trúc cây, BFS sẽ duyệt hết các lá ở cùng mức trước xong mới đến các mức sâu hơn. Do vậy, nếu trong môi trường trạng thái con sinh nhiều thì độ rộng sẽ rất dài và sẽ khá tốn không gian lưu trữ.
- Hình ảnh (.gif) minh họa thuật toán:
![](/picture/CKBFS.gif)

#### Depth First Search
- Thuật toán tìm kiếm theo chiều sâu cách thức hoạt động gần giống BFS chỉ khác cấu trúc lưu trữ. DFS sử dụng cấu trúc lưu trữ là Stack hoạt động theo cơ chế LIFO. Thuật toán này sẽ tối ưu trong trường hợp các kho báu nằm ở một nhánh cụ thể. Nhưng nó sẽ tốn thời gian trong việc duyệt độ sâu vô hạn. khi thuật toán đi tìm mãi nhưng không thấy được kho báu vì kho báu nằm quá sâu. Thì lúc này thuật toán sẽ trở bên không tối ưu. Do phải duyệt độ sâu quá  lớn nhưng về mặt không gian thì thuật toán này tối ưu hơn BFS . Trong trường hợp xấu nhất thuật toán này sẽ có độ phức tạp thời gian bằng BFS đều là O(pd) nhưng về mặt không gian lại tốt hơn là O(p.d) còn BFS là O(pd).
- Hình ảnh (.gif) minh hoặc thuật toán:
![](/picture/CKDFS.gif)

#### Bảng đánh giá thuật toán 
| Thuật toán    |   Thời gian    | Số bước đi   | 
|---------------|----------------|--------------|
| Breadth First Search |  0.245ms|    19        |
| Depth First Search   |  0.589ms|    24        | 


### Nhóm 2: tìm kiếm có thông tin
#### Greedy Search
- Thuật toán Greedy sử dụng cấu trúc lưu trữ Priority Queue. Thuật toán này chọn đường đi có chi phí ước lượng thấp nhất.
- Mỗi lần di chuyển Greedy sẽ gọi h(n) để ước lượng chi phí từ vị trí hiện tại đến vị trí chứa kho báu. H(n) được gọi là Hàm Herurictics để ước lượng chi phí từ vị trí hiện tại đến kho báu. Trong bài h(n) được xây dựng dựa trên công thức tính khoảng cách từ vị trí hiện tại đến vị trí chứa kho báu.
- Thuật toán này muốn tối ưu  sải ước lượng chi phí một các chính xác. Nếu ước lượng sai thuật toán có thể tìm ra đường đi không tối ưu so với thực tế.
- Hình ảnh (.gif) minh họa thuật toán:
![](/picture/CKGreedy.gif)

#### A* Search
- Thuật toán A* sử dụng cấu trúc lưu trữ Priority Queue. Thuật toán này chọn hướng đi có chi phí thấp nhất đi trước. Trong đó chi phí được tính theo công thức:
f(n) = g(n) + h(n)
trong đó: f(n): là tổng chi phí.
	     g(n): chi phí tính từ vị trí xuất phát đến vị trí hiện tại (Path Cost).
	     h(n): ước lượng chi phí từ vị trí hiện tại đến kho báu (Herurictics).
- Hình ảnh (.gif) minh họa thuật toán:
![](/picture/CKAS.gif)

#### Bảng đánh giá thuật toán 
| Thuật toán    |   Thời gian    | Số bước đi   | 
|---------------|----------------|--------------|
| Greedy Search |    0.541ms     |     19       |
| A* Search     |    1.164ms     |     19       | 


### Nhóm 3: tìm kiếm local search
#### Simulated Search
- Thuật toán Simulated Annealing (SA) là một phương pháp tìm kiếm ngẫu nhiên được lấy cảm hứng từ quá trình tôi luyện kim loại (annealing) trong vật lý. Khi nung nóng kim loại rồi làm nguội dần, các nguyên tử có xu hướng sắp xếp lại để đạt được cấu trúc năng lượng thấp nhất. Trong bài toán này, SA được sử dụng để tìm đường đi từ vị trí xuất phát (start) đến kho báu (goal) trên bản đồ mê cung

- Hình ảnh (.gif) minh họa thuật toán: 
![](/picture/CKSA.gif)

#### Genetic Search
- Giải thuật di truyền được thực hiện qua các bước chính như: khởi tại quần thể, chọn lọc các cá thể phù hợp, lai ghép các cặp cá thể, đột biến cá thể. 
- Trong trò chơi giải thuật khởi tạo quần thể có 6 cả thể và đặc biệt là các cả thể này chính là mảng lưu vị trí được random ngẫu nhiên hướng đi từ điểm xuất phát với quá trình lặp là 21 lần. Các cả thể trong này không có thể có độ dài bằng nhau hoặc không bởi vì khi random hướng thì có di hướng đó là tường ngoặc ngỏ cục sẽ bị loại.
- Độ fitness dựa trên công thức:
$$
Fitness = \sqrt{soHang^2 + soCot^2} - \sqrt{(goalX - x)^2 + (goalY - y)^2}
$$
	
- Chiến thuật lựa chọn sẽ lựa chọn 2 thằng  có độ fitness cao nhất (có vị trí gần kho báu nhất) và random ngẫu nhiên một cá thể trong 4 cả thể còn lại.
- Quá trình lai ghép giữa các cặp cả thể sẽ sử dụng phép lại đồng nhất với một tỉ lệ lai ghép là 65%. Quá trình độ biến cũng sử dụng phép đồng nhất với tỉ lệ đột biến là 5%.
- Sau quá trình độ biến sẽ đưa cá thể sinh ra vào quần thể mới tiếp tực quá trình trên đến khi nào quần thể mới có số lượng là 6 thì sẽ kiểm tra xem trong quần thể mới có cả thể nào chứa kho báu chưa nếu chưa thì tiếp tục chọn lại, lai ghép, đột biến với quần thể mới sinh ra đó.
- Giải thuật di truyền được sử dụng trong tìm kiếm đường đi sẽ rất khó để tìm ra đường chính xác. Bởi vì, trong quá trình lai ghép và đột biến sẽ làm đa dạng nhưng cũng làm cho đường đi bị lệnh và không ra một đường chính xác.
- Hình ảnh (.gif) minh họa thuật toán:
![](/picture/CKGA.gif)

#### Bảng đánh giá thuật toán 
| Thuật toán    |   Thời gian    | Số bước đi   | 
|---------------|----------------|--------------|
| Simulted Annealing | 0.362ms   |     26       |
| Genetic Algorithms   | NA      |     NA       | 

### Nhóm 4: tìm kiếm trong môi trường phức tạp
#### And-Or Tree Search
- Thuật toán AND–OR Tree Search là một dạng mở rộng của tìm kiếm theo cây (Tree Search) dùng để giải quyết bài toán có nhiều khả năng hoặc điều kiện rẽ nhánh, trong đó một số hành động có thể dẫn đến nhiều trạng thái con (AND nodes), và từ mỗi trạng thái, có thể có nhiều lựa chọn hành động khác nhau (OR nodes). Trong bài toán tìm đường, mỗi ô là một trạng thái, và việc di chuyển đến các ô kề là các hành động khả thi.
- Hình ảnh (.gif) minh họa thuật toán:
![](/picture/CKAO.gif)

#### Tìm kiếm trong môi trường nhìn thấy một phần
- Thuật toán này có thể được sử dụng với các nhóm thuật toán tìm kiếm có thông tin và không có thông tin. Trong chương trình sử dụng với thuật toán Greedy. Trong thuật toán chỉ nhìn thấy một phần giống như trong bản đồ kho báu biết trước được một vị trí có thể tìm đến kho báu. Thì trong trò chơi cũng vậy, vị trí được biết sẽ tìm đến được mục tiêu là vị trí giả sử (1, 3). Ban đầu thuật toán sử dụng xây dựng các niềm tin ban đầu dùng Greedy để tìm đường đi đến vị trí đó. Khi tìm thấy được thuật toán sẽ bắt đầu tìm đường đến kho báu.
- Trong thuật toán này có thể loại bỏ được các đường đi vô nghĩa, khi biết trước được một vị trí từ đó ta có thể tìm đường đến mục tiêu. Thuật toán này được coi là tối ưu hơn thuật toán tìm kiếm trong môi trường không nhìn thấy. Ngoài ra, thuật toán muốn chạy nhanh hơn thì trong niềm tin mục tiêu phải chứa chiều đường đi đến kho báu mà trong đó phải đi qua vị trí (1, 3).
- Hình ảnh (.gif) minh họa thuật toán: 
![](/picture/CKNTMP.gif)

#### Bảng đánh giá thuật toán 
| Thuật toán    |   Thời gian    | Số bước đi   | 
|---------------|----------------|--------------|
| And-Or Tree   |   0.433ms|         18         |
| Partially Observable   | 0.375ms |   19       | 

### Nhóm 5: tìm kiếm thõa mãn ràng buộc
#### CPS Backtracking
- Thuật toán CSP Backtracking (Constraint Satisfaction Problem) được sử dụng để giải bài toán tìm đường trong mê cung dựa trên việc thỏa mãn các ràng buộc giữa các biến (ở đây là các ô của bản đồ). Thuật toán hoạt động theo nguyên tắc thử – sai (trial and error), kết hợp với việc kiểm tra tính hợp lệ (consistency) để loại bỏ các đường đi không thỏa mãn trước khi tiếp tục mở rộng tìm kiếm. 
- Hình ảnh (.gif) minh họa thuật toán:
![](/picture/CKBTK.gif)

#### Arc Consistency (AC3)
- Thuật toán AC3 có thể được coi là phiên bản tốt hơn của Backtracking. Bởi vì, trước khi đưa vào trong backtracking thì thuật toán sẽ giới hạn các miền giá trị làm tăng khả năng tìm thấy kho báu nhanh hơn.
- Hình ảnh (.gif) minh họa thuật toán: 
![](/picture/CKAC3.gif)

#### Bảng đánh giá thuật toán 
| Thuật toán    |   Thời gian    | Số bước đi   | 
|---------------|----------------|--------------|
| CSP Backtracking | 0.556ms     |    18        |
| AC3   |    4.152ms             |    20        | 

### Nhóm 6: tìm kiếm đối kháng
#### Minimax
- Thuật toán MiniMax là một kỹ thuật tìm kiếm thường được áp dụng trong các trò chơi đối kháng (như cờ vua, cờ caro, hoặc bài toán đường đi có chướng ngại). Mục tiêu của thuật toán là tối ưu hóa quyết định của người chơi trong môi trường có đối thủ, bằng cách giả lập cả hai bên (người chơi và đối thủ) và chọn nước đi tốt nhất trong tình huống xấu nhất. 
- Nguyên lý hoạt động 
\-	Người chơi (MAX) cố gắng tối đa hóa điểm số (giá trị heuristic). 
\-	Đối thủ (MIN) cố gắng tối thiểu hóa điểm số (làm cho người chơi thua). 
\-	MiniMax duyệt qua toàn bộ cây trạng thái đến độ sâu xác định (depth) để đánh giá nước đi nào mang lại kết quả tốt nhất trong tình huống xấu nhất. 
- Trong bài toán tìm kho báu, ta mô phỏng: 
\-	Người chơi là MAX: muốn đi gần đến kho báu. 
\-	Môi trường (đối thủ) là MIN: khiến người chơi đi xa hơn hoặc bị kẹt. 

- Hình ảnh (.gif) minh họa thuật toán: 
![](/picture/CKMM.gif)


#### Alpha-Beta Pruning
- Thuật toán Alpha-Beta là phiên bản tối ưu hơn của Minimax. Thay vì thử hết đường thì Alpha-Beta chỉ chọn những đường đảm bảo ngưỡng giá trị alpha và beta nếu lối đi nào vượt quá thì thuật toán sẽ không xét.
- Nhờ quá trình này thuật toán sẽ cắt tỉa bớt các trường hợp không hợp lệ, do đó mà thuật toán sẽ chạy nhanh và hiệu quả hơn thuật toán Minimax.
- Hình ảnh (.gif) minh họa thuật toán:
![](/picture/CKAB.gif)

#### Bảng đánh giá thuật toán 
| Thuật toán    |   Thời gian    | Số bước đi   | 
|---------------|----------------|--------------|
| Minimax       |   78.425ms     |      23      |
| Alpha-Beta Pruning   | 34.153ms|    22        | 

## Thư viện và môi trường cài đặt
- Môi trường: [python bản 3.13.7](https://www.python.org/downloads/)
- Thư viện:
\- tkinter: 
    ```python
    pip install tkinter
    ``` 
    \- PIL:
    ```python
    pip install pillow
    ```
    \- Ngoài ra cần import thêm các thư viện có sẵn trong python như: collections, math, queue, copy, random, os.

### Bảng thống kê các hàm được sử dụng trong chương trình
| **Tên hàm** | **Ý nghĩa** | **Thư viện** |
|--------------|-------------|---------------|
| `Tk()` | Tạo cửa sổ chính. | `tkinter` |
| `Toplevel()` | Tạo cửa sổ con. | `tkinter` |
| `Canvas(master, width, height, bg=None)` | Khu vực để vẽ. | `tkinter` |
| `Frame(master, bg=None)` | Khung chứa các widget. | `tkinter` |
| `Label(master, text='', font=None, bg=None, fg=None, image=None)` | Hiển thị văn bản hoặc hình ảnh. | `tkinter` |
| `Button(master, text='', command=None, bg=None, fg=None, font=None)` | Nút nhấn. | `tkinter` |
| `Text(master, width, height)` | Ô hiển thị văn bản. | `tkinter` |
| `Scrollbar(master, command=None)` | Thanh cuộn cho đoạn văn bản. | `tkinter` |
| `messagebox.showinfo()` / `messagebox.showwarning()` | Hiển thị thông báo hoặc cảnh báo. | `tkinter.messagebox` |
| `Combobox(master, values=None)` | Hộp lựa chọn văn bản. | `tkinter.ttk` |
| `Font()` | Định dạng phông chữ. | `tkinter.font` |
| `create_image()` | Tạo hình ảnh trên canvas. | `tkinter.Canvas` |
| `create_rectangle(x1, y1, x2, y2, fill=None, outline=None, width=None)` | Tạo hình chữ nhật trên canvas. | `tkinter.Canvas` |
| `create_line(x1, y1, x2, y2, fill=None, width=None)` | Tạo đường kẻ trên canvas. | `tkinter.Canvas` |
| `create_oval(x1, y1, x2, y2, fill=None, width=None)` | Tạo hình tròn/ellipse trên canvas. | `tkinter.Canvas` |
| `create_text(x, y, text='', fill=None, font=None)` | Vẽ chữ trực tiếp lên canvas. | `tkinter.Canvas` |
| `bind("<Enter>")`, `bind("<Leave>")` | Gán sự kiện khi rê chuột vào/ra. | `tkinter` |
| `delete(item)` | Xóa đối tượng trên canvas. | `tkinter.Canvas` |
| `move(item, dx, dy)` | Di chuyển đối tượng trên canvas. | `tkinter.Canvas` |
| `winfo_width()`, `winfo_height()` | Lấy kích thước của canvas. | `tkinter` |
| `after(ms, func)` | Gọi hàm sau khoảng thời gian ms (hàm định kỳ). | `tkinter` |
| `mainloop()` | Vòng lặp chính cho giao diện luôn hiển thị. | `tkinter` |
| `grid()` | Đặt widget dưới dạng lưới. | `tkinter` |
| `pack()` | Đặt widget theo chiều dọc hoặc ngang. | `tkinter` |
| `place()` | Đặt widget theo tọa độ cụ thể. | `tkinter` |
| `destroy()` | Đóng cửa sổ. | `tkinter` |
| `Image.new(mode, size, color)` | Tạo một ảnh mới. | `PIL.Image` |
| `ImageDraw.Draw(image)` | Tạo đối tượng vẽ và cho phép vẽ lên ảnh. | `PIL.ImageDraw` |
| `ImageDraw.ellipse(bounding_box, fill, outline)` | Vẽ hình ellipse. | `PIL.ImageDraw` |
| `ImageDraw.rectangle(bounding_box, fill, outline)` | Vẽ hình chữ nhật. | `PIL.ImageDraw` |
| `Image.open(path)` | Mở file ảnh. | `PIL.Image` |
| `Image.getdata()` | Lấy toàn bộ dữ liệu pixel của ảnh. | `PIL.Image` |
| `Image.putdata(sequence)` | Gán dữ liệu pixel mới vào ảnh. | `PIL.Image` |
| `Image.getbbox()` | Trả về hộp giới hạn vùng ảnh không rỗng. | `PIL.Image` |
| `Image.resize((width, height))` | Thay đổi kích thước ảnh. | `PIL.Image` |
| `Image.crop((left, top, right, bottom))` | Cắt hình ảnh. | `PIL.Image` |
| `ImageDraw.text((x, y), "Nội dung", fill, font)` | Vẽ chữ lên hình ảnh. | `PIL.ImageDraw` |
| `ImageTk.PhotoImage(image)` | Chuyển ảnh PIL thành định dạng Tkinter có thể dùng. | `PIL.ImageTk` |
| `math.cos(x)`, `math.sin(x)` | Hàm sin, cos. | `math` |
| `math.radians(deg)` | Chuyển độ sang radian. | `math` |
| `math.pi` | Hằng số π (≈ 3.14159). | `math` |
| `random.uniform(a, b)` | Tạo số thực ngẫu nhiên trong đoạn `[a, b]`. | `random` |
| `random.randint(a, b)` | Tạo số nguyên ngẫu nhiên trong đoạn `[a, b]`. | `random` |
| `random.choice(seq)` | Chọn ngẫu nhiên một phần tử trong chuỗi. | `random` |
| `math.sqrt(x)` | Lấy căn bậc 2. | `math` |
| `math.inf` | Đại diện cho vô cùng lớn. | `math` |
| `math.exp(x)` | Tính e^x. | `math` |
| `random.random()` | Trả về số ngẫu nhiên trong [0,1). | `random` |
| `subplots()` | Tạo khung vẽ đồ thị. | `matplotlib.pyplot` |
| `bar(x, height, color=None)` | Vẽ đồ thị dạng cột. | `matplotlib.pyplot` |
| `set_title(title)` | Tạo tiêu đề cho đồ thị. | `matplotlib.axes` |
| `set_xlabel(label)` | Gán nhãn cho trục hoành. | `matplotlib.axes` |
| `text(x, y, s, ha='center')` | Hiển thị giá trị lên đỉnh cột. | `matplotlib.pyplot` |
| `FigureCanvasTkAgg(fig, master)` | Chèn đồ thị matplotlib vào cửa sổ Tkinter. | `matplotlib.backends.backend_tkagg` |
| `perf_counter()` | Đo thời gian chạy với độ chính xác cao. | `time` |
| `datetime.now()` | Lấy thời gian hiện tại. | `datetime` |
| `pygame.mixer.init()` | Khởi tạo âm thanh. | `pygame` |
| `pygame.mixer.music.load(path)` | Nạp file âm thanh. | `pygame` |
| `pygame.mixer.music.play(loops=0)` | Phát nhạc (loops=-1 để phát lặp vô hạn). | `pygame` |
| `pygame.mixer.music.stop()` | Dừng nhạc. | `pygame` |
| `pygame.mixer.music.pause()` | Tạm dừng nhạc. | `pygame` |
| `pygame.mixer.music.unpause()` | Tiếp tục phát nhạc. | `pygame` |
| `pygame.mixer.music.set_volume(volume)` | Điều chỉnh âm lượng. | `pygame` |
| `pygame.mixer.Sound(file)` | Nạp hiệu ứng âm thanh ngắn. | `pygame` |
| `Sound.play()` | Phát âm thanh ngắn. | `pygame` |
| `getcwd()` | Trả về đường dẫn thư mục hiện tại. | `os` |
| `chdir(path)` | Thay đổi thư mục hiện tại. | `os` |
| `listdir(path)` | Liệt kê tất cả file và thư mục trong đường dẫn. | `os` |
| `path.join(a, b)` | Ghép đường dẫn `a` và `b`. | `os.path` |
| `path.exists(path)` | Kiểm tra đường dẫn có tồn tại không. | `os.path` |
| `mkdir(path)` | Tạo thư mục mới. | `os` |
| `remove(path)` | Xóa file. | `os` |
| `rename(old, new)` | Đổi tên file. | `os` |
| `splitext(path)` | Tách tên file và phần mở rộng. | `os.path` |
| `basename(path)` | Lấy tên file từ đường dẫn. | `os.path` |
| `dirname(path)` | Lấy thư mục chứa file. | `os.path` |
| `abspath(path)` | Lấy đường dẫn tuyệt đối. | `os.path` |
| `deque.popleft()` | Lấy phần tử đầu hàng đợi. | `collections.deque` |
| `deque.pop()` | Lấy phần tử cuối hàng đợi. | `collections.deque` |
| `PriorityQueue.put(item)` | Đưa phần tử vào hàng đợi ưu tiên. | `queue.PriorityQueue` |
| `PriorityQueue.get()` | Lấy phần tử có giá trị nhỏ nhất ra. | `queue.PriorityQueue` |
| `PriorityQueue.queue.clear()` | Xóa toàn bộ phần tử trong hàng đợi ưu tiên. | `queue.PriorityQueue` |
| `copy.deepcopy(obj)` | Tạo bản sao độc lập của đối tượng. | `copy` |

## Các thông tin khác
- Để dễ quản lý code thì chương trình được xây dựng dựa trên mô hình MVC. Trong đó Model là phần quản lý nền bên dưới, chuyên xử lý chạy thuật toán, tìm ra đường đế kho báu. View là phần hiện giao diện trực quan cho người dùng trải nghiệm. Controller là cầu nói giữa Model và View, khi trên View gửi một yêu cầu nào chạy thuật toán nào đó thì Controller sẽ tiếp nhận yêu cầu và chuyển tiếp đến Model để Model xử lý. Khi Model xử lý xong sẽ gửi kết quả lên cho Controller để Controller gửi lên View hiện kết quả cho người dùng xem.

![](/picture/MVC.png)





