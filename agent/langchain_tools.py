"""
LangChain Tool wrappers for linux-utcp CLI commands
"""
import subprocess
import json
from typing import Optional

from langchain_core.tools import tool


@tool
def get_system_info() -> dict:
    """Get basic system information including OS version, kernel, hostname, and uptime.

    Returns:
        dict: System information with hostname, os, os_version, kernel, architecture, uptime, boot_time
    """
    result = subprocess.run(
        ['linux-utcp', 'system', 'info', '--format', 'json'],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)


@tool
def get_cpu_info() -> dict:
    """Get CPU information and load averages.

    Returns:
        dict: CPU information including cpu_model, physical_cores, logical_cores, frequencies,
              cpu_usage_per_core, overall_cpu_usage, load_average_1m, load_average_5m, load_average_15m
    """
    result = subprocess.run(
        ['linux-utcp', 'system', 'cpu', '--format', 'json'],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)


@tool
def get_memory_info() -> dict:
    """Get memory usage including RAM and swap details.

    Returns:
        dict: Memory information including ram_total, ram_available, ram_used, ram_used_percent,
              ram_free, swap_total, swap_used, swap_used_percent, swap_free (all sizes in bytes)
    """
    result = subprocess.run(
        ['linux-utcp', 'system', 'memory', '--format', 'json'],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)


@tool
def get_disk_usage() -> dict:
    """Get filesystem usage and mount points.

    Returns:
        dict: Disk usage with filesystems list containing filesystem, size, used, available,
              use_percent, mounted_on for each partition
    """
    result = subprocess.run(
        ['linux-utcp', 'system', 'disk', '--format', 'json'],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)


@tool
def list_services() -> dict:
    """List all systemd services with their current status.

    Returns:
        dict: Service information with services (formatted listing) and running_count
    """
    result = subprocess.run(
        ['linux-utcp', 'service', 'list', '--format', 'json'],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)


@tool
def get_service_status(service_name: str) -> dict:
    """Get detailed status of a specific systemd service.

    Args:
        service_name: Name of the systemd service (e.g., 'nginx', 'sshd')

    Returns:
        dict: Service status with status field and optional error field
    """
    result = subprocess.run(
        ['linux-utcp', 'service', 'status', service_name, '--format', 'json'],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)


@tool
def get_service_logs(service_name: str, lines: int = 50) -> dict:
    """Get recent logs for a specific systemd service.

    Args:
        service_name: Name of the systemd service
        lines: Number of log lines to retrieve (default: 50, max: 10000)

    Returns:
        dict: Service logs with logs field and optional error field
    """
    result = subprocess.run(
        ['linux-utcp', 'service', 'logs', service_name, '--lines', str(lines), '--format', 'json'],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)


@tool
def list_processes() -> dict:
    """List running processes with CPU and memory usage (top 100 by CPU).

    Returns:
        dict: Process information with processes list (pid, user, cpu_percent, memory_percent,
              status, name, command) and total_count
    """
    result = subprocess.run(
        ['linux-utcp', 'process', 'list', '--format', 'json'],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)


@tool
def get_process_info(pid: int) -> dict:
    """Get detailed information about a specific process.

    Args:
        pid: Process ID (must be >= 1)

    Returns:
        dict: Detailed process information with 15+ fields including name, exe, cmdline, status,
              user, cpu_percent, memory_rss, memory_vms, memory_percent, created, cpu_time_user,
              cpu_time_system, threads, open_files
    """
    result = subprocess.run(
        ['linux-utcp', 'process', 'info', str(pid), '--format', 'json'],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)


@tool
def get_network_interfaces() -> dict:
    """Get network interface information including IP addresses.

    Returns:
        dict: Network information with interfaces list (name, status, speed, mtu, ipv4_addresses,
              ipv6_addresses, mac_address) and io_stats (bytes_sent, bytes_recv, packets_sent,
              packets_recv, errors_in, errors_out, drops_in, drops_out)
    """
    result = subprocess.run(
        ['linux-utcp', 'network', 'interfaces', '--format', 'json'],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)


@tool
def get_listening_ports() -> dict:
    """Get ports that are listening on the system.

    Returns:
        dict: Listening ports with listening_ports list (proto, local_address, pid, program)
              and total_count
    """
    result = subprocess.run(
        ['linux-utcp', 'network', 'ports', '--format', 'json'],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)


# Export all tools as a list
ALL_TOOLS = [
    get_system_info,
    get_cpu_info,
    get_memory_info,
    get_disk_usage,
    list_services,
    get_service_status,
    get_service_logs,
    list_processes,
    get_process_info,
    get_network_interfaces,
    get_listening_ports,
]
