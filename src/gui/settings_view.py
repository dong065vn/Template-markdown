"""
Settings View
===============
GUI for application settings
"""

import os

try:
    import customtkinter as ctk
except ImportError:
    pass


class SettingsView(ctk.CTkFrame):
    """Settings tab view"""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self._create_ui()
    
    def _create_ui(self):
        """Create the UI components"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="⚙️ Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(20, 10))
        
        # Appearance
        appear_frame = ctk.CTkFrame(self)
        appear_frame.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkLabel(
            appear_frame,
            text="🎨 Appearance",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        inner1 = ctk.CTkFrame(appear_frame, fg_color="transparent")
        inner1.pack(fill="x", padx=15, pady=10)
        
        # Theme
        ctk.CTkLabel(inner1, text="Theme:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.theme_var = ctk.StringVar(value="dark")
        theme_menu = ctk.CTkOptionMenu(
            inner1,
            variable=self.theme_var,
            values=["dark", "light", "system"],
            command=self._change_theme
        )
        theme_menu.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Color
        ctk.CTkLabel(inner1, text="Color:").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.color_var = ctk.StringVar(value="blue")
        color_menu = ctk.CTkOptionMenu(
            inner1,
            variable=self.color_var,
            values=["blue", "green", "dark-blue"],
            command=self._change_color
        )
        color_menu.grid(row=0, column=3, padx=10, pady=5, sticky="w")
        
        # Paths
        paths_frame = ctk.CTkFrame(self)
        paths_frame.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkLabel(
            paths_frame,
            text="📁 Paths",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        inner2 = ctk.CTkFrame(paths_frame, fg_color="transparent")
        inner2.pack(fill="x", padx=15, pady=10)
        
        # Function 1 input
        ctk.CTkLabel(inner2, text="F1 Input:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.f1_input = ctk.CTkEntry(inner2, width=300)
        self.f1_input.grid(row=0, column=1, padx=10, pady=5)
        self.f1_input.insert(0, "function1/input")
        
        # Function 1 output
        ctk.CTkLabel(inner2, text="F1 Output:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.f1_output = ctk.CTkEntry(inner2, width=300)
        self.f1_output.grid(row=1, column=1, padx=10, pady=5)
        self.f1_output.insert(0, "function1/output")
        
        # Function 2 project
        ctk.CTkLabel(inner2, text="F2 Project:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.f2_project = ctk.CTkEntry(inner2, width=300)
        self.f2_project.grid(row=2, column=1, padx=10, pady=5)
        self.f2_project.insert(0, "function2/Segmentation")
        
        # Format settings
        format_frame = ctk.CTkFrame(self)
        format_frame.pack(fill="x", padx=40, pady=10)
        
        ctk.CTkLabel(
            format_frame,
            text="📝 Format Settings (NĐ30/2020)",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        inner3 = ctk.CTkFrame(format_frame, fg_color="transparent")
        inner3.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(inner3, text="Font:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.font_var = ctk.StringVar(value="Times New Roman")
        ctk.CTkOptionMenu(
            inner3,
            variable=self.font_var,
            values=["Times New Roman", "Arial", "Calibri"]
        ).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(inner3, text="Size:").grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.size_var = ctk.StringVar(value="14")
        ctk.CTkOptionMenu(
            inner3,
            variable=self.size_var,
            values=["12", "13", "14"]
        ).grid(row=0, column=3, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(inner3, text="Line Spacing:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.spacing_var = ctk.StringVar(value="1.5")
        ctk.CTkOptionMenu(
            inner3,
            variable=self.spacing_var,
            values=["1.0", "1.15", "1.5", "2.0"]
        ).grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # Save button
        ctk.CTkButton(
            self,
            text="💾 Save Settings",
            command=self._save_settings
        ).pack(pady=20)
        
        # Status
        self.status = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.status.pack(pady=5)
    
    def _change_theme(self, value):
        """Change appearance theme"""
        ctk.set_appearance_mode(value)
    
    def _change_color(self, value):
        """Change color theme"""
        ctk.set_default_color_theme(value)
    
    def _save_settings(self):
        """Save settings to config"""
        try:
            from src.core.config import get_config
            
            config = get_config()
            config.set("appearance.theme", self.theme_var.get())
            config.set("appearance.color", self.color_var.get())
            config.set("paths.f1_input", self.f1_input.get())
            config.set("paths.f1_output", self.f1_output.get())
            config.set("paths.f2_project", self.f2_project.get())
            config.set("format.font", self.font_var.get())
            config.set("format.size", int(self.size_var.get()))
            config.set("format.line_spacing", float(self.spacing_var.get()))
            config.save()
            
            self.status.configure(text="✅ Settings saved!", text_color="green")
            
        except Exception as e:
            self.status.configure(text=f"❌ Error: {e}", text_color="red")
