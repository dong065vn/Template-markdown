"""
Academic Document Manager (ADM) v1.0
=====================================
Desktop Application for Academic Document Processing

Functions:
- Function 1: Convert PDF/DOCX → Markdown → LaTeX
- Function 2: AI Content → Markdown → DOCX/PDF (NĐ30/2020)

Usage:
    python main.py              # Launch CLI
    python main.py --help       # Show help
    python main.py gui          # Launch GUI
    python main.py convert      # Function 1
    python main.py generate     # Function 2
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

__version__ = "1.0.0"
__author__ = "ADM Team"


def main():
    """Main entry point"""
    try:
        from src.cli.main import cli
        cli()
    except ImportError as e:
        # Fallback if click not installed
        print(f"⚠ CLI not available: {e}")
        print("Install with: pip install click")
        print("\nFallback mode - use:")
        print("  pip install -r requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    main()
