---
description: ADM Convert - Chuyển PDF/DOCX sang Markdown/LaTeX
---

# /adm-convert - Chuyển đổi định dạng

## Khi nào sử dụng
- Cần chuyển PDF sang Markdown để edit
- Cần chuyển DOCX sang Markdown
- Cần xuất LaTeX từ Markdown

## Workflow

### PDF → Markdown
```bash
python main.py convert pdf-to-md --input document.pdf --output document.md
```

### DOCX → Markdown
```bash
python main.py convert docx-to-md --input document.docx --output document.md
```

### Markdown → LaTeX
```bash
python main.py convert md-to-latex --input document.md --output document.tex
```

## Options
| Option | Description |
|--------|-------------|
| `--input`, `-i` | File đầu vào |
| `--output`, `-o` | File đầu ra |
| `--template` | LaTeX template (optional) |

## Ví dụ

### Chuyển luận văn PDF sang Markdown
```bash
cd academic-document-manager
python main.py convert pdf-to-md -i "thesis.pdf" -o "thesis.md"
```

### Chuyển báo cáo sang LaTeX
```bash
python main.py convert md-to-latex -i "report.md" -o "report.tex"
```

## Lưu ý
- PDF phức tạp có thể cần chỉnh sửa thủ công sau khi convert
- Hình ảnh trong PDF sẽ được extract ra thư mục riêng
- LaTeX output theo chuẩn NĐ30/2020
