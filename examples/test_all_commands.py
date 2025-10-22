#!/usr/bin/env python3
"""
Comprehensive test of all linux-utcp commands
"""
import subprocess
import json


def run_command(cmd: list[str], description: str) -> dict:
    """Run a command and return parsed JSON result"""
    print(f"\n{'='*70}")
    print(f"Testing: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*70)

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)

    # For service list, just check if we got output
    if 'service list' in ' '.join(cmd):
        data = json.loads(result.stdout)
        print(f"Services output length: {len(data.get('services', ''))}")
        print(f"Running count: {data.get('running_count', 0)}")
        return data

    data = json.loads(result.stdout)

    # Pretty print the result (truncated for long output)
    output_str = json.dumps(data, indent=2)
    if len(output_str) > 500:
        print(output_str[:500] + "\n... (truncated)")
    else:
        print(output_str)

    return data


def main():
    """Test all implemented commands"""
    # Count total tools
    total_tools = 11

    print(f"\n🚀 LINUX-UTCP COMPREHENSIVE TEST SUITE")
    print(f"Testing all {total_tools} implemented commands")
    print("="*70 + "\n")

    commands = [
        # System commands (4)
        {
            'cmd': ['linux-utcp', 'system', 'info', '--format', 'json'],
            'desc': '1. System Info - Basic system information',
            'validate': lambda d: all(k in d for k in ['hostname', 'os', 'kernel'])
        },
        {
            'cmd': ['linux-utcp', 'system', 'cpu', '--format', 'json'],
            'desc': '2. CPU Info - CPU details and load averages',
            'validate': lambda d: all(k in d for k in ['cpu_model', 'physical_cores', 'load_average_1m'])
        },
        {
            'cmd': ['linux-utcp', 'system', 'memory', '--format', 'json'],
            'desc': '3. Memory Info - RAM and swap usage',
            'validate': lambda d: all(k in d for k in ['ram_total', 'ram_used_percent', 'swap_total'])
        },
        {
            'cmd': ['linux-utcp', 'system', 'disk', '--format', 'json'],
            'desc': '4. Disk Usage - Filesystem information',
            'validate': lambda d: 'filesystems' in d and len(d['filesystems']) > 0
        },
        # Service commands (3)
        {
            'cmd': ['linux-utcp', 'service', 'list', '--format', 'json'],
            'desc': '5. Service List - All systemd services',
            'validate': lambda d: 'services' in d and 'running_count' in d
        },
        {
            'cmd': ['linux-utcp', 'service', 'status', 'sshd', '--format', 'json'],
            'desc': '6. Service Status - Get service status',
            'validate': lambda d: 'status' in d
        },
        {
            'cmd': ['linux-utcp', 'service', 'logs', 'sshd', '--lines', '10', '--format', 'json'],
            'desc': '7. Service Logs - Get service logs',
            'validate': lambda d: 'logs' in d
        },
        # Process commands (2)
        {
            'cmd': ['linux-utcp', 'process', 'list', '--format', 'json'],
            'desc': '8. Process List - Running processes',
            'validate': lambda d: 'processes' in d and 'total_count' in d and len(d['processes']) > 0
        },
        {
            'cmd': ['linux-utcp', 'process', 'info', '1', '--format', 'json'],
            'desc': '9. Process Info - Detailed process info (PID 1)',
            'validate': lambda d: all(k in d for k in ['pid', 'name', 'cpu_percent', 'memory_percent'])
        },
        # Network commands (2)
        {
            'cmd': ['linux-utcp', 'network', 'interfaces', '--format', 'json'],
            'desc': '10. Network Interfaces - Interface information',
            'validate': lambda d: 'interfaces' in d and 'io_stats' in d and len(d['interfaces']) > 0
        },
        {
            'cmd': ['linux-utcp', 'network', 'ports', '--format', 'json'],
            'desc': '11. Network Ports - Listening ports',
            'validate': lambda d: 'listening_ports' in d and 'total_count' in d
        },
    ]

    results = []
    for test in commands:
        try:
            data = run_command(test['cmd'], test['desc'])

            # Validate result structure
            if test['validate'](data):
                print("\n✓ Validation PASSED")
                results.append(('PASS', test['desc']))
            else:
                print("\n✗ Validation FAILED - Missing expected fields")
                results.append(('FAIL', test['desc']))

        except Exception as e:
            print(f"\n✗ ERROR: {e}")
            results.append(('ERROR', test['desc']))

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    for status, desc in results:
        icon = "✓" if status == "PASS" else "✗"
        print(f"{icon} [{status:5}] {desc}")

    passed = sum(1 for s, _ in results if s == "PASS")
    total = len(results)

    print(f"\n{passed}/{total} tests passed")
    print(f"Implementation Progress: {total_tools}/20 tools ({int(total_tools/20*100)}%)")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! 🎉\n")
        return 0
    else:
        print("\n⚠️  Some tests failed\n")
        return 1


if __name__ == "__main__":
    exit(main())
