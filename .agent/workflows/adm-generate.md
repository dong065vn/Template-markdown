---
description: ADM Generate - Tạo tài liệu từ AI content
---

# /adm-generate - Tạo tài liệu mới

## Khi nào sử dụng
- Tạo luận văn/báo cáo mới
- Có outline và cần tạo structure
- Muốn AI giúp viết nội dung

## Workflow 3 bước

### Bước 1: Init Project
```bash
python main.py generate init --name "Tên project" --type thesis|report|paper
```

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `--name`, `-n` | Tên project | Required |
| `--type`, `-t` | Loại tài liệu | thesis |
| `--pages`, `-p` | Số trang ước tính | 80 |
| `--project-dir`, `-d` | Thư mục | function2/Segmentation |

### Bước 2: Viết Content
1. Mở thư mục `phase3_content/`
2. Tạo file `.md` cho mỗi section
3. Viết nội dung Markdown

**Ví dụ structure:**
```
phase3_content/
├── 01_gioi_thieu.md
├── 02_co_so_ly_thuyet.md
├── 03_phuong_phap.md
└── 04_ket_luan.md
```

### Bước 3: Export & Merge
```bash
# Export ra DOCX/PDF
python main.py generate export --format all

# Ghép thành 1 file
python main.py generate merge --output "TenFile.docx"
```

## Commands chi tiết

| Command | Mô tả |
|---------|-------|
| `generate init` | Tạo project structure |
| `generate sections` | Tạo section outlines |
| `generate export` | Export MD → DOCX/PDF |
| `generate merge` | Ghép sections |
| `generate renew` | Reset phases |

## Ví dụ hoàn chỉnh

```bash
# 1. Init
python main.py generate init --name "Báo cáo thực tập" --type report

# 2. Viết content vào phase3_content/

# 3. Export
python main.py generate export --format docx

# 4. Merge
python main.py generate merge --output "BaoCao_Final.docx"
```

## Project Structure
```
function2/Segmentation/
├── phase1_init/          # Config
├── phase2_sections/      # Section outlines
├── phase3_content/       # Markdown files ← VIẾT Ở ĐÂY
├── phase4_rendered/      # DOCX/PDF output
│   ├── docx/
│   └── pdf/
└── phase5_output/        # Final merged file
```

## Tips
- Dùng `/adm-zolo` để quick start
- Mỗi file MD = 1 section trong output
- Files được sắp xếp theo tên (01_, 02_, ...)
