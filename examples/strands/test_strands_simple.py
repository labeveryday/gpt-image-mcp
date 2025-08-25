"""
Simple test of Strands agents with GPT Thumbnail MCP server.
This is a minimal example to verify the integration works.
"""
import os
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient
from strands_tools import file_write
from strands.models.openai import OpenAIModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("❌ Please set OPENAI_API_KEY environment variable")
    exit(1)

print("🧪 Testing Strands + GPT Thumbnail MCP Integration")
print("=" * 60)

# Simple prompt for testing
prompt = """
Please use the available image generation tools to create a simple test image. 
Generate an image with the prompt "A simple red circle on a white background" 
and tell me about the available tools you can use.
"""

# Initialize OpenAI model
model = OpenAIModel(
    client_args={
        "api_key": OPENAI_API_KEY,
    },
    model_id="gpt-4o-mini"  # Using mini for faster testing
)

try:
    # Connect to our GPT Thumbnail MCP server
    print("🔌 Connecting to GPT Thumbnail MCP Server...")
    stdio_mcp_client = MCPClient(lambda: stdio_client(
        StdioServerParameters(
            command="uv", 
            args=["run", "gpt-thumbnail-mcp"],
            cwd="."
        )
    ))

    # Create and run the agent
    with stdio_mcp_client:
        print("🛠️  Getting tools from MCP server...")
        tools = stdio_mcp_client.list_tools_sync()
        
        print(f"✅ Found {len(tools)} tools:")
        for i, tool in enumerate(tools):
            print(f"   - Tool {i+1}: {getattr(tool, 'name', 'Unknown')} - {getattr(tool, 'description', 'No description')}")
        
        # Create a simple test agent
        agent = Agent(
            tools=[tools],
            model=model,
            name="Test Agent"
        )
        
        print("\n🤖 Running test agent...")
        result = agent(prompt)
        print(f"\n✨ Test completed!")
        print(f"Agent response: {result}")

except Exception as e:
    print(f"❌ Error: {str(e)}")
    print("Make sure the MCP server is working and you have proper credentials.")

print("\n" + "=" * 60)
print("🎉 Strands integration test complete!")