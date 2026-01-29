"""
PDF Parser
===========
Parse PDF files using PyMuPDF (fitz) to IR
"""

import os
from pathlib import Path
from typing import List, Optional, Tuple
import re

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

from .ir import (
    Document, Section, Block, BlockType, Run, 
    create_paragraph, create_heading
)


class PDFParser:
    """Parse PDF files to Intermediate Representation"""
    
    def __init__(self):
        if not PYMUPDF_AVAILABLE:
            raise ImportError(
                "PyMuPDF is not installed. "
                "Install with: pip install PyMuPDF"
            )
    
    def parse(self, pdf_path: str) -> Document:
        """
        Parse PDF file to Document IR
        
        Args:
            pdf_path: Đường dẫn đến file PDF
        
        Returns:
            Document object chứa nội dung đã parse
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"File not found: {pdf_path}")
        
        doc = fitz.open(pdf_path)
        
        # Create IR Document
        ir_doc = Document(
            title=doc.metadata.get("title", Path(pdf_path).stem),
            author=doc.metadata.get("author", ""),
            source_path=pdf_path,
            source_type="pdf"
        )
        
        current_section = None
        
        for page_num, page in enumerate(doc):
            blocks = page.get_text("dict")["blocks"]
            
            for block in blocks:
                if block["type"] == 0:  # Text block
                    for line in block.get("lines", []):
                        text = ""
                        spans = line.get("spans", [])
                        
                        if not spans:
                            continue
                        
                        # Get text and detect if heading
                        for span in spans:
                            text += span["text"]
                        
                        text = text.strip()
                        if not text:
                            continue
                        
                        # Detect heading by font size
                        avg_size = sum(s["size"] for s in spans) / len(spans)
                        is_bold = any(s.get("flags", 0) & 2 for s in spans)
                        
                        if avg_size >= 16 and is_bold:
                            # H1 heading
                            level = 1
                            if current_section:
                                ir_doc.sections.append(current_section)
                            current_section = Section(title=text, level=level)
                        
                        elif avg_size >= 14 and is_bold:
                            # H2 heading
                            if current_section is None:
                                current_section = Section(title="Document", level=1)
                            current_section.blocks.append(create_heading(text, 2))
                        
                        else:
                            # Normal paragraph
                            if current_section is None:
                                current_section = Section(title="Document", level=1)
                            
                            runs = []
                            for span in spans:
                                is_span_bold = span.get("flags", 0) & 2
                                is_italic = span.get("flags", 0) & 1
                                runs.append(Run(
                                    text=span["text"],
                                    bold=bool(is_span_bold),
                                    italic=bool(is_italic)
                                ))
                            
                            current_section.blocks.append(Block(
                                type=BlockType.PARAGRAPH,
                                runs=runs
                            ))
                
                elif block["type"] == 1:  # Image block
                    if current_section is None:
                        current_section = Section(title="Document", level=1)
                    
                    # Extract image info
                    current_section.blocks.append(Block(
                        type=BlockType.IMAGE,
                        metadata={"page": page_num, "bbox": block.get("bbox")}
                    ))
        
        # Add last section
        if current_section:
            ir_doc.sections.append(current_section)
        
        doc.close()
        return ir_doc
    
    def extract_images(self, pdf_path: str, output_dir: str) -> List[str]:
        """
        Extract all images from PDF
        
        Args:
            pdf_path: Đường dẫn PDF
            output_dir: Thư mục lưu images
        
        Returns:
            List đường dẫn các images đã extract
        """
        os.makedirs(output_dir, exist_ok=True)
        
        doc = fitz.open(pdf_path)
        image_paths = []
        
        for page_num, page in enumerate(doc):
            images = page.get_images()
            
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                
                if base_image:
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    filename = f"page{page_num+1}_img{img_index+1}.{image_ext}"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, "wb") as f:
                        f.write(image_bytes)
                    
                    image_paths.append(filepath)
                    print(f"✓ Extracted: {filename}")
        
        doc.close()
        return image_paths


def parse_pdf(pdf_path: str) -> Document:
    """
    Hàm tiện ích để parse PDF
    
    Args:
        pdf_path: Đường dẫn file PDF
    
    Returns:
        Document IR
    
    Example:
        >>> doc = parse_pdf("thesis.pdf")
        >>> print(doc.get_section_count())
    """
    parser = PDFParser()
    return parser.parse(pdf_path)


if __name__ == "__main__":
    import sys
    
    if not PYMUPDF_AVAILABLE:
        print("⚠ PyMuPDF not installed. Install with:")
        print("   pip install PyMuPDF")
        exit(1)
    
    if len(sys.argv) > 1:
        doc = parse_pdf(sys.argv[1])
        print(f"Title: {doc.title}")
        print(f"Sections: {doc.get_section_count()}")
        print(f"Blocks: {doc.get_total_blocks()}")
        print("\n--- Markdown ---\n")
        print(doc.to_markdown()[:2000])
    else:
        print("Usage: python pdf_parser.py <pdf_file>")
