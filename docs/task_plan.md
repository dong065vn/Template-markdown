# 📋 Task Plan: Academic Document Manager v1.0

> **Created**: 2026-01-29  
> **Status**: Ready to Execute  
> **Source**: [PRD ADM](prd_adm.md) | [Implementation Plan](implementation_plan.md)

---

## 🎯 Goal

Xây dựng ADM Desktop App với 2 functions tách biệt:
- **Function 1**: Convert PDF/DOCX → Markdown → LaTeX
- **Function 2**: AI Content → Markdown → DOCX/PDF (chuẩn NĐ30/2020)

---

## 📦 Phases

| Phase | Tên | Status | Tasks | Est. Days |
|-------|-----|--------|-------|-----------|
| 0 | Setup | `[ ]` | 3 | 0.5 |
| 1 | Function 2 - Core | `[ ]` | 5 | 2 |
| 2 | Function 2 - Converters | `[ ]` | 4 | 2 |
| 3 | Function 1 - Core | `[ ]` | 5 | 2 |
| 4 | CLI | `[ ]` | 3 | 1 |
| 5 | GUI | `[ ]` | 5 | 3 |
| 6 | Build & Test | `[ ]` | 4 | 2 |

**Total**: 29 tasks, ~12.5 days

---

## ✅ Phase 0: Setup (Day 1)

| # | Task | Verify | Status |
|---|------|--------|--------|
| 0.1 | Tạo cấu trúc thư mục theo plan | Tree command matches | `[ ]` |
| 0.2 | Tạo `requirements.txt` | `pip install -r` success | `[ ]` |
| 0.3 | Tạo `main.py` entry point | `python main.py --help` works | `[ ]` |

---

## ✅ Phase 1: Function 2 - Core (Day 2-3)

> **Dependencies**: Phase 0

| # | Task | Verify | Status |
|---|------|--------|--------|
| 1.1 | Tạo `src/core/config.py` | Load/save YAML config | `[ ]` |
| 1.2 | Tạo `function2/generators/section_generator.py` | Generate sections from outline | `[ ]` |
| 1.3 | Tạo `function2/generators/prompt_builder.py` | Build prompts with rules | `[ ]` |
| 1.4 | Tạo `function2/validators/nd30_validator.py` | Validate format NĐ30 | `[ ]` |
| 1.5 | Test init workflow với sample project | `project_info.yaml` created | `[ ]` |

---

## ✅ Phase 2: Function 2 - Converters (Day 4-5)

> **Dependencies**: Phase 1, Templates đã có

| # | Task | Verify | Status |
|---|------|--------|--------|
| 2.1 | Hoàn thiện `md_to_docx.py` (inline formatting) | Bold/italic works | `[ ]` |
| 2.2 | Hoàn thiện `docx_merger.py` (copy images) | Images preserved | `[ ]` |
| 2.3 | Tạo `md_to_pdf.py` (via WeasyPrint) | PDF output valid | `[ ]` |
| 2.4 | Test full workflow F2 với sample MD | DOCX + PDF output | `[ ]` |

---

## ✅ Phase 3: Function 1 - Core (Day 6-7)

> **Dependencies**: Phase 0

| # | Task | Verify | Status |
|---|------|--------|--------|
| 3.1 | Tạo `function1/parsers/pdf_parser.py` | Extract text from PDF | `[ ]` |
| 3.2 | Tạo `function1/parsers/docx_parser.py` | Extract paragraphs/styles | `[ ]` |
| 3.3 | Tạo `function1/parsers/ir.py` (Intermediate Rep) | IR dataclasses work | `[ ]` |
| 3.4 | Tạo `function1/processors/splitter.py` | Split by heading level | `[ ]` |
| 3.5 | Tạo `function1/exporters/latex_exporter.py` | Generate valid .tex | `[ ]` |

---

## ✅ Phase 4: CLI (Day 8)

> **Dependencies**: Phase 2, Phase 3

| # | Task | Verify | Status |
|---|------|--------|--------|
| 4.1 | Tạo `src/cli/main.py` (adm command) | `adm --help` works | `[ ]` |
| 4.2 | Tạo `src/cli/convert.py` (adm-convert) | Convert folder works | `[ ]` |
| 4.3 | Tạo `src/cli/generate.py` (adm-generate) | All subcommands work | `[ ]` |

---

## ✅ Phase 5: GUI (Day 9-11)

> **Dependencies**: Phase 4

| # | Task | Verify | Status |
|---|------|--------|--------|
| 5.1 | Tạo `src/gui/main_window.py` (tabs) | Window opens | `[ ]` |
| 5.2 | Tạo `src/gui/function1_view.py` | Convert UI works | `[ ]` |
| 5.3 | Tạo `src/gui/function2_view.py` | Generate UI works | `[ ]` |
| 5.4 | Tạo `src/gui/settings_view.py` | Save settings | `[ ]` |
| 5.5 | Tạo `src/i18n/` (vi.yaml, en.yaml) | Language switch works | `[ ]` |

---

## ✅ Phase 6: Build & Test (Day 12-13)

> **Dependencies**: All phases

| # | Task | Verify | Status |
|---|------|--------|--------|
| 6.1 | Viết unit tests (`tests/`) | Coverage ≥80% | `[ ]` |
| 6.2 | Test integration với sample files | All workflows pass | `[ ]` |
| 6.3 | Build EXE với PyInstaller | .exe runs standalone | `[ ]` |
| 6.4 | Create README.md + User Guide | Docs complete | `[ ]` |

---

## 🔗 Dependencies Graph

```
Phase 0 (Setup)
    │
    ├──► Phase 1 (F2 Core) ──► Phase 2 (F2 Converters) ──┐
    │                                                     │
    └──► Phase 3 (F1 Core) ──────────────────────────────┤
                                                          │
                                                          ▼
                                                    Phase 4 (CLI)
                                                          │
                                                          ▼
                                                    Phase 5 (GUI)
                                                          │
                                                          ▼
                                                    Phase 6 (Build)
```

---

## 🏁 Done When

- [ ] `adm --help` shows all commands
- [ ] `adm-convert` processes PDF/DOCX → LaTeX
- [ ] `adm-generate` creates DOCX/PDF from Markdown
- [ ] GUI runs with Function 1/2 tabs
- [ ] .exe file runs on clean Windows machine
- [ ] All tests pass (≥80% coverage)
