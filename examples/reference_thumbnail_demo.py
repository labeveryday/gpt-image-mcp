#!/usr/bin/env python3
"""
Demo script showing how to use the new reference image thumbnail generation functionality.

This demonstrates creating thumbnails in the user's specific style using a reference image.
"""

import asyncio
import base64
import json
from pathlib import Path

# Add src to path for imports
import sys
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from gpt_thumbnail_mcp.image_generator import ImageGenerationService
from gpt_thumbnail_mcp.models import GenerateImageRequest, ContentType


def encode_image(image_path: str) -> str:
    """Encode an image file to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


async def demo_reference_thumbnail():
    """Demonstrate reference-based thumbnail generation."""
    print("🎯 Reference Image Thumbnail Generation Demo")
    print("=" * 50)
    
    # Example: You would replace this with your actual reference image path
    # reference_image_path = "/path/to/your/photo.jpg"
    # reference_image_b64 = encode_image(reference_image_path)
    
    # For demo purposes, using a placeholder
    print("📸 Note: Replace with your actual reference image in real usage")
    print("   reference_image_b64 = encode_image('path/to/your/photo.jpg')")
    
    # Example thumbnails in the user's style
    thumbnail_examples = [
        {
            "main_text": "5 TECH SIDE HUSTLES",
            "secondary_text": "THAT MAKE $10K/MONTH",
            "topic": "tech side hustles",
            "description": "Tech entrepreneurship thumbnail"
        },
        {
            "main_text": "HOW I PASSED THE AWS CERTIFIED",
            "secondary_text": "CLOUD PRACTITIONER EXAM",
            "topic": "AWS certification",
            "description": "AWS certification tutorial"
        },
        {
            "main_text": "PYTHON CODING SECRETS",
            "secondary_text": "PROS DON'T WANT YOU TO KNOW",
            "topic": "Python programming",
            "description": "Python programming tips"
        }
    ]
    
    print("🎨 Thumbnail Style Specifications:")
    print("   • Person positioned on RIGHT side (40% of thumbnail)")
    print("   • Large WHITE text on LEFT side on dark background")
    print("   • RED banner for secondary text")
    print("   • High contrast, professional appearance")
    print("   • Dark background (black/dark gray)")
    print("   • Confident, engaging expression")
    print()
    
    async with ImageGenerationService() as service:
        for i, example in enumerate(thumbnail_examples, 1):
            print(f"🔄 Generating Example {i}: {example['description']}")
            print(f"   Main Text: '{example['main_text']}'")
            print(f"   Secondary: '{example['secondary_text']}'")
            print(f"   Topic: {example['topic']}")
            
            # Create request with reference image
            request = GenerateImageRequest(
                prompt=f"Professional YouTube thumbnail about {example['topic']}",
                content_type=ContentType.YOUTUBE_THUMBNAIL,
                # reference_image=reference_image_b64,  # Uncomment when you have a real image
                include_text_overlay=True,
                text_overlay=example['main_text'],
                style="professional",
                emotional_tone="confident",
                quality="high",
                brand_colors=["#FF0000"],
                topic=example['topic']
            )
            
            # Add secondary text to prompt
            if example['secondary_text']:
                request.prompt += f" with secondary text '{example['secondary_text']}' in a red banner"
            
            print(f"   🤖 Generating... (this may take 30-60 seconds)")
            
            # Note: Commented out actual generation for demo
            # response = await service.generate_image(request)
            # 
            # if response.success:
            #     print(f"   ✅ Success! Image generated")
            #     print(f"   📁 Metadata: {response.metadata}")
            #     print(f"   💡 Revised Prompt Preview: {response.revised_prompt[:100]}...")
            # else:
            #     print(f"   ❌ Failed: {response.error}")
            
            print(f"   💭 Would generate with optimized prompt for user's style")
            print()
    
    print("🚀 Usage Instructions:")
    print("   1. Take a high-quality photo of yourself")
    print("   2. Encode it to base64: reference_image_b64 = encode_image('your_photo.jpg')")
    print("   3. Use generate_reference_thumbnail() with your image")
    print("   4. Specify main_text and secondary_text for your content")
    print("   5. The system will create thumbnails matching your established style")
    print()
    print("📋 API Usage:")
    print("""
    # Using the MCP tool directly:
    await generate_reference_thumbnail(
        reference_image=reference_image_b64,
        main_text="YOUR MAIN HEADLINE",
        secondary_text="Secondary text for red banner",
        topic="your video topic"
    )
    
    # Or using the enhanced generate_image function:
    await generate_image(
        prompt="Professional YouTube thumbnail about [topic]",
        content_type="youtube_thumbnail",
        reference_image=reference_image_b64,
        text_overlay="YOUR TEXT",
        style="professional",
        emotional_tone="confident"
    )
    """)


async def demo_style_variations():
    """Show how to create variations of the user's style."""
    print("\n🎨 Style Variations Demo")
    print("=" * 30)
    
    style_variations = [
        {
            "name": "Standard Style",
            "override": None,
            "description": "Default professional style with red accents"
        },
        {
            "name": "Tech Focus", 
            "override": "educational",
            "description": "More technical/educational appearance"
        },
        {
            "name": "Entertainment",
            "override": "entertainment", 
            "description": "More vibrant and eye-catching"
        }
    ]
    
    for variation in style_variations:
        print(f"🎯 {variation['name']}")
        print(f"   Description: {variation['description']}")
        print(f"   Style Override: {variation['override']}")
        print(f"   Usage: style_override='{variation['override']}'")
        print()


if __name__ == "__main__":
    print("🖼️ GPT Thumbnail MCP - Reference Image Demo")
    print("=" * 60)
    print()
    
    asyncio.run(demo_reference_thumbnail())
    asyncio.run(demo_style_variations())
    
    print("✨ Demo completed!")
    print("   Ready to generate thumbnails with your reference image!")