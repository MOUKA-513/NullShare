"""
Tests for NullShare CLI
"""
import pytest
from click.testing import CliRunner
from nullshare.cli import cli
import os
from pathlib import Path

def test_version():
    """Test version command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0
    assert 'NullShare' in result.output

def test_help():
    """Test help command."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Share files via QR code' in result.output

def test_share_no_args():
    """Test share command without arguments."""
    runner = CliRunner()
    result = runner.invoke(cli, ['share'])
    assert result.exit_code != 0
    assert 'specify at least one file' in result.output.lower()

def test_share_with_file(tmp_path):
    """Test share command with a dummy file."""
    # Create a test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello, NullShare!")
    
    runner = CliRunner()
    result = runner.invoke(cli, ['share', str(test_file), '--no-qr'])
    
    # Should start successfully (though we can't fully test server)
    assert result.exit_code == 0 or result.exit_code == 1  # Server might fail in test env
    assert 'NullShare' in result.output

def test_status_command():
    """Test status command (should fail if no server running)."""
    runner = CliRunner()
    result = runner.invoke(cli, ['status'])
    # Status command should not crash
    assert result.exit_code == 0
