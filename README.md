# MAZE SOLVER — Backtracking + Stack

## 1. Yêu cầu
- Python 3.10 trở lên
- Pygame

## 2. Cài đặt
Mở Terminal tại thư mục dự án và chạy:

```bash
python -m pip install -r requirements.txt
```

## 3. Khởi chạy

```bash
python main.py
```

## 4. Chức năng hiện có
- Mê cung dạng lưới, thay đổi kích thước.
- Tạo mê cung ngẫu nhiên có đường đi bảo đảm.
- Chạy tự động và chạy từng bước.
- Tạm dừng, đặt lại, điều chỉnh tốc độ.
- Bật chế độ thêm tường; nhấp/kéo chuột để chỉnh sửa mê cung.
- Hiển thị số ô đã thăm, số lần quay lui và Stack.

## 5. Nguyên lý thuật toán
Chương trình dùng Backtracking không đệ quy. Stack lưu các trạng thái
`[row, col, next_direction]`. `next_direction` ghi nhớ hướng tiếp theo
cần thử tại mỗi ô. Khi đã thử hết bốn hướng mà không đi tiếp được,
phần tử trên đỉnh Stack được lấy ra (pop), tương ứng thao tác quay lui.

## 6. Giới hạn của bản khởi đầu
- Chưa có chức năng lưu/tải mê cung ra tệp.
- Chưa có bộ sinh mê cung kiểu mê cung cổ điển; bản hiện tại tạo chướng ngại ngẫu nhiên.
- Chưa có biểu đồ so sánh thuật toán.
