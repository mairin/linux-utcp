"""
CLI entry point for linux-utcp
"""
import click
import json
from typing import Optional

from linux_utcp.commands.system import (
    get_system_info,
    get_cpu_info,
    get_memory_info,
    get_disk_usage,
)
from linux_utcp.commands.service import (
    list_services,
    get_service_status,
    get_service_logs,
)
from linux_utcp.commands.process import (
    list_processes,
    get_process_info,
)
from linux_utcp.commands.network import (
    get_network_interfaces,
    get_listening_ports,
)
from linux_utcp.utils.formatting import format_output, format_error


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Linux system diagnostics toolkit using UTCP"""
    pass


@main.group()
def system():
    """System information commands"""
    pass


@main.group()
def service():
    """Service management commands"""
    pass


@main.group()
def process():
    """Process management commands"""
    pass


@main.group()
def logs():
    """Log and audit commands"""
    pass


@main.group()
def network():
    """Network diagnostics commands"""
    pass


@main.group()
def storage():
    """Storage and disk analysis commands"""
    pass


# Format option for all commands
format_option = click.option(
    '--format',
    type=click.Choice(['json', 'text']),
    default='json',
    help='Output format'
)


# Placeholder commands - we'll implement these next
@system.command('info')
@format_option
def system_info_cmd(format: str):
    """Get system information"""
    try:
        data = get_system_info()
        output = format_output(data, format)
        click.echo(output)
    except Exception as e:
        error_output = format_error(str(e), format)
        click.echo(error_output, err=True)
        raise click.Abort()


@system.command('cpu')
@format_option
def system_cpu(format: str):
    """Get CPU information and load averages"""
    try:
        data = get_cpu_info()
        output = format_output(data, format)
        click.echo(output)
    except Exception as e:
        error_output = format_error(str(e), format)
        click.echo(error_output, err=True)
        raise click.Abort()


@system.command('memory')
@format_option
def system_memory(format: str):
    """Get memory usage including RAM and swap"""
    try:
        data = get_memory_info()
        output = format_output(data, format)
        click.echo(output)
    except Exception as e:
        error_output = format_error(str(e), format)
        click.echo(error_output, err=True)
        raise click.Abort()


@system.command('disk')
@format_option
def system_disk(format: str):
    """Get filesystem usage and mount points"""
    try:
        data = get_disk_usage()
        output = format_output(data, format)
        click.echo(output)
    except Exception as e:
        error_output = format_error(str(e), format)
        click.echo(error_output, err=True)
        raise click.Abort()


# Service commands
@service.command('list')
@format_option
def service_list(format: str):
    """List all systemd services"""
    try:
        data = list_services()
        output = format_output(data, format)
        click.echo(output)
    except Exception as e:
        error_output = format_error(str(e), format)
        click.echo(error_output, err=True)
        raise click.Abort()


@service.command('status')
@click.argument('service_name')
@format_option
def service_status(service_name: str, format: str):
    """Get status of a specific service"""
    try:
        data = get_service_status(service_name)
        output = format_output(data, format)
        click.echo(output)
    except Exception as e:
        error_output = format_error(str(e), format)
        click.echo(error_output, err=True)
        raise click.Abort()


@service.command('logs')
@click.argument('service_name')
@click.option('--lines', default=50, type=int, help='Number of log lines to retrieve')
@format_option
def service_logs(service_name: str, lines: int, format: str):
    """Get logs for a specific service"""
    try:
        data = get_service_logs(service_name, lines)
        output = format_output(data, format)
        click.echo(output)
    except Exception as e:
        error_output = format_error(str(e), format)
        click.echo(error_output, err=True)
        raise click.Abort()


# Process commands
@process.command('list')
@format_option
def process_list(format: str):
    """List running processes (top 100 by CPU)"""
    try:
        data = list_processes()
        output = format_output(data, format)
        click.echo(output)
    except Exception as e:
        error_output = format_error(str(e), format)
        click.echo(error_output, err=True)
        raise click.Abort()


@process.command('info')
@click.argument('pid', type=int)
@format_option
def process_info(pid: int, format: str):
    """Get detailed info about a specific process"""
    try:
        data = get_process_info(pid)
        output = format_output(data, format)
        click.echo(output)
    except Exception as e:
        error_output = format_error(str(e), format)
        click.echo(error_output, err=True)
        raise click.Abort()


# Network commands
@network.command('interfaces')
@format_option
def network_interfaces(format: str):
    """Get network interface information"""
    try:
        data = get_network_interfaces()
        output = format_output(data, format)
        click.echo(output)
    except Exception as e:
        error_output = format_error(str(e), format)
        click.echo(error_output, err=True)
        raise click.Abort()


@network.command('ports')
@format_option
def network_ports(format: str):
    """Get listening ports"""
    try:
        data = get_listening_ports()
        output = format_output(data, format)
        click.echo(output)
    except Exception as e:
        error_output = format_error(str(e), format)
        click.echo(error_output, err=True)
        raise click.Abort()


if __name__ == '__main__':
    main()
