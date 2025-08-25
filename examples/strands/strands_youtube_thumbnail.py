"""
Example using Strands agents to generate YouTube thumbnails with the GPT Thumbnail MCP server.
This demonstrates how to use AI agents to automatically create compelling thumbnails for YouTube videos.
"""
import os
import base64
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

# Video information
video_topic = "Python Machine Learning Tutorial"
video_description = "Learn how to build your first machine learning model in Python using scikit-learn. Perfect for beginners!"

prompt = f"""
I need to create a compelling YouTube thumbnail for my video: "{video_topic}"

Description: {video_description}

Please:
1. Generate a high-quality thumbnail image optimized for YouTube engagement
2. Use a professional yet exciting style that appeals to programming enthusiasts
3. Include text overlay with "Python ML Tutorial"
4. Make it eye-catching with good contrast and readable text
5. Save the generated image to a file called "youtube_thumbnail.png"

The thumbnail should follow YouTube best practices like the 0.3-second rule (instantly understandable), 
high contrast for visibility, and emotional appeal to encourage clicks.
"""

# Initialize OpenAI model
model = OpenAIModel(
    client_args={
        "api_key": OPENAI_API_KEY,
    },
    model_id="gpt-4o"
)

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
    
    print(f"✅ Found {len(tools)} tools available")
    
    # Create an agent with MCP tools and file writing capability
    agent = Agent(
        tools=[tools, file_write],
        model=model,
        system_prompt="""You are an expert YouTube thumbnail creator. You understand what makes thumbnails 
        click-worthy and engaging. Use the available image generation tools to create 
        compelling thumbnails that follow YouTube best practices.
        
        When generating images:
        1. Always use content_type="youtube_thumbnail" for optimal sizing
        2. Choose appropriate styles and emotional tones
        3. Include compelling text overlays when requested
        4. Save the generated images to files for the user"""
    )
    
    print("🤖 Starting thumbnail generation...")
    result = agent(prompt)
    print("\n✨ Thumbnail generation completed!")
    print(f"Agent response: {result}")