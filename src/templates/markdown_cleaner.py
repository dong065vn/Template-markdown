"""
Markdown Cleaner / Parser
==========================
Parse và convert markdown inline formatting thành DOCX runs
với định dạng thực sự (bold, italic, etc.)
"""

import re
from typing import List, Tuple, NamedTuple
from enum import Enum


class FormatType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    BOLD_ITALIC = "bold_italic"
    CODE = "code"
    STRIKETHROUGH = "strikethrough"


class TextRun(NamedTuple):
    """Đại diện cho một đoạn text với format"""
    text: str
    format_type: FormatType


class MarkdownCleaner:
    """
    Parse markdown inline formatting thành các TextRun
    để có thể apply định dạng thực sự trong DOCX
    """
    
    def __init__(self):
        pass
    
    def parse_inline(self, text: str) -> List[TextRun]:
        """
        Parse text với markdown inline formatting
        
        Args:
            text: Text có thể chứa **bold**, *italic*, etc.
        
        Returns:
            List các TextRun với format type
        """
        runs = []
        
        # Pattern cho các format (thứ tự quan trọng!)
        # 1. Bold+Italic: ***text*** hoặc ___text___
        # 2. Bold: **text** hoặc __text__
        # 3. Italic: *text* hoặc _text_
        # 4. Code: `text`
        # 5. Strikethrough: ~~text~~
        
        pattern = (
            r'(\*\*\*(.+?)\*\*\*)'  # ***bold italic***
            r'|(___(.+?)___)'        # ___bold italic___
            r'|(\*\*(.+?)\*\*)'      # **bold**
            r'|(__(.+?)__)'          # __bold__
            r'|(\*([^*]+?)\*)'       # *italic*
            r'|(_([^_]+?)_)'         # _italic_
            r'|(`([^`]+?)`)'         # `code`
            r'|(~~(.+?)~~)'          # ~~strikethrough~~
        )
        
        last_end = 0
        
        for match in re.finditer(pattern, text):
            start = match.start()
            
            # Add plain text before this match
            if start > last_end:
                plain_text = text[last_end:start]
                if plain_text:
                    runs.append(TextRun(plain_text, FormatType.PLAIN))
            
            # Determine which group matched
            groups = match.groups()
            
            if groups[0]:  # ***bold italic***
                runs.append(TextRun(groups[1], FormatType.BOLD_ITALIC))
            elif groups[2]:  # ___bold italic___
                runs.append(TextRun(groups[3], FormatType.BOLD_ITALIC))
            elif groups[4]:  # **bold**
                runs.append(TextRun(groups[5], FormatType.BOLD))
            elif groups[6]:  # __bold__
                runs.append(TextRun(groups[7], FormatType.BOLD))
            elif groups[8]:  # *italic*
                runs.append(TextRun(groups[9], FormatType.ITALIC))
            elif groups[10]:  # _italic_
                runs.append(TextRun(groups[11], FormatType.ITALIC))
            elif groups[12]:  # `code`
                runs.append(TextRun(groups[13], FormatType.CODE))
            elif groups[14]:  # ~~strikethrough~~
                runs.append(TextRun(groups[15], FormatType.STRIKETHROUGH))
            
            last_end = match.end()
        
        # Add remaining plain text
        if last_end < len(text):
            remaining = text[last_end:]
            if remaining:
                runs.append(TextRun(remaining, FormatType.PLAIN))
        
        # If no matches, return whole text as plain
        if not runs:
            runs.append(TextRun(text, FormatType.PLAIN))
        
        return runs
    
    def strip_markdown(self, text: str) -> str:
        """
        Loại bỏ hoàn toàn markdown syntax, chỉ giữ text
        
        Args:
            text: Text có markdown formatting
        
        Returns:
            Text thuần không có markdown
        """
        runs = self.parse_inline(text)
        return ''.join(run.text for run in runs)
    
    def apply_to_paragraph(self, para, text: str, font_name: str = "Times New Roman", 
                           font_size_pt: int = 14):
        """
        Apply parsed markdown runs vào paragraph DOCX
        
        Args:
            para: python-docx Paragraph object
            text: Text với markdown formatting
            font_name: Tên font
            font_size_pt: Cỡ font (pt)
        """
        from docx.shared import Pt
        from docx.shared import RGBColor
        
        runs = self.parse_inline(text)
        
        for text_run in runs:
            run = para.add_run(text_run.text)
            run.font.name = font_name
            run.font.size = Pt(font_size_pt)
            
            if text_run.format_type == FormatType.BOLD:
                run.font.bold = True
            elif text_run.format_type == FormatType.ITALIC:
                run.font.italic = True
            elif text_run.format_type == FormatType.BOLD_ITALIC:
                run.font.bold = True
                run.font.italic = True
            elif text_run.format_type == FormatType.CODE:
                run.font.name = "Consolas"
                run.font.color.rgb = RGBColor(0x60, 0x60, 0x60)
            elif text_run.format_type == FormatType.STRIKETHROUGH:
                run.font.strike = True


# Singleton instance
_cleaner = MarkdownCleaner()


def parse_markdown_inline(text: str) -> List[TextRun]:
    """Parse markdown inline formatting"""
    return _cleaner.parse_inline(text)


def strip_markdown(text: str) -> str:
    """Strip markdown syntax from text"""
    return _cleaner.strip_markdown(text)


def apply_markdown_to_paragraph(para, text: str, font_name: str = "Times New Roman",
                                 font_size_pt: int = 14):
    """Apply markdown formatting to DOCX paragraph"""
    _cleaner.apply_to_paragraph(para, text, font_name, font_size_pt)


# Test
if __name__ == "__main__":
    cleaner = MarkdownCleaner()
    
    test_cases = [
        "Normal text",
        "**bold text**",
        "*italic text*",
        "***bold italic***",
        "Mix of **bold** and *italic* text",
        "**Kết quả mong đợi:** Báo cáo tổng hợp + Slide.",
        "Text with `inline code` inside",
        "~~strikethrough~~ text",
    ]
    
    for test in test_cases:
        print(f"\nInput: {test}")
        runs = cleaner.parse_inline(test)
        for run in runs:
            print(f"  - [{run.format_type.value}] '{run.text}'")
        print(f"Stripped: {cleaner.strip_markdown(test)}")
