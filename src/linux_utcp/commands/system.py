"""
System information commands for linux-utcp
"""
import platform
import subprocess
import os
from datetime import datetime
from typing import Dict, Any, List
import psutil


def get_system_info() -> Dict[str, Any]:
    """
    Get basic system information including OS version, kernel, hostname, and uptime.

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
    result = {}

    # Hostname
    result['hostname'] = platform.node()

    # OS information from /etc/os-release
    try:
        with open('/etc/os-release', 'r') as f:
            os_release = {}
            for line in f:
                if '=' in line:
                    key, value = line.rstrip().split('=', 1)
                    os_release[key] = value.strip('"')
        result['os'] = os_release.get('NAME', 'Unknown')
        result['os_version'] = os_release.get('VERSION', 'Unknown')
    except FileNotFoundError:
        result['os'] = 'Unknown'
        result['os_version'] = 'Unknown'

    # Kernel version
    result['kernel'] = platform.release()

    # Architecture
    result['architecture'] = platform.machine()

    # Uptime - human readable
    try:
        uptime_output = subprocess.run(
            ['uptime', '-p'],
            capture_output=True,
            text=True,
            check=True
        )
        result['uptime'] = uptime_output.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        result['uptime'] = 'Unknown'

    # Boot time
    try:
        boot_time_output = subprocess.run(
            ['uptime', '-s'],
            capture_output=True,
            text=True,
            check=True
        )
        result['boot_time'] = boot_time_output.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        result['boot_time'] = 'Unknown'

    return result


def get_cpu_info() -> Dict[str, Any]:
    """
    Get CPU information and load averages.

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
    result = {}

    # CPU model from /proc/cpuinfo
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if 'model name' in line:
                    result['cpu_model'] = line.split(':')[1].strip()
                    break
            else:
                result['cpu_model'] = 'Unknown'
    except FileNotFoundError:
        result['cpu_model'] = 'Unknown'

    # CPU cores
    result['physical_cores'] = psutil.cpu_count(logical=False) or 0
    result['logical_cores'] = psutil.cpu_count(logical=True) or 0

    # CPU frequency
    try:
        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            result['cpu_freq_current'] = round(cpu_freq.current, 2)
            result['cpu_freq_min'] = round(cpu_freq.min, 2)
            result['cpu_freq_max'] = round(cpu_freq.max, 2)
        else:
            result['cpu_freq_current'] = 0.0
            result['cpu_freq_min'] = 0.0
            result['cpu_freq_max'] = 0.0
    except Exception:
        result['cpu_freq_current'] = 0.0
        result['cpu_freq_min'] = 0.0
        result['cpu_freq_max'] = 0.0

    # CPU usage
    result['cpu_usage_per_core'] = psutil.cpu_percent(interval=1, percpu=True)
    result['overall_cpu_usage'] = psutil.cpu_percent(interval=0)

    # Load averages
    load_avg = os.getloadavg()
    result['load_average_1m'] = round(load_avg[0], 2)
    result['load_average_5m'] = round(load_avg[1], 2)
    result['load_average_15m'] = round(load_avg[2], 2)

    return result


def get_memory_info() -> Dict[str, Any]:
    """
    Get memory usage including RAM and swap details.

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
    result = {}

    # RAM information
    ram = psutil.virtual_memory()
    result['ram_total'] = ram.total
    result['ram_available'] = ram.available
    result['ram_used'] = ram.used
    result['ram_used_percent'] = round(ram.percent, 2)
    result['ram_free'] = ram.free

    # Swap information
    swap = psutil.swap_memory()
    result['swap_total'] = swap.total
    result['swap_used'] = swap.used
    result['swap_used_percent'] = round(swap.percent, 2)
    result['swap_free'] = swap.free

    return result


def get_disk_usage() -> Dict[str, Any]:
    """
    Get filesystem usage and mount points.

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
    result = {'filesystems': []}

    # Get all disk partitions
    partitions = psutil.disk_partitions()

    for partition in partitions:
        # Skip special filesystems
        if partition.fstype == '' or partition.fstype == 'squashfs':
            continue

        try:
            usage = psutil.disk_usage(partition.mountpoint)

            filesystem_info = {
                'filesystem': partition.device,
                'size': _human_readable_size(usage.total),
                'used': _human_readable_size(usage.used),
                'available': _human_readable_size(usage.free),
                'use_percent': round(usage.percent, 1),
                'mounted_on': partition.mountpoint
            }
            result['filesystems'].append(filesystem_info)
        except (PermissionError, OSError):
            # Skip filesystems we can't access
            continue

    return result


def _human_readable_size(size_bytes: int) -> str:
    """
    Convert bytes to human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        str: Human-readable size (e.g., "1.5G", "512M")
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if abs(size_bytes) < 1024.0:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f}P"
