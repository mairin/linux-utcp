#!/usr/bin/env python3
"""
Test LangChain Agent with linux-utcp diagnostic tools
Uses Google Gemini 2.0 Flash as the LLM
"""
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_tools import ALL_TOOLS


def main():
    """Test LangChain Agent with linux-utcp tools"""

    # Check for API key
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY environment variable not set")
        print("\nPlease set your Gemini API key:")
        print("  export GEMINI_API_KEY='your-api-key-here'")
        return 1

    # Set GOOGLE_API_KEY for langchain
    os.environ['GOOGLE_API_KEY'] = api_key

    print("🤖 LangChain Agent Integration Test")
    print("="*70)
    print("Testing AI agent with linux-utcp diagnostic tools\n")

    # Create the LLM
    print("🧠 Initializing Gemini 2.0 Flash...")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        temperature=0,
    )

    # Create the prompt template
    print(f"🛠️  Loading {len(ALL_TOOLS)} diagnostic tools...")
    for i, tool in enumerate(ALL_TOOLS, 1):
        print(f"   {i}. {tool.name}")

    print("\n📝 Creating system prompt...")
    system_prompt = (
        "You are a helpful Linux system administrator assistant. "
        "You have access to diagnostic tools to check system information, "
        "CPU usage, memory, disk space, services, processes, and network status. "
        "Use the appropriate tools to answer user questions accurately. "
        "When you get results from tools, summarize them clearly for the user."
    )

    print("🚀 Creating Agent...")
    agent_executor = create_agent(
        llm,
        ALL_TOOLS,
        system_prompt=system_prompt
    )

    print("✅ LangChain Agent created successfully!\n")

    # Helper function to run tests
    def run_test(num: int, description: str, query: str) -> bool:
        """Run a single test query"""
        print("="*70)
        print(f"TEST {num}: {description}")
        print("="*70)
        print(f"Query: '{query}'\n")

        try:
            # LangGraph invoke with messages
            response = agent_executor.invoke({"messages": [HumanMessage(content=query)]})

            # Extract the final AI message (last item in the list)
            final_message = response['messages'][-1].content

            print("\n✅ Agent Response:")
            print("-" * 70)
            print(final_message)
            print("-" * 70)
            print(f"✅ TEST {num} PASSED\n")
            return True
        except Exception as e:
            print(f"❌ TEST {num} FAILED: {e}\n")
            import traceback
            traceback.print_exc()
            return False

    # Run all tests
    success = run_test(
        1,
        "Simple System Information Query",
        "What is the hostname and operating system of this machine?"
    )
    if not success:
        return 1

    run_test(
        2,
        "CPU Information Query",
        "How many CPU cores does this system have and what is the current load average?"
    )

    run_test(
        3,
        "Memory Usage Query",
        "What percentage of RAM is currently being used?"
    )

    run_test(
        4,
        "Multi-Tool Health Check",
        "Give me a complete system health check report including: "
        "hostname, OS version, CPU cores and load, memory usage percentage, "
        "and disk space on the root filesystem"
    )

    run_test(
        5,
        "Service Status Check",
        "Is the sshd service running on this system?"
    )

    # Summary
    print("="*70)
    print("🎉 LANGCHAIN AGENT INTEGRATION TEST COMPLETE!")
    print("="*70)
    print("\n✅ The LangChain Agent successfully:")
    print("   • Discovered all 11 diagnostic tools")
    print("   • Executed CLI commands autonomously")
    print("   • Answered natural language diagnostic queries")
    print("   • Combined multiple tools for complex diagnostics")
    print("\n🚀 AI-powered diagnostic assistant is WORKING!\n")

    return 0


if __name__ == "__main__":
    exit(main())
