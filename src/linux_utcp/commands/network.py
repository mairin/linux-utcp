"""
Network diagnostics commands for linux-utcp
"""
import psutil
import subprocess
from typing import Dict, Any, List


def get_network_interfaces() -> Dict[str, Any]:
    """
    Get network interface information including IP addresses.

    Returns:
        dict: Network information with keys:
            - interfaces (list[dict]): List of interface information, each containing:
                - name (str): Interface name
                - status (str): UP/DOWN status
                - speed (int): Link speed in Mbps (0 if unknown)
                - mtu (int): Maximum transmission unit
                - ipv4_addresses (list[dict]): IPv4 addresses with address, netmask, broadcast
                - ipv6_addresses (list[dict]): IPv6 addresses with address, netmask
                - mac_address (str): MAC address
            - io_stats (dict): Network I/O statistics:
                - bytes_sent (int)
                - bytes_recv (int)
                - packets_sent (int)
                - packets_recv (int)
                - errors_in (int)
                - errors_out (int)
                - drops_in (int)
                - drops_out (int)
    """
    result = {'interfaces': []}

    # Get all network interfaces
    addrs = psutil.net_if_addrs()
    stats = psutil.net_if_stats()

    for iface_name, iface_addrs in addrs.items():
        iface_info = {
            'name': iface_name,
            'status': 'UP' if stats.get(iface_name) and stats[iface_name].isup else 'DOWN',
            'speed': stats[iface_name].speed if stats.get(iface_name) else 0,
            'mtu': stats[iface_name].mtu if stats.get(iface_name) else 0,
            'ipv4_addresses': [],
            'ipv6_addresses': [],
            'mac_address': ''
        }

        # Parse addresses
        for addr in iface_addrs:
            if addr.family == psutil.AF_LINK:  # MAC address
                iface_info['mac_address'] = addr.address
            elif addr.family == 2:  # AF_INET (IPv4)
                ipv4_info = {
                    'address': addr.address,
                    'netmask': addr.netmask or '',
                    'broadcast': addr.broadcast or ''
                }
                iface_info['ipv4_addresses'].append(ipv4_info)
            elif addr.family == 10:  # AF_INET6 (IPv6)
                ipv6_info = {
                    'address': addr.address,
                    'netmask': addr.netmask or ''
                }
                iface_info['ipv6_addresses'].append(ipv6_info)

        result['interfaces'].append(iface_info)

    # Get I/O statistics
    io_counters = psutil.net_io_counters()
    result['io_stats'] = {
        'bytes_sent': io_counters.bytes_sent,
        'bytes_recv': io_counters.bytes_recv,
        'packets_sent': io_counters.packets_sent,
        'packets_recv': io_counters.packets_recv,
        'errors_in': io_counters.errin,
        'errors_out': io_counters.errout,
        'drops_in': io_counters.dropin,
        'drops_out': io_counters.dropout
    }

    return result


def get_listening_ports() -> Dict[str, Any]:
    """
    Get ports that are listening on the system.

    Returns:
        dict: Listening ports information with keys:
            - listening_ports (list[dict]): List of listening ports, each containing:
                - proto (str): Protocol (TCP/UDP)
                - local_address (str): Local address and port
                - pid (int, optional): Process ID
                - program (str, optional): Program name
            - total_count (int): Total number of listening ports
    """
    result = {'listening_ports': []}

    try:
        # Get all listening connections
        connections = psutil.net_connections(kind='inet')

        for conn in connections:
            # Only include LISTEN status for TCP, or all UDP (UDP is connectionless)
            if conn.status == 'LISTEN' or (conn.type == 2 and conn.laddr):  # type 2 is UDP
                proto = 'TCP' if conn.type == 1 else 'UDP'

                port_info = {
                    'proto': proto,
                    'local_address': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else 'unknown',
                    'pid': conn.pid if conn.pid else None,
                    'program': None
                }

                # Try to get program name from PID
                if conn.pid:
                    try:
                        proc = psutil.Process(conn.pid)
                        port_info['program'] = proc.name()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass

                result['listening_ports'].append(port_info)

    except psutil.AccessDenied:
        # Fallback: try using ss command
        try:
            ss_output = subprocess.run(
                ['ss', '-tulnp'],
                capture_output=True,
                text=True,
                check=True
            )

            # Parse ss output (simplified - just return raw output)
            for line in ss_output.stdout.split('\n')[1:]:  # Skip header
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 5:
                        result['listening_ports'].append({
                            'proto': parts[0].upper(),
                            'local_address': parts[4],
                            'pid': None,
                            'program': None
                        })

        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

    result['total_count'] = len(result['listening_ports'])

    return result
