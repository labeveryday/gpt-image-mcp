# GPT Thumbnail MCP Server

A powerful MCP (Model Context Protocol) server that generates dynamic images using OpenAI's latest models for YouTube thumbnails, blog images, and social media content. Built with FastMCP and optimized for performance and simplicity.

## 🌟 Features

### 🎯 **Specialized Content Generation**
- **YouTube Thumbnails**: Optimized for engagement (1536×1024 landscape format)
- **Blog Images**: Professional headers and featured images  
- **Social Media**: Platform-optimized content for Instagram, Twitter, Facebook
- **General Purpose**: Flexible image generation for any use case

### 🚀 **Advanced AI Integration**
- **GPT-Image-1 Support**: Uses OpenAI's latest and best image generation model
- **Multi-Model Fallback**: Automatic fallback to DALL-E 3 for reliability
- **Smart Prompt Optimization**: Enhanced prompts based on content type
- **Batch Processing**: Generate multiple images concurrently

### 🎨 **Platform Intelligence**
- **Auto-Sizing**: Intelligent size selection based on content type
- **Style Variants**: Professional, casual, dramatic, minimalist, educational
- **Emotional Tones**: Excited, confident, friendly, serious, and more
- **Brand Integration**: Custom color schemes and consistent styling

### 📊 **Analysis & Optimization**
- **Effectiveness Scoring**: Thumbnail analysis with 0-10 effectiveness scoring
- **Platform Optimization**: Convert images for specific platforms
- **Improvement Suggestions**: Actionable recommendations for better performance
- **Best Practices**: Built-in knowledge of platform requirements

## 📦 Installation

### Prerequisites
- Python 3.11+
- OpenAI API key with GPT-Image-1/DALL-E 3 access
- [UV package manager](https://github.com/astral-sh/uv) (recommended)

### Quick Start
```bash
# Clone the repository
git clone https://github.com/labeveryday/gpt-thumbnail-mcp.git
cd gpt-thumbnail-mcp

# Install dependencies
uv sync

# Configure your API key
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=your_key_here

# Test the installation
uv run python demo.py
```

## 🚀 Usage

### Starting the MCP Server
```bash
# Start with UV (recommended)
uv run gpt-thumbnail-mcp

# Or run the server directly
uv run python src/gpt_thumbnail_mcp/server.py
```

### MCP Client Integration
Add to your MCP client configuration (Claude Code, etc.):

```json
{
  "name": "gpt-thumbnail-mcp",
  "command": "uv",
  "args": ["run", "gpt-thumbnail-mcp"],
  "cwd": "/path/to/gpt-thumbnail-mcp"
}
```

### Demo Usage
```bash
# Run the demo to test functionality
uv run python demo.py

# Test individual features
uv run python -c "from demo import demo_youtube_thumbnail; import asyncio; asyncio.run(demo_youtube_thumbnail())"
```

## 🛠️ Available Tools

### 1. `generate_image` - Primary Image Generation
Generate optimized images for any platform or purpose.

```json
{
  "prompt": "Excited tech reviewer with the latest gadget, studio lighting",
  "content_type": "youtube_thumbnail",
  "style": "professional", 
  "emotional_tone": "excited",
  "size": "1536x1024",
  "include_text_overlay": true,
  "text_overlay": "Amazing New Tech!",
  "brand_colors": ["#FF6B6B", "#4ECDC4"]
}
```

### 2. `analyze_thumbnail` - AI-Powered Analysis
Get effectiveness scores and improvement suggestions.

```json
{
  "image_data": "base64_encoded_image_data",
  "platform": "youtube",
  "content_category": "education"
}
```

### 3. `optimize_for_platform` - Platform Conversion
Adapt existing images for different platforms.

```json
{
  "image_data": "base64_encoded_image_data", 
  "target_platform": "instagram",
  "optimization_focus": ["engagement", "readability"]
}
```

### 4. `generate_batch` - Bulk Generation
Generate multiple images efficiently.

```json
{
  "requests": [
    {"prompt": "Tutorial thumbnail 1", "content_type": "youtube_thumbnail"},
    {"prompt": "Tutorial thumbnail 2", "content_type": "youtube_thumbnail"}
  ],
  "max_concurrent": 3
}
```

### 5. `get_prompt_suggestions` - Prompt Enhancement
Get AI suggestions for better prompts.

```json
{
  "content_type": "youtube_thumbnail",
  "current_prompt": "Python tutorial video"
}
```

## 📐 Supported Sizes & Platforms

| Platform | Optimal Size | Aspect Ratio | Notes |
|----------|-------------|--------------|--------|
| **YouTube** | 1792×1024 | ~16:9 | OpenAI supported landscape |
| **Instagram** | 1024×1024 | 1:1 | Square format |
| **Twitter** | 1792×1024 | ~16:9 | Wide landscape format |
| **Facebook** | 1792×1024 | ~16:9 | Cover images |
| **Blog Header** | 1792×1024 | ~16:9 | Professional headers |
| **Blog Featured** | 1024×1792 | ~9:16 | Portrait format |

*All sizes use OpenAI's currently supported dimensions: 1024×1024, 1024×1792, and 1792×1024.*

## 🎨 Content Types & Styles

### Content Types
- `youtube_thumbnail` - High-impact video thumbnails
- `blog_header` - Professional article headers
- `blog_featured` - Featured/hero images
- `social_media` - General social content
- `general` - Flexible general-purpose images

### Styles
- `professional` - Clean, business-appropriate
- `casual` - Relaxed, approachable
- `dramatic` - High-contrast, bold
- `minimalist` - Simple, elegant
- `educational` - Clear, instructional
- `entertainment` - Fun, engaging

### Emotional Tones
- `excited` - High energy, enthusiastic
- `confident` - Strong, authoritative  
- `friendly` - Warm, approachable
- `curious` - Intriguing, mysterious
- `serious` - Professional, formal
- `surprised` - Attention-grabbing
- `dramatic` - Intense, compelling

## 💾 File Storage

### Temporary Image Storage
Generated images are automatically saved to cross-platform temporary directories:

- **macOS**: `/var/folders/.../gpt-thumbnail-mcp/`
- **Windows**: `C:\Users\{user}\AppData\Local\Temp\gpt-thumbnail-mcp\`  
- **Linux**: `/tmp/gpt-thumbnail-mcp/`

**Automatic Cleanup:**
- Files older than 24 hours are automatically deleted
- Cleanup runs on server startup and via the `cleanup_temp_files` tool
- Unique filenames prevent conflicts: `image_20250825_142324_3566695c.png`

**Manual Management:**
```bash
# Check temp directory status
uv run python -c "from src.gpt_thumbnail_mcp.file_manager import temp_image_manager; print(temp_image_manager.get_temp_dir_info())"

# Clean up old files manually
uv run python -c "from src.gpt_thumbnail_mcp.file_manager import temp_image_manager; print(f'Cleaned {temp_image_manager.cleanup_old_files()} files')"
```

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Required
OPENAI_API_KEY=your_openai_api_key

# Optional - Model Configuration
DEFAULT_MODEL=gpt-image-1               # Primary model (OpenAI's best)
IMAGE_MODEL=gpt-image-1                 # Direct image model  
FALLBACK_MODEL=dall-e-3                 # Fallback option

# Optional - Performance
MAX_CONCURRENT_GENERATIONS=5            # Batch processing limit
TIMEOUT_SECONDS=120                     # Request timeout
RATE_LIMIT_PER_MINUTE=30               # API rate limiting

# Optional - Quality  
DEFAULT_QUALITY=auto                    # Image quality
ENABLE_COMPRESSION=true                 # File size optimization
MAX_IMAGE_SIZE_MB=10.0                 # Size limits

# Optional - Logging
LOG_LEVEL=INFO                         # DEBUG for verbose logging
ENABLE_DETAILED_LOGGING=false          # Request/response logging
```

## 📋 Examples

### YouTube Tutorial Thumbnail
```python
request = {
    "prompt": "Enthusiastic developer coding Python, modern setup, vibrant colors",
    "content_type": "youtube_thumbnail", 
    "style": "professional",
    "emotional_tone": "excited",
    "text_overlay": "Master Python Fast!",
    "brand_colors": ["#3776ab", "#ffd343"]  # Python colors
}
```

### Blog Header Image  
```python
request = {
    "prompt": "Modern digital workspace with analytics and growth charts",
    "content_type": "blog_header",
    "topic": "business growth",
    "target_audience": "entrepreneurs", 
    "style": "professional"
}
```

### Social Media Post
```python
request = {
    "prompt": "Cozy coffee shop workspace with laptop and notebook",
    "content_type": "social_media",
    "style": "casual",
    "emotional_tone": "friendly",
    "size": "1024x1024"  # Instagram square
}
```

## 🧪 Testing & Development

### Run Tests
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/gpt_thumbnail_mcp

# Test specific functionality
uv run python demo.py
```

### Code Quality
```bash
# Format code  
uv run black src/ tests/

# Lint code
uv run ruff check src/ tests/

# Type checking
uv run mypy src/
```

### Development Server
```bash
# Start in development mode with detailed logging
LOG_LEVEL=DEBUG ENABLE_DETAILED_LOGGING=true uv run python src/gpt_thumbnail_mcp/server.py
```

## 🤖 Integration Examples

### Direct MCP Usage
```python
import asyncio
from mcp import ClientSession, stdio_client, StdioServerParameters

async def generate_thumbnail():
    async with stdio_client(StdioServerParameters(
        command="uv", args=["run", "gpt-thumbnail-mcp"]
    )) as (read, write):
        async with ClientSession(read, write) as client:
            result = await client.call_tool("generate_image", {
                "prompt": "Amazing tech review thumbnail",
                "content_type": "youtube_thumbnail"
            })
            return result

# Run it
result = asyncio.run(generate_thumbnail())
```

### Claude Code Integration
The server integrates seamlessly with Claude Code for AI-powered content creation workflows.

## 🔍 Troubleshooting

### Common Issues

**API Key Errors**
```bash
# Verify your API key is set
echo $OPENAI_API_KEY

# Check API key validity
uv run python -c "import openai; print(openai.api_key)"
```

**Image Generation Fails**
- Simplify complex prompts
- Check API credits and rate limits  
- Try fallback models (DALL-E 3)

**Large File Sizes**
- Enable compression: `ENABLE_COMPRESSION=true`
- Reduce quality: `DEFAULT_QUALITY=medium`
- Check size limits: `MAX_IMAGE_SIZE_MB=10`

**Rate Limiting**  
- Adjust concurrent requests: `MAX_CONCURRENT_GENERATIONS=3`
- Increase timeout: `TIMEOUT_SECONDS=180`
- Lower rate limit: `RATE_LIMIT_PER_MINUTE=20`

### Debug Mode
```bash
# Enable verbose logging
LOG_LEVEL=DEBUG ENABLE_DETAILED_LOGGING=true uv run gpt-thumbnail-mcp

# Check server health
uv run python -c "from src.gpt_thumbnail_mcp.config import settings; print(settings)"
```

## 📈 Performance Notes

- **OpenAI API Compatibility**: Uses OpenAI-supported image dimensions (1024×1024, 1792×1024, 1024×1792)
- **Optimized Tool Schemas**: Simplified models for better MCP client compatibility
- **Batch Processing**: Use `generate_batch` for multiple images
- **Fallback Strategy**: Automatic model fallback ensures reliability

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make changes with proper Pydantic validation
4. Add tests for new functionality
5. Run code quality checks: `uv run black src/ && uv run ruff check src/`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastMCP](https://github.com/pydantic/fastmcp) for clean MCP server architecture
- Powered by [OpenAI](https://openai.com) GPT and DALL-E models  
- Uses [Pydantic](https://pydantic.dev) for robust data validation
- Package management with [UV](https://github.com/astral-sh/uv)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/gpt-thumbnail-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/gpt-thumbnail-mcp/discussions)
- **Documentation**: See `docs/` directory for detailed guides

---

**Happy image generating!** 🎨✨
