"""
ADM Main Window
================
Main GUI application with tabs for Function 1/2/Settings
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    import customtkinter as ctk
except ImportError:
    print("⚠ CustomTkinter not installed. Install with:")
    print("   pip install customtkinter")
    sys.exit(1)

from src.gui.function1_view import Function1View
from src.gui.function2_view import Function2View
from src.gui.settings_view import SettingsView


class MainWindow(ctk.CTk):
    """Main Application Window"""
    
    def __init__(self):
        super().__init__()
        
        # Window config
        self.title("ADM - Academic Document Manager v1.0")
        self.geometry("900x650")
        self.minsize(800, 600)
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create UI
        self._create_header()
        self._create_tabs()
        self._create_footer()
    
    def _create_header(self):
        """Create header with title"""
        header = ctk.CTkFrame(self, height=60, corner_radius=0)
        header.pack(fill="x", padx=10, pady=(10, 5))
        header.pack_propagate(False)
        
        title = ctk.CTkLabel(
            header, 
            text="📄 Academic Document Manager",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(side="left", padx=20, pady=10)
        
        version = ctk.CTkLabel(
            header,
            text="v1.0.0",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        version.pack(side="right", padx=20, pady=10)
    
    def _create_tabs(self):
        """Create tabbed interface"""
        self.tabview = ctk.CTkTabview(self, corner_radius=10)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Add tabs
        self.tab_convert = self.tabview.add("🔄 Convert")
        self.tab_generate = self.tabview.add("✨ Generate")
        self.tab_settings = self.tabview.add("⚙️ Settings")
        
        # Add views to tabs
        Function1View(self.tab_convert).pack(fill="both", expand=True)
        Function2View(self.tab_generate).pack(fill="both", expand=True)
        SettingsView(self.tab_settings).pack(fill="both", expand=True)
    
    def _create_footer(self):
        """Create footer with status"""
        footer = ctk.CTkFrame(self, height=30, corner_radius=0)
        footer.pack(fill="x", padx=10, pady=(5, 10))
        footer.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            footer,
            text="Ready",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.status_label.pack(side="left", padx=10)
        
        help_btn = ctk.CTkButton(
            footer,
            text="Help",
            width=60,
            height=24,
            font=ctk.CTkFont(size=11),
            command=self._show_help
        )
        help_btn.pack(side="right", padx=10)
    
    def _show_help(self):
        """Show help dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Help")
        dialog.geometry("400x300")
        dialog.transient(self)
        
        text = ctk.CTkTextbox(dialog, wrap="word")
        text.pack(fill="both", expand=True, padx=10, pady=10)
        
        help_text = """
📄 Academic Document Manager (ADM) v1.0

FUNCTION 1: CONVERT
- Chuyển đổi PDF/DOCX sang Markdown và LaTeX
- Drop file vào input/ hoặc chọn file
- Kết quả trong output/

FUNCTION 2: GENERATE
- Tạo tài liệu từ AI content
- Workflow: Init → Sections → Export → Merge
- Chuẩn format NĐ30/2020

SETTINGS
- Cài đặt theme, ngôn ngữ
- Cấu hình đường dẫn

CLI Commands:
  python main.py convert --help
  python main.py generate --help
"""
        text.insert("1.0", help_text)
        text.configure(state="disabled")
    
    def set_status(self, message: str):
        """Update status bar"""
        self.status_label.configure(text=message)


def main():
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
