# Task: Brainstorming Academic Document Tool

## Mục tiêu
Thu thập và xác nhận yêu cầu cho tool Python xử lý văn bản học thuật (luận văn, báo cáo) theo workflow /brainstorm.

## Checklist

### 1. Thu thập Requirements
- [x] Đọc file `y-tuong-du-an.md` - Ý tưởng pipeline Word → LaTeX
- [x] Đọc file `gop-y-them.md` - Ý tưởng PDM từ video ItsDD
- [x] Đọc folder `Van Ban, Nghi Dinh ve INAN` - Quy chuẩn Nghị định 30/2020
- [x] Xác nhận yêu cầu với user

### 2. Tổng hợp Understanding Summary
- [x] Tạo Understanding Summary (5-7 bullets)
- [x] Liệt kê Assumptions
- [x] Xác định Open Questions (nếu có)

### 3. Đề xuất Design Options
- [x] Phương án 1: Modular Multi-Pipeline Architecture
- [x] Phương án 2: Plugin-based Architecture
- [x] So sánh ưu/nhược điểm

### 4. Hoàn thành Brainstorm
- [x] Tạo Decision Log
- [x] Xác nhận với user trước khi sang Planning

### 5. Implementation Plan
- [x] Tạo Implementation Plan chi tiết
- [x] Cập nhật PDM Workflow cho Function 2
- [x] User review và xác nhận plan

### 6. PRD Document
- [x] Viết Problem Statement
- [x] Định nghĩa Solution & Features
- [x] Tạo User Stories
- [x] Xác định Success Metrics
- [x] List Out of Scope
- [x] RICE prioritization
- [x] User review PRD

### 7. Python Templates (NĐ30/2020)
- [/] Tạo base template với styles chuẩn
- [ ] Template: Luận văn/Thesis
- [ ] Template: Báo cáo/Report
- [ ] Template: Công văn
- [ ] Template: Quyết định
- [ ] Template: Tờ trình
- [ ] Rule bases cho AI

### 8. Function 2 - PDM Workflow (3 bước)
- [ ] Bước 1: Init (tạo PRD.md + config)
- [ ] Bước 2: Generate Markdown (AI via Antigravity)
- [ ] Bước 3: Python Convert (MD → DOCX)
