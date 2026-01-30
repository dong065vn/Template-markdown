"""
Function 3 - Regenerate CLI
============================
CLI cho Function 3: Lấy nội dung từ file gốc → Format lại → DOCX/PDF

Function 3 có tất cả chức năng của Function 2 nhưng:
- Thay vì TẠO content mới → LẤY content từ file gốc
- AI chỉ FORMAT LẠI, không thêm bớt nội dung
"""

import os
import shutil
from pathlib import Path
import click


# Project directory for Function 3
DEFAULT_PROJECT_DIR = "function3/Segmentation"


@click.group()
def regenerate():
    """
    Function 3: AI Regenerate - Lấy nội dung từ file gốc
    
    \\b
    Workflow:
      1. adm regenerate init      - Extract nội dung từ file gốc
      2. [AI format lại content]  - Dùng prompt để AI format MD
      3. adm regenerate export    - Export to DOCX/PDF
      4. adm regenerate merge     - Merge all sections
    
    \\b
    Khác với Function 2:
      - F2: AI TẠO content mới
      - F3: AI CHỈ FORMAT LẠI content có sẵn
    """
    pass


@regenerate.command()
@click.option('--file', '-f', 'source_file', required=True, 
              type=click.Path(exists=True), help='File PDF/DOCX nguồn')
@click.option('--name', '-n', help='Tên project (mặc định: tên file)')
@click.option('--project-dir', '-d', default=DEFAULT_PROJECT_DIR, 
              help='Thư mục project')
@click.option('--split-level', '-s', type=int, default=1,
              help='Mức chia section (1=H1, 2=H2)')
def init(source_file, name, project_dir, split_level):
    """
    Khởi tạo project từ file PDF/DOCX gốc
    
    \\b
    Workflow:
      1. Extract nội dung từ file
      2. Tạo cấu trúc phases
      3. Tạo prompt cho AI format
    
    \\b
    Example:
      adm regenerate init --file thesis.docx
      adm regenerate init --file report.pdf --name "Báo cáo"
    """
    click.echo("\n🔄 ADM Regenerate - Init from File")
    click.echo("=" * 40)
    
    source_path = Path(source_file)
    project_name = name or source_path.stem
    
    click.echo(f"📄 Source: {source_file}")
    click.echo(f"📝 Project: {project_name}")
    click.echo(f"📁 Directory: {project_dir}")
    click.echo()
    
    try:
        from function3.extractors import ContentExtractor
        
        # Create project structure
        project_path = Path(project_dir)
        (project_path / "phase1_source").mkdir(parents=True, exist_ok=True)
        (project_path / "phase2_prompt").mkdir(parents=True, exist_ok=True)
        (project_path / "phase3_content").mkdir(parents=True, exist_ok=True)
        (project_path / "phase4_rendered").mkdir(parents=True, exist_ok=True)
        (project_path / "phase5_output").mkdir(parents=True, exist_ok=True)
        
        # Extract content
        extractor = ContentExtractor()
        content = extractor.extract(source_file)
        
        click.echo(f"📑 Title: {content['title']}")
        click.echo(f"👤 Author: {content['author']}")
        click.echo(f"📄 Type: {content['source_type']}")
        
        # Save source info
        import yaml
        config = {
            "project_name": project_name,
            "source_file": str(source_path.absolute()),
            "source_type": content['source_type'],
            "title": content['title'],
            "author": content['author'],
            "split_level": split_level
        }
        
        config_path = project_path / "phase1_source" / "config.yaml"
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
        
        # Save original content
        original_path = project_path / "phase1_source" / "original_content.txt"
        with open(original_path, 'w', encoding='utf-8') as f:
            f.write(content['full_text'])
        
        click.echo(f"✓ Saved: {original_path}")
        
        # Create AI prompt
        prompt = extractor.create_prompt_for_regenerate(content)
        prompt_path = project_path / "phase2_prompt" / "prompt_for_ai.txt"
        with open(prompt_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        
        click.echo(f"✓ Saved: {prompt_path}")
        
        click.echo()
        click.echo("✅ Project initialized!")
        click.echo()
        click.echo("📌 Next steps:")
        click.echo("   1. Mở file: phase2_prompt/prompt_for_ai.txt")
        click.echo("   2. Copy prompt → Gửi cho AI (ChatGPT/Claude)")
        click.echo("   3. AI trả về Markdown → Lưu vào phase3_content/content.md")
        click.echo("   4. Chạy: adm regenerate export")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        raise


@regenerate.command()
@click.option('--project-dir', '-d', default=DEFAULT_PROJECT_DIR,
              type=click.Path(exists=True), help='Thư mục project')
@click.option('--format', 'output_format', default='all',
              type=click.Choice(['docx', 'pdf', 'text', 'all']),
              help='Format output')
def export(project_dir, output_format):
    """
    Export Markdown content ra DOCX/PDF
    
    \\b
    Example:
      adm regenerate export --format all
    """
    click.echo("\n📤 ADM Regenerate - Export")
    click.echo("=" * 40)
    
    project_path = Path(project_dir)
    content_folder = project_path / "phase3_content"
    output_folder = project_path / "phase4_rendered"
    
    # Check for content
    md_files = list(content_folder.glob("*.md"))
    if not md_files:
        click.echo(f"⚠ No .md files in {content_folder}")
        click.echo("   Lưu kết quả từ AI vào phase3_content/ trước")
        return
    
    click.echo(f"📁 Input: {content_folder} ({len(md_files)} files)")
    
    output_folder.mkdir(parents=True, exist_ok=True)
    
    try:
        # Process to plain text first
        if output_format in ['text', 'all']:
            from src.templates import TextProcessor
            processor = TextProcessor()
            
            text_folder = output_folder / "text"
            text_folder.mkdir(exist_ok=True)
            
            for md_file in md_files:
                txt_path = text_folder / f"{md_file.stem}.txt"
                processor.process_file(str(md_file), str(txt_path))
            
            click.echo(f"✅ Text saved: {text_folder}")
        
        # Export to DOCX
        if output_format in ['docx', 'all']:
            from function2.templates.converters.md_to_docx import convert_folder
            
            docx_folder = output_folder / "docx"
            convert_folder(str(content_folder), str(docx_folder))
            click.echo(f"✅ DOCX saved: {docx_folder}")
        
        # Export to PDF
        if output_format in ['pdf', 'all']:
            try:
                from function2.templates.converters.md_to_pdf import convert_folder_to_pdf
                
                pdf_folder = output_folder / "pdf"
                convert_folder_to_pdf(str(content_folder), str(pdf_folder))
                click.echo(f"✅ PDF saved: {pdf_folder}")
            except ImportError:
                click.echo("⚠ PDF skipped: pip install weasyprint")
        
        click.echo()
        click.echo("📌 Next: adm regenerate merge")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@regenerate.command()
@click.option('--project-dir', '-d', default=DEFAULT_PROJECT_DIR,
              type=click.Path(exists=True), help='Thư mục project')
@click.option('--output', '-o', help='Tên file output')
def merge(project_dir, output):
    """
    Merge tất cả DOCX sections thành 1 file
    
    \\b
    Example:
      adm regenerate merge --output "final.docx"
    """
    click.echo("\n🔗 ADM Regenerate - Merge")
    click.echo("=" * 40)
    
    project_path = Path(project_dir)
    docx_folder = project_path / "phase4_rendered" / "docx"
    
    if not docx_folder.exists():
        click.echo(f"⚠ DOCX folder not found: {docx_folder}")
        click.echo("   Chạy 'adm regenerate export' trước")
        return
    
    docx_files = sorted(docx_folder.glob("*.docx"))
    if not docx_files:
        click.echo("⚠ No DOCX files found")
        return
    
    click.echo(f"📁 Found {len(docx_files)} DOCX files")
    
    output_folder = project_path / "phase5_output"
    output_folder.mkdir(parents=True, exist_ok=True)
    
    # Determine output name
    if output:
        output_path = output_folder / output
    else:
        # Get project name from config
        try:
            import yaml
            config_path = project_path / "phase1_source" / "config.yaml"
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            project_name = config.get('project_name', 'document')
            output_path = output_folder / f"{project_name}_regenerated.docx"
        except:
            output_path = output_folder / "MERGED_regenerated.docx"
    
    try:
        from function2.templates.converters.docx_merger import merge_docx_folder
        
        result = merge_docx_folder(str(docx_folder), str(output_path))
        
        click.echo(f"\n✅ Merged: {result}")
        click.echo("\n🎉 Document regeneration complete!")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@regenerate.command()
@click.option('--project-dir', '-d', default=DEFAULT_PROJECT_DIR, 
              help='Thư mục project')
@click.option('--phase', '-p', default='content',
              type=click.Choice(['all', 'content', 'rendered', 'output']),
              help='Phase để reset')
@click.option('--confirm', '-y', is_flag=True, help='Skip xác nhận')
def renew(project_dir, phase, confirm):
    """
    Reset phases để xử lý file mới
    
    \\b
    Phases:
      content  - Clear phase3_content/ (default)
      rendered - Clear phase4_rendered/
      output   - Clear phase5_output/
      all      - Clear tất cả (bao gồm source & prompt)
    
    \\b
    Example:
      adm regenerate renew               - Reset content
      adm regenerate renew --phase all   - Reset tất cả
    """
    click.echo("\n🔄 ADM Regenerate - Renew")
    click.echo("=" * 40)
    
    project_path = Path(project_dir)
    
    phases_to_clear = []
    if phase == 'all':
        phases_to_clear = [
            'phase1_source', 'phase2_prompt', 
            'phase3_content', 'phase4_rendered', 'phase5_output'
        ]
    elif phase == 'content':
        phases_to_clear = ['phase3_content', 'phase4_rendered', 'phase5_output']
    elif phase == 'rendered':
        phases_to_clear = ['phase4_rendered', 'phase5_output']
    elif phase == 'output':
        phases_to_clear = ['phase5_output']
    
    # Count files
    total_files = 0
    for p in phases_to_clear:
        folder = project_path / p
        if folder.exists():
            total_files += len(list(folder.rglob("*")))
    
    click.echo(f"📁 Project: {project_dir}")
    click.echo(f"🗑️ Phases to clear: {', '.join(phases_to_clear)}")
    click.echo(f"📄 Files affected: {total_files}")
    click.echo()
    
    if not confirm and total_files > 0:
        if not click.confirm('Proceed?'):
            click.echo("❌ Cancelled")
            return
    
    for p in phases_to_clear:
        folder = project_path / p
        if folder.exists():
            shutil.rmtree(folder)
            click.echo(f"  ✓ Cleared: {p}")
        folder.mkdir(parents=True, exist_ok=True)
        click.echo(f"  ✓ Created: {p}")
    
    click.echo()
    click.echo("✅ Phases renewed!")
    if phase == 'all':
        click.echo("📌 Next: adm regenerate init --file <file>")
    else:
        click.echo("📌 Ready for new content")


@regenerate.command()
@click.option('--project-dir', '-d', default=DEFAULT_PROJECT_DIR,
              type=click.Path(exists=True), help='Thư mục project')
def status(project_dir):
    """
    Xem trạng thái project hiện tại
    """
    click.echo("\n📊 ADM Regenerate - Status")
    click.echo("=" * 40)
    
    project_path = Path(project_dir)
    
    if not project_path.exists():
        click.echo(f"⚠ Project not found: {project_dir}")
        click.echo("   Chạy: adm regenerate init --file <file>")
        return
    
    # Check each phase
    phases = [
        ('phase1_source', 'Source files'),
        ('phase2_prompt', 'AI prompts'),
        ('phase3_content', 'Markdown content'),
        ('phase4_rendered', 'Rendered output'),
        ('phase5_output', 'Final merged'),
    ]
    
    click.echo(f"📁 Project: {project_dir}\n")
    
    for phase_dir, description in phases:
        folder = project_path / phase_dir
        if folder.exists():
            files = list(folder.rglob("*"))
            file_count = len([f for f in files if f.is_file()])
            status = "✅" if file_count > 0 else "📁"
            click.echo(f"  {status} {phase_dir}: {file_count} files")
        else:
            click.echo(f"  ❌ {phase_dir}: not created")
    
    # Show config if exists
    config_path = project_path / "phase1_source" / "config.yaml"
    if config_path.exists():
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        click.echo()
        click.echo(f"📝 Project: {config.get('project_name', 'N/A')}")
        click.echo(f"📄 Source: {config.get('source_file', 'N/A')}")


@regenerate.command()
@click.option('--project-dir', '-d', default=DEFAULT_PROJECT_DIR,
              type=click.Path(exists=True), help='Thư mục project')
def scan(project_dir):
    """
    Scan và thống kê nội dung markdown
    
    \\b
    Kiểm tra để đảm bảo không bị mất content
    """
    click.echo("\n📊 ADM Regenerate - Scan Content")
    click.echo("=" * 40)
    
    project_path = Path(project_dir)
    content_folder = project_path / "phase3_content"
    
    md_files = list(content_folder.glob("*.md"))
    if not md_files:
        click.echo(f"⚠ No .md files in {content_folder}")
        return
    
    try:
        from src.templates.section_renderer import MarkdownScanner
        
        scanner = MarkdownScanner()
        
        for md_file in md_files:
            click.echo(f"\n📄 File: {md_file.name}")
            stats = scanner.scan_file(str(md_file))
            scanner.print_report(stats)
    
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@regenerate.command('render-sections')
@click.option('--project-dir', '-d', default=DEFAULT_PROJECT_DIR,
              type=click.Path(exists=True), help='Thư mục project')
@click.option('--output', '-o', default='MERGED_regenerated.docx', help='Tên file output cuối cùng')
def render_sections(project_dir, output):
    """
    Render TẤT CẢ markdown files và merge thành 1 file
    
    \\b
    Workflow:
      1. Quét tất cả *.md trong phase3_content
      2. Render từng file qua section splitting
      3. Merge TẤT CẢ thành 1 file cuối cùng
    
    \\b
    Output: 1 file DOCX chứa tất cả nội dung
    """
    click.echo("\n🔄 ADM Regenerate - Render All Sections")
    click.echo("=" * 40)
    
    project_path = Path(project_dir)
    content_folder = project_path / "phase3_content"
    output_folder = project_path / "phase5_output"
    temp_folder = project_path / "phase4_rendered" / "temp_sections"
    
    md_files = sorted(content_folder.glob("*.md"))
    if not md_files:
        click.echo(f"⚠ No .md files in {content_folder}")
        return
    
    click.echo(f"📁 Found {len(md_files)} markdown files:")
    for f in md_files:
        click.echo(f"   - {f.name}")
    
    try:
        from src.templates.section_renderer import render_with_sections
        from function2.templates.converters.docx_merger import merge_docx_seamless
        
        output_folder.mkdir(parents=True, exist_ok=True)
        temp_folder.mkdir(parents=True, exist_ok=True)
        
        rendered_files = []
        
        # Step 1: Render each MD file
        for i, md_file in enumerate(md_files):
            click.echo(f"\n📄 [{i+1}/{len(md_files)}] Rendering: {md_file.name}")
            
            temp_output = temp_folder / f"{md_file.stem}.docx"
            
            result = render_with_sections(str(md_file), str(temp_output))
            
            if os.path.exists(result):
                rendered_files.append(result)
                click.echo(f"   ✓ Done: {md_file.stem}.docx")
        
        # Step 2: Merge all rendered files
        click.echo(f"\n🔗 Merging {len(rendered_files)} files...")
        
        final_output = output_folder / output
        
        if len(rendered_files) == 1:
            shutil.copy(rendered_files[0], final_output)
        else:
            merge_docx_seamless(rendered_files, str(final_output))
        
        click.echo(f"\n✅ Final output: {final_output}")
        click.echo(f"📄 Contains {len(md_files)} sections merged")
        click.echo("\n🎉 All sections rendered and merged!")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    regenerate()
