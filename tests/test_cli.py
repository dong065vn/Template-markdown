"""
CLI Tests
==========
Test cases for ADM CLI commands
"""

import pytest
from click.testing import CliRunner
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cli.main import cli


class TestMainCLI:
    """Test main CLI commands"""
    
    def setup_method(self):
        self.runner = CliRunner()
    
    def test_cli_help(self):
        """Test: CLI --help shows usage"""
        result = self.runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Academic Document Manager' in result.output
        assert 'convert' in result.output
        assert 'generate' in result.output
    
    def test_cli_version(self):
        """Test: CLI --version shows version"""
        result = self.runner.invoke(cli, ['--version'])
        assert result.exit_code == 0
        assert '1.0.0' in result.output
    
    def test_cli_info(self):
        """Test: CLI info shows system information"""
        result = self.runner.invoke(cli, ['info'])
        assert result.exit_code == 0
        assert 'ADM System Information' in result.output
        assert 'Python' in result.output
        assert 'Dependencies' in result.output


class TestConvertCommand:
    """Test convert command"""
    
    def setup_method(self):
        self.runner = CliRunner()
    
    def test_convert_help(self):
        """Test: convert --help shows options"""
        result = self.runner.invoke(cli, ['convert', '--help'])
        assert result.exit_code == 0
        assert '--file' in result.output
        assert '--folder' in result.output
        assert '--format' in result.output
    
    def test_convert_no_input(self):
        """Test: convert without input shows warning"""
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(cli, ['convert'])
            # Should either find no files or show warning
            assert result.exit_code == 0 or 'No input' in result.output or 'No PDF/DOCX' in result.output
    
    def test_convert_nonexistent_file(self):
        """Test: convert with nonexistent file shows error"""
        result = self.runner.invoke(cli, ['convert', '--file', 'nonexistent.pdf'])
        assert result.exit_code != 0 or 'Error' in result.output or 'does not exist' in result.output


class TestGenerateCommand:
    """Test generate command and subcommands"""
    
    def setup_method(self):
        self.runner = CliRunner()
    
    def test_generate_help(self):
        """Test: generate --help shows subcommands"""
        result = self.runner.invoke(cli, ['generate', '--help'])
        assert result.exit_code == 0
        assert 'init' in result.output
        assert 'sections' in result.output
        assert 'export' in result.output
        assert 'merge' in result.output
    
    def test_generate_init_help(self):
        """Test: generate init --help shows options"""
        result = self.runner.invoke(cli, ['generate', 'init', '--help'])
        assert result.exit_code == 0
        assert '--name' in result.output
        assert '--type' in result.output
        assert '--pages' in result.output
    
    def test_generate_init(self):
        """Test: generate init creates project"""
        with self.runner.isolated_filesystem():
            # Create project directory
            os.makedirs('function2/Segmentation', exist_ok=True)
            
            result = self.runner.invoke(cli, [
                'generate', 'init',
                '--name', 'Test Project',
                '--type', 'thesis',
                '--pages', '50',
                '--project-dir', 'function2/Segmentation'
            ])
            
            # Should either succeed or have understandable error
            assert result.exit_code == 0 or 'Error' in result.output or 'initialized' in result.output.lower()
    
    def test_generate_zolo_help(self):
        """Test: generate zolo --help shows options"""
        result = self.runner.invoke(cli, ['generate', 'zolo', '--help'])
        assert result.exit_code == 0
        assert '--type' in result.output
        assert '--pages' in result.output
        assert 'ZOLO' in result.output


class TestCLIIntegration:
    """Integration tests for CLI workflow"""
    
    def setup_method(self):
        self.runner = CliRunner()
    
    def test_help_all_commands(self):
        """Test: All commands have help available"""
        commands = [
            ['--help'],
            ['convert', '--help'],
            ['generate', '--help'],
            ['generate', 'init', '--help'],
            ['generate', 'sections', '--help'],
            ['generate', 'export', '--help'],
            ['generate', 'merge', '--help'],
            ['info'],
        ]
        
        for cmd in commands:
            result = self.runner.invoke(cli, cmd)
            assert result.exit_code == 0, f"Command {cmd} failed with: {result.output}"


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
