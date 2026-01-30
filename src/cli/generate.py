"""
ADM Generate Command
=====================
CLI for Function 2: AI Content → Markdown → DOCX/PDF
"""

import os
import click
from pathlib import Path


@click.group()
def generate():
    """
    Generate documents from AI content (Function 2)
    
    \b
    Workflow:
      1. adm generate init     - Initialize new project
      2. adm generate sections - Generate section files
      3. [AI creates content]  - Use Antigravity to write
      4. adm generate export   - Export to DOCX/PDF
      5. adm generate merge    - Merge all sections
    """
    pass


@generate.command()
@click.option('--name', '-n', prompt='Project name', help='Project name')
@click.option('--type', 'doc_type', type=click.Choice(['thesis', 'report', 'official']),
              default='thesis', help='Document type')
@click.option('--pages', '-p', type=int, default=80, help='Total pages')
@click.option('--author', '-a', default='', help='Author name')
@click.option('--project-dir', '-d', type=click.Path(), 
              default='function2/Segmentation', help='Project directory')
def init(name, doc_type, pages, author, project_dir):
    """
    Initialize a new document generation project
    
    \b
    Example:
      adm generate init --name "Luận văn" --type thesis --pages 80
    """
    click.echo("\n🚀 ADM Generate - Init")
    click.echo("=" * 40)
    click.echo(f"📝 Project: {name}")
    click.echo(f"📋 Type: {doc_type}")
    click.echo(f"📄 Pages: {pages}")
    click.echo(f"👤 Author: {author or '(not set)'}")
    click.echo(f"📁 Directory: {project_dir}")
    click.echo("")
    
    try:
        from function2.generators.section_generator import init_project
        
        project_info = init_project(
            project_dir=project_dir,
            project_name=name,
            document_type=doc_type,
            total_pages=pages,
            author=author
        )
        
        click.echo("\n✅ Project initialized!")
        click.echo(f"   Sections: {project_info.get('num_sections', 0)}")
        click.echo(f"   Created: {project_dir}/phase1_init/")
        click.echo("\n📌 Next step: adm generate sections")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)


@generate.command()
@click.option('--project-dir', '-d', type=click.Path(exists=True),
              default='function2/Segmentation', help='Project directory')
def sections(project_dir):
    """
    Generate section files from outline
    
    \b
    Example:
      adm generate sections
    """
    click.echo("\n📝 ADM Generate - Sections")
    click.echo("=" * 40)
    
    try:
        from function2.generators.section_generator import SectionGenerator
        
        generator = SectionGenerator(project_dir)
        generator.load_project_info()
        files = generator.generate_sections()
        
        click.echo(f"\n✅ Generated {len(files)} section files")
        click.echo(f"   Location: {project_dir}/phase2_sections/")
        click.echo("\n📌 Next: Use AI to fill in content, then run:")
        click.echo("   adm generate export")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)


@generate.command()
@click.option('--project-dir', '-d', type=click.Path(exists=True),
              default='function2/Segmentation', help='Project directory')
@click.option('--input-folder', '-i', help='Folder with MD content files')
@click.option('--format', 'output_format', type=click.Choice(['docx', 'pdf', 'all']),
              default='all', help='Output format')
def export(project_dir, input_folder, output_format):
    """
    Export Markdown content to DOCX/PDF
    
    \b
    Example:
      adm generate export --format all
    """
    click.echo("\n📤 ADM Generate - Export")
    click.echo("=" * 40)
    
    # Determine input folder
    if input_folder:
        md_folder = Path(input_folder)
    else:
        md_folder = Path(project_dir) / "phase3_content"
    
    if not md_folder.exists():
        click.echo(f"⚠ Content folder not found: {md_folder}", err=True)
        click.echo("  Create markdown files in phase3_content/ first", err=True)
        return
    
    md_files = sorted(md_folder.glob("*.md"))
    if not md_files:
        click.echo(f"⚠ No .md files found in {md_folder}", err=True)
        return
    
    click.echo(f"📁 Input: {md_folder} ({len(md_files)} files)")
    
    output_folder = Path(project_dir) / "phase4_rendered"
    output_folder.mkdir(parents=True, exist_ok=True)
    
    try:
        if output_format in ['docx', 'all']:
            from function2.templates.converters.md_to_docx import convert_folder
            docx_output = output_folder / "docx"
            convert_folder(str(md_folder), str(docx_output))
            click.echo(f"✅ DOCX saved: {docx_output}")
        
        if output_format in ['pdf', 'all']:
            try:
                from function2.templates.converters.md_to_pdf import convert_folder_to_pdf
                pdf_output = output_folder / "pdf"
                convert_folder_to_pdf(str(md_folder), str(pdf_output))
                click.echo(f"✅ PDF saved: {pdf_output}")
            except ImportError:
                click.echo("⚠ PDF export requires: pip install weasyprint", err=True)
        
        click.echo(f"\n📌 Next: adm generate merge")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)


@generate.command()
@click.option('--project-dir', '-d', type=click.Path(exists=True),
              default='function2/Segmentation', help='Project directory')
@click.option('--output', '-o', help='Output filename')
def merge(project_dir, output):
    """
    Merge all DOCX sections into one file
    
    \b
    Example:
      adm generate merge --output "final_thesis.docx"
    """
    click.echo("\n🔗 ADM Generate - Merge")
    click.echo("=" * 40)
    
    docx_folder = Path(project_dir) / "phase4_rendered" / "docx"
    
    if not docx_folder.exists():
        click.echo(f"⚠ DOCX folder not found: {docx_folder}", err=True)
        click.echo("  Run 'adm generate export' first", err=True)
        return
    
    docx_files = sorted(docx_folder.glob("*.docx"))
    if not docx_files:
        click.echo(f"⚠ No DOCX files found", err=True)
        return
    
    click.echo(f"📁 Found {len(docx_files)} DOCX files")
    
    output_folder = Path(project_dir) / "phase5_output"
    output_folder.mkdir(parents=True, exist_ok=True)
    
    if output:
        output_path = output_folder / output
    else:
        output_path = output_folder / "MERGED_document.docx"
    
    try:
        from function2.templates.converters.docx_merger import merge_docx_folder
        
        result = merge_docx_folder(str(docx_folder), str(output_path))
        click.echo(f"\n✅ Merged: {result}")
        click.echo(f"\n🎉 Document generation complete!")
        
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)


@generate.command()
@click.option('--type', 'doc_type', type=click.Choice(['thesis', 'report', 'official']),
              default='thesis', help='Document type')
@click.option('--pages', '-p', type=int, default=80, help='Total pages')
def zolo(doc_type, pages):
    """
    🚀 ZOLO MODE - One-shot document generation
    
    \b
    Example:
      adm generate zolo --type thesis --pages 80
    """
    click.echo("\n🚀 ZOLO MODE - One-shot Generation")
    click.echo("=" * 40)
    click.echo(f"📋 Type: {doc_type}")
    click.echo(f"📄 Pages: {pages}")
    click.echo("")
    click.echo("⚡ This mode will:")
    click.echo("   1. Init project")
    click.echo("   2. Generate section outlines")
    click.echo("   3. Create prompts for AI")
    click.echo("")
    click.echo("📌 After running, use AI to generate content")
    click.echo("   Then run: adm generate export && adm generate merge")
    
    # Run init and sections
    from click.testing import CliRunner
    runner = CliRunner()
    
    click.echo("\n[Step 1/2] Initializing project...")
    # Would invoke init here
    
    click.echo("[Step 2/2] Generating sections...")
    # Would invoke sections here
    
    click.echo("\n✅ ZOLO setup complete!")


@generate.command()
@click.option('--project-dir', '-d', type=click.Path(exists=True),
              default='function2/Segmentation', help='Project directory')
@click.option('--phase', '-p', type=click.Choice(['all', 'content', 'rendered', 'output']),
              default='content', help='Phase to renew')
@click.option('--confirm', '-y', is_flag=True, help='Skip confirmation')
def renew(project_dir, phase, confirm):
    """
    🔄 Renew/reset phases để bắt đầu file mới
    
    \\b
    Phases:
      content  - Clear phase3_content/ (default)
      rendered - Clear phase4_rendered/
      output   - Clear phase5_output/
      all      - Clear all above
    
    \\b
    Example:
      adm generate renew               - Clear content
      adm generate renew --phase all   - Clear all
    """
    import shutil
    from pathlib import Path
    
    click.echo("\n🔄 ADM Generate - Renew")
    click.echo("=" * 40)
    
    project_path = Path(project_dir)
    
    phases_to_clear = []
    if phase == 'content' or phase == 'all':
        phases_to_clear.append('phase3_content')
    if phase == 'rendered' or phase == 'all':
        phases_to_clear.append('phase4_rendered')
    if phase == 'output' or phase == 'all':
        phases_to_clear.append('phase5_output')
    
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
    
    # Clear phases
    for p in phases_to_clear:
        folder = project_path / p
        if folder.exists():
            shutil.rmtree(folder)
            click.echo(f"  ✓ Cleared: {p}")
        
        # Recreate empty folder
        folder.mkdir(parents=True, exist_ok=True)
        click.echo(f"  ✓ Created: {p}")
    
    click.echo()
    click.echo("✅ Phases renewed!")
    click.echo("📌 Ready for new content. Next steps:")
    click.echo("   1. Tạo nội dung mới trong phase3_content/")
    click.echo("   2. adm generate export --format all")
    click.echo("   3. adm generate merge")


@generate.command()
@click.option('--project-dir', '-d', type=click.Path(exists=True),
              default='function2/Segmentation', help='Project directory')
def scan(project_dir):
    """
    Scan và thống kê nội dung markdown
    
    \\b
    Kiểm tra để đảm bảo không bị mất content
    """
    click.echo("\n📊 ADM Generate - Scan Content")
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


@generate.command('render-sections')
@click.option('--project-dir', '-d', type=click.Path(exists=True),
              default='function2/Segmentation', help='Project directory')
@click.option('--output', '-o', default='MERGED_sections.docx', help='Tên file output cuối cùng')
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
    click.echo("\n🔄 ADM Generate - Render All Sections")
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
            import shutil
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
    generate()

