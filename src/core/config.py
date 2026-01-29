"""
Configuration Manager
======================
Load/save application and project settings from YAML files
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml


# Default paths
APP_ROOT = Path(__file__).parent.parent.parent
CONFIG_DIR = APP_ROOT / "config"
DEFAULT_CONFIG_FILE = CONFIG_DIR / "settings.yaml"


# Default configuration
DEFAULT_CONFIG = {
    "app": {
        "name": "Academic Document Manager",
        "version": "1.0.0",
        "language": "vi",  # vi | en
    },
    "paths": {
        "function1_input": "function1/input",
        "function1_output": "function1/output",
        "function2_segmentation": "function2/Segmentation",
    },
    "function1": {
        "split_level": 1,  # Heading level to split (1 = H1, 2 = H2)
        "max_chars": 6000,  # Max characters per chunk
        "output_format": "latex",  # latex | markdown
    },
    "function2": {
        "default_type": "thesis",  # thesis | report | official
        "pages_per_section": 10,
        "font_name": "Times New Roman",
        "font_size": 14,
    },
    "nd30_2020": {
        "paper_size": "A4",
        "margin_top": 20,
        "margin_bottom": 20,
        "margin_left": 30,
        "margin_right": 15,
    }
}


class ConfigManager:
    """Manages application and project configuration"""
    
    def __init__(self, config_file: str = None):
        self.config_file = Path(config_file) if config_file else DEFAULT_CONFIG_FILE
        self._config: Dict[str, Any] = {}
        self._load_or_create()
    
    def _load_or_create(self):
        """Load config from file or create default"""
        if self.config_file.exists():
            self.load()
        else:
            self._config = DEFAULT_CONFIG.copy()
            self.save()
    
    def load(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f) or {}
            # Merge with defaults for any missing keys
            self._config = self._deep_merge(DEFAULT_CONFIG, self._config)
        except Exception as e:
            print(f"⚠ Error loading config: {e}")
            self._config = DEFAULT_CONFIG.copy()
        return self._config
    
    def save(self) -> bool:
        """Save configuration to YAML file"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(self._config, f, allow_unicode=True, 
                         default_flow_style=False, sort_keys=False)
            return True
        except Exception as e:
            print(f"⚠ Error saving config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a config value using dot notation (e.g., 'app.language')"""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
    
    def set(self, key: str, value: Any) -> None:
        """Set a config value using dot notation"""
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
    
    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Deep merge two dictionaries"""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    @property
    def config(self) -> Dict[str, Any]:
        return self._config


class ProjectConfig:
    """Manages per-project configuration (project_info.yaml)"""
    
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.config_file = self.project_dir / "project_info.yaml"
        self._config: Dict[str, Any] = {}
        if self.config_file.exists():
            self.load()
    
    def load(self) -> Dict[str, Any]:
        """Load project config"""
        with open(self.config_file, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f) or {}
        return self._config
    
    def save(self) -> bool:
        """Save project config"""
        try:
            self.project_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(self._config, f, allow_unicode=True,
                         default_flow_style=False, sort_keys=False)
            return True
        except Exception as e:
            print(f"⚠ Error saving project config: {e}")
            return False
    
    def create(self, project_name: str, document_type: str = "thesis",
               total_pages: int = 80, author: str = "") -> Dict[str, Any]:
        """Create new project configuration"""
        import math
        from datetime import datetime
        
        # Calculate pages per section
        if total_pages <= 50:
            pages_per_section = 8
        elif total_pages <= 100:
            pages_per_section = 10
        elif total_pages <= 200:
            pages_per_section = 12
        else:
            pages_per_section = 15
        
        num_sections = math.ceil(total_pages / pages_per_section)
        
        self._config = {
            "project_name": project_name,
            "author": author,
            "document_type": document_type,
            "total_pages": total_pages,
            "pages_per_section": pages_per_section,
            "num_sections": num_sections,
            "created_at": datetime.now().isoformat(),
            "status": "init",
        }
        self.save()
        return self._config
    
    def get(self, key: str, default: Any = None) -> Any:
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        self._config[key] = value
    
    @property
    def config(self) -> Dict[str, Any]:
        return self._config


# Singleton instance
_config_manager: Optional[ConfigManager] = None

def get_config() -> ConfigManager:
    """Get singleton config manager"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager


if __name__ == "__main__":
    # Test config
    config = get_config()
    print("App name:", config.get("app.name"))
    print("Language:", config.get("app.language"))
    print("F1 max chars:", config.get("function1.max_chars"))
    print("NĐ30 margin left:", config.get("nd30_2020.margin_left"))
