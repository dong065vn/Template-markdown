---
description: ADM Export - Xuất Markdown ra DOCX/PDF
---

# /adm-export - Export Documents

## Mục đích
Chuyển đổi các file Markdown trong `phase3_content/` thành DOCX và PDF chuẩn NĐ30/2020.

## Cú pháp
```bash
cd academic-document-manager
python main.py generate export --format all
```

## Options
```bash
--format docx    # Chỉ DOCX
--format pdf     # Chỉ PDF
--format all     # Cả hai (khuyến nghị)
```

## Input yêu cầu
Files `.md` trong `function2/Segmentation/phase3_content/`

## Output
- `phase4_rendered/docx/` - Các file DOCX riêng lẻ
- `phase4_rendered/pdf/` - Các file PDF riêng lẻ

## Sau export, chạy merge
```bash
python main.py generate merge
```
→ Ghép tất cả thành 1 file `MERGED_document.docx`

## Ví dụ đầy đủ
```bash
cd academic-document-manager

# Export
python main.py generate export --format all

# Merge
python main.py generate merge

# Kết quả: phase5_output/MERGED_document.docx
```
