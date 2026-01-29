"""
NĐ30/2020 Validator
====================
Validate document format theo Nghị định 30/2020/NĐ-CP
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
from docx import Document
from docx.shared import Pt, Cm, Mm
import os


@dataclass
class ValidationResult:
    """Kết quả validation"""
    passed: bool
    message: str
    category: str
    severity: str = "warning"  # error | warning | info


class ND30Validator:
    """Validate document theo tiêu chuẩn Nghị định 30/2020/NĐ-CP"""
    
    # Tiêu chuẩn NĐ30/2020
    STANDARDS = {
        "page_size": {
            "width_mm": 210,  # A4
            "height_mm": 297,
        },
        "margins_mm": {
            "top": (20, 25),      # min, max
            "bottom": (20, 25),
            "left": (30, 35),
            "right": (15, 20),
        },
        "font": {
            "name": "Times New Roman",
            "body_size_pt": (13, 14),  # min, max
            "heading_size_pt": (13, 14),
        },
        "line_spacing": {
            "min": 1.0,
            "max": 1.5,
        },
        "first_line_indent_cm": 1.0,
    }
    
    def __init__(self):
        self.results: List[ValidationResult] = []
    
    def validate_docx(self, docx_path: str) -> Tuple[bool, List[ValidationResult]]:
        """
        Validate file DOCX
        
        Args:
            docx_path: Đường dẫn đến file DOCX
        
        Returns:
            (passed, results) - True nếu pass, list kết quả chi tiết
        """
        self.results = []
        
        if not os.path.exists(docx_path):
            self.results.append(ValidationResult(
                passed=False,
                message=f"File not found: {docx_path}",
                category="file",
                severity="error"
            ))
            return False, self.results
        
        doc = Document(docx_path)
        
        # Validate từng tiêu chí
        self._validate_page_size(doc)
        self._validate_margins(doc)
        self._validate_fonts(doc)
        
        # Calculate overall result
        has_errors = any(r.severity == "error" and not r.passed for r in self.results)
        
        return not has_errors, self.results
    
    def _validate_page_size(self, doc: Document):
        """Validate kích thước trang A4"""
        for section in doc.sections:
            width_mm = section.page_width.mm
            height_mm = section.page_height.mm
            
            expected_w = self.STANDARDS["page_size"]["width_mm"]
            expected_h = self.STANDARDS["page_size"]["height_mm"]
            
            # Allow 1mm tolerance
            if abs(width_mm - expected_w) > 1 or abs(height_mm - expected_h) > 1:
                self.results.append(ValidationResult(
                    passed=False,
                    message=f"Kích thước trang không đúng A4. Hiện tại: {width_mm:.0f}x{height_mm:.0f}mm",
                    category="page_size",
                    severity="error"
                ))
            else:
                self.results.append(ValidationResult(
                    passed=True,
                    message="Kích thước trang A4 đạt chuẩn",
                    category="page_size",
                    severity="info"
                ))
            break  # Only check first section
    
    def _validate_margins(self, doc: Document):
        """Validate lề trang"""
        for section in doc.sections:
            margins = {
                "top": section.top_margin.mm,
                "bottom": section.bottom_margin.mm,
                "left": section.left_margin.mm,
                "right": section.right_margin.mm,
            }
            
            for margin_name, value in margins.items():
                min_val, max_val = self.STANDARDS["margins_mm"][margin_name]
                
                # Allow 1mm tolerance
                if value < min_val - 1 or value > max_val + 1:
                    self.results.append(ValidationResult(
                        passed=False,
                        message=f"Lề {margin_name} không đạt: {value:.0f}mm (chuẩn: {min_val}-{max_val}mm)",
                        category="margins",
                        severity="warning"
                    ))
                else:
                    self.results.append(ValidationResult(
                        passed=True,
                        message=f"Lề {margin_name} đạt chuẩn: {value:.0f}mm",
                        category="margins",
                        severity="info"
                    ))
            break
    
    def _validate_fonts(self, doc: Document):
        """Validate font chữ"""
        expected_font = self.STANDARDS["font"]["name"]
        min_size, max_size = self.STANDARDS["font"]["body_size_pt"]
        
        fonts_found = set()
        sizes_found = set()
        
        for para in doc.paragraphs:
            for run in para.runs:
                if run.font.name:
                    fonts_found.add(run.font.name)
                if run.font.size:
                    sizes_found.add(run.font.size.pt)
        
        # Check font name
        if expected_font not in fonts_found and fonts_found:
            self.results.append(ValidationResult(
                passed=False,
                message=f"Font không đúng. Tìm thấy: {fonts_found}. Chuẩn: {expected_font}",
                category="font",
                severity="warning"
            ))
        else:
            self.results.append(ValidationResult(
                passed=True,
                message=f"Font {expected_font} đạt chuẩn",
                category="font",
                severity="info"
            ))
        
        # Check font sizes
        invalid_sizes = [s for s in sizes_found if s < min_size - 1 or s > max_size + 1]
        if invalid_sizes and len(invalid_sizes) / max(1, len(sizes_found)) > 0.3:
            self.results.append(ValidationResult(
                passed=False,
                message=f"Cỡ chữ không đạt. Tìm thấy: {invalid_sizes}pt. Chuẩn: {min_size}-{max_size}pt",
                category="font_size",
                severity="warning"
            ))
        else:
            self.results.append(ValidationResult(
                passed=True,
                message=f"Cỡ chữ đạt chuẩn ({min_size}-{max_size}pt)",
                category="font_size",
                severity="info"
            ))
    
    def generate_report(self, output_path: str = None) -> str:
        """Generate validation report"""
        lines = ["# Báo cáo Validation NĐ30/2020", ""]
        
        # Summary
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        
        lines.append(f"## Tổng quan")
        lines.append(f"- **Tổng số kiểm tra**: {total}")
        lines.append(f"- **Đạt**: {passed} ✅")
        lines.append(f"- **Không đạt**: {failed} ❌")
        lines.append("")
        
        # Details
        lines.append("## Chi tiết")
        lines.append("")
        
        for r in self.results:
            icon = "✅" if r.passed else "❌"
            lines.append(f"- {icon} **[{r.category}]** {r.message}")
        
        report = "\n".join(lines)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"📝 Report saved: {output_path}")
        
        return report


def validate_docx(docx_path: str, report_path: str = None) -> bool:
    """
    Validate file DOCX theo NĐ30/2020
    
    Args:
        docx_path: Đường dẫn file DOCX
        report_path: Đường dẫn lưu report (optional)
    
    Returns:
        True nếu đạt chuẩn
    
    Example:
        >>> validate_docx("document.docx", "validation_report.md")
    """
    validator = ND30Validator()
    passed, results = validator.validate_docx(docx_path)
    
    if report_path:
        validator.generate_report(report_path)
    
    return passed


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        result = validate_docx(sys.argv[1], "validation_report.md")
        print(f"\nResult: {'PASSED ✅' if result else 'FAILED ❌'}")
    else:
        print("Usage: python nd30_validator.py <docx_file>")
