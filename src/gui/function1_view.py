"""
Function 1 View - Convert
==========================
GUI for PDF/DOCX → Markdown → LaTeX conversion
"""

import os
from pathlib import Path
import threading

try:
    import customtkinter as ctk
    from tkinter import filedialog
except ImportError:
    pass


class Function1View(ctk.CTkFrame):
    """Convert tab view"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.selected_files = []
        self._create_ui()
    
    def _create_ui(self):
        """Create the UI components"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="🔄 Function 1: Convert",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(20, 10))
        
        desc = ctk.CTkLabel(
            self,
            text="Chuyển đổi PDF/DOCX → Markdown → LaTeX",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        desc.pack(pady=(0, 20))
        
        # Input section
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkLabel(
            input_frame,
            text="📁 Input Files:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        # File list
        self.file_listbox = ctk.CTkTextbox(input_frame, height=100)
        self.file_listbox.pack(fill="x", padx=15, pady=5)
        self.file_listbox.insert("1.0", "(No files selected)")
        self.file_listbox.configure(state="disabled")
        
        # Buttons
        btn_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkButton(
            btn_frame,
            text="📂 Select Files",
            command=self._select_files
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="📁 Select Folder",
            command=self._select_folder
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="🗑️ Clear",
            fg_color="gray",
            command=self._clear_files
        ).pack(side="left", padx=5)
        
        # Options
        options_frame = ctk.CTkFrame(self)
        options_frame.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkLabel(
            options_frame,
            text="⚙️ Options:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 5))
        
        opt_inner = ctk.CTkFrame(options_frame, fg_color="transparent")
        opt_inner.pack(fill="x", padx=15, pady=10)
        
        # Format
        ctk.CTkLabel(opt_inner, text="Format:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.format_var = ctk.StringVar(value="latex")
        ctk.CTkOptionMenu(
            opt_inner,
            variable=self.format_var,
            values=["latex", "markdown", "both"]
        ).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Split level
        ctk.CTkLabel(opt_inner, text="Split Level:").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.split_var = ctk.StringVar(value="1")
        ctk.CTkOptionMenu(
            opt_inner,
            variable=self.split_var,
            values=["1", "2", "3"]
        ).grid(row=0, column=3, padx=10, pady=5, sticky="w")
        
        # Convert button
        self.convert_btn = ctk.CTkButton(
            self,
            text="🚀 Convert",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            command=self._convert
        )
        self.convert_btn.pack(pady=20)
        
        # Progress
        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.pack(pady=10)
        self.progress.set(0)
        
        # Status
        self.status = ctk.CTkLabel(
            self,
            text="Ready to convert",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.status.pack(pady=5)
    
    def _select_files(self):
        """Select files dialog"""
        files = filedialog.askopenfilenames(
            title="Select PDF/DOCX files",
            filetypes=[
                ("Documents", "*.pdf *.docx"),
                ("PDF files", "*.pdf"),
                ("Word files", "*.docx")
            ]
        )
        if files:
            self.selected_files = list(files)
            self._update_file_list()
    
    def _select_folder(self):
        """Select folder dialog"""
        folder = filedialog.askdirectory(title="Select folder")
        if folder:
            folder_path = Path(folder)
            files = list(folder_path.glob("*.pdf")) + list(folder_path.glob("*.docx"))
            self.selected_files = [str(f) for f in files]
            self._update_file_list()
    
    def _clear_files(self):
        """Clear selected files"""
        self.selected_files = []
        self._update_file_list()
    
    def _update_file_list(self):
        """Update file list display"""
        self.file_listbox.configure(state="normal")
        self.file_listbox.delete("1.0", "end")
        
        if self.selected_files:
            for f in self.selected_files:
                self.file_listbox.insert("end", f"• {Path(f).name}\n")
        else:
            self.file_listbox.insert("1.0", "(No files selected)")
        
        self.file_listbox.configure(state="disabled")
    
    def _convert(self):
        """Run conversion"""
        if not self.selected_files:
            self.status.configure(text="⚠️ No files selected!", text_color="orange")
            return
        
        self.convert_btn.configure(state="disabled")
        self.status.configure(text="Converting...", text_color="white")
        self.progress.set(0)
        
        # Run in thread
        thread = threading.Thread(target=self._do_convert)
        thread.start()
    
    def _do_convert(self):
        """Actual conversion in background"""
        total = len(self.selected_files)
        
        for i, filepath in enumerate(self.selected_files):
            try:
                # Update progress
                self.after(0, lambda p=(i/total): self.progress.set(p))
                self.after(0, lambda f=filepath: self.status.configure(
                    text=f"Converting: {Path(f).name}..."
                ))
                
                # Do conversion
                ext = Path(filepath).suffix.lower()
                if ext == '.pdf':
                    from function1.parsers.pdf_parser import parse_pdf
                    doc = parse_pdf(filepath)
                else:
                    from function1.parsers.docx_parser import parse_docx
                    doc = parse_docx(filepath)
                
                # Split
                from function1.processors.splitter import Splitter
                splitter = Splitter(int(self.split_var.get()))
                chunks = splitter.split(doc)
                
                # Export
                output_dir = Path("function1/output") / Path(filepath).stem
                output_dir.mkdir(parents=True, exist_ok=True)
                
                fmt = self.format_var.get()
                if fmt in ['markdown', 'both']:
                    splitter.save_chunks(chunks, str(output_dir / "markdown"))
                
                if fmt in ['latex', 'both']:
                    from function1.exporters.latex_exporter import LaTeXExporter
                    exporter = LaTeXExporter()
                    exporter.export_sections(chunks, str(output_dir / "latex"))
                
            except Exception as e:
                self.after(0, lambda e=e: self.status.configure(
                    text=f"❌ Error: {str(e)[:50]}",
                    text_color="red"
                ))
        
        # Done
        self.after(0, lambda: self.progress.set(1))
        self.after(0, lambda: self.status.configure(
            text=f"✅ Converted {total} files!",
            text_color="green"
        ))
        self.after(0, lambda: self.convert_btn.configure(state="normal"))
