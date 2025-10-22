#!/usr/bin/env python3
"""
Generate UTCP manual for linux-utcp tools
"""
import json
from pathlib import Path
from typing import Dict, List

from utcp.data.utcp_manual import UtcpManual
from utcp.python_specific_tooling.tool_decorator import utcp_tool
from utcp_cli.cli_call_template import CliCallTemplate


# Define all tools using decorators

@utcp_tool(
    tool_call_template=CliCallTemplate(
        commands=[{"command": "linux-utcp system info --format json"}]
    ),
    tags=["system", "diagnostics", "linux", "info"]
)
def get_system_info() -> Dict:
    """Get basic system information including OS version, kernel, hostname, and uptime.

    Returns:
        dict: System information with keys:
            - hostname (str): System hostname
            - os (str): Operating system name
            - os_version (str): OS version identifier
            - kernel (str): Linux kernel version
            - architecture (str): CPU architecture
            - uptime (str): System uptime in human-readable format
            - boot_time (str): System boot timestamp
    """
    pass


@utcp_tool(
    tool_call_template=CliCallTemplate(
        commands=[{"command": "linux-utcp system cpu --format json"}]
    ),
    tags=["system", "diagnostics", "cpu", "performance", "load"]
)
def get_cpu_info() -> Dict:
    """Get CPU information and load averages.

    Returns:
        dict: CPU information with keys:
            - cpu_model (str): CPU model name
            - physical_cores (int): Number of physical cores
            - logical_cores (int): Number of logical cores
            - cpu_freq_current (float): Current CPU frequency in MHz
            - cpu_freq_min (float): Minimum CPU frequency in MHz
            - cpu_freq_max (float): Maximum CPU frequency in MHz
            - cpu_usage_per_core (list[float]): CPU usage percentage per core
            - overall_cpu_usage (float): Overall CPU usage percentage
            - load_average_1m (float): 1-minute load average
            - load_average_5m (float): 5-minute load average
            - load_average_15m (float): 15-minute load average
    """
    pass


@utcp_tool(
    tool_call_template=CliCallTemplate(
        commands=[{"command": "linux-utcp system memory --format json"}]
    ),
    tags=["system", "diagnostics", "memory", "ram", "swap"]
)
def get_memory_info() -> Dict:
    """Get memory usage including RAM and swap details.

    Returns:
        dict: Memory information with keys:
            - ram_total (int): Total RAM in bytes
            - ram_available (int): Available RAM in bytes
            - ram_used (int): Used RAM in bytes
            - ram_used_percent (float): RAM usage percentage
            - ram_free (int): Free RAM in bytes
            - swap_total (int): Total swap in bytes
            - swap_used (int): Used swap in bytes
            - swap_used_percent (float): Swap usage percentage
            - swap_free (int): Free swap in bytes
    """
    pass


@utcp_tool(
    tool_call_template=CliCallTemplate(
        commands=[{"command": "linux-utcp system disk --format json"}]
    ),
    tags=["system", "diagnostics", "disk", "storage", "filesystem"]
)
def get_disk_usage() -> Dict:
    """Get filesystem usage and mount points.

    Returns:
        dict: Disk usage information with key:
            - filesystems (list[dict]): List of filesystem information, each containing:
                - filesystem (str): Device name
                - size (str): Total size in human-readable format
                - used (str): Used space in human-readable format
                - available (str): Available space in human-readable format
                - use_percent (float): Usage percentage
                - mounted_on (str): Mount point
    """
    pass


# Service Management Tools

@utcp_tool(
    tool_call_template=CliCallTemplate(
        commands=[{"command": "linux-utcp service list --format json"}]
    ),
    tags=["service", "systemd", "diagnostics", "management"]
)
def list_services() -> Dict:
    """List all systemd services with their current status.

    Returns:
        dict: Service information with keys:
            - services (str): Formatted service listing
            - running_count (int): Number of running services
    """
    pass


@utcp_tool(
    tool_call_template=CliCallTemplate(
        commands=[{"command": "linux-utcp service status UTCP_ARG_service_name_UTCP_END --format json"}]
    ),
    tags=["service", "systemd", "status", "diagnostics"]
)
def get_service_status(service_name: str) -> Dict:
    """Get detailed status of a specific systemd service.

    Args:
        service_name: Name of the systemd service (e.g., 'nginx', 'sshd')

    Returns:
        dict: Service status with keys:
            - status (str): Full systemctl status output
            - error (str, optional): Error message if service not found
    """
    pass


@utcp_tool(
    tool_call_template=CliCallTemplate(
        commands=[{"command": "linux-utcp service logs UTCP_ARG_service_name_UTCP_END --lines UTCP_ARG_lines_UTCP_END --format json"}]
    ),
    tags=["service", "systemd", "logs", "diagnostics"]
)
def get_service_logs(service_name: str, lines: int = 50) -> Dict:
    """Get recent logs for a specific systemd service.

    Args:
        service_name: Name of the systemd service
        lines: Number of log lines to retrieve (default: 50, max: 10000)

    Returns:
        dict: Service logs with keys:
            - logs (str): Log entries
            - error (str, optional): Error message if service not found
    """
    pass


# Process Management Tools

@utcp_tool(
    tool_call_template=CliCallTemplate(
        commands=[{"command": "linux-utcp process list --format json"}]
    ),
    tags=["process", "diagnostics", "performance", "monitoring"]
)
def list_processes() -> Dict:
    """List running processes with CPU and memory usage (top 100 by CPU).

    Returns:
        dict: Process information with keys:
            - processes (list[dict]): Process details (pid, user, cpu_percent, memory_percent, status, name, command)
            - total_count (int): Total number of processes
    """
    pass


@utcp_tool(
    tool_call_template=CliCallTemplate(
        commands=[{"command": "linux-utcp process info UTCP_ARG_pid_UTCP_END --format json"}]
    ),
    tags=["process", "diagnostics", "details"]
)
def get_process_info(pid: int) -> Dict:
    """Get detailed information about a specific process.

    Args:
        pid: Process ID (must be >= 1)

    Returns:
        dict: Process information with 15+ fields including CPU, memory, threads, open files
    """
    pass


# Network Diagnostics Tools

@utcp_tool(
    tool_call_template=CliCallTemplate(
        commands=[{"command": "linux-utcp network interfaces --format json"}]
    ),
    tags=["network", "diagnostics", "interface", "connectivity"]
)
def get_network_interfaces() -> Dict:
    """Get network interface information including IP addresses.

    Returns:
        dict: Network information with keys:
            - interfaces (list[dict]): Interface details with IPs, MAC, MTU, speed
            - io_stats (dict): Network I/O statistics
    """
    pass


@utcp_tool(
    tool_call_template=CliCallTemplate(
        commands=[{"command": "linux-utcp network ports --format json"}]
    ),
    tags=["network", "diagnostics", "ports", "listening", "security"]
)
def get_listening_ports() -> Dict:
    """Get ports that are listening on the system.

    Returns:
        dict: Listening ports information with keys:
            - listening_ports (list[dict]): Port details (proto, local_address, pid, program)
            - total_count (int): Total number of listening ports
    """
    pass


def main():
    """Generate the UTCP manual and save it to manuals/linux-utcp.json"""
    # Generate manual from decorated functions
    manual = UtcpManual.create_from_decorators(
        manual_version="1.0.0"
    )

    # Determine output path
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    output_path = repo_root / "manuals" / "linux-utcp.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Export to JSON file and add custom metadata
    manual_dict = manual.model_dump()
    manual_dict['name'] = 'linux-utcp'
    manual_dict['description'] = 'Linux system diagnostics toolkit providing read-only diagnostic tools for system administration and troubleshooting'

    with open(output_path, "w") as f:
        json.dump(manual_dict, f, indent=2)

    print(f"✓ UTCP manual generated successfully: {output_path}")
    print(f"  - Manual version: {manual.manual_version}")
    print(f"  - Tools defined: {len(manual.tools)}")


if __name__ == "__main__":
    main()
