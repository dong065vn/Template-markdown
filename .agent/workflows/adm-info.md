---
description: ADM Info - Xem thông tin hệ thống
---

# /adm-info - System Information

## Cách sử dụng
```bash
python main.py info
```

## Thông tin hiển thị

### Version
- ADM version
- Python version
- Dependencies versions

### Configuration
- Working directory
- Default output formats
- Template settings

### Paths
- `function1/` - Convert logic
- `function2/` - Generate logic
- `function3/` - Regenerate logic
- `src/templates/` - Processors

### Dependencies Status
| Package | Purpose |
|---------|---------|
| python-docx | DOCX manipulation |
| PyMuPDF | PDF parsing |
| mistune | Markdown parsing |
| PyYAML | Config files |
| click | CLI framework |
| customtkinter | GUI |
| weasyprint | PDF export (optional) |

## Check Dependencies
```bash
python -c "import docx; import fitz; import mistune; print('OK')"
```

## Format Standards (NĐ30/2020)
- Font: Times New Roman 14pt
- Margins: Top/Bottom 2cm, Left 3cm, Right 1.5cm
- Page: A4 (21x29.7cm)
