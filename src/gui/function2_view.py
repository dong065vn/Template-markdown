"""
Function 2 View - Generate
===========================
GUI for AI Content → Markdown → DOCX/PDF generation
"""

import os
from pathlib import Path
import threading

try:
    import customtkinter as ctk
    from tkinter import filedialog
except ImportError:
    pass


class Function2View(ctk.CTkFrame):
    """Generate tab view"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the UI components"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="✨ Function 2: Generate",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(20, 10))
        
        desc = ctk.CTkLabel(
            self,
            text="Tạo tài liệu từ AI content → DOCX/PDF (NĐ30/2020)",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        desc.pack(pady=(0, 20))
        
        # Workflow steps
        steps_frame = ctk.CTkFrame(self)
        steps_frame.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkLabel(
            steps_frame,
            text="🔄 Workflow 3 Bước:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Step 1: Init
        step1 = ctk.CTkFrame(steps_frame)
        step1.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(step1, text="1️⃣ Init Project", width=120).pack(side="left", padx=10)
        
        self.project_name = ctk.CTkEntry(step1, placeholder_text="Tên dự án...", width=200)
        self.project_name.pack(side="left", padx=5)
        
        self.doc_type = ctk.CTkOptionMenu(step1, values=["thesis", "report"], width=100)
        self.doc_type.pack(side="left", padx=5)
        
        self.pages = ctk.CTkEntry(step1, placeholder_text="Pages", width=60)
        self.pages.pack(side="left", padx=5)
        self.pages.insert(0, "80")
        
        ctk.CTkButton(
            step1,
            text="Init",
            width=80,
            command=self._init_project
        ).pack(side="left", padx=10)
        
        # Step 2: Sections
        step2 = ctk.CTkFrame(steps_frame)
        step2.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(step2, text="2️⃣ Generate Sections", width=120).pack(side="left", padx=10)
        
        ctk.CTkButton(
            step2,
            text="Generate",
            width=80,
            command=self._generate_sections
        ).pack(side="left", padx=10)
        
        ctk.CTkLabel(
            step2,
            text="→ Dùng AI viết content → Lưu vào phase3_content/",
            text_color="gray"
        ).pack(side="left", padx=10)
        
        # Step 3: Export & Merge
        step3 = ctk.CTkFrame(steps_frame)
        step3.pack(fill="x", padx=15, pady=5)
        
        ctk.CTkLabel(step3, text="3️⃣ Export & Merge", width=120).pack(side="left", padx=10)
        
        self.export_format = ctk.CTkOptionMenu(step3, values=["all", "docx", "pdf"], width=80)
        self.export_format.pack(side="left", padx=5)
        
        ctk.CTkButton(
            step3,
            text="Export",
            width=80,
            command=self._export
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            step3,
            text="Merge",
            width=80,
            command=self._merge
        ).pack(side="left", padx=5)
        
        # ZOLO Mode
        zolo_frame = ctk.CTkFrame(self, fg_color="#1a4d1a")
        zolo_frame.pack(fill="x", padx=40, pady=20)
        
        ctk.CTkLabel(
            zolo_frame,
            text="⚡ ZOLO Mode - One-Shot Setup",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        zolo_inner = ctk.CTkFrame(zolo_frame, fg_color="transparent")
        zolo_inner.pack(fill="x", padx=15, pady=10)
        
        self.zolo_name = ctk.CTkEntry(zolo_inner, placeholder_text="Tên luận văn...", width=250)
        self.zolo_name.pack(side="left", padx=5)
        
        self.zolo_pages = ctk.CTkEntry(zolo_inner, placeholder_text="Pages", width=60)
        self.zolo_pages.pack(side="left", padx=5)
        self.zolo_pages.insert(0, "80")
        
        ctk.CTkButton(
            zolo_inner,
            text="🚀 ZOLO!",
            font=ctk.CTkFont(weight="bold"),
            fg_color="#2d7d2d",
            command=self._zolo
        ).pack(side="left", padx=10)
        
        # Progress & Status
        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.pack(pady=(30, 10))
        self.progress.set(0)
        
        self.status = ctk.CTkLabel(
            self,
            text="Ready",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.status.pack(pady=5)
        
        # Output info
        out_frame = ctk.CTkFrame(self)
        out_frame.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkLabel(
            out_frame,
            text="📂 Output: function2/Segmentation/phase5_output/",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(padx=15, pady=10)
    
    def _init_project(self):
        """Initialize new project"""
        name = self.project_name.get() or "Untitled"
        doc_type = self.doc_type.get()
        pages = int(self.pages.get() or "80")
        
        self.status.configure(text=f"Initializing: {name}...", text_color="white")
        
        try:
            from function2.generators.section_generator import init_project
            
            init_project(
                project_dir="function2/Segmentation",
                project_name=name,
                document_type=doc_type,
                total_pages=pages
            )
            
            self.status.configure(text=f"✅ Initialized: {name}", text_color="green")
            self.progress.set(0.33)
            
        except Exception as e:
            self.status.configure(text=f"❌ Error: {e}", text_color="red")
    
    def _generate_sections(self):
        """Generate section files"""
        self.status.configure(text="Generating sections...", text_color="white")
        
        try:
            from function2.generators.section_generator import SectionGenerator
            
            generator = SectionGenerator("function2/Segmentation")
            generator.generate_sections()
            
            self.status.configure(text="✅ Sections generated!", text_color="green")
            self.progress.set(0.5)
            
        except Exception as e:
            self.status.configure(text=f"❌ Error: {e}", text_color="red")
    
    def _export(self):
        """Export to DOCX/PDF"""
        fmt = self.export_format.get()
        self.status.configure(text=f"Exporting ({fmt})...", text_color="white")
        
        thread = threading.Thread(target=self._do_export, args=(fmt,))
        thread.start()
    
    def _do_export(self, fmt):
        """Export in background"""
        try:
            md_folder = Path("function2/Segmentation/phase3_content")
            
            if not md_folder.exists() or not list(md_folder.glob("*.md")):
                self.after(0, lambda: self.status.configure(
                    text="⚠️ No content in phase3_content/",
                    text_color="orange"
                ))
                return
            
            output = Path("function2/Segmentation/phase4_rendered")
            
            if fmt in ['docx', 'all']:
                from function2.templates.converters.md_to_docx import convert_folder
                convert_folder(str(md_folder), str(output / "docx"))
            
            if fmt in ['pdf', 'all']:
                try:
                    from function2.templates.converters.md_to_pdf import convert_folder_to_pdf
                    convert_folder_to_pdf(str(md_folder), str(output / "pdf"))
                except ImportError:
                    pass
            
            self.after(0, lambda: self.status.configure(
                text="✅ Export complete!",
                text_color="green"
            ))
            self.after(0, lambda: self.progress.set(0.75))
            
        except Exception as e:
            self.after(0, lambda: self.status.configure(
                text=f"❌ Error: {e}",
                text_color="red"
            ))
    
    def _merge(self):
        """Merge all sections"""
        self.status.configure(text="Merging...", text_color="white")
        
        try:
            docx_folder = Path("function2/Segmentation/phase4_rendered/docx")
            
            if not docx_folder.exists():
                self.status.configure(text="⚠️ Export first!", text_color="orange")
                return
            
            from function2.templates.converters.docx_merger import merge_docx_folder
            
            output = "function2/Segmentation/phase5_output/MERGED_document.docx"
            merge_docx_folder(str(docx_folder), output)
            
            self.status.configure(text="✅ Merged! Check phase5_output/", text_color="green")
            self.progress.set(1)
            
        except Exception as e:
            self.status.configure(text=f"❌ Error: {e}", text_color="red")
    
    def _zolo(self):
        """ZOLO one-shot mode"""
        name = self.zolo_name.get() or "Luận văn"
        pages = int(self.zolo_pages.get() or "80")
        
        self.status.configure(text="⚡ ZOLO Mode...", text_color="yellow")
        
        try:
            from function2.generators.section_generator import init_project, SectionGenerator
            
            init_project(
                project_dir="function2/Segmentation",
                project_name=name,
                document_type="thesis",
                total_pages=pages
            )
            
            generator = SectionGenerator("function2/Segmentation")
            generator.generate_sections()
            
            self.status.configure(
                text="✅ ZOLO Complete! Check phase2_sections/",
                text_color="green"
            )
            self.progress.set(0.5)
            
        except Exception as e:
            self.status.configure(text=f"❌ Error: {e}", text_color="red")
