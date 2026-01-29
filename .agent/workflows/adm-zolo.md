---
description: ADM ZOLO - Khởi tạo luận văn siêu nhanh
---

# /adm-zolo - ZOLO Mode

## Mục đích
Khởi tạo project luận văn/báo cáo chỉ với 1 lệnh.

## Cú pháp
```bash
cd academic-document-manager
python main.py generate init --name "Tên" --type thesis --pages 80
python main.py generate sections
```

## Thesis 80 trang
```bash
cd academic-document-manager
python main.py generate init --name "Luận văn tốt nghiệp" --type thesis --pages 80
python main.py generate sections
```

## Report 30 trang
```bash
cd academic-document-manager
python main.py generate init --name "Báo cáo thực tập" --type report --pages 30
python main.py generate sections
```

## Sau khi chạy
1. Mở `function2/Segmentation/phase2_sections/`
2. Xem các file `section_XXX.md` - đây là outline
3. Dùng AI để viết content theo outline
4. Lưu content vào `phase3_content/`
5. Chạy `/adm-export` để xuất file

## Tips
- Pages 50-80: Luận văn thạc sĩ
- Pages 100+: Luận văn tiến sĩ
- Pages 20-30: Báo cáo, tiểu luận
