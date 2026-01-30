---
description: ADM Renew - Reset phases để bắt đầu file mới
---

# /adm-renew - Reset Project

## Khi nào sử dụng
- Muốn làm file mới
- Cần xóa content cũ
- Reset phases để bắt đầu lại

## Commands

### Function 2 (Generate)
```bash
python main.py generate renew --phase all|content|rendered|output
```

### Function 3 (Regenerate)
```bash
python main.py regenerate renew --phase all|content|rendered|output
```

## Phase Options

| Phase | Xóa những gì |
|-------|--------------|
| `content` | phase3_content + phase4 + phase5 |
| `rendered` | phase4_rendered + phase5 |
| `output` | phase5_output only |
| `all` | Tất cả phases (bao gồm source & prompt) |

## Ví dụ

### Reset content (giữ lại source)
```bash
python main.py regenerate renew --phase content -y
```

### Reset hoàn toàn
```bash
python main.py generate renew --phase all -y
```

### Reset output only
```bash
python main.py regenerate renew --phase output -y
```

## Options
| Option | Description |
|--------|-------------|
| `--phase`, `-p` | Phase để reset |
| `--confirm`, `-y` | Skip xác nhận |
| `--project-dir`, `-d` | Thư mục project |

## Workflow

### Làm file mới với F3
```bash
# 1. Reset
python main.py regenerate renew --phase all -y

# 2. Init với file mới
python main.py regenerate init --file "NewDocument.docx"
```

### Giữ source, xóa content
```bash
# Xóa content cũ nhưng giữ prompt
python main.py regenerate renew --phase content -y

# Viết content mới vào phase3_content/
```

## Lưu ý
- `-y` để skip xác nhận
- `all` sẽ xóa tất cả, cần init lại từ đầu
- `content` phổ biến nhất khi muốn viết lại
