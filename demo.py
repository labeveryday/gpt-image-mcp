#!/usr/bin/env python3
"""
Demo script for GPT Thumbnail MCP Server

This script demonstrates the basic functionality without requiring a full MCP client.
It shows how the image generation service would work in practice.

To run this demo, you need to set your OpenAI API key in the environment:
export OPENAI_API_KEY="your-api-key-here"

Then run: python demo.py
"""

import asyncio
import json
import os
from pathlib import Path

from src.gpt_image_mcp.models import GenerateImageRequest, ContentType, ThumbnailStyle, EmotionalTone
from src.gpt_image_mcp.image_generator import ImageGenerationService


async def demo_youtube_thumbnail():
    """Demo YouTube thumbnail generation."""
    print("🎬 Generating YouTube Thumbnail...")
    
    request = GenerateImageRequest(
        prompt="Excited tech reviewer holding the latest iPhone, bright studio lighting, tech setup in background",
        content_type=ContentType.YOUTUBE_THUMBNAIL,
        style=ThumbnailStyle.PROFESSIONAL,
        emotional_tone=EmotionalTone.EXCITED,
        include_text_overlay=True,
        text_overlay="iPhone 15 Pro Review!",
        brand_colors=["#FF0000", "#FFFFFF"],
        topic="tech review"
    )
    
    print(f"📝 Prompt: {request.prompt}")
    print(f"📊 Content Type: {request.content_type.value}")
    print(f"🎨 Style: {request.style.value if request.style else 'None'}")
    print(f"😊 Emotional Tone: {request.emotional_tone.value if request.emotional_tone else 'None'}")
    print(f"📐 Size: {request.size.value if request.size else 'Auto'}")
    
    # In a real scenario with API key, this would generate an actual image
    print("✅ YouTube thumbnail request configured successfully!")
    print("   (Set OPENAI_API_KEY to generate actual images)")
    
    return request


async def demo_blog_image():
    """Demo blog image generation."""
    print("\n📝 Generating Blog Header Image...")
    
    request = GenerateImageRequest(
        prompt="Modern workspace with laptop, coffee, and productivity tools, clean professional aesthetic",
        content_type=ContentType.BLOG_HEADER,
        style=ThumbnailStyle.PROFESSIONAL,
        topic="productivity tips",
        target_audience="professionals"
    )
    
    print(f"📝 Prompt: {request.prompt}")
    print(f"📊 Content Type: {request.content_type.value}")
    print(f"🎯 Topic: {request.topic}")
    print(f"👥 Target Audience: {request.target_audience}")
    print(f"📐 Size: {request.size.value if request.size else 'Auto'}")
    
    print("✅ Blog header request configured successfully!")
    
    return request


async def demo_with_api():
    """Demo with actual API calls if API key is available."""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("\n⚠️  No OpenAI API key found. Set OPENAI_API_KEY to test actual generation.")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        return
    
    print(f"\n🔑 Found API key: {api_key[:8]}...")
    print("🚀 Testing actual image generation...")
    
    try:
        # Create a simple request
        request = GenerateImageRequest(
            prompt="A simple red circle on white background",
            content_type=ContentType.GENERAL,
            quality="low"  # Use low quality for faster demo
        )
        
        async with ImageGenerationService() as service:
            print("📞 Calling OpenAI API...")
            response = await service.generate_image(request)
            
            if response.success:
                print("✅ Image generated successfully!")
                print(f"📊 Metadata: {json.dumps(response.metadata, indent=2)}")
                
                # Save image if data is available
                if response.image_data:
                    output_file = "demo_output.png"
                    import base64
                    with open(output_file, "wb") as f:
                        f.write(base64.b64decode(response.image_data))
                    print(f"💾 Image saved to: {output_file}")
            else:
                print(f"❌ Generation failed: {response.error}")
                if response.suggestions:
                    print("💡 Suggestions:")
                    for suggestion in response.suggestions:
                        print(f"   - {suggestion}")
    
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("💡 Make sure your API key is valid and has sufficient credits")


async def show_features():
    """Show key features of the MCP server."""
    print("\n" + "="*60)
    print("🎨 GPT THUMBNAIL MCP SERVER - KEY FEATURES")
    print("="*60)
    
    features = [
        "🎯 Specialized Content Types",
        "   • YouTube thumbnails optimized for engagement",
        "   • Blog headers and featured images",
        "   • Social media posts for multiple platforms",
        "",
        "🚀 Advanced AI Integration",
        "   • GPT-5 powered image generation",
        "   • Intelligent prompt optimization",
        "   • Automatic fallback to DALL-E 3",
        "",
        "🎨 Smart Optimization",
        "   • Platform-specific dimensions",
        "   • Style and emotional tone customization",
        "   • Brand color integration",
        "   • Text overlay support",
        "",
        "📊 Analysis & Insights",
        "   • Thumbnail effectiveness scoring",
        "   • AI-powered improvement suggestions",
        "   • Platform optimization recommendations",
        "",
        "⚡ Performance Features",
        "   • Batch generation support",
        "   • Concurrent processing",
        "   • Image compression and optimization",
        "   • Comprehensive error handling"
    ]
    
    for feature in features:
        print(feature)


async def show_mcp_tools():
    """Show available MCP tools."""
    print("\n" + "="*60)
    print("🔧 AVAILABLE MCP TOOLS")
    print("="*60)
    
    tools = {
        "generate_image": "Generate optimized images for different platforms",
        "optimize_for_platform": "Convert existing images for specific platforms",
        "analyze_thumbnail": "AI analysis of thumbnail effectiveness",
        "generate_batch": "Generate multiple images concurrently",
        "get_prompt_suggestions": "Get suggestions for improving prompts"
    }
    
    for tool_name, description in tools.items():
        print(f"🔧 {tool_name}")
        print(f"   {description}")
        print()


async def main():
    """Run the demo."""
    print("🎬 GPT Thumbnail MCP Server Demo")
    print("=" * 50)
    
    # Show features
    await show_features()
    await show_mcp_tools()
    
    print("\n" + "="*60)
    print("🧪 DEMO EXAMPLES")
    print("="*60)
    
    # Demo examples
    await demo_youtube_thumbnail()
    await demo_blog_image()
    
    # Try actual API if available
    await demo_with_api()
    
    print("\n" + "="*60)
    print("🚀 NEXT STEPS")
    print("="*60)
    
    next_steps = [
        "1. Set your OpenAI API key: export OPENAI_API_KEY='your-key'",
        "2. Configure MCP client with this server",
        "3. Start generating amazing thumbnails and images!",
        "",
        "📖 See README.md for full documentation",
        "🔧 Check examples/ directory for usage examples",
        "💬 Report issues on GitHub"
    ]
    
    for step in next_steps:
        print(step)
    
    print("\n✨ Happy image generating!")


if __name__ == "__main__":
    asyncio.run(main())