#!/usr/bin/env python3
"""
Test if UTCP manual can be loaded correctly
"""
import asyncio
import json
from pathlib import Path

from utcp.utcp_client import UtcpClient


async def test_manual():
    """Test loading the UTCP manual"""

    # Find the manual
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    manual_path = repo_root / "manuals" / "linux-utcp.json"

    print(f"📄 Manual path: {manual_path}")
    print(f"   Exists: {manual_path.exists()}")

    # Load the manual JSON
    with open(manual_path) as f:
        manual_data = json.load(f)

    print(f"\n📋 Manual contents:")
    print(f"   Name: {manual_data.get('name')}")
    print(f"   Description: {manual_data.get('description')}")
    print(f"   UTCP Version: {manual_data.get('utcp_version')}")
    print(f"   Tools count: {len(manual_data.get('tools', []))}")

    print(f"\n🔧 Tools in manual:")
    for i, tool in enumerate(manual_data.get('tools', []), 1):
        print(f"   {i}. {tool.get('name')} - {tool.get('description', '')[:60]}...")

    # Try to create a UTCP client
    print(f"\n🚀 Creating UTCP Client...")
    try:
        client = await UtcpClient.create(config={
            "manuals": [{
                "manual_url": f"file://{manual_path.absolute()}"
            }]
        })
        print(f"✅ UTCP Client created successfully!")

        # Try to list tools
        print(f"\n🔍 Attempting to discover tools...")
        # The client should have loaded the tools
        print(f"   Client created, manual should be loaded")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_manual())
