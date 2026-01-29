"""
ADM CLI Main
=============
Main entry point for CLI commands
"""

import click

from . import convert, generate


@click.group()
@click.version_option(version="1.0.0", prog_name="adm")
def cli():
    """
    Academic Document Manager - Xử lý văn bản học thuật
    
    \b
    Functions:
      adm convert   - Convert PDF/DOCX → Markdown → LaTeX
      adm generate  - Generate documents from AI content
    """
    pass


# Register sub-commands
cli.add_command(convert.convert, name="convert")
cli.add_command(generate.generate, name="generate")


@cli.command()
def gui():
    """Launch GUI application"""
    try:
        from src.gui.main_window import MainWindow
        click.echo("🚀 Launching ADM GUI...")
        app = MainWindow()
        app.mainloop()
    except ImportError as e:
        click.echo(f"⚠ GUI not available: {e}", err=True)
        click.echo("Install with: pip install customtkinter", err=True)
        raise SystemExit(1)


@cli.command()
def info():
    """Show system information"""
    import sys
    import os
    
    click.echo("\n📋 ADM System Information")
    click.echo("=" * 40)
    click.echo(f"Python: {sys.version}")
    click.echo(f"OS: {os.name}")
    click.echo(f"CWD: {os.getcwd()}")
    
    # Check dependencies
    click.echo("\n📦 Dependencies:")
    
    deps = [
        ("python-docx", "docx"),
        ("PyMuPDF", "fitz"),
        ("customtkinter", "customtkinter"),
        ("mistune", "mistune"),
        ("PyYAML", "yaml"),
        ("click", "click"),
    ]
    
    for name, module in deps:
        try:
            __import__(module)
            click.echo(f"  ✅ {name}")
        except ImportError:
            click.echo(f"  ❌ {name}")


def main():
    """Entry point"""
    cli()


if __name__ == "__main__":
    main()
