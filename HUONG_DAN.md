# MazeSolver – Tiểu luận Đề tài 49 (Quay lui + Stack)

## Cấu trúc thư mục
```
MazeSolver_TieuLuan/
├── web/index.html      <- Trang web tiểu luận + mô phỏng (1 file duy nhất)
├── pygame/             <- Chương trình Pygame gốc
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
└── HUONG_DAN.md        <- File này
```

## 1. Mở trang web
- Nhấp đúp `web/index.html` (mở bằng Chrome, Edge hoặc Firefox). Không cần cài đặt gì.
- Cần Internet ở lần mở để tải phông chữ đẹp và vẽ sơ đồ lưu đồ (mục 4.1).
  Không có mạng thì trang vẫn chạy đầy đủ, chỉ khác phông chữ và sơ đồ lưu đồ hiện dạng chữ.
- Muốn đưa lên mạng: kéo thả `index.html` lên GitHub Pages, Netlify hoặc Vercel.

## 2. Dùng phần mô phỏng (Chương 6)
| Nút | Tác dụng |
|---|---|
| Chạy | Tự động chạy thuật toán |
| Bước tiếp | Chạy đúng 1 thao tác, xem Stack và dòng mã giả thay đổi |
| Tạm dừng / Tiếp tục | Dừng hoặc chạy tiếp |
| Chạy tới cuối | Chạy ngay đến khi kết thúc |
| Đặt lại | Chạy lại từ đầu trên cùng mê cung |
| Mê cung mới | Sinh mê cung mới theo loại đang chọn |
| − / + | Đổi kích thước (7×7 đến 31×35) |
| Vẽ tường / Xóa tường | Nhấp hoặc kéo chuột lên mê cung để sửa, rồi bấm Chạy |
| Thanh Tốc độ | Số bước mỗi giây |
| Hiện ngõ cụt | Bật/tắt màu hồng của ô đã bỏ |

Mẹo khi trình bày: chọn "Mẫu 3 · Không có lối thoát" rồi "Chạy tới cuối" để minh họa trường hợp xấu nhất (180 bước = 5 × 36 ô). Chọn "Mẫu 2 · Đường rắn" để minh họa Stack sâu nhất.

## 3. Chạy chương trình Pygame
Cần Python 3.10 trở lên. Mở Terminal trong thư mục `pygame/`:
```bash
python -m pip install -r requirements.txt
python main.py
```
Windows nếu lệnh `python` không chạy thì dùng `py` thay thế.

## 4. Chỉnh nội dung bài tiểu luận
Mở `web/index.html` bằng VS Code hoặc Notepad. Thêm họ tên, MSSV, giảng viên: tìm dòng
`<div class="eyebrow">Đề tài 49` rồi thêm một dòng `<p>Sinh viên: ...</p>` ngay dưới thẻ `<h1>`.
Nội dung các chương nằm trong các thẻ `<section>`, chữ thường nằm trong thẻ `<p>`, `<li>`.

## 5. Gợi ý nộp bài
Dùng trang web làm bản trình bày. Nếu cần bản giấy: mở bằng Chrome, nhấn Ctrl+P rồi chọn "Lưu dưới dạng PDF".
