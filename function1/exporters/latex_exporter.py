"""
LaTeX Exporter
===============
Export Document IR to LaTeX format
"""

import os
from pathlib import Path
from typing import List, Optional, Dict
from string import Template

from function1.parsers.ir import Document, Section, Block, BlockType, Run


# LaTeX templates
MAIN_TEMPLATE = Template(r"""
\documentclass[12pt,a4paper]{report}

% ===== PACKAGES =====
\usepackage[utf8]{inputenc}
\usepackage[vietnamese]{babel}
\usepackage{times}
\usepackage{geometry}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{indentfirst}
\usepackage{setspace}
\usepackage{fancyhdr}
\usepackage{tocloft}
\usepackage{titlesec}
\usepackage{longtable}

% ===== PAGE SETUP (NĐ30/2020) =====
\geometry{
    a4paper,
    top=20mm,
    bottom=20mm,
    left=30mm,
    right=15mm
}

% ===== FONTS =====
\renewcommand{\rmdefault}{ptm}  % Times New Roman

% ===== LINE SPACING =====
\onehalfspacing

% ===== PARAGRAPH INDENT =====
\setlength{\parindent}{1.27cm}

% ===== TITLE FORMATTING =====
\titleformat{\chapter}[display]
{\normalfont\bfseries\centering}
{\MakeUppercase{\chaptertitlename}\ \thechapter}{12pt}{\MakeUppercase}

\titleformat{\section}
{\normalfont\bfseries}
{\thesection}{1em}{}

\titleformat{\subsection}
{\normalfont\bfseries\itshape}
{\thesubsection}{1em}{}

% ===== DOCUMENT INFO =====
\title{$title}
\author{$author}
\date{$date}

\begin{document}

% ===== FRONT MATTER =====
\maketitle
\tableofcontents

% ===== MAIN CONTENT =====
$content

% ===== BIBLIOGRAPHY =====
% \bibliographystyle{plain}
% \bibliography{references}

\end{document}
""")

CHAPTER_TEMPLATE = Template(r"""
\chapter{$title}
\label{ch:$label}

$content
""")

SECTION_TEMPLATE = Template(r"""
\section{$title}
\label{sec:$label}

$content
""")


class LaTeXExporter:
    """Export Document IR to LaTeX"""
    
    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or "."
    
    def export(self, document: Document, output_path: str = None) -> str:
        """
        Export document to LaTeX
        
        Args:
            document: Document IR
            output_path: Output .tex file path
        
        Returns:
            Path to main.tex
        """
        if output_path is None:
            output_path = os.path.join(self.output_dir, "main.tex")
        
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        
        # Generate content from sections
        content_parts = []
        for section in document.sections:
            content_parts.append(self._export_section(section))
        
        content = "\n\n".join(content_parts)
        
        # Fill main template
        from datetime import datetime
        
        latex = MAIN_TEMPLATE.substitute(
            title=self._escape_latex(document.title),
            author=self._escape_latex(document.author),
            date=datetime.now().strftime("%d/%m/%Y"),
            content=content
        )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(latex)
        
        print(f"✅ Exported: {output_path}")
        return output_path
    
    def export_sections(self, sections: List[Section], output_dir: str) -> List[str]:
        """
        Export each section to separate .tex file
        
        Args:
            sections: List của Section
            output_dir: Output directory
        
        Returns:
            List đường dẫn các files
        """
        os.makedirs(output_dir, exist_ok=True)
        saved_files = []
        
        for i, section in enumerate(sections, 1):
            filename = f"chapter_{i:02d}.tex"
            filepath = os.path.join(output_dir, filename)
            
            latex = self._export_section(section)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(latex)
            
            saved_files.append(filepath)
            print(f"✓ Saved: {filename}")
        
        # Create main.tex that includes all chapters
        self._create_main_include(saved_files, output_dir)
        
        return saved_files
    
    def _create_main_include(self, chapter_files: List[str], output_dir: str):
        """Create main.tex that includes all chapter files"""
        includes = []
        for filepath in chapter_files:
            filename = os.path.basename(filepath)
            name_without_ext = os.path.splitext(filename)[0]
            includes.append(f"\\input{{{name_without_ext}}}")
        
        content = "\n".join(includes)
        
        from datetime import datetime
        
        latex = MAIN_TEMPLATE.substitute(
            title="Document",
            author="Author",
            date=datetime.now().strftime("%d/%m/%Y"),
            content=content
        )
        
        main_path = os.path.join(output_dir, "main.tex")
        with open(main_path, 'w', encoding='utf-8') as f:
            f.write(latex)
        
        print(f"✅ Created: main.tex (includes {len(chapter_files)} chapters)")
    
    def _export_section(self, section: Section) -> str:
        """Export single section to LaTeX"""
        lines = []
        
        # Add chapter/section header
        if section.level == 1:
            label = self._make_label(section.title)
            lines.append(f"\\chapter{{{self._escape_latex(section.title)}}}")
            lines.append(f"\\label{{ch:{label}}}")
        elif section.level == 2:
            label = self._make_label(section.title)
            lines.append(f"\\section{{{self._escape_latex(section.title)}}}")
            lines.append(f"\\label{{sec:{label}}}")
        
        lines.append("")
        
        # Export blocks
        for block in section.blocks:
            lines.append(self._export_block(block))
        
        return "\n".join(lines)
    
    def _export_block(self, block: Block) -> str:
        """Export single block to LaTeX"""
        if block.type == BlockType.HEADING:
            level = block.level
            text = self._runs_to_latex(block.runs)
            
            if level == 2:
                return f"\\section{{{text}}}\n"
            elif level == 3:
                return f"\\subsection{{{text}}}\n"
            elif level == 4:
                return f"\\subsubsection{{{text}}}\n"
            else:
                return f"\\paragraph{{{text}}}\n"
        
        elif block.type == BlockType.PARAGRAPH:
            text = self._runs_to_latex(block.runs)
            return f"{text}\n"
        
        elif block.type == BlockType.LIST:
            env = "enumerate" if block.ordered else "itemize"
            items = []
            for item in block.items:
                item_text = self._runs_to_latex(item.content)
                items.append(f"\\item {item_text}")
            
            return f"\\begin{{{env}}}\n" + "\n".join(items) + f"\n\\end{{{env}}}\n"
        
        elif block.type == BlockType.QUOTE:
            text = self._runs_to_latex(block.runs)
            return f"\\begin{{quote}}\n{text}\n\\end{{quote}}\n"
        
        elif block.type == BlockType.TABLE:
            return self._export_table(block)
        
        elif block.type == BlockType.IMAGE:
            if block.image_path:
                return f"\\includegraphics[width=0.8\\textwidth]{{{block.image_path}}}\n"
            return ""
        
        return ""
    
    def _export_table(self, block: Block) -> str:
        """Export table block to LaTeX"""
        if not block.rows:
            return ""
        
        num_cols = len(block.rows[0].cells) if block.rows else 0
        col_spec = "|" + "l|" * num_cols
        
        lines = [f"\\begin{{tabular}}{{{col_spec}}}"]
        lines.append("\\hline")
        
        for row in block.rows:
            cells = [self._runs_to_latex(cell.content) for cell in row.cells]
            lines.append(" & ".join(cells) + " \\\\")
            lines.append("\\hline")
        
        lines.append("\\end{tabular}")
        return "\n".join(lines) + "\n"
    
    def _runs_to_latex(self, runs: List[Run]) -> str:
        """Convert runs to LaTeX text"""
        parts = []
        for run in runs:
            text = self._escape_latex(run.text)
            if run.bold and run.italic:
                text = f"\\textbf{{\\textit{{{text}}}}}"
            elif run.bold:
                text = f"\\textbf{{{text}}}"
            elif run.italic:
                text = f"\\textit{{{text}}}"
            parts.append(text)
        return "".join(parts)
    
    def _escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters"""
        if not text:
            return ""
        
        replacements = {
            '\\': '\\textbackslash{}',
            '&': '\\&',
            '%': '\\%',
            '$': '\\$',
            '#': '\\#',
            '_': '\\_',
            '{': '\\{',
            '}': '\\}',
            '~': '\\textasciitilde{}',
            '^': '\\textasciicircum{}',
        }
        
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        
        return text
    
    def _make_label(self, text: str) -> str:
        """Create safe label from text"""
        safe = "".join(c if c.isalnum() else "_" for c in text.lower())
        return safe[:30]


def export_to_latex(document: Document, output_path: str) -> str:
    """
    Hàm tiện ích để export document sang LaTeX
    
    Args:
        document: Document IR
        output_path: Output file path
    
    Returns:
        Path to main.tex
    
    Example:
        >>> from function1.parsers import parse_pdf
        >>> doc = parse_pdf("thesis.pdf")
        >>> export_to_latex(doc, "output/main.tex")
    """
    exporter = LaTeXExporter()
    return exporter.export(document, output_path)


if __name__ == "__main__":
    # Test
    from function1.parsers.ir import create_paragraph, create_heading, create_list
    
    doc = Document(title="Test Thesis", author="Author Name")
    
    section = Section(title="Chapter 1: Introduction", level=1)
    section.blocks.append(create_heading("Background", 2))
    section.blocks.append(create_paragraph("This is the first paragraph."))
    section.blocks.append(create_list(["Item 1", "Item 2", "Item 3"]))
    
    doc.sections.append(section)
    
    exporter = LaTeXExporter()
    exporter.export(doc, "test_output.tex")
    
    with open("test_output.tex", 'r') as f:
        print(f.read()[:1000])
