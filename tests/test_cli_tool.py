"""CLI tests using subprocess."""

import subprocess
import sys


def run_command(args):
    """Run the CLI and return output."""
    result = subprocess.run(
        [sys.executable, "main.py"] + args,
        capture_output=True,
        text=True,
    )
    return result.stdout + result.stderr


def test_help_command():
    output = run_command([])
    assert "Project Management CLI Tool" in output or "usage:" in output


def test_add_user_help():
    output = run_command(["add-user", "--help"])
    assert "--name" in output
