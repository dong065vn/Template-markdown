"""
ADM Convert Command
====================
CLI for Function 1: Convert PDF/DOCX → Markdown → LaTeX
"""

import os
import click
from pathlib import Path


@click.command()
@click.option('--file', '-f', type=click.Path(exists=True),
              help='Single PDF/DOCX file to convert')
@click.option('--folder', '-d', type=click.Path(exists=True),
              help='Folder containing files (or use input/ by default)')
@click.option('--output', '-o', type=click.Path(),
              help='Output folder')
@click.option('--format', 'output_format', type=click.Choice(['latex', 'markdown', 'both']),
              default='latex', help='Output format')
@click.option('--split-level', type=int, default=1,
              help='Heading level to split (1=H1, 2=H2)')
@click.option('--max-chars', type=int, default=6000,
              help='Max characters per chunk')
def convert(file, folder, output, output_format, split_level, max_chars):
    """
    Convert PDF/DOCX files to Markdown/LaTeX
    
    \b
    Examples:
      adm convert --file thesis.pdf
      adm convert --folder input/ --format latex
      adm convert --file doc.docx --output output/ --split-level 2
    """
    click.echo("\n🔄 ADM Convert")
    click.echo("=" * 40)
    
    # Determine input
    if file:
        files = [Path(file)]
        click.echo(f"📄 Input: {file}")
    elif folder:
        folder_path = Path(folder)
        files = list(folder_path.glob("*.pdf")) + list(folder_path.glob("*.docx"))
        click.echo(f"📁 Input folder: {folder}")
        click.echo(f"   Found: {len(files)} files")
    else:
        # Default to input/ folder
        input_folder = Path("function1/input")
        if input_folder.exists():
            files = list(input_folder.glob("*.pdf")) + list(input_folder.glob("*.docx"))
            click.echo(f"📁 Using default: {input_folder}")
            click.echo(f"   Found: {len(files)} files")
        else:
            click.echo("⚠ No input specified. Use --file or --folder", err=True)
            click.echo("  Or drop files into function1/input/", err=True)
            return
    
    if not files:
        click.echo("⚠ No PDF/DOCX files found", err=True)
        return
    
    # Determine output folder
    if output:
        output_folder = Path(output)
    else:
        output_folder = Path("function1/output")
    
    output_folder.mkdir(parents=True, exist_ok=True)
    click.echo(f"📂 Output: {output_folder}")
    click.echo(f"📊 Format: {output_format}")
    click.echo(f"✂️  Split level: H{split_level}")
    click.echo("")
    
    # Process each file
    for filepath in files:
        click.echo(f"Processing: {filepath.name}...")
        
        try:
            # Import parsers
            if filepath.suffix.lower() == '.pdf':
                from function1.parsers.pdf_parser import parse_pdf
                doc = parse_pdf(str(filepath))
            else:
                from function1.parsers.docx_parser import parse_docx
                doc = parse_docx(str(filepath))
            
            click.echo(f"  ✓ Parsed: {doc.get_section_count()} sections, {doc.get_total_blocks()} blocks")
            
            # Split
            from function1.processors.splitter import Splitter
            splitter = Splitter(split_level, max_chars)
            chunks = splitter.split(doc)
            click.echo(f"  ✓ Split: {len(chunks)} chunks")
            
            # Export
            file_output = output_folder / filepath.stem
            file_output.mkdir(parents=True, exist_ok=True)
            
            if output_format in ['markdown', 'both']:
                md_folder = file_output / "markdown"
                splitter.save_chunks(chunks, str(md_folder), format="md")
                click.echo(f"  ✓ Saved: {md_folder}")
            
            if output_format in ['latex', 'both']:
                from function1.exporters.latex_exporter import LaTeXExporter
                exporter = LaTeXExporter(str(file_output))
                
                latex_folder = file_output / "latex"
                latex_folder.mkdir(exist_ok=True)
                exporter.export_sections(chunks, str(latex_folder))
                click.echo(f"  ✓ Saved: {latex_folder}")
            
            click.echo(f"  ✅ Done: {filepath.name}")
            
        except Exception as e:
            click.echo(f"  ❌ Error: {e}", err=True)
    
    click.echo(f"\n✅ Processed {len(files)} files")


if __name__ == "__main__":
    convert()
