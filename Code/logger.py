#!/usr/bin/env python3
"""
Logging utilities for service diagnostic tool
"""


class Logger:
    """Handle logging to file and console simultaneously"""

    def __init__(self, logfile):
        """
        Initialize logger with a logfile handle.

        Args:
            logfile: File object to write logs to
        """
        self.logfile = logfile

    def log(self, msg):
        """
        Log a message to both console and file.

        Args:
            msg (str): Message to log
        """
        print(msg)
        self.logfile.write(msg + "\n")

    def section(self, title):
        """
        Log a section header with decorative border.

        Args:
            title (str): Section title
        """
        self.log("\n" + "="*85)
        self.log(title)
        self.log("="*85)

    def raw_output(self, label, output):
        """
        Log raw command output with a label.

        Args:
            label (str): Label for the output
            output (str): Raw output content
        """
        self.log(f"[{label}]")
        self.log(output)

    def result(self, status, message):
        """
        Log a result message.

        Args:
            status (str): Status label (e.g., "SUCCESS", "ERROR")
            message (str): Result message
        """
        self.log(f"{status}: {message}")
