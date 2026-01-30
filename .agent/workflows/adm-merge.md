---
description: ADM Merge - Ghép tất cả sections thành 1 file
---

# /adm-merge - Ghép tài liệu

## Khi nào sử dụng
- Đã export xong các sections
- Muốn ghép thành 1 file hoàn chỉnh
- Cần file DOCX cuối cùng để nộp

## Commands

### Function 2 (Generate)
```bash
python main.py generate merge --output "final.docx"
```

### Function 3 (Regenerate)
```bash
python main.py regenerate merge --output "final.docx"
```

## Options
| Option | Description |
|--------|-------------|
| `--output`, `-o` | Tên file output |
| `--project-dir`, `-d` | Thư mục project |

## Ví dụ

### Merge cơ bản
```bash
python main.py generate merge
```

### Merge với tên tùy chỉnh
```bash
python main.py regenerate merge --output "LuanVan_HoanChinh.docx"
```

## Output
File được lưu tại:
- `phase5_output/TenFile.docx`

## Chế độ Merge

### Standard Merge
- Có page break giữa sections
- Có mục lục tự động
- Có đánh số trang

### Seamless Merge (render-sections)
- KHÔNG có page break
- KHÔNG có khoảng trắng thừa
- Sections nối liền mạch

```bash
# Dùng seamless merge
python main.py regenerate render-sections --output "Seamless.docx"
```

## Workflow hoàn chỉnh
```bash
# 1. Export
python main.py generate export --format docx

# 2. Merge
python main.py generate merge --output "Final.docx"

# Kết quả: function2/Segmentation/phase5_output/Final.docx
```
