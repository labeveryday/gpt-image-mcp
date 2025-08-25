"""
Example using Strands agents to generate multiple YouTube thumbnails for a video series.
This demonstrates batch processing capabilities and A/B testing thumbnail variations.
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

# Video series information
video_series = {
    "title": "Complete Python Course",
    "videos": [
        {
            "episode": 1,
            "title": "Python Basics - Variables and Data Types",
            "style": "educational",
            "tone": "friendly"
        },
        {
            "episode": 2,
            "title": "Control Flow - If Statements and Loops",
            "style": "professional", 
            "tone": "confident"
        },
        {
            "episode": 3,
            "title": "Functions and Modules",
            "style": "casual",
            "tone": "excited"
        }
    ]
}

prompt = f"""
I need to create a consistent set of YouTube thumbnails for my video series: "{video_series['title']}"

Please generate thumbnails for each video with the following requirements:

Videos to create thumbnails for:
{chr(10).join([f"Episode {v['episode']}: {v['title']} (Style: {v['style']}, Tone: {v['tone']})" for v in video_series['videos']])}

Requirements:
1. Use batch generation to create all thumbnails efficiently
2. Maintain visual consistency across the series (similar color scheme, typography)
3. Each thumbnail should have the episode number prominently displayed
4. Include "Python Course" branding on each thumbnail
5. Use the specified style and tone for each episode
6. Make them optimized for YouTube engagement
7. Save each thumbnail as "episode_X_thumbnail.png" where X is the episode number

Additionally, create 2 variation thumbnails for Episode 1 to A/B test:
- One with a dramatic style and excited tone
- One with a minimalist style and serious tone
- Save these as "episode_1_variant_A.png" and "episode_1_variant_B.png"

Use the batch generation tool for efficiency and ensure all thumbnails follow YouTube best practices.
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
    
    # Create an agent specialized in batch thumbnail creation
    agent = Agent(
        tools=[tools, file_write],
        model=model,
        
        system_prompt="""
        You are an expert at creating consistent, professional YouTube thumbnail series. 
        You understand the importance of visual branding across video series while making 
        each thumbnail unique and engaging.
        
        For batch operations:
        - Use the generate_batch tool for efficient processing
        - Maintain consistent branding elements across all thumbnails
        - Vary styles and tones as requested while keeping series coherence
        - Always optimize for YouTube's best practices
        
        For individual thumbnails:
        - Include episode numbers prominently
        - Use content_type="youtube_thumbnail" 
        - Apply the requested style and emotional tone
        - Ensure text is readable and eye-catching
        """
    )
    
    print("🤖 Starting batch thumbnail generation...")
    result = agent(prompt)
    print("\n✨ Batch thumbnail generation completed!")
    print(f"Agent response: {result}")