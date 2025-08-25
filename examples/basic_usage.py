"""Basic usage examples for the GPT Thumbnail MCP server."""

import asyncio
import json
from typing import Dict, Any

# These examples show how to use the MCP server tools
# In practice, these would be called through the MCP protocol

async def example_youtube_thumbnail():
    """Example of generating a YouTube thumbnail."""
    request = {
        "prompt": "Excited tech reviewer holding the latest smartphone, bright studio lighting, tech gear in background",
        "content_type": "youtube_thumbnail",
        "style": "professional",
        "emotional_tone": "excited",
        "include_text_overlay": True,
        "text_overlay": "iPhone 15 Review!",
        "brand_colors": ["#FF0000", "#FFFFFF"],
        "topic": "tech review",
        "target_audience": "tech enthusiasts"
    }
    
    print("YouTube Thumbnail Generation Request:")
    print(json.dumps(request, indent=2))
    print("\nThis would generate a 1792x1024 thumbnail optimized for YouTube engagement.")
    return request


async def example_blog_header():
    """Example of generating a blog header image."""
    request = {
        "prompt": "Professional workspace with laptop, coffee, and productivity tools, clean modern aesthetic",
        "content_type": "blog_header",
        "style": "professional",
        "topic": "productivity tips",
        "target_audience": "professionals",
        "quality": "high"
    }
    
    print("\nBlog Header Generation Request:")
    print(json.dumps(request, indent=2))
    print("\nThis would generate a 1792x1024 professional blog header image.")
    return request


async def example_social_media():
    """Example of generating social media content."""
    request = {
        "prompt": "Inspiring quote card with beautiful nature background, minimalist typography",
        "content_type": "social_media",
        "style": "minimalist",
        "emotional_tone": "friendly",
        "include_text_overlay": True,
        "text_overlay": "Dream Big, Start Small",
        "size": "1024x1024"
    }
    
    print("\nSocial Media Generation Request:")
    print(json.dumps(request, indent=2))
    print("\nThis would generate a square Instagram-optimized image.")
    return request


async def example_batch_generation():
    """Example of generating multiple images at once."""
    requests = [
        {
            "prompt": "Happy chef in kitchen with fresh ingredients",
            "content_type": "youtube_thumbnail",
            "style": "casual",
            "emotional_tone": "friendly",
            "text_overlay": "Easy Pasta Recipe"
        },
        {
            "prompt": "Modern gym equipment and weights",
            "content_type": "blog_header",
            "style": "professional",
            "topic": "fitness"
        },
        {
            "prompt": "Cozy reading nook with books and warm lighting",
            "content_type": "social_media",
            "style": "minimalist",
            "emotional_tone": "calm"
        }
    ]
    
    batch_request = {
        "requests": requests,
        "max_concurrent": 3
    }
    
    print("\nBatch Generation Request:")
    print(json.dumps(batch_request, indent=2))
    print("\nThis would generate 3 different images concurrently.")
    return batch_request


async def example_platform_optimization():
    """Example of optimizing an image for different platforms."""
    # Note: In real usage, image_data would be a base64 encoded image
    request = {
        "image_data": "base64_encoded_image_data_here",
        "target_platform": "instagram",
        "content_type": "lifestyle",
        "optimization_focus": ["mobile_viewing", "engagement", "color_vibrancy"]
    }
    
    print("\nPlatform Optimization Request:")
    print(json.dumps(request, indent=2))
    print("\nThis would optimize an existing image for Instagram.")
    return request


async def example_thumbnail_analysis():
    """Example of analyzing a thumbnail's effectiveness."""
    request = {
        "image_data": "base64_encoded_thumbnail_data_here",
        "platform": "youtube",
        "content_category": "technology"
    }
    
    print("\nThumbnail Analysis Request:")
    print(json.dumps(request, indent=2))
    print("\nThis would analyze the thumbnail and provide effectiveness scoring and suggestions.")
    return request


async def example_prompt_suggestions():
    """Example of getting prompt improvement suggestions."""
    request = {
        "content_type": "youtube_thumbnail",
        "current_prompt": "Person with laptop"
    }
    
    print("\nPrompt Suggestions Request:")
    print(json.dumps(request, indent=2))
    print("\nThis would provide suggestions for improving the prompt for YouTube thumbnails.")
    return request


def demonstrate_response_formats():
    """Show expected response formats for different operations."""
    
    print("\n" + "="*50)
    print("EXPECTED RESPONSE FORMATS")
    print("="*50)
    
    # Successful image generation response
    success_response = {
        "success": True,
        "image_data": "base64_encoded_image_data...",
        "revised_prompt": "Enhanced version of the original prompt used by the model",
        "metadata": {
            "content_type": "youtube_thumbnail",
            "size": "1792x1024",
            "quality": "high",
            "processing_time": 12.5,
            "model_used": "gpt-image-1"
        },
        "message": "Image generated successfully!"
    }
    
    print("\nSuccessful Generation Response:")
    print(json.dumps(success_response, indent=2))
    
    # Analysis response
    analysis_response = {
        "success": True,
        "effectiveness_score": 8.5,
        "analysis": {
            "visual_impact": "High - eye-catching colors and composition",
            "clarity": "Good - clear main subject",
            "text_readability": "Excellent - large, contrasting text",
            "platform_optimization": "Very Good - proper dimensions and quality"
        },
        "suggestions": [
            "Consider adding more emotional expression to faces",
            "Increase contrast between background and foreground elements",
            "Test thumbnail visibility at smaller sizes"
        ]
    }
    
    print("\nAnalysis Response:")
    print(json.dumps(analysis_response, indent=2))
    
    # Error response
    error_response = {
        "success": False,
        "error": "API rate limit exceeded",
        "suggestions": [
            "Wait before making another request",
            "Consider upgrading your API plan",
            "Try again in a few minutes"
        ]
    }
    
    print("\nError Response:")
    print(json.dumps(error_response, indent=2))


async def main():
    """Run all examples."""
    print("GPT Thumbnail MCP Server - Usage Examples")
    print("=" * 50)
    
    await example_youtube_thumbnail()
    await example_blog_header()
    await example_social_media()
    await example_batch_generation()
    await example_platform_optimization()
    await example_thumbnail_analysis()
    await example_prompt_suggestions()
    
    demonstrate_response_formats()
    
    print("\n" + "="*50)
    print("TIPS FOR BEST RESULTS")
    print("="*50)
    
    tips = [
        "Be specific and descriptive in your prompts",
        "Include emotional context and desired style",
        "Specify the target audience when relevant",
        "Use appropriate content types for automatic optimization",
        "Consider brand colors and consistency",
        "Test generated thumbnails at actual display sizes",
        "Use the analysis tool to improve thumbnail effectiveness",
        "Leverage batch generation for A/B testing different approaches"
    ]
    
    for i, tip in enumerate(tips, 1):
        print(f"{i}. {tip}")


if __name__ == "__main__":
    asyncio.run(main())