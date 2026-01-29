"""
Prompt Builder
===============
Xây dựng prompts cho AI với rules từ rule_bases
"""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml


class PromptBuilder:
    """Build prompts cho AI với rules và context"""
    
    def __init__(self, rules_file: str = None):
        if rules_file is None:
            # Find rules file
            rules_dir = Path(__file__).parent.parent / "rules"
            rules_file = rules_dir / "rule_bases.yaml"
        
        self.rules_file = Path(rules_file)
        self._rules: Dict = {}
        self._load_rules()
    
    def _load_rules(self):
        """Load rules từ YAML file"""
        if self.rules_file.exists():
            with open(self.rules_file, 'r', encoding='utf-8') as f:
                self._rules = yaml.safe_load(f) or {}
    
    def get_academic_rules(self) -> List[str]:
        """Get rules cho văn bản học thuật"""
        rules = self._rules.get("academic_document_rules", {})
        result = []
        for category, items in rules.items():
            if isinstance(items, list):
                result.extend(items)
        return result
    
    def get_official_rules(self) -> List[str]:
        """Get rules cho văn bản hành chính"""
        rules = self._rules.get("official_document_rules", {})
        result = []
        for category, items in rules.items():
            if isinstance(items, list):
                result.extend(items)
        return result
    
    def build_section_prompt(self, section_title: str, 
                            section_outline: List[str],
                            target_words: int = 1500,
                            document_type: str = "thesis",
                            context: str = "") -> str:
        """
        Build prompt cho AI để generate 1 section
        
        Args:
            section_title: Tiêu đề section
            section_outline: List các điểm cần cover
            target_words: Số từ mục tiêu
            document_type: thesis | report | official
            context: Context bổ sung (optional)
        
        Returns:
            Prompt string hoàn chỉnh
        """
        # Get appropriate rules
        if document_type in ["thesis", "report"]:
            rules = self.get_academic_rules()
        else:
            rules = self.get_official_rules()
        
        # Format outline
        outline_text = "\n".join(f"- {item}" for item in section_outline)
        
        # Format rules
        rules_text = "\n".join(f"- {rule}" for rule in rules[:5])  # Limit to 5 rules
        
        prompt = f"""# Yêu cầu viết nội dung

## Section: {section_title}

## Mục tiêu
Viết nội dung hoàn chỉnh cho section này.

## Outline cần cover
{outline_text}

## Yêu cầu format
- **Số từ**: ~{target_words} từ
- **Format output**: Markdown thuần túy
- **KHÔNG dùng**: HTML, format đặc biệt
- **Heading**: Dùng ## và ### cho các mục

## Quy tắc viết
{rules_text}

## Cấu trúc output
```markdown
## [Tiêu đề mục 1]

[Nội dung đoạn văn 1, 100-200 từ]

[Nội dung đoạn văn 2, 100-200 từ]

### [Tiêu đề mục con 1.1]

[Nội dung...]

## [Tiêu đề mục 2]

[Nội dung...]
```

{f"## Context bổ sung{chr(10)}{context}" if context else ""}

---
**Bắt đầu viết nội dung:**
"""
        return prompt
    
    def build_batch_prompt(self, sections: List[Dict]) -> str:
        """
        Build prompt cho nhiều sections (batch processing)
        
        Args:
            sections: List of {title, outline, words}
        """
        prompts = []
        for i, section in enumerate(sections, 1):
            header = f"=== SECTION {i}: {section['title']} ==="
            prompt = self.build_section_prompt(
                section['title'],
                section.get('outline', []),
                section.get('words', 1500)
            )
            prompts.append(f"{header}\n\n{prompt}")
        
        return "\n\n" + "="*50 + "\n\n".join(prompts)
    
    def save_prompts(self, prompts: List[Dict], output_file: str):
        """Save prompts to YAML for reference"""
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump({"prompts": prompts}, f, allow_unicode=True)


# Singleton
_prompt_builder: Optional[PromptBuilder] = None

def get_prompt_builder() -> PromptBuilder:
    global _prompt_builder
    if _prompt_builder is None:
        _prompt_builder = PromptBuilder()
    return _prompt_builder


if __name__ == "__main__":
    builder = PromptBuilder()
    
    prompt = builder.build_section_prompt(
        "Chương 1: Tổng quan",
        ["Đặt vấn đề", "Mục tiêu nghiên cứu", "Phạm vi nghiên cứu"],
        target_words=2000,
        document_type="thesis"
    )
    
    print(prompt)
