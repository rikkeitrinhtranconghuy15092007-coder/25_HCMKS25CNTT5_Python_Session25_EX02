class NetflixAccount:
    # Class attributes (Thuộc tính cấp Lớp áp dụng toàn hệ thống)
    platform_name = "Netflix"
    max_profiles = 5

    def __init__(self, email: str, password: str):
        self.email = email
        self.profiles = []  # List chứa danh sách tên người xem
        
        # Các thuộc tính Private áp dụng Name Mangling để giấu dữ liệu
        self.__plan = "Basic"
        self.__password = ""
        
        # Kích hoạt setter để kiểm tra tính hợp lệ của mật khẩu ngay khi khởi tạo
        self.password = password

    # --- PROPERTIES & SETTERS (Tính Đóng Gói) ---

    @property
    def password(self) -> str:
        """Getter cho password: Trả về chuỗi mặt nạ để bảo mật thông tin."""
        return "********"

    @password.setter
    def password(self, new_password: str):
        """Setter cho password: Bẫy dữ liệu số 2, bắt buộc độ dài >= 6 ký tự."""
        if len(new_password) < 6:
            raise ValueError("Password is too short. It must be at least 6 characters.")
        self.__password = new_password

    @property
    def plan(self) -> str:
        """Getter cho plan: Read-only property, không có setter để tránh gian lận."""
        return self.__plan

    # --- CLASS & STATIC METHODS ---

    @staticmethod
    def validate_email(email: str) -> bool:
        """Static Method: Hàm tiện ích độc lập dùng để kiểm tra định dạng email."""
        return "@" in email and "." in email

    @classmethod
    def update_max_profiles(cls, new_limit: int):
        """Class Method: Thay đổi chính sách giới hạn profile áp dụng toàn cầu."""
        if new_limit < 1:
            print("Giới hạn số lượng Profile tối thiểu phải là 1.")
            return
        cls.max_profiles = new_limit
        print(f"Đã cập nhật giới hạn Profile toàn hệ thống thành {cls.max_profiles}")

    # --- INSTANCE METHODS (Nghiệp vụ trên từng tài khoản) ---

    def add_profile(self, profile_name: str):
        """Bẫy dữ liệu 3: Kiểm tra giới hạn tối đa trước khi thêm profile mới."""
        cleaned_name = profile_name.strip()
        if not cleaned_name:
            print("Tên Profile không được để trống!")
            return

        if len(self.profiles) >= NetflixAccount.max_profiles:
            print(f"Đã đạt giới hạn số lượng Profile trên tài khoản này (Tối đa: {NetflixAccount.max_profiles}).")
            return
        
        self.profiles.append(cleaned_name)
        print(f"Thêm profile '{cleaned_name}' thành công!")

    def upgrade_plan(self, new_plan: str):
        """Phương thức kiểm soát duy nhất dùng để cập nhật gói cước ẩn."""
        valid_plans = ["Basic", "Standard", "Premium"]
        if new_plan not in valid_plans:
            print(f"Gói cước không hợp lệ! Vui lòng chọn một trong các gói: {', '.join(valid_plans)}")
            return
        
        self.__plan = new_plan
        print(f"Tài khoản đã được cập nhật lên gói: {self.__plan}")

    def display_info(self):
        """In ra cấu trúc thông tin chi tiết hiện tại của tài khoản."""
        print(f"Nền tảng: {NetflixAccount.platform_name}")
        print(f"Email tài khoản: {self.email}")
        print(f"Mật khẩu: {self.password}")  # Gọi qua property để lấy chuỗi che giấu
        print(f"Gói dịch vụ: {self.plan}")
        print(f"Danh sách Profile ({len(self.profiles)}/{NetflixAccount.max_profiles}):")
        if not self.profiles:
            print("  (Chưa có profile nào)")
        for idx, profile in enumerate(self.profiles, 1):
            print(f"  {idx}. {profile}")


# --- CLI MENU CONTROL SYSTEM ---

def main():
    current_account = None

    while True:
        print("\n===== NETFLIX ACCOUNT MANAGER =====")
        print("1. Đăng ký tài khoản mới")
        print("2. Xem thông tin tài khoản")
        print("3. Thêm người xem")
        print("4. Nâng cấp gói cước")
        print("5. Cập nhật chính sách Netflix (Admin Only)")
        print("6. Thoát chương trình")
        print("===================================")

        choice = input("Chọn chức năng (1-6): ").strip()

        if choice == "1":
            print("\n--- ĐĂNG KÝ TÀI KHOẢN MỚI ---")
            email = input("Nhập email đăng ký: ").strip()
            
            # Bẫy dữ liệu 1: Kiểm tra định dạng bằng staticmethod
            if not NetflixAccount.validate_email(email):
                print("Email không hợp lệ, vui lòng chứa ký tự '@' và '.'")
                continue

            password = input("Nhập mật khẩu (tối thiểu 6 ký tự): ")
            
            # Bẫy dữ liệu 2: Sử dụng try...except bắt lỗi ValueError từ setter
            try:
                current_account = NetflixAccount(email, password)
                print("Đăng ký tài khoản thành công!")
            except ValueError as e:
                print(f"Đăng ký thất bại: {e}")
                current_account = None

        elif choice in ["2", "3", "4"]:
            # Bẫy dữ liệu 4: Ngăn chặn thao tác khi chưa đăng nhập/khởi tạo tài khoản
            if current_account is None:
                print("\nVui lòng đăng ký tài khoản trước (Chức năng 1)")
                continue

            if choice == "2":
                print("\n--- THÔNG TIN TÀI KHOẢN ---")
                current_account.display_info()

            elif choice == "3":
                print("\n--- THÊM NGƯỜI XEM (ADD PROFILE) ---")
                prof_name = input("Nhập tên người xem mới: ")
                current_account.add_profile(prof_name)

            elif choice == "4":
                print("\n--- NÂNG CẤP GÓI CƯỚC ---")
                print("Các gói dịch vụ hiện có: Basic, Standard, Premium")
                new_plan = input("Nhập tên gói cước muốn đổi: ").strip()
                current_account.upgrade_plan(new_plan)

        elif choice == "5":
            print("\n--- CẬP NHẬT CHÍNH SÁCH NETFLIX ---")
            print(f"Giới hạn Profile hiện tại toàn cầu: {NetflixAccount.max_profiles}")
            try:
                new_limit = int(input("Nhập số lượng Profile tối đa mới: ").strip())
                NetflixAccount.update_max_profiles(new_limit)
            except ValueError:
                print("Lỗi: Số lượng giới hạn phải là một số nguyên hợp lệ.")

        elif choice == "6":
            print("\nCảm ơn bạn đã sử dụng Netflix Account Manager. Tạm biệt!")
            break
        else:
            print("\nChức năng không hợp lệ. Vui lòng chọn lại từ số 1 đến 6.")


if __name__ == "__main__":
    main()