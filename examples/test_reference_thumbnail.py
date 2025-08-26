#!/usr/bin/env python3
"""
Test the reference thumbnail generation functionality.

Usage:
    python test_reference_thumbnail.py path/to/your/photo.jpg
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


def encode_image(image_path: str) -> str:
    """Encode an image file to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


async def test_reference_generation(image_path: str):
    """Test reference thumbnail generation."""
    print("🎯 Testing Reference Thumbnail Generation")
    print("=" * 50)
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    print(f"📸 Using reference image: {Path(image_path).name}")
    
    try:
        # Encode the reference image
        reference_image_b64 = encode_image(image_path)
        print("✅ Image encoded successfully")
        
        # Test thumbnail generation
        async with ImageGenerationService() as service:
            print("🔄 Generating thumbnail (this takes 30-60 seconds)...")
            
            # Create request matching your style
            request = GenerateImageRequest(
                prompt="Professional YouTube thumbnail in the exact style shown in the reference image",
                content_type=ContentType.YOUTUBE_THUMBNAIL,
                reference_image=reference_image_b64,
                include_text_overlay=True,
                text_overlay="TEST THUMBNAIL",
                style="professional",
                emotional_tone="confident",
                quality="high",
                brand_colors=["#FF0000"],
                topic="test generation"
            )
            
            # Add style instructions
            request.prompt += """ with:
            - Person positioned on the RIGHT side of thumbnail (40% width)
            - Large white text 'TEST THUMBNAIL' on LEFT side on dark background
            - Red banner with secondary text
            - High contrast, professional appearance
            - Dark background (black/dark gray)
            - Confident, engaging expression matching reference style"""
            
            response = await service.generate_image(request)
            
            if response.success:
                print("✅ Thumbnail generated successfully!")
                
                # Save using temp file manager
                file_path = temp_image_manager.save_image(response.image_data, "png")
                print(f"💾 Saved to: {file_path}")
                
                # Show metadata
                print(f"📊 Generation metadata:")
                for key, value in response.metadata.items():
                    print(f"   {key}: {value}")
                
                print(f"\n💭 Revised prompt preview:")
                print(f"   {response.revised_prompt[:300]}...")
                
                return file_path
                
            else:
                print(f"❌ Generation failed: {response.error}")
                if response.suggestions:
                    for suggestion in response.suggestions:
                        print(f"   💡 {suggestion}")
                        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """Main function."""
    print("🖼️ Reference Thumbnail Test")
    print("=" * 40)
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set")
        print("   Set with: export OPENAI_API_KEY='your-key'")
        return
    
    # Get image path from command line
    if len(sys.argv) < 2:
        print("📝 Usage: python test_reference_thumbnail.py path/to/image.jpg")
        print("\n📋 Examples:")
        print("   python test_reference_thumbnail.py ~/Photos/headshot.jpg")
        print("   python test_reference_thumbnail.py /Users/you/Desktop/photo.png")
        print("\n💡 You can use any photo of yourself as reference")
        return
    
    image_path = sys.argv[1]
    print(f"🎯 Testing with: {image_path}")
    
    asyncio.run(test_reference_generation(image_path))


if __name__ == "__main__":
    main()