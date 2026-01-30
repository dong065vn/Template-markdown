"""
Content Extractor
==================
Trích xuất nội dung từ PDF/DOCX để AI regenerate
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from docx import Document as DocxDocument
except ImportError:
    DocxDocument = None

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None


class ContentExtractor:
    """Trích xuất nội dung gốc từ file để AI dùng regenerate"""
    
    def __init__(self):
        pass
    
    def extract(self, file_path: str) -> Dict[str, Any]:
        """
        Trích xuất nội dung từ file PDF hoặc DOCX
        
        Args:
            file_path: Đường dẫn file
        
        Returns:
            Dict chứa nội dung và metadata
        """
        ext = Path(file_path).suffix.lower()
        
        if ext == '.pdf':
            return self._extract_pdf(file_path)
        elif ext == '.docx':
            return self._extract_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    def _extract_pdf(self, file_path: str) -> Dict[str, Any]:
        """Trích xuất từ PDF"""
        if fitz is None:
            raise ImportError("PyMuPDF required: pip install PyMuPDF")
        
        doc = fitz.open(file_path)
        
        content = {
            "title": doc.metadata.get("title", Path(file_path).stem),
            "author": doc.metadata.get("author", ""),
            "pages": [],
            "full_text": "",
            "source_type": "pdf"
        }
        
        full_text_parts = []
        
        for page_num, page in enumerate(doc, 1):
            page_text = page.get_text("text")
            content["pages"].append({
                "page": page_num,
                "text": page_text
            })
            full_text_parts.append(f"--- Page {page_num} ---\n{page_text}")
        
        content["full_text"] = "\n\n".join(full_text_parts)
        doc.close()
        
        return content
    
    def _extract_docx(self, file_path: str) -> Dict[str, Any]:
        """Trích xuất từ DOCX"""
        if DocxDocument is None:
            raise ImportError("python-docx required: pip install python-docx")
        
        doc = DocxDocument(file_path)
        
        content = {
            "title": doc.core_properties.title or Path(file_path).stem,
            "author": doc.core_properties.author or "",
            "paragraphs": [],
            "full_text": "",
            "source_type": "docx"
        }
        
        text_parts = []
        
        for para in doc.paragraphs:
            if para.text.strip():
                # Detect style
                style_name = para.style.name if para.style else "Normal"
                
                content["paragraphs"].append({
                    "style": style_name,
                    "text": para.text
                })
                
                # Format based on style
                if "Heading 1" in style_name:
                    text_parts.append(f"\n# {para.text}\n")
                elif "Heading 2" in style_name:
                    text_parts.append(f"\n## {para.text}\n")
                elif "Heading 3" in style_name:
                    text_parts.append(f"\n### {para.text}\n")
                else:
                    text_parts.append(para.text)
        
        content["full_text"] = "\n\n".join(text_parts)
        
        return content
    
    def create_prompt_for_regenerate(self, content: Dict[str, Any]) -> str:
        """
        Tạo prompt cho AI để regenerate nội dung
        
        Args:
            content: Dict từ extract()
        
        Returns:
            Prompt string để gửi cho AI
        """
        prompt = f"""Bạn là AI chuyên format lại văn bản. 
Nhiệm vụ: Chuyển đổi nội dung sau thành Markdown thuần túy.

QUY TẮC QUAN TRỌNG:
1. KHÔNG thêm, bớt hay sửa đổi nội dung gốc
2. KHÔNG sáng tạo thêm thông tin mới
3. CHỈ format lại thành Markdown chuẩn
4. Giữ nguyên cấu trúc heading, list, paragraph
5. Sửa các lỗi format nhưng giữ nguyên nghĩa

Tiêu đề gốc: {content['title']}
Tác giả: {content['author']}

NỘI DUNG GỐC:
================
{content['full_text']}
================

Hãy xuất ra file Markdown đã được format lại, giữ nguyên 100% nội dung gốc.
"""
        return prompt
    
    def save_for_ai(self, content: Dict[str, Any], output_dir: str) -> str:
        """
        Lưu nội dung và prompt ra file để AI xử lý
        
        Args:
            content: Dict từ extract()
            output_dir: Thư mục output
        
        Returns:
            Đường dẫn file prompt
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Save original content
        original_path = os.path.join(output_dir, "original_content.txt")
        with open(original_path, 'w', encoding='utf-8') as f:
            f.write(content['full_text'])
        
        # Save prompt
        prompt = self.create_prompt_for_regenerate(content)
        prompt_path = os.path.join(output_dir, "prompt_for_ai.txt")
        with open(prompt_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        print(f"✓ Saved: {original_path}")
        print(f"✓ Saved: {prompt_path}")
        
        return prompt_path


def extract_content(file_path: str) -> Dict[str, Any]:
    """Hàm tiện ích trích xuất nội dung"""
    extractor = ContentExtractor()
    return extractor.extract(file_path)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        content = extract_content(sys.argv[1])
        print(f"Title: {content['title']}")
        print(f"Author: {content['author']}")
        print(f"Type: {content['source_type']}")
        print(f"\nContent preview ({len(content['full_text'])} chars):")
        print(content['full_text'][:1000])
    else:
        print("Usage: python content_extractor.py <file.pdf|docx>")
