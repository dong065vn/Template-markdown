"""
Document Splitter
==================
Split document thành chunks theo heading level
"""

import os
from pathlib import Path
from typing import List, Optional

from function1.parsers.ir import Document, Section, Block, BlockType


class Splitter:
    """Split document theo heading level"""
    
    def __init__(self, split_level: int = 1, max_chars: int = 6000):
        """
        Args:
            split_level: Heading level để split (1 = H1, 2 = H2)
            max_chars: Max characters per chunk (optional further split)
        """
        self.split_level = split_level
        self.max_chars = max_chars
    
    def split(self, document: Document) -> List[Section]:
        """
        Split document thành các sections
        
        Args:
            document: Document IR đã parse
        
        Returns:
            List các Section (chunks)
        """
        if self.split_level == 1:
            # Mỗi section trong document là 1 chunk
            return document.sections
        
        # Split theo heading level cao hơn
        chunks = []
        for section in document.sections:
            sub_chunks = self._split_section(section)
            chunks.extend(sub_chunks)
        
        return chunks
    
    def _split_section(self, section: Section) -> List[Section]:
        """Split 1 section thành sub-sections dựa trên headings"""
        if not section.blocks:
            return [section]
        
        chunks = []
        current_chunk = Section(title=section.title, level=section.level)
        
        for block in section.blocks:
            if block.type == BlockType.HEADING and block.level <= self.split_level:
                # Start new chunk
                if current_chunk.blocks:
                    chunks.append(current_chunk)
                
                # Get title from heading
                title = ""
                if block.runs:
                    title = "".join(r.text for r in block.runs)
                
                current_chunk = Section(title=title or section.title, level=block.level)
            else:
                current_chunk.blocks.append(block)
        
        if current_chunk.blocks or not chunks:
            chunks.append(current_chunk)
        
        return chunks
    
    def save_chunks(self, chunks: List[Section], output_dir: str, 
                   format: str = "md") -> List[str]:
        """
        Save chunks to files
        
        Args:
            chunks: List sections to save
            output_dir: Output directory
            format: Output format (md | txt)
        
        Returns:
            List đường dẫn các files đã tạo
        """
        os.makedirs(output_dir, exist_ok=True)
        saved_files = []
        
        for i, chunk in enumerate(chunks, 1):
            # Generate filename
            safe_title = "".join(c if c.isalnum() or c in " -_" else "_" 
                                for c in chunk.title[:30])
            filename = f"chunk_{i:03d}_{safe_title.strip()}.{format}"
            filepath = os.path.join(output_dir, filename)
            
            # Convert to format
            if format == "md":
                content = chunk.to_markdown()
            else:
                content = self._to_plain_text(chunk)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            saved_files.append(filepath)
            print(f"✓ Saved: {filename}")
        
        print(f"\n✅ Total: {len(saved_files)} chunks saved")
        return saved_files
    
    def _to_plain_text(self, section: Section) -> str:
        """Convert section to plain text"""
        lines = [section.title, "=" * len(section.title), ""]
        
        for block in section.blocks:
            if block.runs:
                text = "".join(r.text for r in block.runs)
                lines.append(text)
                lines.append("")
        
        return "\n".join(lines)


def split_document(document: Document, output_dir: str,
                   split_level: int = 1, max_chars: int = 6000) -> List[str]:
    """
    Hàm tiện ích để split document
    
    Args:
        document: Document IR
        output_dir: Thư mục output
        split_level: Heading level để split
        max_chars: Max chars per chunk
    
    Returns:
        List đường dẫn các files đã tạo
    
    Example:
        >>> from function1.parsers import parse_pdf
        >>> doc = parse_pdf("thesis.pdf")
        >>> chunks = split_document(doc, "output/chunks", split_level=1)
    """
    splitter = Splitter(split_level, max_chars)
    chunks = splitter.split(document)
    return splitter.save_chunks(chunks, output_dir)


if __name__ == "__main__":
    # Test với sample data
    from function1.parsers.ir import create_paragraph, create_heading
    
    doc = Document(title="Test Document")
    
    section1 = Section(title="Chapter 1", level=1)
    section1.blocks.append(create_heading("Section 1.1", 2))
    section1.blocks.append(create_paragraph("Paragraph 1"))
    section1.blocks.append(create_heading("Section 1.2", 2))
    section1.blocks.append(create_paragraph("Paragraph 2"))
    
    section2 = Section(title="Chapter 2", level=1)
    section2.blocks.append(create_paragraph("Paragraph 3"))
    
    doc.sections = [section1, section2]
    
    splitter = Splitter(split_level=2)
    chunks = splitter.split(doc)
    
    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i+1}: {chunk.title} ---")
        print(chunk.to_markdown()[:200])
