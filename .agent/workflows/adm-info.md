---
description: ADM Info - Xem thông tin hệ thống
---

# /adm-info - System Info

## Mục đích
Xem thông tin về Python, dependencies và trạng thái hệ thống.

## Cú pháp
```bash
cd academic-document-manager
python main.py info
```

## Output hiển thị
- Python version
- OS
- Current working directory
- Dependencies status (✅ hoặc ❌)

## Dependencies cần có
```
✅ python-docx   - Xử lý DOCX
✅ PyMuPDF       - Parse PDF
✅ customtkinter - GUI
✅ mistune       - Parse Markdown
✅ PyYAML        - Config files
✅ click         - CLI framework
```

## Cài đặt nếu thiếu
```bash
cd academic-document-manager
pip install -r requirements.txt
```
