---
description: ADM Generate - Tạo tài liệu từ AI content
---

# /adm-generate - Generate Documents

## Mục đích
Tạo luận văn, báo cáo từ AI content theo workflow 3 bước.

## Workflow 3 Bước

### Bước 1: Init Project
```bash
cd academic-document-manager
python main.py generate init --name "Tên luận văn" --type thesis --pages 80
```

Options:
- `--type thesis` (luận văn) hoặc `--type report` (báo cáo)
- `--pages 80` số trang dự kiến
- `--author "Tên tác giả"`

### Bước 2: Generate Sections
```bash
python main.py generate sections
```
→ Tạo các file outline trong `phase2_sections/`

### Bước 3: Export & Merge
```bash
# Sau khi AI viết content vào phase3_content/
python main.py generate export --format all
python main.py generate merge
```

## Output
- `function2/Segmentation/phase1_init/` - PRD + config
- `function2/Segmentation/phase2_sections/` - Outlines
- `function2/Segmentation/phase3_content/` - (bạn tạo MD ở đây)
- `function2/Segmentation/phase4_rendered/` - DOCX + PDF
- `function2/Segmentation/phase5_output/` - MERGED file

## Ví dụ đầy đủ
```bash
cd academic-document-manager

# Bước 1
python main.py generate init --name "Luận văn tốt nghiệp" --type thesis --pages 80

# Bước 2
python main.py generate sections

# [Dùng AI viết content, lưu vào phase3_content/]

# Bước 3
python main.py generate export --format all
python main.py generate merge

# Done! File ở phase5_output/MERGED_document.docx
```
