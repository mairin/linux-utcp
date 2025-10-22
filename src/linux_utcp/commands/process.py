"""
Process management commands for linux-utcp
"""
import psutil
from typing import Dict, Any, List
from datetime import datetime


def list_processes() -> Dict[str, Any]:
    """
    List running processes with CPU and memory usage (top 100 by CPU).

    Returns:
        dict: Process information with keys:
            - processes (list[dict]): List of process information, each containing:
                - pid (int): Process ID
                - user (str): Process owner username
                - cpu_percent (float): CPU usage percentage
                - memory_percent (float): Memory usage percentage
                - status (str): Process status
                - name (str): Process name
                - command (str): Full command line
            - total_count (int): Total number of processes
    """
    result = {'processes': []}

    all_processes = []

    # Iterate over all processes
    for proc in psutil.process_iter(['pid', 'name', 'username', 'status', 'cmdline']):
        try:
            # Get process info
            pinfo = proc.info

            # Get CPU and memory percent (may require brief wait)
            cpu_percent = proc.cpu_percent(interval=0)
            memory_percent = proc.memory_percent()

            process_info = {
                'pid': pinfo['pid'],
                'user': pinfo['username'] or 'unknown',
                'cpu_percent': round(cpu_percent, 1),
                'memory_percent': round(memory_percent, 1),
                'status': pinfo['status'],
                'name': pinfo['name'],
                'command': ' '.join(pinfo['cmdline']) if pinfo['cmdline'] else pinfo['name']
            }
            all_processes.append(process_info)

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Skip processes we can't access
            continue

    # Sort by CPU usage (descending) and take top 100
    all_processes.sort(key=lambda p: p['cpu_percent'], reverse=True)
    result['processes'] = all_processes[:100]
    result['total_count'] = len(all_processes)

    return result


def get_process_info(pid: int) -> Dict[str, Any]:
    """
    Get detailed information about a specific process.

    Args:
        pid: Process ID (must be >= 1)

    Returns:
        dict: Process information with keys:
            - name (str): Process name
            - exe (str): Executable path
            - cmdline (str): Full command line
            - status (str): Process status
            - user (str): Process owner
            - pid (int): Process ID
            - ppid (int): Parent process ID
            - cpu_percent (float): CPU usage percentage
            - memory_rss (int): Resident set size in bytes
            - memory_vms (int): Virtual memory size in bytes
            - memory_percent (float): Memory usage percentage
            - created (str): Process creation timestamp
            - cpu_time_user (float): User CPU time in seconds
            - cpu_time_system (float): System CPU time in seconds
            - threads (int): Number of threads
            - open_files (int): Number of open files
            - error (str, optional): Error message if process not found
    """
    result = {}

    # Validate PID
    if pid < 1:
        result['error'] = f"Invalid PID: {pid} (must be >= 1)"
        return result

    try:
        proc = psutil.Process(pid)

        # Basic info
        result['name'] = proc.name()
        result['exe'] = proc.exe() if proc.exe() else 'unknown'
        result['cmdline'] = ' '.join(proc.cmdline()) if proc.cmdline() else proc.name()
        result['status'] = proc.status()
        result['user'] = proc.username()
        result['pid'] = proc.pid
        result['ppid'] = proc.ppid()

        # CPU and memory
        result['cpu_percent'] = round(proc.cpu_percent(interval=0.1), 1)

        mem_info = proc.memory_info()
        result['memory_rss'] = mem_info.rss
        result['memory_vms'] = mem_info.vms
        result['memory_percent'] = round(proc.memory_percent(), 2)

        # Timing info
        create_time = datetime.fromtimestamp(proc.create_time())
        result['created'] = create_time.strftime('%Y-%m-%d %H:%M:%S')

        cpu_times = proc.cpu_times()
        result['cpu_time_user'] = round(cpu_times.user, 2)
        result['cpu_time_system'] = round(cpu_times.system, 2)

        # Thread and file info
        result['threads'] = proc.num_threads()

        try:
            result['open_files'] = len(proc.open_files())
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            result['open_files'] = 0

    except psutil.NoSuchProcess:
        result['error'] = f"Process {pid} not found"
    except psutil.AccessDenied:
        result['error'] = f"Access denied to process {pid} (try sudo)"
    except Exception as e:
        result['error'] = f"Error getting process info: {str(e)}"

    return result
