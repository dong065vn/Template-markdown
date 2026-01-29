"""Templates Package - Unified access to all document templates"""

from .styles import (
    STYLES,
    FONT_NAME,
    FontSize, 
    PageMargins,
    ParagraphFormat,
    apply_style,
    create_nd30_styles,
)

from .thesis import ThesisTemplate, create_thesis_from_markdown
from .report import ReportTemplate, create_report_from_markdown
from .official import (
    OfficialDocumentTemplate,
    CongVanTemplate,
    QuyetDinhTemplate,
    ToTrinhTemplate,
)

__all__ = [
    # Styles
    "STYLES",
    "FONT_NAME",
    "FontSize",
    "PageMargins", 
    "ParagraphFormat",
    "apply_style",
    "create_nd30_styles",
    
    # Thesis
    "ThesisTemplate",
    "create_thesis_from_markdown",
    
    # Report
    "ReportTemplate",
    "create_report_from_markdown",
    
    # Official Documents
    "OfficialDocumentTemplate",
    "CongVanTemplate",
    "QuyetDinhTemplate",
    "ToTrinhTemplate",
]


# Template registry for easy access
TEMPLATE_REGISTRY = {
    "thesis": ThesisTemplate,
    "luanvan": ThesisTemplate,
    "report": ReportTemplate,
    "baocao": ReportTemplate,
    "congvan": CongVanTemplate,
    "quyetdinh": QuyetDinhTemplate,
    "totrinh": ToTrinhTemplate,
}


def get_template(template_type: str):
    """Get template class by type name"""
    template_type = template_type.lower().replace(" ", "").replace("_", "")
    if template_type not in TEMPLATE_REGISTRY:
        available = ", ".join(TEMPLATE_REGISTRY.keys())
        raise ValueError(f"Unknown template type: {template_type}. Available: {available}")
    return TEMPLATE_REGISTRY[template_type]
