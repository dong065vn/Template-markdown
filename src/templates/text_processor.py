"""
Text Processor
===============
Xử lý nội dung Markdown thành văn bản thuần túy chuẩn
"""

import re
import os
from pathlib import Path
from typing import List, Optional


class TextProcessor:
    """
    Xử lý Markdown thành văn bản thuần túy chuẩn
    - Loại bỏ markdown syntax
    - Giữ nguyên nội dung
    - Format đẹp cho văn bản thuần
    """
    
    def __init__(self):
        pass
    
    def process(self, markdown_content: str) -> str:
        """
        Chuyển đổi Markdown thành văn bản thuần
        
        Args:
            markdown_content: Nội dung Markdown
        
        Returns:
            Văn bản thuần đã xử lý
        """
        text = markdown_content
        
        # 1. Convert headings to uppercase with underline
        text = self._process_headings(text)
        
        # 2. Remove bold/italic markers but keep text
        text = self._remove_formatting(text)
        
        # 3. Convert lists to proper format
        text = self._process_lists(text)
        
        # 4. Convert code blocks to indented text
        text = self._process_code_blocks(text)
        
        # 5. Remove tables markdown, keep content
        text = self._process_tables(text)
        
        # 6. Remove links but keep text
        text = self._process_links(text)
        
        # 7. Clean up extra whitespace
        text = self._clean_whitespace(text)
        
        return text
    
    def _process_headings(self, text: str) -> str:
        """Convert # headings to plain text format"""
        lines = text.split('\n')
        result = []
        
        for line in lines:
            # Match heading patterns
            match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                heading_text = match.group(2)
                
                if level == 1:
                    # Chương - uppercase + box
                    result.append('')
                    result.append('=' * 60)
                    result.append(heading_text.upper())
                    result.append('=' * 60)
                    result.append('')
                elif level == 2:
                    # Section - uppercase + underline
                    result.append('')
                    result.append(heading_text.upper())
                    result.append('-' * len(heading_text))
                    result.append('')
                elif level == 3:
                    # Subsection - bold style
                    result.append('')
                    result.append(f"    {heading_text}")
                    result.append('')
                else:
                    result.append(f"        {heading_text}")
            else:
                result.append(line)
        
        return '\n'.join(result)
    
    def _remove_formatting(self, text: str) -> str:
        """Remove bold/italic/underline markers"""
        # Bold + italic
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', text)
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        # Italic
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        # Underline (custom)
        text = re.sub(r'__(.+?)__', r'\1', text)
        
        return text
    
    def _process_lists(self, text: str) -> str:
        """Convert list markers"""
        lines = text.split('\n')
        result = []
        
        for line in lines:
            # Unordered list
            if re.match(r'^\s*[-*+]\s+', line):
                line = re.sub(r'^(\s*)[-*+]\s+', r'\1• ', line)
            
            # Ordered list - keep number
            match = re.match(r'^(\s*)(\d+)\.\s+(.+)$', line)
            if match:
                indent = match.group(1)
                num = match.group(2)
                content = match.group(3)
                line = f"{indent}{num}. {content}"
            
            result.append(line)
        
        return '\n'.join(result)
    
    def _process_code_blocks(self, text: str) -> str:
        """Convert code blocks to indented text"""
        # Fenced code blocks
        def replace_code_block(match):
            code = match.group(2)
            lines = code.strip().split('\n')
            indented = '\n'.join(f"        {line}" for line in lines)
            return f"\n    [Code]\n{indented}\n    [/Code]\n"
        
        text = re.sub(r'```(\w*)\n(.*?)```', replace_code_block, text, flags=re.DOTALL)
        
        # Inline code
        text = re.sub(r'`([^`]+)`', r'"\1"', text)
        
        return text
    
    def _process_tables(self, text: str) -> str:
        """Convert tables to plain text format"""
        lines = text.split('\n')
        result = []
        in_table = False
        table_rows = []
        
        for line in lines:
            if '|' in line:
                # Table row
                if not in_table:
                    in_table = True
                    table_rows = []
                
                # Skip separator row
                if re.match(r'^\s*\|[\s\-:|]+\|\s*$', line):
                    continue
                
                # Extract cells
                cells = [c.strip() for c in line.split('|')[1:-1]]
                table_rows.append(cells)
            else:
                if in_table:
                    # Output table
                    result.extend(self._format_table(table_rows))
                    in_table = False
                    table_rows = []
                
                result.append(line)
        
        # Handle table at end
        if in_table:
            result.extend(self._format_table(table_rows))
        
        return '\n'.join(result)
    
    def _format_table(self, rows: List[List[str]]) -> List[str]:
        """Format table rows as plain text"""
        if not rows:
            return []
        
        result = []
        result.append('')
        
        # Calculate column widths
        num_cols = max(len(row) for row in rows)
        col_widths = [0] * num_cols
        
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(cell))
        
        # Output rows
        for i, row in enumerate(rows):
            line_parts = []
            for j in range(num_cols):
                cell = row[j] if j < len(row) else ''
                line_parts.append(cell.ljust(col_widths[j]))
            
            line = '    ' + '  |  '.join(line_parts)
            result.append(line)
            
            # Separator after header
            if i == 0:
                sep = '    ' + '-+-'.join('-' * w for w in col_widths)
                result.append(sep)
        
        result.append('')
        return result
    
    def _process_links(self, text: str) -> str:
        """Remove link markdown, keep text"""
        # [text](url) -> text
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        
        # ![alt](url) -> [Image: alt]
        text = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'[Hình: \1]', text)
        
        return text
    
    def _clean_whitespace(self, text: str) -> str:
        """Clean up extra whitespace"""
        # Remove multiple blank lines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove trailing whitespace
        lines = [line.rstrip() for line in text.split('\n')]
        
        return '\n'.join(lines)
    
    def process_file(self, input_path: str, output_path: str = None) -> str:
        """
        Xử lý file Markdown
        
        Args:
            input_path: Đường dẫn file input
            output_path: Đường dẫn output (optional)
        
        Returns:
            Đường dẫn file output
        """
        with open(input_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        plain_text = self.process(md_content)
        
        if output_path is None:
            output_path = str(Path(input_path).with_suffix('.txt'))
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(plain_text)
        
        print(f"✓ Processed: {output_path}")
        return output_path
    
    def process_folder(self, input_dir: str, output_dir: str) -> List[str]:
        """
        Xử lý tất cả file MD trong folder
        
        Args:
            input_dir: Thư mục input
            output_dir: Thư mục output
        
        Returns:
            List đường dẫn files đã xử lý
        """
        os.makedirs(output_dir, exist_ok=True)
        
        input_path = Path(input_dir)
        md_files = sorted(input_path.glob("*.md"))
        
        results = []
        for md_file in md_files:
            txt_name = md_file.stem + '.txt'
            output_path = os.path.join(output_dir, txt_name)
            
            self.process_file(str(md_file), output_path)
            results.append(output_path)
        
        print(f"\n✅ Processed {len(results)} files")
        return results


def process_markdown_to_text(input_path: str, output_path: str = None) -> str:
    """Hàm tiện ích xử lý markdown"""
    processor = TextProcessor()
    return processor.process_file(input_path, output_path)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        process_markdown_to_text(sys.argv[1])
    else:
        # Demo
        sample = """
# Chương 1: Giới thiệu

## 1.1 Đặt vấn đề

Đây là đoạn văn **bold** và *italic*.

### 1.1.1 Chi tiết

- Item 1
- Item 2
- Item 3

| Cột 1 | Cột 2 |
|-------|-------|
| A | B |
| C | D |

```python
def hello():
    print("Hello")
```

Kết thúc.
"""
        processor = TextProcessor()
        result = processor.process(sample)
        print(result)
