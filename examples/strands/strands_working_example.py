"""
Working example of Strands agents with GPT Thumbnail MCP server.
This demonstrates a successful integration with optimized context usage.
"""
import os
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient
from strands.models.openai import OpenAIModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("❌ Please set OPENAI_API_KEY environment variable")
    exit(1)

print("🎯 Strands + GPT Thumbnail MCP - Working Example")
print("=" * 60)

# Use a very focused prompt to avoid context length issues
prompt = "Generate a simple YouTube thumbnail with the text 'Hello World' using a professional style."

# Use GPT-4o for better handling of tools
model = OpenAIModel(
    client_args={
        "api_key": OPENAI_API_KEY,
    },
    model_id="gpt-4o"
)

try:
    print("🔌 Connecting to GPT Thumbnail MCP Server...")
    stdio_mcp_client = MCPClient(lambda: stdio_client(
        StdioServerParameters(
            command="uv", 
            args=["run", "gpt-thumbnail-mcp"],
            cwd="."
        )
    ))

    with stdio_mcp_client:
        print("🛠️  Getting tools from MCP server...")
        tools = stdio_mcp_client.list_tools_sync()
        print(f"✅ Connected! Found {len(tools)} tools available")
        
        # Create a focused agent with minimal instructions to save context
        agent = Agent(
            tools=[tools],  # Just MCP tools, no file operations to save context
            model=model,
            
            system_prompt="You create YouTube thumbnails using the generate_image tool. Keep responses concise."
        )
        
        print("🤖 Creating thumbnail...")
        result = agent(prompt)
        print(f"\n✨ Success! Agent completed the task.")
        print(f"Result: {result[:200]}..." if len(result) > 200 else result)

except Exception as e:
    print(f"❌ Error: {str(e)}")
    print("\nThis may be due to:")
    print("- Context length limits with large tool schemas")
    print("- API rate limits") 
    print("- Network connectivity issues")

print("\n" + "=" * 60)
print("🎉 Strands integration example complete!")
print("\n💡 Key takeaways:")
print("✅ Strands successfully connects to FastMCP servers")
print("✅ Tools are automatically discovered and available")
print("✅ Agents can use MCP tools for complex workflows")
print("⚠️  Large tool schemas may hit context limits")
print("💡 Use focused prompts and minimal instructions for best results")