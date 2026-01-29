"""
Markdown to PDF Converter
==========================
Chuyển đổi Markdown thành PDF thông qua HTML + WeasyPrint
"""

import os
from pathlib import Path
from typing import Optional, List

# Try to import weasyprint, fallback to basic method if not available
try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

import mistune


# CSS styles theo NĐ30/2020
ND30_CSS = """
@page {
    size: A4;
    margin: 2cm 1.5cm 2cm 3cm;  /* top right bottom left */
}

body {
    font-family: 'Times New Roman', serif;
    font-size: 14pt;
    line-height: 1.5;
    text-align: justify;
}

h1 {
    font-size: 14pt;
    font-weight: bold;
    text-align: center;
    text-transform: uppercase;
    margin-top: 12pt;
    margin-bottom: 6pt;
}

h2 {
    font-size: 14pt;
    font-weight: bold;
    text-align: left;
    margin-top: 12pt;
    margin-bottom: 6pt;
}

h3 {
    font-size: 14pt;
    font-weight: bold;
    font-style: italic;
    margin-left: 1.27cm;
    margin-top: 6pt;
    margin-bottom: 6pt;
}

p {
    text-indent: 1.27cm;
    margin: 0 0 6pt 0;
}

ul, ol {
    margin-left: 1.27cm;
    margin-bottom: 6pt;
}

blockquote {
    margin-left: 2cm;
    margin-right: 1cm;
    font-style: italic;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 12pt 0;
}

th, td {
    border: 1px solid black;
    padding: 6pt;
    text-align: left;
}

th {
    background-color: #f0f0f0;
    font-weight: bold;
}
"""


class MarkdownToPdf:
    """Chuyển đổi Markdown sang PDF với styles chuẩn NĐ30/2020"""
    
    def __init__(self, custom_css: str = None):
        self.css = custom_css or ND30_CSS
        self.markdown_parser = mistune.create_markdown(escape=False)
    
    def convert_file(self, md_path: str, output_path: str = None) -> str:
        """
        Chuyển đổi file Markdown sang PDF
        
        Args:
            md_path: Đường dẫn file Markdown
            output_path: Đường dẫn file output (optional)
        
        Returns:
            Đường dẫn file PDF đã tạo
        """
        if not os.path.exists(md_path):
            raise FileNotFoundError(f"File not found: {md_path}")
        
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        if output_path is None:
            output_path = str(Path(md_path).with_suffix('.pdf'))
        
        return self.convert_content(md_content, output_path)
    
    def convert_content(self, md_content: str, output_path: str) -> str:
        """
        Chuyển đổi nội dung Markdown sang PDF
        
        Args:
            md_content: Nội dung Markdown
            output_path: Đường dẫn file output
        
        Returns:
            Đường dẫn file PDF đã tạo
        """
        if not WEASYPRINT_AVAILABLE:
            raise ImportError(
                "WeasyPrint is not installed. "
                "Install with: pip install weasyprint"
            )
        
        # Convert Markdown to HTML
        html_content = self.markdown_parser(md_content)
        
        # Wrap in full HTML document
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>{self.css}</style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        
        # Convert to PDF
        HTML(string=full_html).write_pdf(output_path)
        
        print(f"✅ Saved PDF: {output_path}")
        return output_path


def convert_md_to_pdf(md_path: str, output_path: str = None) -> str:
    """
    Hàm tiện ích để chuyển đổi Markdown sang PDF
    
    Args:
        md_path: Đường dẫn file Markdown
        output_path: Đường dẫn output (optional)
    
    Returns:
        Đường dẫn file PDF
    
    Example:
        >>> convert_md_to_pdf('content_001.md', 'section_001.pdf')
    """
    converter = MarkdownToPdf()
    return converter.convert_file(md_path, output_path)


def convert_folder_to_pdf(input_folder: str, output_folder: str,
                          pattern: str = "*.md") -> List[str]:
    """
    Chuyển đổi tất cả file MD trong folder sang PDF
    
    Args:
        input_folder: Folder chứa file MD
        output_folder: Folder output
        pattern: Pattern filter
    
    Returns:
        List đường dẫn files đã tạo
    """
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    
    files = sorted(input_path.glob(pattern))
    results = []
    
    for md_file in files:
        pdf_name = md_file.stem + '.pdf'
        pdf_path = output_path / pdf_name
        
        try:
            result = convert_md_to_pdf(str(md_file), str(pdf_path))
            results.append(result)
        except ImportError as e:
            print(f"⚠ Skipped {md_file.name}: {e}")
    
    print(f"\n✅ Converted {len(results)} files to PDF")
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert Markdown to PDF")
    parser.add_argument('--file', '-f', help='Single MD file to convert')
    parser.add_argument('--folder', '-d', help='Folder containing MD files')
    parser.add_argument('--output', '-o', help='Output path or folder')
    
    args = parser.parse_args()
    
    if not WEASYPRINT_AVAILABLE:
        print("⚠ WeasyPrint not installed. Install with:")
        print("   pip install weasyprint")
        exit(1)
    
    if args.file:
        convert_md_to_pdf(args.file, args.output)
    elif args.folder:
        if not args.output:
            print("Please specify --output folder")
        else:
            convert_folder_to_pdf(args.folder, args.output)
    else:
        print("Please specify --file or --folder")
        parser.print_help()
