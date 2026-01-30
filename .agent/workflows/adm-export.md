---
description: ADM Export - Xuất Markdown ra DOCX/PDF
---

# /adm-export - Export tài liệu

## Khi nào sử dụng
- Đã viết xong content Markdown
- Cần xuất ra DOCX hoặc PDF
- Muốn xuất nhiều format cùng lúc

## Commands

### Function 2 (Generate)
```bash
python main.py generate export --format docx|pdf|all
```

### Function 3 (Regenerate)
```bash
python main.py regenerate export --format docx|pdf|text|all
```

## Options
| Format | Output |
|--------|--------|
| `docx` | File Word (.docx) |
| `pdf` | File PDF |
| `text` | File văn bản thuần (.txt) |
| `all` | Tất cả các format |

## Ví dụ

### Export DOCX
```bash
python main.py generate export --format docx
```

### Export tất cả
```bash
python main.py regenerate export --format all
```

## Output Structure
```
phase4_rendered/
├── docx/
│   ├── section_01.docx
│   └── section_02.docx
├── pdf/
│   └── section_01.pdf
└── text/
    └── section_01.txt
```

## Sau khi export
Chạy `merge` để ghép thành 1 file:
```bash
python main.py generate merge
# hoặc
python main.py regenerate merge
```

## Lưu ý
- PDF cần cài `weasyprint`: `pip install weasyprint`
- Format theo chuẩn NĐ30/2020
- Bold/Italic được render đúng trong DOCX
