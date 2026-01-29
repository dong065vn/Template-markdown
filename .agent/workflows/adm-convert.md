---
description: ADM Convert - Chuyển PDF/DOCX sang Markdown/LaTeX
---

# /adm-convert - Convert Documents

## Mục đích
Chuyển đổi file PDF hoặc DOCX thành Markdown và LaTeX.

## Cách dùng

### Convert file cụ thể
```bash
cd academic-document-manager
python main.py convert --file "đường/dẫn/file.pdf"
python main.py convert --file "đường/dẫn/file.docx"
```

### Convert từ thư mục input/
```bash
# Drop files vào function1/input/ trước
cd academic-document-manager
python main.py convert
```

### Convert folder
```bash
cd academic-document-manager
python main.py convert --folder "đường/dẫn/folder/"
```

### Options
```bash
--format latex      # Xuất LaTeX (mặc định)
--format markdown   # Xuất Markdown
--format both       # Xuất cả hai
--split-level 1     # Chia theo H1 (mặc định)
--split-level 2     # Chia theo H2
--max-chars 6000    # Max chars mỗi chunk
```

## Output
- `function1/output/{tên_file}/markdown/` - Các file .md
- `function1/output/{tên_file}/latex/` - Các file .tex + main.tex

## Ví dụ đầy đủ
```bash
cd academic-document-manager
python main.py convert --file thesis.pdf --format both --split-level 1
```
