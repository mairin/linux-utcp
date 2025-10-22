# linux-utcp

Linux system diagnostics toolkit using UTCP (Universal Tool Calling Protocol) for AI agent integration.

## Overview

`linux-utcp` provides 20 read-only diagnostic tools for Linux system administration and troubleshooting, accessible to AI agents via UTCP without requiring server infrastructure.

## Features

- **20 Diagnostic Tools** across 6 categories:
  - System Information (5 tools)
  - Service Management (3 tools)
  - Process Management (2 tools)
  - Logs & Audit (3 tools)
  - Network Diagnostics (3 tools)
  - Storage & Disk Analysis (4 tools)

- **UTCP Native**: AI agents can discover and use tools via UTCP manuals
- **Standalone Agent**: Powered by Google Gemini 2.5 Pro
- **Read-Only**: All operations are strictly read-only for safety
- **JSON & Text Output**: Structured data for agents, human-readable for developers

## Installation

### Prerequisites

- Python 3.10 or higher
- systemd (for service and journal tools)
- Google API key for Gemini

### Install with uv

```bash
# Clone repository
git clone <repo-url>
cd utcp-experiment

# Install dependencies
uv sync

# Set up environment
export GOOGLE_API_KEY="your-google-api-key"
```

## Quick Start

### CLI Usage

```bash
# System information
linux-utcp system info --format json

# Service status
linux-utcp service status nginx

# Process list
linux-utcp process list

# Network interfaces
linux-utcp network interfaces

# Disk usage
linux-utcp system disk
```

### UTCP Agent Usage

```python
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from utcp_agent import UtcpAgent

async def main():
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0)

    agent = await UtcpAgent.create(
        llm=llm,
        utcp_config={
            "manual_call_templates": [{
                "manual_url": "file:///path/to/manuals/linux-utcp.json"
            }]
        }
    )

    result = await agent.chat("What's my disk usage?")
    print(result)

asyncio.run(main())
```

## Project Structure

```
utcp-experiment/
├── src/linux_utcp/       # Main package
│   ├── commands/         # Command implementations
│   │   ├── system.py     # System info commands
│   │   ├── service.py    # Service management
│   │   ├── process.py    # Process management
│   │   ├── logs.py       # Log commands
│   │   ├── network.py    # Network diagnostics
│   │   └── storage.py    # Storage analysis
│   ├── utils/            # Utilities
│   ├── cli.py            # CLI entry point
│   └── __init__.py
├── manuals/              # UTCP manual specifications
├── agent/                # UTCP agent examples
├── tests/                # Test suite
├── examples/             # Usage examples
├── scripts/              # Helper scripts
└── docs/                 # Documentation
```

## Development

```bash
# Install dev dependencies
uv sync --all-extras

# Run tests
pytest

# Format code
black src/ tests/

# Lint
ruff check src/ tests/
```

## Documentation

See [docs/brief.md](docs/brief.md) for the complete project brief and architecture.

## License

MIT
