---
description: ADM Help - Xem tất cả commands
---

# /adm-help - All Commands

## Mục đích
Xem danh sách tất cả CLI commands và options.

## Xem help chính
```bash
cd academic-document-manager
python main.py --help
```

## Xem help từng command
```bash
python main.py convert --help
python main.py generate --help
python main.py generate init --help
python main.py generate export --help
python main.py generate merge --help
```

## Quick Reference

### Function 1: Convert
```bash
python main.py convert --file "file.pdf"
python main.py convert --folder "folder/"
python main.py convert --format latex
```

### Function 2: Generate
```bash
python main.py generate init --name "Tên" --type thesis --pages 80
python main.py generate sections
python main.py generate export --format all
python main.py generate merge
```

### Utilities
```bash
python main.py info      # System info
python main.py gui       # Launch GUI
python main.py --version # Version
```

## Slash Commands
- `/adm-convert` - Convert PDF/DOCX
- `/adm-generate` - Generate workflow
- `/adm-zolo` - Quick start
- `/adm-export` - Export DOCX/PDF
- `/adm-merge` - Merge files
- `/adm-info` - System info
