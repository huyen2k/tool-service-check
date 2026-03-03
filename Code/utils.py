#!/usr/bin/env python3
"""
Utility functions for executing shell commands
"""

import subprocess


def run_cmd(cmd):
    """
    Execute a shell command and return its output.

    Args:
        cmd (str): Shell command to execute

    Returns:
        str: Combined stdout and stderr output
    """
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error executing command: {str(e)}"
