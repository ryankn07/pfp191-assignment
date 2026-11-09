
"""Chương trình chính của game Battleship dành cho 2 người chơi."""

# Import các class và hàm từ những file khác trong dự án
from data_manager import DataError, DataManager
from game_logic import play_match
from player_manager import PlayerManager, player_menu
from reports import report_menu


# Hàm main: Khởi tạo hệ thống và điều khiển menu chính
def main():

    # Khởi tạo các đối tượng quản lý dữ liệu và người chơi
    try:
        # Tạo đối tượng để quản lý việc đọc và lưu dữ liệu
        storage = DataManager()

        # Tạo đối tượng quản lý người chơi
        # Truyền storage để PlayerManager sử dụng dữ liệu
        manager = PlayerManager(storage)

    # Bắt lỗi nếu quá trình khởi tạo gặp lỗi DataError
    except DataError as error:
        print("Cannot open player data:", error)
        print("Please fix the data file before starting the game.")

        # Kết thúc hàm main nếu không khởi tạo thành công
        return

    # Lặp menu liên tục cho đến khi người dùng chọn thoát
    while True:

        # Hiển thị menu chính của Battleship
        print("\n" + "=" * 36)
        print("          BATTLESHIP")
        print("=" * 36)
        print("1. Player Management")
        print("2. New Game")
        print("3. History and Reports")
        print("0. Exit")

        # Nhận lựa chọn từ bàn phím
        # strip() loại bỏ khoảng trắng ở đầu và cuối
        choice = input("Choose an option: ").strip()

        # Lựa chọn 1: Mở menu quản lý người chơi
        if choice == "1":
            player_menu(manager)

        # Lựa chọn 2: Bắt đầu trận đấu mới
        # Truyền manager và storage cho hàm play_match
        elif choice == "2":
            play_match(manager, storage)

        # Lựa chọn 3: Xem lịch sử và báo cáo
        elif choice == "3":
            report_menu(manager, storage)

        # Lựa chọn 0: Thoát chương trình
        elif choice == "0":
            print("Goodbye!")

            # Thoát vòng lặp while True
            break

        # Xử lý khi người dùng nhập lựa chọn không hợp lệ
        else:
            print("Invalid choice. Please try again.")


# Chỉ chạy main() khi file này được thực thi trực tiếp
# Không tự chạy main() nếu file được import từ module khác
if __name__ == "__main__":

    try:
        # Gọi hàm main để bắt đầu chương trình
        main()

    # Xử lý khi người dùng nhấn Ctrl+C
    # hoặc không còn dữ liệu đầu vào (EOFError)
    except (KeyboardInterrupt, EOFError):
        print("\nProgram closed.")
