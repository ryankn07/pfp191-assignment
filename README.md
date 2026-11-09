# Battleship - PFP191

Battleship là trò chơi bắn tàu cho hai người thay phiên trên cùng một máy. Mỗi người đặt 5 tàu trên bàn cờ 10×10. Ai đánh chìm toàn bộ tàu đối thủ trước sẽ thắng.

## Chạy game

Cần Git và Python 3. Mở PowerShell rồi chạy:

```powershell
git clone https://github.com/ryankn07/pfp191-assignment.git
cd pfp191-assignment
python main.py
```

Nếu đã clone repo, mở PowerShell trong thư mục repo rồi cập nhật:

```powershell
git switch main
git pull --ff-only
python main.py
```

## Cách chơi

1. Chọn **1. Player Management → 2. Add player** để tạo hai hồ sơ. Chọn **0. Back** để quay về menu chính.
2. Chọn **2. New Game** và nhập ID của hai người chơi. Mỗi người đặt 5 tàu, chọn ô bắt đầu từ `A1` đến `J10` và hướng `H` (ngang) hoặc `V` (dọc).
3. Khi game yêu cầu, chuyền máy cho người đến lượt. Nhập tọa độ để bắn, ví dụ `B4`. Game giấu tàu đối thủ và hiển thị số tàu của bạn còn nổi.
4. Sau ván, chọn **3. History and Reports** để xem xếp hạng, xem lịch sử hoặc xuất báo cáo. Chọn **0. Exit** ở menu chính để thoát.

## Dữ liệu lưu trên máy

- `data/players.json` lưu hồ sơ người chơi.
- `data/history.json` lưu kết quả các ván đã hoàn tất.
- `data/report.txt` được tạo khi chọn **Export report to text file**.

## Chạy test

Trong thư mục repo, chạy:

```powershell
python -m unittest discover -s tests -v
```
