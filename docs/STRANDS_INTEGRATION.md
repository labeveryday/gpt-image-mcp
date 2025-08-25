# Strands Agents Integration Guide

## 🎯 Overview

This guide demonstrates how to use **Strands Agents** with the GPT Thumbnail MCP server to create powerful AI-powered image generation workflows. Strands provides a clean framework for building agents that can autonomously use tools and work with MCP servers.

## ✅ Integration Status

**✅ WORKING**: The integration between Strands and our FastMCP server is functional!

- **Connection**: Strands successfully connects to the FastMCP server
- **Tool Discovery**: All 5 MCP tools are automatically discovered
- **Execution**: Agents can successfully call MCP tools
- **Image Generation**: Actual image creation works via OpenAI API

## 🔧 Key Components

### FastMCP Server
Our server provides these tools to Strands agents:
- `generate_image` - Create optimized images for different platforms
- `optimize_for_platform` - Convert images for specific platforms  
- `analyze_thumbnail` - AI analysis of thumbnail effectiveness
- `generate_batch` - Generate multiple images concurrently
- `get_prompt_suggestions` - Get prompt improvement suggestions

### Strands Agent Framework
Strands provides:
- **MCPClient**: Seamless connection to MCP servers via stdio
- **Agent**: Intelligent tool usage with natural language instructions
- **OpenAI Integration**: Built-in support for GPT models
- **Tool Chaining**: Automatic composition of complex workflows

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Already included in pyproject.toml
uv add strands-agents strands-agents-tools 'strands-agents[openai]'
```

### 2. Set Environment Variables
```bash
export OPENAI_API_KEY="your-openai-api-key"
```

### 3. Basic Usage Pattern
```python
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient
from strands.models.openai import OpenAIModel

# Connect to our MCP server
stdio_mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="uv", 
        args=["run", "gpt-thumbnail-mcp"],
        cwd="."
    )
))

# Create specialized agent
with stdio_mcp_client:
    tools = stdio_mcp_client.list_tools_sync()
    agent = Agent(
        tools=[tools],
        model=OpenAIModel(api_key=OPENAI_API_KEY, model_id="gpt-4o"),
        name="Thumbnail Creator"
    )
    
    result = agent("Create a YouTube thumbnail for my Python tutorial")
```

## 📋 Working Examples

### 1. Simple Thumbnail Creation
```bash
uv run python examples/strands_working_example.py
```
**What it does**: Creates a basic YouTube thumbnail with text overlay

### 2. YouTube Content Creator
```bash  
uv run python examples/strands_youtube_thumbnail.py
```
**What it does**: Generates engaging thumbnails optimized for YouTube engagement

### 3. Blog Content Package
```bash
uv run python examples/strands_blog_content.py  
```
**What it does**: Creates blog posts with matching header images

### 4. Batch Processing
```bash
uv run python examples/strands_batch_thumbnails.py
```
**What it does**: Generates multiple thumbnails for video series

### 5. Social Media Campaign
```bash
uv run python examples/strands_social_media.py
```
**What it does**: Creates multi-platform social media image campaigns

## ⚠️ Current Limitations & Solutions

### Context Length Issues
**Problem**: Large tool schemas can exceed model context limits

**Solutions**:
1. **Use GPT-4o**: Better at handling large contexts
2. **Focused Prompts**: Keep instructions concise and specific  
3. **Minimal Agent Instructions**: Avoid verbose system prompts
4. **Tool Subset**: Use only required tools when possible

### Example of Optimized Usage:
```python
# ✅ Good - Focused and concise
agent = Agent(
    tools=[tools],
    model=OpenAIModel(model_id="gpt-4o"),  # Better context handling
    instructions="Create thumbnails using generate_image. Be concise."
)
result = agent("Make a simple YouTube thumbnail with 'Hello World' text")

# ❌ Avoid - Too verbose
agent = Agent(
    tools=[tools, file_read, file_write, other_tools],  # Too many tools
    instructions="You are an expert content creator with deep knowledge of..."  # Too long
)
```

## 🎯 Best Practices

### 1. **Agent Specialization**
Create focused agents for specific tasks:
```python
thumbnail_agent = Agent(
    name="YouTube Thumbnail Creator",
    instructions="Expert at creating engaging YouTube thumbnails"
)

blog_agent = Agent(
    name="Blog Content Creator", 
    instructions="Creates professional blog images and content"
)
```

### 2. **Tool Selection**
Only include tools needed for the specific workflow:
```python
# For image generation only
tools = [mcp_tools]

# For complete workflows  
tools = [mcp_tools, file_write, file_read]
```

### 3. **Error Handling**
Wrap agent calls in try-catch blocks:
```python
try:
    result = agent(prompt)
except Exception as e:
    print(f"Agent failed: {e}")
    # Fallback logic
```

### 4. **Prompt Engineering**
Use clear, specific prompts:
```python
# ✅ Specific and actionable
prompt = "Create a YouTube thumbnail for 'Python Tutorial' with professional style and excited tone"

# ❌ Too vague
prompt = "Make me a good thumbnail"
```

## 🔄 Advanced Workflows

### Multi-Step Processes
Agents can chain multiple MCP tool calls:
1. Generate initial image
2. Analyze effectiveness  
3. Optimize based on analysis
4. Create variations for A/B testing

### Batch Operations
Use the `generate_batch` tool for efficiency:
```python
agent("Create 5 thumbnails for my video series using batch generation")
```

### Cross-Platform Optimization
Generate once, optimize for multiple platforms:
```python  
agent("Create a master image then optimize it for Instagram, Twitter, and Facebook")
```

## 🐛 Troubleshooting

### Common Issues:

1. **"Context length exceeded"**
   - Use GPT-4o model
   - Simplify prompts and instructions
   - Reduce tool count

2. **"Connection failed"**  
   - Ensure MCP server starts properly
   - Check OPENAI_API_KEY is set
   - Verify uv and dependencies are installed

3. **"No tools found"**
   - Check MCP server startup logs
   - Verify FastMCP server is running
   - Test direct server connection

4. **"Image generation failed"**
   - Check OpenAI API credits
   - Verify API key permissions
   - Try fallback models (DALL-E 3)

### Debug Mode:
```python
import logging
logging.basicConfig(level=logging.INFO)
# Shows detailed agent execution steps
```

## 🎉 Success Stories

The integration successfully demonstrates:

✅ **Automated Workflows**: Agents understand context and make smart tool choices  
✅ **Professional Results**: Generated images follow platform best practices  
✅ **Batch Processing**: Efficient handling of multiple requests  
✅ **Cross-Platform**: Seamless optimization for different social platforms  
✅ **Analysis & Improvement**: AI-powered effectiveness scoring and suggestions

## 🚀 Next Steps

1. **Try the Examples**: Start with `strands_working_example.py`
2. **Customize Agents**: Modify instructions for your specific needs
3. **Build Workflows**: Chain multiple agents for complex processes
4. **Optimize Performance**: Tune prompts and tool selection for efficiency

The combination of Strands agents and the GPT Thumbnail MCP server provides a powerful platform for automating sophisticated image generation workflows while maintaining professional quality and platform optimization.