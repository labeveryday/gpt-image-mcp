# Strands Agents Examples

This directory contains examples showing how to use **Strands agents** with the GPT Thumbnail MCP server to create sophisticated AI-powered image generation workflows.

## What is Strands?

[Strands](https://github.com/pydantic/strands) is a framework for building AI agents that can use tools and work autonomously. It provides a clean way to combine language models with MCP servers and other tools to create powerful automation workflows.

## Prerequisites

```bash
# Install Strands dependencies (already included in pyproject.toml)
uv add strands-agents strands-agents-tools 'strands-agents[openai]'

# Set your OpenAI API key
export OPENAI_API_KEY="your-openai-api-key"
```

## Examples Overview

### 1. 🎬 YouTube Thumbnail Creation (`strands_youtube_thumbnail.py`)

Creates compelling YouTube thumbnails with AI agents that understand engagement best practices.

**Features:**
- Automatic prompt optimization for YouTube
- Follows 0.3-second rule and engagement principles
- Saves generated thumbnails to files
- Professional styling with emotional appeal

**Usage:**
```bash
uv run python examples/strands_youtube_thumbnail.py
```

**What it does:**
- Connects to the GPT Thumbnail MCP server
- Uses an AI agent to generate YouTube-optimized thumbnails
- Applies text overlays and branding
- Saves the result as a PNG file

### 2. 📝 Blog Content Creation (`strands_blog_content.py`)

Creates complete blog posts with professionally designed header images.

**Features:**
- Generates both written content and visual assets
- Professional styling for business audiences
- Coordinated visual and textual content
- Web-optimized image formats

**Usage:**
```bash
uv run python examples/strands_blog_content.py
```

**What it does:**
- Creates professional blog header images
- Writes comprehensive blog post content
- Ensures visual and textual content alignment
- Saves both markdown content and header image

### 3. 🔄 Batch Thumbnail Generation (`strands_batch_thumbnails.py`)

Demonstrates batch processing for video series with consistent branding.

**Features:**
- Batch generation for efficiency
- Consistent series branding
- A/B testing variations
- Episode numbering and styling

**Usage:**
```bash
uv run python examples/strands_batch_thumbnails.py
```

**What it does:**
- Generates thumbnails for entire video series
- Maintains visual consistency across episodes
- Creates A/B test variations for optimization
- Uses batch processing for efficiency

### 4. 📊 Thumbnail Analysis & Optimization (`strands_thumbnail_analyzer.py`)

Analyzes existing thumbnails and creates improved versions.

**Features:**
- AI-powered thumbnail analysis
- Effectiveness scoring and insights
- Automated optimization suggestions
- Before/after comparison reports

**Usage:**
```bash
uv run python examples/strands_thumbnail_analyzer.py
```

**What it does:**
- Analyzes thumbnail effectiveness
- Identifies improvement opportunities
- Generates optimized versions
- Creates detailed analysis reports

### 5. 📱 Social Media Campaign (`strands_social_media.py`)

Creates comprehensive social media campaigns with platform-optimized images.

**Features:**
- Multi-platform optimization
- Brand consistency across platforms
- Emotional tone variations
- Campaign strategy documentation

**Usage:**
```bash
uv run python examples/strands_social_media.py
```

**What it does:**
- Creates master campaign image
- Optimizes for Instagram, Twitter, Facebook
- Generates multiple emotional tone variations
- Produces campaign strategy documentation

## Key Benefits of Using Strands

### 🤖 **Intelligent Automation**
- Agents understand context and make smart decisions
- Automatic tool selection and chaining
- Natural language instructions for complex workflows

### 🔧 **Tool Integration**
- Seamless MCP server integration
- File operations and data persistence
- Extensible with custom tools

### 🎯 **Task Specialization**
- Each agent has specialized knowledge
- Context-aware decision making
- Professional expertise in image generation

### 📈 **Workflow Efficiency**
- Batch processing capabilities
- Consistent results across tasks
- Reduced manual intervention

## Example Agent Architecture

```python
# Connect to MCP server
stdio_mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="uv", 
        args=["run", "gpt-thumbnail-mcp"],
        cwd="."
    )
))

# Create specialized agent
agent = Agent(
    tools=[mcp_tools, file_write, file_read],
    model=OpenAIModel(api_key=OPENAI_API_KEY, model_id="gpt-4o"),
    name="YouTube Thumbnail Creator",
    instructions="You are an expert thumbnail creator..."
)

# Execute complex workflow
result = agent("Create compelling thumbnails for my video series...")
```

## Advanced Patterns

### 🔄 **Chain Multiple Agents**
Different agents can specialize in different aspects:
- Content strategy agent
- Image generation agent  
- Optimization agent
- Analysis agent

### 📊 **Data-Driven Decisions**
Agents can analyze previous results and improve future outputs:
- Effectiveness scoring
- A/B testing results
- Performance metrics

### 🎨 **Creative Exploration**
Agents can generate multiple variations:
- Style variations
- Color scheme options
- Layout alternatives
- Emotional tone variants

## Tips for Success

### 💡 **Clear Instructions**
- Provide specific, detailed instructions to agents
- Include context about target audience and goals
- Specify file naming and organization preferences

### 🔧 **Tool Selection**
- Combine MCP tools with file operations
- Use batch operations for efficiency
- Leverage analysis tools for optimization

### 📈 **Iterative Improvement**
- Start with simple workflows
- Add complexity gradually
- Use analysis results to improve future prompts

### 🎯 **Quality Control**
- Review agent outputs
- Provide feedback for future improvements
- Maintain brand guidelines and standards

## Troubleshooting

### Common Issues:
1. **MCP Connection**: Ensure the server is accessible and OPENAI_API_KEY is set
2. **File Permissions**: Check write permissions for output directories
3. **API Limits**: Monitor OpenAI API usage and rate limits
4. **Image Size**: Large batch operations may take time

### Debug Mode:
Add logging to see what the agent is doing:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Next Steps

1. **Try the Examples**: Run each example to see different capabilities
2. **Customize Workflows**: Modify prompts and instructions for your needs
3. **Combine Patterns**: Mix and match techniques from different examples
4. **Build Custom Agents**: Create specialized agents for your specific use cases

The combination of Strands agents and the GPT Thumbnail MCP server provides a powerful platform for automating complex image generation workflows while maintaining high quality and professional results.