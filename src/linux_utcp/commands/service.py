"""
Service management commands for linux-utcp
"""
import subprocess
from typing import Dict, Any, Optional


def list_services() -> Dict[str, Any]:
    """
    List all systemd services with their current status.

    Returns:
        dict: Service information with keys:
            - services (str): Formatted service listing
            - running_count (int): Number of running services
    """
    result = {}

    try:
        # Get all services
        all_services = subprocess.run(
            ['systemctl', 'list-units', '--type=service', '--all', '--no-pager'],
            capture_output=True,
            text=True,
            check=True
        )
        result['services'] = all_services.stdout

        # Get running count
        running_services = subprocess.run(
            ['systemctl', 'list-units', '--type=service', '--state=running', '--no-pager'],
            capture_output=True,
            text=True,
            check=True
        )
        # Count lines (minus header and footer)
        running_lines = [line for line in running_services.stdout.split('\n') if '.service' in line]
        result['running_count'] = len(running_lines)

    except subprocess.CalledProcessError as e:
        result['services'] = f"Error listing services: {e}"
        result['running_count'] = 0
    except FileNotFoundError:
        result['services'] = "Error: systemctl not found (systemd required)"
        result['running_count'] = 0

    return result


def get_service_status(service_name: str) -> Dict[str, Any]:
    """
    Get detailed status of a specific systemd service.

    Args:
        service_name: Name of the systemd service (e.g., 'nginx', 'sshd')

    Returns:
        dict: Service status with keys:
            - status (str): Full systemctl status output
            - error (str, optional): Error message if service not found
    """
    result = {}

    # Auto-append .service if not present
    if not service_name.endswith('.service'):
        service_name = f"{service_name}.service"

    try:
        status_output = subprocess.run(
            ['systemctl', 'status', service_name, '--no-pager', '--full'],
            capture_output=True,
            text=True,
            check=False  # Don't raise on non-zero exit (service might be stopped)
        )
        result['status'] = status_output.stdout

        # Check if service exists
        if 'could not be found' in status_output.stdout.lower() or \
           'not loaded' in status_output.stdout.lower():
            result['error'] = f"Service '{service_name}' not found"

    except FileNotFoundError:
        result['error'] = "Error: systemctl not found (systemd required)"
        result['status'] = ""

    return result


def get_service_logs(service_name: str, lines: int = 50) -> Dict[str, Any]:
    """
    Get recent logs for a specific systemd service.

    Args:
        service_name: Name of the systemd service
        lines: Number of log lines to retrieve (default: 50, max: 10000)

    Returns:
        dict: Service logs with keys:
            - logs (str): Log entries
            - error (str, optional): Error message if service not found
    """
    result = {}

    # Validate lines parameter
    lines = max(1, min(lines, 10000))

    # Auto-append .service if not present
    if not service_name.endswith('.service'):
        service_name = f"{service_name}.service"

    try:
        logs_output = subprocess.run(
            ['journalctl', '-u', service_name, '-n', str(lines), '--no-pager'],
            capture_output=True,
            text=True,
            check=False
        )
        result['logs'] = logs_output.stdout

        # Check if service exists
        if 'No journal files were found' in logs_output.stdout or \
           logs_output.returncode != 0 and not logs_output.stdout:
            result['error'] = f"Service '{service_name}' not found or no logs available"

    except FileNotFoundError:
        result['error'] = "Error: journalctl not found (systemd required)"
        result['logs'] = ""

    return result
