#!/usr/bin/env python3
"""
Test the UTCP CLI integration with linux-utcp
Simplified test that just calls the CLI directly through subprocess
"""
import asyncio
import subprocess
import json
from pathlib import Path


async def main():
    """Test CLI command execution"""
    print("Testing linux-utcp CLI command...\n")

    # Call the CLI directly
    result = subprocess.run(
        ['linux-utcp', 'system', 'info', '--format', 'json'],
        capture_output=True,
        text=True,
        check=True
    )

    print("✓ CLI execution completed!")
    print(f"\nJSON Output:\n{result.stdout}")

    # Parse and validate JSON
    data = json.loads(result.stdout)
    print(f"\n✓ JSON parsing successful!")
    print(f"  Hostname: {data.get('hostname')}")
    print(f"  OS: {data.get('os')}")
    print(f"  Kernel: {data.get('kernel')}")

    # Now test with text format
    print("\n" + "="*60)
    print("Testing text format...\n")

    result = subprocess.run(
        ['linux-utcp', 'system', 'info', '--format', 'text'],
        capture_output=True,
        text=True,
        check=True
    )

    print("✓ Text format execution completed!")
    print(f"\n{result.stdout}")


if __name__ == "__main__":
    asyncio.run(main())
