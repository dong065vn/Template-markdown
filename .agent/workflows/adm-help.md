---
description: ADM Help - Xem tất cả commands
---

# /adm-help - Danh sách Commands

## Overview
Academic Document Manager (ADM) có 3 functions chính:
- **Function 1**: Convert - Chuyển đổi định dạng
- **Function 2**: Generate - Tạo tài liệu mới
- **Function 3**: Regenerate - Tái tạo/format lại

---

## Slash Commands

### Conversion
| Command | Mô tả |
|---------|-------|
| `/adm-convert` | Convert PDF/DOCX → Markdown/LaTeX |

### Generation (Function 2)
| Command | Mô tả |
|---------|-------|
| `/adm-generate` | Tạo tài liệu mới (3 bước) |
| `/adm-zolo` | Quick start luận văn |
| `/adm-export` | Export MD → DOCX/PDF |
| `/adm-merge` | Ghép sections thành 1 file |

### Regeneration (Function 3)
| Command | Mô tả |
|---------|-------|
| `/adm-regenerate` | Tái tạo từ file PDF/DOCX gốc |

### Utilities
| Command | Mô tả |
|---------|-------|
| `/adm-renew` | Reset phases để làm mới |
| `/adm-info` | Thông tin hệ thống |
| `/adm-help` | Xem danh sách này |

---

## CLI Commands

### Main
```bash
python main.py convert     # Function 1
python main.py generate    # Function 2
python main.py regenerate  # Function 3
python main.py gui         # GUI
python main.py info        # System info
```

### Generate Subcommands
```bash
adm generate init --name "Name" --type thesis|report|paper
adm generate sections
adm generate export --format docx|pdf|all
adm generate merge --output "final.docx"
adm generate renew --phase all|content|rendered|output
```

### Regenerate Subcommands
```bash
adm regenerate init --file "input.pdf|docx"
adm regenerate export --format docx|pdf|text|all
adm regenerate merge --output "final.docx"
adm regenerate scan
adm regenerate render-sections --output "final.docx"
adm regenerate status
adm regenerate renew --phase all|content|rendered|output
```

---

## Quick Reference

### Tạo luận văn mới (F2)
```
/adm-generate hoặc /adm-zolo
```

### Chuẩn hóa file cũ (F3)
```
/adm-regenerate
```

### Convert định dạng (F1)
```
/adm-convert
```
