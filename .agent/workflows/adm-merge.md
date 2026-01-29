---
description: ADM Merge - Ghép tất cả sections thành 1 file
---

# /adm-merge - Merge Documents

## Mục đích
Ghép tất cả file DOCX sections thành 1 file hoàn chỉnh.

## Cú pháp
```bash
cd academic-document-manager
python main.py generate merge
```

## Options
```bash
--output "tên_file.docx"   # Đặt tên file output
```

## Input yêu cầu
Các file `.docx` trong `function2/Segmentation/phase4_rendered/docx/`

→ Chạy `/adm-export` trước nếu chưa có

## Output
`function2/Segmentation/phase5_output/MERGED_document.docx`

## Ví dụ
```bash
cd academic-document-manager
python main.py generate merge --output "Luan_van_final.docx"
```

## Lưu ý
- Merge giữ nguyên format NĐ30/2020
- Giữ nguyên hình ảnh, bảng
- TOC sẽ được tự động cập nhật
