"""
Intermediate Representation (IR)
=================================
Dataclasses để đại diện document structure
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class BlockType(Enum):
    """Loại block trong document"""
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST = "list"
    TABLE = "table"
    IMAGE = "image"
    CODE = "code"
    QUOTE = "quote"
    PAGEBREAK = "pagebreak"


@dataclass
class Run:
    """Một đoạn text với formatting"""
    text: str
    bold: bool = False
    italic: bool = False
    underline: bool = False
    font_name: Optional[str] = None
    font_size: Optional[int] = None


@dataclass
class ListItem:
    """Item trong list"""
    content: List[Run] = field(default_factory=list)
    level: int = 0  # Indent level


@dataclass
class TableCell:
    """Cell trong table"""
    content: List[Run] = field(default_factory=list)
    row_span: int = 1
    col_span: int = 1


@dataclass
class TableRow:
    """Row trong table"""
    cells: List[TableCell] = field(default_factory=list)
    is_header: bool = False


@dataclass 
class Block:
    """Base block trong document"""
    type: BlockType
    content: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Heading specific
    level: int = 0  # H1=1, H2=2, etc
    
    # Paragraph specific
    runs: List[Run] = field(default_factory=list)
    alignment: str = "left"  # left, center, right, justify
    
    # List specific
    items: List[ListItem] = field(default_factory=list)
    ordered: bool = False
    
    # Table specific
    rows: List[TableRow] = field(default_factory=list)
    
    # Image specific
    image_path: Optional[str] = None
    caption: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None


@dataclass
class Section:
    """Section trong document (chunk)"""
    title: str
    level: int  # Heading level của section
    blocks: List[Block] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_markdown(self) -> str:
        """Convert section to Markdown"""
        lines = []
        
        # Title
        lines.append(f"{'#' * self.level} {self.title}")
        lines.append("")
        
        for block in self.blocks:
            if block.type == BlockType.HEADING:
                lines.append(f"{'#' * block.level} {self._runs_to_text(block.runs)}")
                lines.append("")
            
            elif block.type == BlockType.PARAGRAPH:
                lines.append(self._runs_to_text(block.runs))
                lines.append("")
            
            elif block.type == BlockType.LIST:
                for i, item in enumerate(block.items):
                    prefix = f"{i+1}. " if block.ordered else "- "
                    indent = "  " * item.level
                    lines.append(f"{indent}{prefix}{self._runs_to_text(item.content)}")
                lines.append("")
            
            elif block.type == BlockType.QUOTE:
                lines.append(f"> {self._runs_to_text(block.runs)}")
                lines.append("")
            
            elif block.type == BlockType.IMAGE:
                caption = block.caption or ""
                lines.append(f"![{caption}]({block.image_path})")
                lines.append("")
        
        return "\n".join(lines)
    
    def _runs_to_text(self, runs: List[Run]) -> str:
        """Convert runs to plain text with markdown formatting"""
        parts = []
        for run in runs:
            text = run.text
            if run.bold and run.italic:
                text = f"***{text}***"
            elif run.bold:
                text = f"**{text}**"
            elif run.italic:
                text = f"*{text}*"
            parts.append(text)
        return "".join(parts)


@dataclass
class Document:
    """Đại diện cho toàn bộ document"""
    title: str = ""
    author: str = ""
    sections: List[Section] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Original file info
    source_path: Optional[str] = None
    source_type: Optional[str] = None  # pdf, docx
    
    def get_section_count(self) -> int:
        return len(self.sections)
    
    def get_total_blocks(self) -> int:
        return sum(len(s.blocks) for s in self.sections)
    
    def to_markdown(self) -> str:
        """Convert entire document to Markdown"""
        parts = []
        for section in self.sections:
            parts.append(section.to_markdown())
        return "\n---\n\n".join(parts)


# Factory functions
def create_paragraph(text: str, bold: bool = False, italic: bool = False) -> Block:
    """Tạo paragraph block"""
    return Block(
        type=BlockType.PARAGRAPH,
        runs=[Run(text=text, bold=bold, italic=italic)]
    )


def create_heading(text: str, level: int = 1) -> Block:
    """Tạo heading block"""
    return Block(
        type=BlockType.HEADING,
        level=level,
        runs=[Run(text=text, bold=True)]
    )


def create_list(items: List[str], ordered: bool = False) -> Block:
    """Tạo list block"""
    return Block(
        type=BlockType.LIST,
        ordered=ordered,
        items=[ListItem(content=[Run(text=item)]) for item in items]
    )


if __name__ == "__main__":
    # Test
    doc = Document(title="Test Document", author="Author")
    
    section = Section(title="Chapter 1", level=1)
    section.blocks.append(create_heading("Introduction", 2))
    section.blocks.append(create_paragraph("This is a test paragraph."))
    section.blocks.append(create_list(["Item 1", "Item 2", "Item 3"]))
    
    doc.sections.append(section)
    
    print(doc.to_markdown())
