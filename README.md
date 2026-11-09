# Battleship - PFP191

Battleship là trò chơi bắn tàu cho hai người thay phiên trên cùng một máy. Mỗi người đặt 5 tàu trên bàn cờ . Ai đánh chìm toàn bộ tàu đối thủ trước sẽ thắng.


## Cách chơi

1. Chọn **1. Player Management → 2. Add player** để tạo hai hồ sơ. Chọn **0. Back** để quay về menu chính.
2. Chọn **2. New Game** và nhập ID của hai người chơi. Mỗi người đặt 5 tàu, chọn ô bắt đầu từ `A1` đến `J10` và hướng `H` (ngang) hoặc `V` (dọc).
3. Khi game yêu cầu, chuyền máy cho người đến lượt. Nhập tọa độ để bắn, ví dụ `B4`. Game giấu tàu đối thủ và hiển thị số tàu của bạn còn nổi.
4. Sau ván, chọn **3. History and Reports** để xem xếp hạng, xem lịch sử hoặc xuất báo cáo. Chọn **0. Exit** ở menu chính để thoát.

## Dữ liệu lưu trên máy

- `data/players.json` lưu hồ sơ người chơi.
- `data/history.json` lưu kết quả các ván đã hoàn tất.
- `data/report.txt` được tạo khi chọn **Export report to text file**.
