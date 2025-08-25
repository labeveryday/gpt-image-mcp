"""
Example using Strands agents to analyze and optimize existing YouTube thumbnails.
This demonstrates how to use AI agents for thumbnail analysis and improvement workflows.
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

# This example assumes you have a thumbnail image file
# In practice, you would provide the base64 data of your thumbnail
example_thumbnail_path = "existing_thumbnail.png"

prompt = f"""
I have an existing YouTube thumbnail that I'd like to analyze and improve. 
The video is about "JavaScript Fundamentals for Beginners" and targets new programmers.

Please help me:

1. If there's an existing thumbnail file at "{example_thumbnail_path}", read it and convert it to base64 for analysis

2. If no existing file is found, create a sample thumbnail first to demonstrate the analysis process

3. Analyze the thumbnail's effectiveness using the analyze_thumbnail tool, focusing on:
   - Visual impact and eye-catching qualities  
   - Clarity and readability
   - Color usage and contrast
   - Overall engagement potential for the programming/education category

4. Based on the analysis results, generate an improved version of the thumbnail that addresses any identified issues

5. Create a detailed report comparing the original and improved versions, including:
   - Effectiveness scores
   - Specific improvements made
   - Recommendations for future thumbnails

6. Save the improved thumbnail as "optimized_thumbnail.png"
7. Save the analysis report as "thumbnail_analysis_report.md"

Focus on creating thumbnails that will perform well with the target audience of beginner programmers.
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
    
    # Create an agent specialized in thumbnail analysis and optimization
    agent = Agent(
        tools=[tools, file_write, file_read],
        model=model,
        
        system_prompt="""
        You are an expert YouTube thumbnail analyst and optimizer. You understand what 
        makes thumbnails effective and can provide actionable insights for improvement.
        
        Your analysis process:
        1. Examine thumbnails for visual impact, clarity, and engagement factors
        2. Use the analyze_thumbnail tool for AI-powered effectiveness scoring
        3. Identify specific areas for improvement
        4. Generate optimized versions addressing the identified issues
        5. Provide detailed reports with before/after comparisons
        
        When generating improved thumbnails:
        - Use content_type="youtube_thumbnail"
        - Apply insights from the analysis
        - Focus on the target audience and content category
        - Maintain or improve visual branding while fixing issues
        
        When creating reports:
        - Include specific metrics and scores
        - Explain the reasoning behind improvements
        - Provide actionable recommendations for future thumbnails
        """
    )
    
    print("🤖 Starting thumbnail analysis and optimization...")
    result = agent(prompt)
    print("\n✨ Thumbnail analysis and optimization completed!")
    print(f"Agent response: {result}")