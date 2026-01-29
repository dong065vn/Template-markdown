# Academic Document Manager (ADM) v1.0

📄 Desktop application for academic document processing

## Features

### Function 1: Convert
- PDF/DOCX → Markdown → LaTeX
- Split by heading level
- Extract images

### Function 2: Generate
- AI Content → DOCX/PDF
- Format theo NĐ30/2020
- ZOLO Mode (one-shot)

## Installation

### From Source
```bash
# Clone repo
git clone https://github.com/example/academic-document-manager
cd academic-document-manager

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

### From PyPI (future)
```bash
pip install academic-document-manager
adm --help
```

## Quick Start

### CLI Commands
```bash
# Help
python main.py --help

# Convert
python main.py convert --file thesis.pdf

# Generate
python main.py generate init --name "Luận văn" --pages 80
python main.py generate sections
python main.py generate export --format all
python main.py generate merge

# GUI
python main.py gui
```

### Slash Commands
- `/adm-convert` - Convert documents
- `/adm-generate` - Generate workflow
- `/adm-zolo` - Quick start
- `/adm-export` - Export DOCX/PDF
- `/adm-merge` - Merge files
- `/adm-help` - All commands

## Project Structure

```
academic-document-manager/
├── main.py              # Entry point
├── src/
│   ├── cli/             # CLI commands
│   ├── gui/             # GUI views
│   ├── core/            # Config, utils
│   ├── templates/       # Python templates
│   └── rules/           # Rule bases
├── function1/           # Convert (PDF/DOCX → LaTeX)
│   ├── parsers/         # PDF, DOCX parsers
│   ├── processors/      # Splitter
│   └── exporters/       # LaTeX exporter
└── function2/           # Generate (AI → DOCX/PDF)
    ├── generators/      # Section, prompt
    ├── validators/      # NĐ30 validator
    └── templates/       # DOCX templates
```

## Build

```bash
# Windows
build.bat

# Output: dist/ADM.exe
```

## Requirements

- Python 3.10+
- Windows 10/11

## License

MIT License
