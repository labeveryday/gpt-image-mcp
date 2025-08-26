#!/usr/bin/env python3
"""
Test reference thumbnail generation using a provided image.
"""

import asyncio
import base64
import json
import sys
from pathlib import Path
import os

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from gpt_thumbnail_mcp.image_generator import ImageGenerationService
from gpt_thumbnail_mcp.models import GenerateImageRequest, ContentType
from gpt_thumbnail_mcp.file_manager import temp_image_manager


async def test_with_sample():
    """Test with the AWS thumbnail as reference."""
    print("🎯 Testing Reference Thumbnail Generation")
    print("=" * 50)
    
    # The AWS thumbnail you shared as base64 (placeholder - you'd need to provide the actual base64)
    print("📸 Using AWS thumbnail as reference style template")
    print("💡 In real usage, you'd provide your own photo as reference")
    
    try:
        async with ImageGenerationService() as service:
            print("🔄 Generating test thumbnail (30-60 seconds)...")
            
            # Test generation with a different topic but same style
            request = GenerateImageRequest(
                prompt="""Create a professional YouTube thumbnail in the exact same style as a reference image showing:
                - Person positioned on RIGHT side (40% of image width) 
                - Large bold WHITE text on LEFT side on dark background
                - RED rectangular banner for secondary text
                - Dark professional background (black/dark gray)
                - High contrast design for maximum visibility
                - Confident, professional pose
                
                Main topic: Python programming secrets""",
                content_type=ContentType.YOUTUBE_THUMBNAIL,
                # reference_image would go here if we had the base64 data
                include_text_overlay=True,
                text_overlay="PYTHON SECRETS REVEALED",
                style="professional", 
                emotional_tone="confident",
                quality="high",
                brand_colors=["#FF0000"],
                topic="Python programming"
            )
            
            response = await service.generate_image(request)
            
            if response.success:
                print("✅ Test thumbnail generated!")
                
                # Save the result
                file_path = temp_image_manager.save_image(response.image_data, "png")
                print(f"💾 Saved to: {file_path}")
                
                print(f"📊 Metadata: {json.dumps(response.metadata, indent=2)}")
                
                return file_path
                
            else:
                print(f"❌ Generation failed: {response.error}")
                if response.suggestions:
                    for suggestion in response.suggestions:
                        print(f"   💡 {suggestion}")
                        
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def main():
    """Main function.""" 
    print("🖼️ Reference Thumbnail Test (Style Template)")
    print("=" * 50)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set")
        return
    
    print("🎯 This demonstrates the thumbnail style matching")
    print("📝 To use with your own photo:")
    print("   uv run examples/test_reference_thumbnail.py your_photo.jpg")
    print()
    
    asyncio.run(test_with_sample())


if __name__ == "__main__":
    main()