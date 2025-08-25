"""
Example using Strands agents to create a complete social media campaign with platform-optimized images.
This demonstrates cross-platform content creation and optimization workflows.
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

# Campaign information
campaign = {
    "product": "AI-Powered Code Assistant",
    "message": "Boost your coding productivity with AI",
    "target_audience": "software developers and programmers",
    "brand_colors": ["#2563eb", "#7c3aed", "#059669"]
}

platforms = ["instagram", "twitter", "facebook"]

prompt = f"""
I'm launching a social media campaign for: "{campaign['product']}"
Campaign message: "{campaign['message']}"
Target audience: {campaign['target_audience']}
Brand colors: {campaign['brand_colors']}

Please create a comprehensive social media campaign package:

1. Generate a master image that represents our product and message using our brand colors

2. Create platform-optimized versions for:
   - Instagram (square format, mobile-friendly)
   - Twitter (engaging for tech community)
   - Facebook (professional appearance)

3. Use the optimize_for_platform tool to ensure each image is perfectly sized and styled for its platform

4. For each platform, create variations with different emotional tones:
   - Professional version for LinkedIn-style sharing
   - Casual/friendly version for community engagement
   - Exciting version to generate buzz

5. Generate prompt suggestions for each platform to help with future campaigns

6. Save all images with descriptive filenames like:
   - "campaign_master.png"
   - "instagram_professional.png"
   - "twitter_exciting.png"
   - etc.

7. Create a campaign summary document with:
   - Image descriptions and usage recommendations
   - Platform-specific posting strategies
   - Suggested captions and hashtags

Make sure all images maintain brand consistency while being optimized for their specific platforms.
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
    
    # Create an agent specialized in social media campaigns
    agent = Agent(
        tools=[tools, file_write],
        model=model,
        
        system_prompt="""
        You are an expert social media marketing specialist who creates compelling 
        visual campaigns across multiple platforms. You understand the unique requirements 
        and audience behaviors of each social media platform.
        
        Your campaign creation process:
        1. Start with a strong master image that embodies the campaign message
        2. Use platform optimization tools to create perfectly sized variants
        3. Apply appropriate emotional tones for different engagement goals
        4. Maintain brand consistency across all platforms
        5. Consider mobile-first design for all platforms
        
        Platform considerations:
        - Instagram: Visual storytelling, aesthetic appeal, mobile-optimized
        - Twitter: Clear messaging, tech community appeal, concise visual communication
        - Facebook: Professional appearance, broader demographic appeal
        
        Always use:
        - content_type="social_media" for initial generation
        - optimize_for_platform tool for platform-specific versions
        - Brand colors and consistent visual identity
        - Appropriate emotional tones for campaign goals
        """
    )
    
    print("🤖 Starting social media campaign creation...")
    result = agent(prompt)
    print("\n✨ Social media campaign creation completed!")
    print(f"Agent response: {result}")