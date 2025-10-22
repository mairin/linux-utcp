"""
Output formatting utilities for linux-utcp
"""
import json
from typing import Any, Dict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


def format_output(data: Any, format_type: str) -> str:
    """
    Format output data as JSON or human-readable text.

    Args:
        data: The data to format (dict, list, or primitive)
        format_type: Either 'json' or 'text'

    Returns:
        str: Formatted output string
    """
    if format_type == 'json':
        return json.dumps(data, indent=2)
    else:
        return format_text(data)


def format_text(data: Any) -> str:
    """
    Format data as human-readable text using Rich library.

    Args:
        data: The data to format

    Returns:
        str: Human-readable text output
    """
    console = Console()

    if isinstance(data, dict):
        # Create a table for dict data
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Field", style="green")
        table.add_column("Value", style="white")

        for key, value in data.items():
            # Format the key nicely (snake_case to Title Case)
            formatted_key = key.replace('_', ' ').title()
            table.add_row(formatted_key, str(value))

        # Capture console output to string
        import io
        string_io = io.StringIO()
        temp_console = Console(file=string_io, force_terminal=True)
        temp_console.print(table)
        return string_io.getvalue()

    elif isinstance(data, list):
        # For lists, just join items with newlines
        return '\n'.join(str(item) for item in data)

    else:
        # For primitives, just convert to string
        return str(data)


def format_error(error_message: str, format_type: str) -> str:
    """
    Format error messages consistently.

    Args:
        error_message: The error message
        format_type: Either 'json' or 'text'

    Returns:
        str: Formatted error output
    """
    if format_type == 'json':
        return json.dumps({"error": error_message}, indent=2)
    else:
        return f"ERROR: {error_message}"
