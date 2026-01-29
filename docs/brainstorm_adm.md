# 🎯 Brainstorm: Academic Document Manager (ADM)

> **Ngày**: 2026-01-29  
> **Mục tiêu**: Tool Python Desktop App (exe) với GUI xử lý văn bản học thuật

---

## 📋 Understanding Summary

Dựa trên yêu cầu đã xác nhận, đây là tổng hợp hiểu biết:

1. **Hai luồng xử lý song song**:
   - **Luồng 1 (Convert)**: PDF/Word → Markdown → LaTeX (pipeline 4 phases)
   - **Luồng 2 (Generate)**: AI → Markdown → Word/PDF (theo quy trình PDM)

2. **Loại văn bản**: Luận văn, báo cáo học thuật, thesis

3. **Output đa dạng**: LaTeX (.tex), Word (.docx), PDF, Markdown

4. **Môi trường**: Desktop App (exe) với GUI, lưu trữ local trên ổ cứng

5. **Tuân thủ quy chuẩn**: Nghị định 30/2020/NĐ-CP về định dạng văn bản hành chính

6. **Kỹ thuật xử lý file lớn**: Chia nhỏ theo section/heading để tránh tràn context

7. **Tích hợp AI**: Hỗ trợ generate nội dung với rule chặt chẽ (YAML/Markdown)

---

## 📌 Assumptions (Giả định)

| # | Giả định | Ghi chú |
|---|----------|---------|
| A1 | Người dùng có cài Python 3.10+ trên máy | Hoặc đóng gói với PyInstaller |
| A2 | AI integration sử dụng Claude API hoặc OpenAI API | Cần API key |
| A3 | Template LaTeX cho luận văn theo chuẩn trường đại học VN | Cần thu thập mẫu |
| A4 | File lưu trữ sử dụng SQLite hoặc JSON | Đơn giản, không cần database server |
| A5 | GUI framework sử dụng PyQt6 hoặc CustomTkinter | Cross-platform, modern UI |

---

## ❓ Open Questions

1. **API AI nào?** Claude API, OpenAI API, hay local model (Ollama)?

2. **Template luận văn theo trường nào?** Có mẫu sẵn không hay cần tự thiết kế?

3. **Ngôn ngữ GUI?** Tiếng Việt hoàn toàn hay song ngữ Việt-Anh?

4. **Phạm vi tính năng v1.0?** Muốn MVP đơn giản hay full-featured?

---

## 🎨 Design Options

### Phương án 1: Modular Multi-Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Academic Document Manager                     │
│                         (Desktop GUI)                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐         ┌──────────────────┐              │
│  │   📥 LUỒNG 1     │         │   📤 LUỒNG 2     │              │
│  │   (Convert)      │         │   (Generate)     │              │
│  └────────┬─────────┘         └────────┬─────────┘              │
│           │                            │                         │
│           ▼                            ▼                         │
│  ┌────────────────┐          ┌────────────────┐                 │
│  │ Phase 1:       │          │ AI Content     │                 │
│  │ Extract        │          │ Generator      │                 │
│  │ (PDF/DOCX→IR)  │          │ (Claude/GPT)   │                 │
│  └───────┬────────┘          └───────┬────────┘                 │
│          │                           │                           │
│          ▼                           ▼                           │
│  ┌────────────────┐          ┌────────────────┐                 │
│  │ Phase 2:       │          │ Markdown       │                 │
│  │ Split          │          │ Parser         │                 │
│  │ (IR→Chunks)    │          │                │                 │
│  └───────┬────────┘          └───────┬────────┘                 │
│          │                           │                           │
│          ▼                           ▼                           │
│  ┌────────────────┐          ┌────────────────┐                 │
│  │ Phase 3:       │◄────────►│ Format         │                 │
│  │ Render         │  Shared  │ Validator      │                 │
│  │ (Chunks→.tex)  │          │ (NĐ30/2020)    │                 │
│  └───────┬────────┘          └───────┬────────┘                 │
│          │                           │                           │
│          ▼                           ▼                           │
│  ┌────────────────┐          ┌────────────────┐                 │
│  │ Phase 4:       │          │ Document       │                 │
│  │ Assemble       │◄────────►│ Exporter       │                 │
│  │ (main.tex)     │  Shared  │ (DOCX/PDF)     │                 │
│  └───────┬────────┘          └───────┬────────┘                 │
│          │                           │                           │
│          └───────────┬───────────────┘                          │
│                      ▼                                           │
│             ┌────────────────┐                                  │
│             │ 📁 Project     │                                  │
│             │ Manager        │                                  │
│             │ (SQLite/JSON)  │                                  │
│             └────────────────┘                                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Ưu điểm:**
- ✅ Kiến trúc rõ ràng, dễ maintain
- ✅ Tái sử dụng components giữa 2 luồng
- ✅ Dễ test từng module độc lập
- ✅ Scalable cho tính năng mới

**Nhược điểm:**
- ⚠️ Cần setup nhiều module ban đầu
- ⚠️ Phức tạp hơn cho MVP

---

### Phương án 2: Plugin-based Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Academic Document Manager                     │
├─────────────────────────────────────────────────────────────────┤
│                         ┌─────────────┐                         │
│                         │   🎛️ Core   │                         │
│                         │   Engine    │                         │
│                         └──────┬──────┘                         │
│                                │                                 │
│         ┌──────────────────────┼──────────────────────┐         │
│         │                      │                      │         │
│         ▼                      ▼                      ▼         │
│  ┌─────────────┐       ┌─────────────┐       ┌─────────────┐   │
│  │ 📄 Parser   │       │ 🧠 AI       │       │ 📝 Export   │   │
│  │  Plugins    │       │  Plugins    │       │  Plugins    │   │
│  ├─────────────┤       ├─────────────┤       ├─────────────┤   │
│  │ • PDF       │       │ • Claude    │       │ • LaTeX     │   │
│  │ • DOCX      │       │ • OpenAI    │       │ • DOCX      │   │
│  │ • Markdown  │       │ • Ollama    │       │ • PDF       │   │
│  │ • HTML      │       │ • Custom    │       │ • HTML      │   │
│  └─────────────┘       └─────────────┘       └─────────────┘   │
│         │                      │                      │         │
│         └──────────────────────┼──────────────────────┘         │
│                                ▼                                 │
│                        ┌─────────────┐                          │
│                        │ 📋 Template │                          │
│                        │   Manager   │                          │
│                        │ (NĐ30/2020) │                          │
│                        └─────────────┘                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Ưu điểm:**
- ✅ Mở rộng dễ dàng bằng plugin
- ✅ Người dùng có thể custom
- ✅ Linh hoạt cho nhiều use case

**Nhược điểm:**
- ⚠️ Phức tạp hơn về architecture
- ⚠️ Cần plugin API specification
- ⚠️ Khó bảo đảm chất lượng plugin

---

## 📊 So sánh 2 Phương án

| Tiêu chí | Phương án 1 (Modular) | Phương án 2 (Plugin) |
|----------|----------------------|---------------------|
| **Độ phức tạp ban đầu** | ⭐⭐⭐ Trung bình | ⭐⭐⭐⭐ Cao |
| **Tốc độ phát triển MVP** | ⭐⭐⭐⭐ Nhanh | ⭐⭐⭐ Chậm hơn |
| **Khả năng mở rộng** | ⭐⭐⭐ Tốt | ⭐⭐⭐⭐⭐ Rất tốt |
| **Dễ maintenance** | ⭐⭐⭐⭐ Dễ | ⭐⭐⭐ Trung bình |
| **Performance** | ⭐⭐⭐⭐ Tốt | ⭐⭐⭐ Tùy thuộc plugin |

> **🎯 Đề xuất**: Bắt đầu với **Phương án 1 (Modular)** cho MVP, sau đó nâng cấp lên plugin-based khi cần mở rộng.

---

## 🛠️ Tech Stack Đề xuất

| Component | Technology | Lý do |
|-----------|------------|-------|
| **GUI Framework** | CustomTkinter | Modern, dễ học, cross-platform |
| **PDF Parser** | PyMuPDF (fitz) | Nhanh, hỗ trợ extract text/images |
| **DOCX Parser** | python-docx | Mature, well-documented |
| **LaTeX Generator** | Custom (Jinja2 templates) | Linh hoạt, dễ customize |
| **PDF Export** | WeasyPrint hoặc pdflatex | Chất lượng cao |
| **DOCX Export** | python-docx | Tương thích Word |
| **Markdown Parser** | mistune | Nhanh, extensible |
| **AI Integration** | anthropic SDK | Claude API |
| **Database** | SQLite | Lightweight, embedded |
| **Packaging** | PyInstaller | Tạo exe cho Windows |
| **Config** | YAML/TOML | Human-readable |

---

## 📁 Cấu trúc thư mục đề xuất

```
academic-document-manager/
├── 📁 src/
│   ├── 📁 core/                 # Core engine
│   │   ├── pipeline.py          # Pipeline orchestrator
│   │   ├── ir.py                # Intermediate Representation
│   │   └── config.py            # Configuration manager
│   │
│   ├── 📁 parsers/              # Input parsers (Phase 1)
│   │   ├── pdf_parser.py
│   │   ├── docx_parser.py
│   │   └── markdown_parser.py
│   │
│   ├── 📁 processors/           # Processing (Phase 2-3)
│   │   ├── splitter.py          # Split into chunks
│   │   ├── renderer.py          # Render to output format
│   │   └── validator.py         # Validate against NĐ30
│   │
│   ├── 📁 exporters/            # Output exporters (Phase 4)
│   │   ├── latex_exporter.py
│   │   ├── docx_exporter.py
│   │   └── pdf_exporter.py
│   │
│   ├── 📁 ai/                   # AI integration
│   │   ├── content_generator.py
│   │   └── prompts/
│   │       └── thesis_prompts.yaml
│   │
│   ├── 📁 gui/                  # Desktop GUI
│   │   ├── main_window.py
│   │   ├── widgets/
│   │   └── themes/
│   │
│   └── 📁 templates/            # LaTeX/DOCX templates
│       ├── thesis/
│       └── report/
│
├── 📁 data/                     # User data (SQLite, projects)
├── 📁 resources/                # Icons, fonts, assets
├── 📁 tests/                    # Unit tests
├── 📄 main.py                   # Entry point
├── 📄 requirements.txt
└── 📄 build.spec                # PyInstaller config
```

---

## 📝 Decision Log

| # | Quyết định | Lý do | Ngày |
|---|------------|-------|------|
| D1 | Sử dụng Phương án 1 (Modular) | Phù hợp MVP, dễ maintain | 2026-01-29 |
| D2 | GUI: CustomTkinter | Modern UI, dễ học | Pending |
| D3 | AI: Claude API | Chất lượng tốt cho tiếng Việt | Pending |
| D4 | Database: SQLite | Lightweight, không cần server | Pending |

---

## ✅ Next Steps

Sau khi user xác nhận brainstorm này, sẽ tiến hành:

1. **Tạo Implementation Plan chi tiết** với các phases và tasks cụ thể
2. **Thiết kế UI/UX mockup** cho Desktop App
3. **Bắt đầu coding** theo thứ tự ưu tiên

---

> [!IMPORTANT]
> Vui lòng review và xác nhận:
> 1. Phương án kiến trúc nào bạn chọn? (1 hoặc 2)
> 2. Tech stack có cần thay đổi gì không?
> 3. Có câu hỏi nào trong Open Questions cần trả lời ngay?
