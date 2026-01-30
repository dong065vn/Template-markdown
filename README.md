# Academic Document Manager (ADM)

> Công cụ xử lý và quản lý văn bản học thuật theo chuẩn NĐ30/2020

## ✨ Features

### 📄 Function 1: Convert
Chuyển đổi định dạng tài liệu:
- **PDF → Markdown** - Trích xuất text, cấu trúc
- **DOCX → Markdown** - Giữ nguyên formatting
- **Markdown → LaTeX** - Xuất theo chuẩn học thuật

### ✍️ Function 2: Generate
Tạo tài liệu mới từ AI:
- Khởi tạo outline luận văn/báo cáo
- Export ra DOCX, PDF
- Merge sections thành file hoàn chỉnh

### 🔄 Function 3: Regenerate
Tái tạo/format lại tài liệu có sẵn:
- Extract content từ PDF/DOCX
- AI format lại chuẩn Markdown
- Export với formatting đúng

---

## 🚀 Quick Start

### Installation

```bash
# Clone repo
git clone https://github.com/your-repo/academic-document-manager.git
cd academic-document-manager

# Install dependencies
pip install -r requirements.txt

# Or with PDM
pdm install
```

### Basic Usage

```bash
# Function 1: Convert
python main.py convert pdf-to-md --input thesis.pdf --output thesis.md

# Function 2: Generate
python main.py generate init --name "Luận văn" --type thesis
python main.py generate export --format docx
python main.py generate merge

# Function 3: Regenerate
python main.py regenerate init --file old_document.docx
python main.py regenerate export --format all
python main.py regenerate merge

# GUI
python main.py gui
```

---

## 📋 CLI Commands

### Generate Commands
| Command | Description |
|---------|-------------|
| `generate init` | Khởi tạo project mới |
| `generate sections` | Tạo section outlines |
| `generate export` | Export MD → DOCX/PDF |
| `generate merge` | Ghép sections thành 1 file |
| `generate renew` | Reset phases |

### Regenerate Commands
| Command | Description |
|---------|-------------|
| `regenerate init --file <path>` | Extract content từ file |
| `regenerate export` | Export content đã format |
| `regenerate merge` | Ghép thành file cuối |
| `regenerate scan` | Kiểm tra nội dung |
| `regenerate render-sections` | Render từng section riêng |
| `regenerate status` | Xem trạng thái project |
| `regenerate renew` | Reset phases |

---

## 📁 Project Structure

```
academic-document-manager/
├── main.py                 # Entry point
├── src/
│   ├── cli/                # CLI commands
│   │   ├── main.py
│   │   ├── convert.py
│   │   ├── generate.py
│   │   └── regenerate.py
│   ├── templates/          # Processors
│   │   ├── markdown_cleaner.py
│   │   ├── text_processor.py
│   │   └── section_renderer.py
│   └── gui/                # GUI (CustomTkinter)
├── function1/              # Convert logic
│   ├── parsers/
│   └── exporters/
├── function2/              # Generate logic
│   └── templates/converters/
├── function3/              # Regenerate logic
│   └── extractors/
└── .agent/workflows/       # Slash commands
```

---

## 🎯 Slash Commands

Khi làm việc với AI assistant:

| Command | Mô tả |
|---------|-------|
| `/adm-convert` | Convert PDF/DOCX → MD/LaTeX |
| `/adm-generate` | Tạo tài liệu mới |
| `/adm-regenerate` | Tái tạo từ file gốc |
| `/adm-export` | Export sang DOCX/PDF |
| `/adm-merge` | Ghép sections |
| `/adm-zolo` | Quick start luận văn |
| `/adm-renew` | Reset để làm file mới |
| `/adm-info` | Thông tin hệ thống |
| `/adm-help` | Xem tất cả commands |

---

## ⚙️ Configuration

### Formatting Standards (NĐ30/2020)
- **Font:** Times New Roman 14pt
- **Margins:** Top/Bottom 2cm, Left 3cm, Right 1.5cm
- **Page size:** A4 (21 x 29.7 cm)
- **Line spacing:** 1.5

### Dependencies
```
python-docx>=0.8.11
PyMuPDF>=1.21.0
mistune>=2.0.0
PyYAML>=6.0
click>=8.0.0
customtkinter>=5.0.0
weasyprint>=58.0 (optional, for PDF)
```

---

## 📝 Examples

### Regenerate Workflow
```bash
# 1. Init từ file cũ
python main.py regenerate init --file "De-Cuong-Thuc-Tap.docx"

# 2. Lấy prompt, gửi cho AI, lưu MD vào phase3_content/

# 3. Export
python main.py regenerate export --format all

# 4. Hoặc render sections (cho file lớn)
python main.py regenerate render-sections --output "Final.docx"
```

### Generate Workflow
```bash
# 1. Init
python main.py generate init --name "Báo cáo thực tập" --type report

# 2. Viết content vào phase3_content/*.md

# 3. Export & Merge
python main.py generate export --format docx
python main.py generate merge --output "BaoCao_Final.docx"
```

---

## 🛠️ Development

```bash
# Run tests
pytest tests/

# Build executable
pyinstaller adm.spec

# Check CLI
python main.py --help
```

---

## 📄 License

MIT License - See LICENSE file

---

## 👥 Contributors

- WENet Team
