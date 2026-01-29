"""
Base Styles for Document Generation
====================================
Tuân thủ Nghị định 30/2020/NĐ-CP về Công tác văn thư

Quy định chung:
- Khổ giấy: A4 (210mm x 297mm)  
- Font: Times New Roman, Unicode TCVN 6909:2001
- Màu chữ: Đen
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE


class FontSize(Enum):
    """Cỡ chữ theo NĐ30/2020"""
    QUOC_HIEU = 12          # Quốc hiệu: 12-13pt
    TIEU_NGU = 13           # Tiêu ngữ: 13-14pt
    TEN_CO_QUAN = 12        # Tên cơ quan: 12-13pt
    SO_KY_HIEU = 13         # Số, ký hiệu: 13pt
    DIA_DANH_NGAY = 13      # Địa danh, ngày: 13-14pt
    TEN_LOAI_VAN_BAN = 14   # Tên loại văn bản: 13-14pt, đậm
    TRICH_YEU = 14          # Trích yếu: 13-14pt, đậm
    NOI_DUNG = 14           # Nội dung: 13-14pt
    CHUC_VU_KY = 14         # Chức vụ người ký: 13-14pt, đậm
    HO_TEN_KY = 14          # Họ tên người ký: 13-14pt, đậm
    NOI_NHAN_TITLE = 12     # "Nơi nhận:": 12pt, nghiêng, đậm
    NOI_NHAN_LIST = 11      # Danh sách nơi nhận: 11pt
    SO_TRANG = 13           # Số trang: 13-14pt


@dataclass
class PageMargins:
    """Định lề trang theo NĐ30/2020"""
    top: float = 2.0        # 20-25mm
    bottom: float = 2.0     # 20-25mm  
    left: float = 3.0       # 30-35mm
    right: float = 1.5      # 15-20mm
    
    def apply_to_section(self, section):
        """Apply margins to a document section"""
        section.top_margin = Cm(self.top)
        section.bottom_margin = Cm(self.bottom)
        section.left_margin = Cm(self.left)
        section.right_margin = Cm(self.right)


@dataclass
class ParagraphFormat:
    """Định dạng đoạn văn theo NĐ30/2020"""
    first_line_indent: float = 1.27  # Lùi đầu dòng: 1cm hoặc 1.27cm
    space_after: int = 6             # Khoảng cách sau đoạn: tối thiểu 6pt
    line_spacing: float = 1.0        # Khoảng cách dòng: đơn đến 1.5


# ============================================================
# STYLE DEFINITIONS
# ============================================================

FONT_NAME = "Times New Roman"

STYLES = {
    # Quốc hiệu và Tiêu ngữ
    "quoc_hieu": {
        "font_name": FONT_NAME,
        "font_size": Pt(12),
        "bold": True,
        "alignment": WD_ALIGN_PARAGRAPH.CENTER,
        "all_caps": True,
    },
    "tieu_ngu": {
        "font_name": FONT_NAME,
        "font_size": Pt(13),
        "bold": True,
        "alignment": WD_ALIGN_PARAGRAPH.CENTER,
    },
    
    # Tên cơ quan
    "ten_co_quan_chu_quan": {
        "font_name": FONT_NAME,
        "font_size": Pt(12),
        "bold": False,
        "alignment": WD_ALIGN_PARAGRAPH.CENTER,
        "all_caps": True,
    },
    "ten_co_quan_ban_hanh": {
        "font_name": FONT_NAME,
        "font_size": Pt(12),
        "bold": True,
        "alignment": WD_ALIGN_PARAGRAPH.CENTER,
        "all_caps": True,
    },
    
    # Số, ký hiệu
    "so_ky_hieu": {
        "font_name": FONT_NAME,
        "font_size": Pt(13),
        "bold": False,
        "alignment": WD_ALIGN_PARAGRAPH.CENTER,
    },
    
    # Địa danh và ngày tháng
    "dia_danh_ngay": {
        "font_name": FONT_NAME,
        "font_size": Pt(13),
        "bold": False,
        "italic": True,
        "alignment": WD_ALIGN_PARAGRAPH.CENTER,
    },
    
    # Tên loại văn bản
    "ten_loai_van_ban": {
        "font_name": FONT_NAME,
        "font_size": Pt(14),
        "bold": True,
        "alignment": WD_ALIGN_PARAGRAPH.CENTER,
        "all_caps": True,
    },
    
    # Trích yếu
    "trich_yeu": {
        "font_name": FONT_NAME,
        "font_size": Pt(14),
        "bold": True,
        "alignment": WD_ALIGN_PARAGRAPH.CENTER,
    },
    
    # Nội dung văn bản
    "noi_dung": {
        "font_name": FONT_NAME,
        "font_size": Pt(14),
        "bold": False,
        "alignment": WD_ALIGN_PARAGRAPH.JUSTIFY,
        "first_line_indent": Cm(1.27),
        "space_after": Pt(6),
    },
    
    # Heading levels (cho luận văn, báo cáo)
    "heading_1": {
        "font_name": FONT_NAME,
        "font_size": Pt(14),
        "bold": True,
        "alignment": WD_ALIGN_PARAGRAPH.CENTER,
        "all_caps": True,
        "space_before": Pt(12),
        "space_after": Pt(6),
    },
    "heading_2": {
        "font_name": FONT_NAME,
        "font_size": Pt(14),
        "bold": True,
        "alignment": WD_ALIGN_PARAGRAPH.LEFT,
        "space_before": Pt(12),
        "space_after": Pt(6),
    },
    "heading_3": {
        "font_name": FONT_NAME,
        "font_size": Pt(14),
        "bold": True,
        "italic": True,
        "alignment": WD_ALIGN_PARAGRAPH.LEFT,
        "first_line_indent": Cm(1.27),
        "space_before": Pt(6),
        "space_after": Pt(6),
    },
    
    # Chữ ký
    "chuc_vu_ky": {
        "font_name": FONT_NAME,
        "font_size": Pt(14),
        "bold": True,
        "alignment": WD_ALIGN_PARAGRAPH.CENTER,
        "all_caps": True,
    },
    "ho_ten_ky": {
        "font_name": FONT_NAME,
        "font_size": Pt(14),
        "bold": True,
        "alignment": WD_ALIGN_PARAGRAPH.CENTER,
    },
    
    # Nơi nhận
    "noi_nhan_title": {
        "font_name": FONT_NAME,
        "font_size": Pt(12),
        "bold": True,
        "italic": True,
    },
    "noi_nhan_item": {
        "font_name": FONT_NAME,
        "font_size": Pt(11),
        "bold": False,
    },
}


def apply_style(paragraph, style_name: str):
    """Apply predefined style to a paragraph"""
    if style_name not in STYLES:
        raise ValueError(f"Style '{style_name}' not found")
    
    style = STYLES[style_name]
    run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()
    
    # Font settings
    run.font.name = style.get("font_name", FONT_NAME)
    run.font.size = style.get("font_size", Pt(14))
    run.font.bold = style.get("bold", False)
    run.font.italic = style.get("italic", False)
    run.font.all_caps = style.get("all_caps", False)
    
    # Paragraph settings
    if "alignment" in style:
        paragraph.alignment = style["alignment"]
    if "first_line_indent" in style:
        paragraph.paragraph_format.first_line_indent = style["first_line_indent"]
    if "space_before" in style:
        paragraph.paragraph_format.space_before = style["space_before"]
    if "space_after" in style:
        paragraph.paragraph_format.space_after = style["space_after"]


def create_nd30_styles(document):
    """Create all NĐ30/2020 styles in a document"""
    styles = document.styles
    
    for style_name, style_config in STYLES.items():
        try:
            # Create new paragraph style
            new_style = styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)
            new_style.base_style = styles['Normal']
            
            # Font settings
            font = new_style.font
            font.name = style_config.get("font_name", FONT_NAME)
            font.size = style_config.get("font_size", Pt(14))
            font.bold = style_config.get("bold", False)
            font.italic = style_config.get("italic", False)
            font.all_caps = style_config.get("all_caps", False)
            
            # Paragraph settings
            pf = new_style.paragraph_format
            if "alignment" in style_config:
                pf.alignment = style_config["alignment"]
            if "first_line_indent" in style_config:
                pf.first_line_indent = style_config["first_line_indent"]
            if "space_before" in style_config:
                pf.space_before = style_config["space_before"]
            if "space_after" in style_config:
                pf.space_after = style_config["space_after"]
                
        except ValueError:
            # Style already exists
            pass
    
    return document
