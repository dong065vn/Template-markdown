---
description: ADM Regenerate - AI tái tạo nội dung gốc thành Markdown
---

# /adm-regenerate - Tái tạo tài liệu

## Khi nào sử dụng
- Có file PDF/DOCX cũ cần chuẩn hóa format
- Muốn convert file sang Markdown chuẩn
- Cần sửa lỗi format nhưng giữ nguyên nội dung

## Đặc điểm quan trọng
- ⚠️ **KHÔNG thêm/bớt nội dung** - Chỉ format lại
- ✅ **Giữ nguyên 100%** thông tin gốc
- 🎯 AI chỉ làm nhiệm vụ formatting

## Workflow

### Bước 1: Init từ file gốc
```bash
python main.py regenerate init --file "document.docx"
```

**Output:**
- `phase1_source/original_content.txt` - Nội dung gốc
- `phase1_source/config.yaml` - Thông tin project
- `phase2_prompt/prompt_for_ai.txt` - Prompt cho AI

### Bước 2: AI Format lại
1. Mở `phase2_prompt/prompt_for_ai.txt`
2. Copy nội dung → Gửi cho ChatGPT/Claude
3. AI trả về Markdown chuẩn
4. Lưu vào `phase3_content/content.md`

### Bước 3: Export
```bash
# Export thường
python main.py regenerate export --format all

# Hoặc render từng section (cho file lớn)
python main.py regenerate render-sections --output "Final.docx"
```

### Bước 4: Merge (optional)
```bash
python main.py regenerate merge --output "Document_Regenerated.docx"
```

## Commands chi tiết

| Command | Mô tả |
|---------|-------|
| `regenerate init --file <path>` | Extract từ PDF/DOCX |
| `regenerate export --format all` | Export MD → DOCX/PDF/Text |
| `regenerate merge` | Ghép thành 1 file |
| `regenerate scan` | Kiểm tra nội dung MD |
| `regenerate render-sections` | Render từng section riêng |
| `regenerate status` | Xem trạng thái project |
| `regenerate renew` | Reset phases |

## Ví dụ hoàn chỉnh

```bash
# 1. Init
python main.py regenerate init --file "De-Cuong-Thuc-Tap.docx"

# 2. Mở prompt_for_ai.txt, gửi AI, lưu MD vào phase3_content/

# 3. Kiểm tra
python main.py regenerate scan

# 4. Export
python main.py regenerate render-sections --output "De_Cuong_Final.docx"
```

## Project Structure
```
function3/Segmentation/
├── phase1_source/        # File gốc + config
│   ├── config.yaml
│   └── original_content.txt
├── phase2_prompt/        # Prompt cho AI
│   └── prompt_for_ai.txt
├── phase3_content/       # Markdown từ AI ← LƯU Ở ĐÂY
│   └── content.md
├── phase4_rendered/      # Output
│   ├── docx/
│   ├── pdf/
│   └── text/
└── phase5_output/        # Final file
```

## Tips

### Khi file lớn, dùng render-sections
```bash
python main.py regenerate render-sections --output "Final.docx"
```
Chức năng này:
1. Chia markdown theo `---`, `#`, `##`
2. Render từng section riêng
3. Merge không có khoảng trắng thừa

### Kiểm tra trước khi export
```bash
python main.py regenerate scan
```
Hiển thị:
- Số dòng, ký tự
- Số heading, list, table
- Cấu trúc document

### Reset để làm file mới
```bash
python main.py regenerate renew --phase all -y
```
