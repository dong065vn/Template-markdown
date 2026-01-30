---
description: ADM ZOLO - Khởi tạo luận văn siêu nhanh
---

# /adm-zolo - Quick Start Luận văn

## Khi nào sử dụng
- Muốn tạo nhanh cấu trúc luận văn
- Không cần config chi tiết
- Bắt đầu viết ngay

## Cách dùng

### Bước 1: Init nhanh
```bash
python main.py generate init --name "Tên luận văn" --type thesis --pages 80
```

### Bước 2: Structure tự động tạo
```
function2/Segmentation/
├── phase1_init/config.yaml
├── phase2_sections/
├── phase3_content/      ← VIẾT Ở ĐÂY
├── phase4_rendered/
└── phase5_output/
```

### Bước 3: Viết content
Tạo files trong `phase3_content/`:
```
01_mo_dau.md
02_co_so_ly_thuyet.md
03_phuong_phap.md
04_ket_qua.md
05_ket_luan.md
```

### Bước 4: Export & Merge
```bash
python main.py generate export --format docx
python main.py generate merge --output "LuanVan.docx"
```

## Template Luận văn

### Cấu trúc chuẩn
```markdown
# CHƯƠNG 1: MỞ ĐẦU

## 1.1 Đặt vấn đề

## 1.2 Mục tiêu nghiên cứu

## 1.3 Phạm vi nghiên cứu

---

# CHƯƠNG 2: CƠ SỞ LÝ THUYẾT

## 2.1 Tổng quan

## 2.2 Các nghiên cứu liên quan

---

# CHƯƠNG 3: PHƯƠNG PHÁP

## 3.1 Phương pháp nghiên cứu

## 3.2 Công cụ sử dụng

---

# CHƯƠNG 4: KẾT QUẢ

## 4.1 Kết quả đạt được

## 4.2 Đánh giá

---

# CHƯƠNG 5: KẾT LUẬN

## 5.1 Kết luận

## 5.2 Hướng phát triển
```

## Tips
- Mỗi chương = 1 file .md
- Đặt tên với prefix số: 01_, 02_...
- Dùng `---` để chia phần
- **Bold** cho từ khóa quan trọng
