# linux-utcp Tutorial: Getting Started

This tutorial will guide you through installing, running, and using linux-utcp to perform system diagnostics.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Basic Usage](#basic-usage)
4. [Output Formats](#output-formats)
5. [Available Commands](#available-commands)
6. [AI Agent Integration (NEW!)](#ai-agent-integration-new)
7. [Next Steps](#next-steps)

---

## Prerequisites

Before you begin, ensure you have:

- **Python 3.10 or higher** installed
- **systemd** (required for service and journal tools)
- **uv** package manager (recommended) or pip
- **Linux system** (tested on Fedora, should work on Ubuntu/Debian)

### Installing uv (if needed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or use your package manager:

```bash
# Fedora
sudo dnf install uv

# Ubuntu/Debian
# Follow instructions at https://github.com/astral-sh/uv
```

---

## Installation

### 1. Clone the Repository

```bash
git clone <repo-url>
cd utcp-experiment
```

### 2. Install Dependencies

Using uv (recommended):

```bash
uv sync
```

Using pip:

```bash
pip install -e .
```

### 3. Verify Installation

```bash
uv run linux-utcp --version
# or if installed globally
linux-utcp --version
```

You should see:

```
linux-utcp, version 0.1.0
```

---

## Basic Usage

### Your First Command: System Info

The simplest way to start is with the `system info` command:

```bash
uv run linux-utcp system info
```

This will output JSON by default:

```json
{
  "hostname": "your-hostname",
  "os": "Fedora Linux",
  "os_version": "42 (Workstation Edition)",
  "kernel": "6.16.12-200.fc42.x86_64",
  "architecture": "x86_64",
  "uptime": "up 1 hour, 15 minutes",
  "boot_time": "2025-10-21 21:07:26"
}
```

---

## Output Formats

linux-utcp supports two output formats: **JSON** (machine-readable) and **text** (human-readable).

### JSON Format (Default)

Perfect for parsing with scripts or AI agents:

```bash
linux-utcp system info --format json
```

**Use cases:**
- AI agent integration
- Scripting and automation
- Piping to `jq` for processing

**Example with jq:**

```bash
linux-utcp system info --format json | jq '.hostname'
# Output: "your-hostname"
```

### Text Format

Beautiful terminal tables for humans:

```bash
linux-utcp system info --format text
```

**Output:**

```
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Field        ┃ Value                    ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Hostname     │ your-hostname            │
│ Os           │ Fedora Linux             │
│ Os Version   │ 42 (Workstation Edition) │
│ Kernel       │ 6.16.12-200.fc42.x86_64  │
│ Architecture │ x86_64                   │
│ Uptime       │ up 1 hour, 15 minutes    │
│ Boot Time    │ 2025-10-21 21:07:26      │
└──────────────┴──────────────────────────┘
```

**Use cases:**
- Manual inspection
- Terminal dashboards
- Quick diagnostics

---

## Available Commands

linux-utcp organizes commands into logical groups. Currently implemented:

### System Commands

Get comprehensive system information:

```bash
# Basic system info (OS, kernel, hostname, uptime)
linux-utcp system info

# CPU information (coming soon)
linux-utcp system cpu

# Memory information (coming soon)
linux-utcp system memory

# Disk usage (coming soon)
linux-utcp system disk

# Hardware info (coming soon)
linux-utcp system hardware
```

### Service Commands (Coming Soon)

Manage and inspect systemd services:

```bash
# List all services
linux-utcp service list

# Get service status
linux-utcp service status nginx

# Get service logs
linux-utcp service logs nginx --lines 50
```

### Process Commands

Monitor running processes:

```bash
# List all processes (top 100 by CPU)
linux-utcp process list

# Get detailed process info
linux-utcp process info 1234
```

### Network Commands

Network diagnostics:

```bash
# Show network interfaces
linux-utcp network interfaces

# Show listening ports
linux-utcp network ports
```

### Log Commands (Coming Soon)

Access system logs:

```bash
# Query systemd journal
linux-utcp logs journal --unit nginx --lines 100

# Read audit logs
linux-utcp logs audit

# Read specific log file
linux-utcp logs read /var/log/syslog --lines 50
```

### Storage Commands (Coming Soon)

Analyze storage and directories:

```bash
# List block devices
linux-utcp storage devices

# List directories by size
linux-utcp storage list-dir /var/log --sort size --top 10

# List directories by name
linux-utcp storage list-dir /home --sort name

# List directories by modification date
linux-utcp storage list-dir /tmp --sort modified --oldest-first
```

---

## AI Agent Integration (NEW!)

**🎉 NEW: AI-Powered Diagnostic Assistant!**

linux-utcp now includes an AI agent that can autonomously use diagnostic tools based on natural language queries!

### What is This?

Instead of manually running commands, you can ask questions in plain English and the AI agent will:
1. Figure out which tools to use
2. Execute them automatically
3. Synthesize the results into a clear answer

### Prerequisites

You'll need a **Google Gemini API key**:

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create an API key
3. Set it in your environment:

```bash
export GEMINI_API_KEY="your-key-here"
```

### Quick Start

Run the AI agent test to see it in action:

```bash
uv run python agent/test_langchain_agent.py
```

**What you'll see:**

The agent will run 5 tests, answering questions like:
- "What is the hostname and operating system?"
- "How many CPU cores and what's the load?"
- "What percentage of RAM is being used?"
- "Give me a complete system health check"
- "Is the sshd service running?"

**Example output:**

```
======================================================================
TEST 1: Simple System Information Query
======================================================================
Query: 'What is the hostname and operating system of this machine?'

✅ Agent Response:
----------------------------------------------------------------------
The hostname is riomhaire and the operating system is Fedora Linux 42
(Workstation Edition).
----------------------------------------------------------------------
✅ TEST 1 PASSED
```

### Using the Agent Programmatically

You can use the AI agent in your own Python code:

```python
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os

# Import the diagnostic tools
import sys
sys.path.append('agent')
from langchain_tools import ALL_TOOLS

# Set up Gemini
os.environ['GOOGLE_API_KEY'] = os.getenv('GEMINI_API_KEY')
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0)

# Create the agent
agent = create_agent(
    llm,
    ALL_TOOLS,
    system_prompt="You are a helpful Linux system administrator assistant."
)

# Ask a question!
response = agent.invoke({
    "messages": [HumanMessage(content="What's using all my disk space?")]
})

# Get the answer
print(response['messages'][-1].content)
```

### What the Agent Can Do

The AI agent has access to all 11 diagnostic tools:

**System Information:**
- Get hostname, OS, kernel version, uptime
- Get CPU model, cores, frequency, load
- Get RAM and swap usage
- Get disk usage and mount points

**Service Management:**
- List all systemd services
- Get service status
- Get service logs

**Process Management:**
- List running processes
- Get detailed process information

**Network Diagnostics:**
- List network interfaces with IPs
- Show listening ports

### Example Queries

Try asking the agent natural language questions:

```python
# System health
"Give me a complete system health check"

# Troubleshooting
"Why is my system slow?"
"What processes are using the most CPU?"
"Is nginx running?"

# Capacity planning
"How much disk space is available?"
"What's the memory usage?"

# Network debugging
"What ports are listening?"
"Show me the network configuration"
```

### How It Works

1. **You ask a question** in natural language
2. **The AI decides** which tools to use (e.g., `get_cpu_info`, `get_memory_info`)
3. **Tools execute** the actual CLI commands (`linux-utcp system cpu --format json`)
4. **AI synthesizes** the results into a clear answer

**The AI can combine multiple tools** to answer complex questions!

### Advanced: Multi-Tool Queries

The agent intelligently combines tools for complex diagnostics:

**Query:** "Give me a system health check with hostname, CPU, memory, and disk"

**What happens:**
1. Calls `get_system_info()` → Gets hostname and OS
2. Calls `get_cpu_info()` → Gets CPU details and load
3. Calls `get_memory_info()` → Gets RAM usage
4. Calls `get_disk_usage()` → Gets filesystem info
5. Synthesizes everything into a formatted report!

**Agent Response:**
```
Here is the system health check report:

* Hostname: riomhaire
* OS Version: Fedora Linux 42 (Workstation Edition)
* CPU:
  * Model: AMD Ryzen AI 7 PRO 360 w/ Radeon 880M
  * Physical Cores: 8
  * Logical Cores: 16
  * Overall CPU Usage: 5.4%
  * Load Average (1m, 5m, 15m): 0.19, 0.5, 0.68
* Memory:
  * RAM Used: 66.9%
* Disk Space (Root Filesystem):
  * Size: 952.3G
  * Used: 505.3G
  * Available: 443.3G
  * Use Percentage: 53.3%
```

### Files

- **`agent/langchain_tools.py`** - Tool wrappers for the 11 CLI commands
- **`agent/test_langchain_agent.py`** - Test script (run this to try it!)
- **`docs/LANGCHAIN_SUCCESS.md`** - Detailed documentation

### Troubleshooting

**Error: "GEMINI_API_KEY not set"**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

**Error: "Module not found"**
```bash
# Make sure dependencies are installed
uv sync
```

**Agent not finding tools?**
- Make sure you're in the project root directory
- Verify CLI commands work: `uv run linux-utcp system info`

---

## Testing All Commands

Run the comprehensive test suite to verify all 11 CLI commands:

```bash
uv run python examples/test_all_commands.py
```

**Expected output:**

```
🚀 LINUX-UTCP COMPREHENSIVE TEST SUITE
Testing all 11 implemented commands
======================================================================

[Tests run for all 11 commands...]

TEST SUMMARY
======================================================================
✓ [PASS ] 1. System Info - Basic system information
✓ [PASS ] 2. CPU Info - CPU details and load averages
✓ [PASS ] 3. Memory Info - RAM and swap usage
✓ [PASS ] 4. Disk Usage - Filesystem information
✓ [PASS ] 5. Service List - All systemd services
✓ [PASS ] 6. Service Status - Get service status
✓ [PASS ] 7. Service Logs - Get service logs
✓ [PASS ] 8. Process List - Running processes
✓ [PASS ] 9. Process Info - Detailed process info (PID 1)
✓ [PASS ] 10. Network Interfaces - Interface information
✓ [PASS ] 11. Network Ports - Listening ports

11/11 tests passed
Implementation Progress: 11/20 tools (55%)

🎉 ALL TESTS PASSED! 🎉
```

---

## Practical Examples

### Example 1: Quick System Check

Get a quick overview of your system:

```bash
linux-utcp system info --format text
```

### Example 2: JSON for Scripting

Extract just the kernel version:

```bash
linux-utcp system info --format json | jq -r '.kernel'
# Output: 6.16.12-200.fc42.x86_64
```

### Example 3: Check if System Needs Reboot

Compare kernel versions to see if reboot is needed:

```bash
RUNNING_KERNEL=$(linux-utcp system info --format json | jq -r '.kernel')
INSTALLED_KERNEL=$(uname -r)

if [ "$RUNNING_KERNEL" != "$INSTALLED_KERNEL" ]; then
    echo "System may need a reboot"
fi
```

### Example 4: Export System Info to File

Save system information for documentation:

```bash
linux-utcp system info --format json > system-info-$(date +%Y%m%d).json
```

### Example 5: Monitor Uptime

Track system uptime over time:

```bash
while true; do
    UPTIME=$(linux-utcp system info --format json | jq -r '.uptime')
    echo "$(date): $UPTIME"
    sleep 3600  # Check every hour
done
```

---

## Troubleshooting

### Command Not Found

If you see `command not found: linux-utcp`:

**Using uv:**
```bash
# Always prefix with uv run
uv run linux-utcp system info
```

**Or install globally:**
```bash
uv pip install -e .
linux-utcp system info
```

### Permission Errors

Some commands may require elevated privileges:

```bash
# If needed for certain operations
sudo uv run linux-utcp system info
```

### Missing Dependencies

If you see import errors:

```bash
# Reinstall dependencies
uv sync --reinstall
```

---

## Next Steps

### For Users

1. **Explore more commands** as they become available (CPU, memory, disk, etc.)
2. **Integrate with scripts** using JSON output and `jq`
3. **Try UTCP Agent integration** once available
4. **Provide feedback** via GitHub issues

### For Developers

1. **Add more commands** - See `docs/brief.md` for the full roadmap of 20 tools
2. **Improve error handling** - Add validation and better error messages
3. **Write tests** - Add unit and integration tests
4. **Contribute** - PRs welcome!

---

## Getting Help

### Command Help

Every command has built-in help:

```bash
# General help
linux-utcp --help

# Group help
linux-utcp system --help

# Command help
linux-utcp system info --help
```

### Documentation

- **Project Brief**: `docs/brief.md` - Complete project overview and architecture
- **README**: `README.md` - Quick start and installation
- **This Tutorial**: `docs/TUTORIAL.md` - Comprehensive usage guide

### Support

- **GitHub Issues**: Report bugs or request features
- **Discussions**: Ask questions and share ideas

---

## What You Learned

✓ How to install linux-utcp
✓ How to run your first diagnostic command
✓ The difference between JSON and text output formats
✓ How to use linux-utcp in scripts
✓ How UTCP integration works
✓ Practical examples for real-world use cases

**Ready to explore?** Try running `linux-utcp system info --format text` and see your system information! 🚀

---

## Quick Reference Card

```bash
# Installation
uv sync

# Basic usage
uv run linux-utcp system info

# JSON output (default)
linux-utcp system info --format json

# Text output
linux-utcp system info --format text

# Use with jq
linux-utcp system info --format json | jq '.hostname'

# Generate UTCP manual
uv run python scripts/generate_manual.py

# Run integration tests
uv run python examples/test_utcp_client.py

# Get help
linux-utcp --help
```

---

**Happy diagnosing!** 🔧
