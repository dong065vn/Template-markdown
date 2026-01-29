"""
Rule Loader
============
Load và validate các rule bases cho AI content generation
"""

import os
import yaml
from typing import Dict, List, Any
from pathlib import Path


class RuleLoader:
    """Load và quản lý rule bases"""
    
    def __init__(self, rules_dir: str = None):
        if rules_dir is None:
            rules_dir = os.path.dirname(os.path.abspath(__file__))
        self.rules_dir = Path(rules_dir)
        self._cached_rules: Dict[str, Any] = {}
    
    def load_rules(self, rule_file: str = "rule_bases.yaml") -> Dict:
        """Load rules từ file YAML"""
        if rule_file in self._cached_rules:
            return self._cached_rules[rule_file]
        
        rule_path = self.rules_dir / rule_file
        if not rule_path.exists():
            raise FileNotFoundError(f"Rule file not found: {rule_path}")
        
        with open(rule_path, 'r', encoding='utf-8') as f:
            rules = yaml.safe_load(f)
        
        self._cached_rules[rule_file] = rules
        return rules
    
    def get_academic_rules(self) -> Dict:
        """Lấy rules cho văn bản học thuật"""
        rules = self.load_rules()
        return rules.get('academic_document_rules', {})
    
    def get_official_rules(self) -> Dict:
        """Lấy rules cho văn bản hành chính"""
        rules = self.load_rules()
        return rules.get('official_document_rules', {})
    
    def get_segmentation_rules(self) -> Dict:
        """Lấy rules cho segmentation"""
        rules = self.load_rules()
        return rules.get('segmentation_rules', {})
    
    def get_ai_prompt_rules(self) -> Dict:
        """Lấy rules cho AI prompts"""
        rules = self.load_rules()
        return rules.get('ai_prompt_rules', {})
    
    def get_nd30_rules(self) -> Dict:
        """Lấy rules theo Nghị định 30/2020"""
        rules = self.load_rules()
        return rules.get('nd30_2020_rules', {})
    
    def get_tech_docs_framework(self) -> Dict:
        """Lấy framework tài liệu kỹ thuật (7 bước)"""
        rules = self.load_rules()
        return rules.get('tech_docs_framework', {})
    
    def get_legal_docs_framework(self) -> Dict:
        """Lấy framework tài liệu pháp lý"""
        rules = self.load_rules()
        return rules.get('legal_docs_framework', {})
    
    def calculate_sections(self, total_pages: int) -> int:
        """Tính số sections dựa trên số trang"""
        if total_pages <= 50:
            pages_per_section = 8
        elif total_pages <= 100:
            pages_per_section = 10
        elif total_pages <= 200:
            pages_per_section = 12
        else:
            pages_per_section = 15
        
        import math
        return math.ceil(total_pages / pages_per_section)
    
    def validate_section_content(self, content: str) -> List[str]:
        """Validate nội dung section theo rules"""
        issues = []
        prompt_rules = self.get_ai_prompt_rules()
        
        # Check for placeholder text
        placeholders = ['[INSERT]', '[TODO]', '[PLACEHOLDER]', '...']
        for ph in placeholders:
            if ph in content:
                issues.append(f"Tìm thấy placeholder: {ph}")
        
        # Check heading structure
        if '# ' not in content and '## ' not in content:
            issues.append("Thiếu heading structure")
        
        # Check minimum paragraphs
        paragraphs = [p for p in content.split('\n\n') if p.strip()]
        if len(paragraphs) < 3:
            issues.append(f"Chỉ có {len(paragraphs)} paragraphs, cần ít nhất 3")
        
        return issues


# Singleton instance
_rule_loader = None

def get_rule_loader() -> RuleLoader:
    """Get singleton RuleLoader instance"""
    global _rule_loader
    if _rule_loader is None:
        _rule_loader = RuleLoader()
    return _rule_loader


if __name__ == "__main__":
    loader = RuleLoader()
    
    # Test load rules
    print("=== Academic Rules ===")
    print(loader.get_academic_rules())
    
    print("\n=== Segmentation Rules ===")
    print(loader.get_segmentation_rules())
    
    print("\n=== Calculate Sections ===")
    for pages in [30, 50, 80, 150, 250]:
        sections = loader.calculate_sections(pages)
        print(f"  {pages} pages -> {sections} sections")
