"""
Example using Strands agents to create a complete blog post with optimized header images.
This demonstrates how to use AI agents for comprehensive content creation workflows.
"""
import os
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient
from strands_tools import file_write, file_read
from strands.models.openai import OpenAIModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("❌ Please set OPENAI_API_KEY environment variable")
    exit(1)

# Blog post requirements
blog_topic = "The Future of Remote Work: 10 Trends Shaping 2024"
target_audience = "business professionals and remote workers"

prompt = f"""
I'm writing a comprehensive blog post about: "{blog_topic}"
Target audience: {target_audience}

Please help me create a complete blog post package:

1. First, generate a professional blog header image that:
   - Represents the concept of remote work and future trends
   - Uses a modern, professional style
   - Is optimized for web display
   - Has good visual appeal for business professionals

2. Create the blog post content with:
   - Engaging introduction
   - 10 detailed trends with explanations
   - Professional tone suitable for business audience
   - Proper formatting with headers and bullet points

3. Save the header image as "blog_header.png"
4. Save the blog content as "blog_post.md"

Make sure the image complements the written content and both maintain a professional, forward-thinking tone.
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
    
    # Create an agent with MCP tools and file operations
    agent = Agent(
        tools=[tools, file_write, file_read],
        model=model,
        system_prompt="""You are an expert content creator specializing in business and professional blogs. 
        You create both compelling written content and supporting visual assets.
        
        For image generation:
        - Use content_type="blog_header" for header images
        - Choose professional, modern styles
        - Ensure images complement the written content
        - Consider the target audience when selecting visual elements
        
        For content creation:
        - Write in a professional but engaging tone
        - Use proper markdown formatting
        - Structure content logically with clear sections
        - Include actionable insights and practical information"""
    )
    
    print("🤖 Starting blog content creation...")
    result = agent(prompt)
    print("\n✨ Blog content creation completed!")
    print(f"Agent response: {result}")