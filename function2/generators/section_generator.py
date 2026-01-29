"""
Section Generator
==================
Tạo outline và sections cho document dựa trên project info
"""

import os
import math
from pathlib import Path
from typing import Dict, List, Any
import yaml


# Templates cho các loại document
THESIS_STRUCTURE = {
    "name": "Luận văn",
    "sections": [
        {"id": "cover", "title": "Trang bìa", "pages": 2, "type": "front"},
        {"id": "declaration", "title": "Lời cam đoan", "pages": 1, "type": "front"},
        {"id": "acknowledgment", "title": "Lời cảm ơn", "pages": 1, "type": "front"},
        {"id": "abstract", "title": "Tóm tắt", "pages": 2, "type": "front"},
        {"id": "toc", "title": "Mục lục", "pages": 2, "type": "front"},
        {"id": "intro", "title": "Mở đầu", "pages": 5, "type": "main"},
        {"id": "ch1", "title": "Chương 1: Tổng quan", "pages": 15, "type": "main"},
        {"id": "ch2", "title": "Chương 2: Cơ sở lý thuyết", "pages": 15, "type": "main"},
        {"id": "ch3", "title": "Chương 3: Phương pháp nghiên cứu", "pages": 15, "type": "main"},
        {"id": "ch4", "title": "Chương 4: Kết quả và thảo luận", "pages": 20, "type": "main"},
        {"id": "conclusion", "title": "Kết luận và kiến nghị", "pages": 5, "type": "main"},
        {"id": "references", "title": "Tài liệu tham khảo", "pages": 5, "type": "back"},
        {"id": "appendix", "title": "Phụ lục", "pages": 10, "type": "back"},
    ]
}

REPORT_STRUCTURE = {
    "name": "Báo cáo",
    "sections": [
        {"id": "cover", "title": "Trang bìa", "pages": 1, "type": "front"},
        {"id": "toc", "title": "Mục lục", "pages": 1, "type": "front"},
        {"id": "intro", "title": "Giới thiệu", "pages": 3, "type": "main"},
        {"id": "main", "title": "Nội dung chính", "pages": 20, "type": "main"},
        {"id": "conclusion", "title": "Kết luận", "pages": 3, "type": "main"},
        {"id": "references", "title": "Tài liệu tham khảo", "pages": 2, "type": "back"},
    ]
}

STRUCTURES = {
    "thesis": THESIS_STRUCTURE,
    "report": REPORT_STRUCTURE,
}


class SectionGenerator:
    """Generate sections từ project configuration"""
    
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.phase1_dir = self.project_dir / "phase1_init"
        self.phase2_dir = self.project_dir / "phase2_sections"
        self._project_info: Dict = {}
    
    def load_project_info(self) -> Dict:
        """Load project info from phase1_init"""
        info_file = self.phase1_dir / "project_info.yaml"
        if info_file.exists():
            with open(info_file, 'r', encoding='utf-8') as f:
                self._project_info = yaml.safe_load(f) or {}
        return self._project_info
    
    def generate_outline(self, document_type: str = "thesis", 
                        total_pages: int = 80) -> Dict:
        """
        Generate outline dựa trên loại document và số trang
        
        Args:
            document_type: thesis | report
            total_pages: Tổng số trang dự kiến
        
        Returns:
            Outline dict với các sections
        """
        template = STRUCTURES.get(document_type, THESIS_STRUCTURE)
        
        # Calculate scaling factor
        template_pages = sum(s["pages"] for s in template["sections"])
        scale = total_pages / template_pages
        
        outline = {
            "document_type": document_type,
            "total_pages": total_pages,
            "sections": []
        }
        
        for section in template["sections"]:
            scaled_pages = max(1, round(section["pages"] * scale))
            outline["sections"].append({
                "id": section["id"],
                "title": section["title"],
                "pages": scaled_pages,
                "type": section["type"],
                "status": "pending"
            })
        
        return outline
    
    def generate_sections(self, outline: Dict = None) -> List[str]:
        """
        Tạo các file section_XXX.md trong phase2_sections
        
        Args:
            outline: Outline dict (load từ file nếu None)
        
        Returns:
            List các file paths đã tạo
        """
        if outline is None:
            outline_file = self.phase1_dir / "outline.yaml"
            if outline_file.exists():
                with open(outline_file, 'r', encoding='utf-8') as f:
                    outline = yaml.safe_load(f)
            else:
                raise FileNotFoundError("Outline not found. Run init first.")
        
        # Create phase2 directory
        self.phase2_dir.mkdir(parents=True, exist_ok=True)
        
        created_files = []
        
        for i, section in enumerate(outline.get("sections", []), 1):
            # Skip front matter for now
            if section.get("type") == "front":
                continue
            
            filename = f"section_{i:03d}.md"
            filepath = self.phase2_dir / filename
            
            content = self._create_section_template(section, i)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            created_files.append(str(filepath))
            print(f"✓ Created: {filename}")
        
        # Save metadata
        metadata = {
            "document_type": outline.get("document_type"),
            "total_sections": len(created_files),
            "sections": [s["title"] for s in outline.get("sections", []) 
                        if s.get("type") != "front"]
        }
        with open(self.phase2_dir / "metadata.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(metadata, f, allow_unicode=True)
        
        return created_files
    
    def _create_section_template(self, section: Dict, index: int) -> str:
        """Tạo template cho 1 section"""
        return f"""# {section['title']}

## Mục tiêu
- [Mô tả mục tiêu của section này]

## Outline
1. [Điểm chính 1]
2. [Điểm chính 2]
3. [Điểm chính 3]

## Yêu cầu nội dung
- Số trang dự kiến: ~{section.get('pages', 10)} trang
- Giọng văn: học thuật, khách quan
- Có trích dẫn nguồn nếu cần

## Prompt cho AI
```
Viết nội dung cho section "{section['title']}" của luận văn.

Yêu cầu:
- Khoảng {section.get('pages', 10) * 300} từ
- Giọng văn học thuật, khách quan
- Chia thành các mục rõ ràng với heading
- Mỗi đoạn 100-200 từ
- Format: Markdown thuần (không HTML)

Outline cần cover:
[Điền outline chi tiết ở đây]
```

---
<!-- Status: pending -->
"""
    
    def save_outline(self, outline: Dict) -> str:
        """Save outline to phase1_init"""
        self.phase1_dir.mkdir(parents=True, exist_ok=True)
        filepath = self.phase1_dir / "outline.yaml"
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(outline, f, allow_unicode=True)
        return str(filepath)


def init_project(project_dir: str, project_name: str,
                 document_type: str = "thesis", 
                 total_pages: int = 80,
                 author: str = "") -> Dict:
    """
    Initialize a new project
    
    Example:
        >>> init_project(
        ...     "function2/Segmentation",
        ...     "Luận văn tốt nghiệp",
        ...     "thesis",
        ...     80,
        ...     "Nguyễn Văn A"
        ... )
    """
    import datetime
    
    project_path = Path(project_dir)
    phase1_dir = project_path / "phase1_init"
    phase1_dir.mkdir(parents=True, exist_ok=True)
    
    # Calculate sections
    if total_pages <= 50:
        pages_per_section = 8
    elif total_pages <= 100:
        pages_per_section = 10
    elif total_pages <= 200:
        pages_per_section = 12
    else:
        pages_per_section = 15
    
    num_sections = math.ceil(total_pages / pages_per_section)
    
    # Create project_info.yaml
    project_info = {
        "project_name": project_name,
        "author": author,
        "document_type": document_type,
        "total_pages": total_pages,
        "pages_per_section": pages_per_section,
        "num_sections": num_sections,
        "created_at": datetime.datetime.now().isoformat(),
        "status": "init",
    }
    
    with open(phase1_dir / "project_info.yaml", 'w', encoding='utf-8') as f:
        yaml.dump(project_info, f, allow_unicode=True)
    
    # Generate and save outline
    generator = SectionGenerator(project_dir)
    outline = generator.generate_outline(document_type, total_pages)
    generator.save_outline(outline)
    
    print(f"✅ Project initialized: {project_name}")
    print(f"   Type: {document_type}")
    print(f"   Pages: {total_pages} ({num_sections} sections)")
    
    return project_info


if __name__ == "__main__":
    # Test
    test_dir = "test_project"
    init_project(test_dir, "Test Thesis", "thesis", 80, "Author")
    
    generator = SectionGenerator(test_dir)
    generator.generate_sections()
