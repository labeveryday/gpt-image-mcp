#!/usr/bin/env python3
"""
Generate a YouTube thumbnail using the superhero sample with specific text.
"""

import asyncio
import base64
import json
from pathlib import Path
import os

# Add src to path for imports
import sys
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from gpt_thumbnail_mcp.image_generator import ImageGenerationService
from gpt_thumbnail_mcp.models import GenerateImageRequest, ContentType
from gpt_thumbnail_mcp.file_manager import temp_image_manager


def encode_image(image_path: str) -> str:
    """Encode an image file to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


async def generate_superhero_thumbnail():
    """Generate a YouTube thumbnail for 'The Next Most Powerful Super Hero'."""
    print("🦸 Generating Superhero Thumbnail")
    print("=" * 40)
    
    # Use the superhero sample as reference
    image_path = "examples/sample-images/black_superhero_sample.png"
    
    if not os.path.exists(image_path):
        print(f"❌ Reference image not found: {image_path}")
        return
    
    print(f"📸 Using reference: {Path(image_path).name}")
    reference_image_b64 = encode_image(image_path)
    
    try:
        async with ImageGenerationService() as service:
            print("🔄 Generating thumbnail: 'The Next Most Powerful Super Hero'")
            print("   This will take 30-60 seconds...")
            
            # Create request for superhero thumbnail in your style
            request = GenerateImageRequest(
                prompt="Professional YouTube thumbnail about the next most powerful superhero",
                content_type=ContentType.YOUTUBE_THUMBNAIL,
                reference_image=reference_image_b64,
                include_text_overlay=True,
                text_overlay="THE NEXT MOST POWERFUL",
                style="professional",
                emotional_tone="confident",
                quality="high",
                brand_colors=["#FF0000"],
                topic="superhero content"
            )
            
            # Add secondary text instruction to prompt
            request.prompt += " with secondary text 'SUPER HERO' in a red banner"
            
            response = await service.generate_image(request)
            
            if response.success:
                print("✅ Superhero thumbnail generated!")
                
                # Save the result
                file_path = temp_image_manager.save_image(response.image_data, "png")
                print(f"💾 Saved to: {file_path}")
                
                # Also save to examples directory for easy access
                output_path = Path("examples/sample-images/superhero_thumbnail_result.png")
                image_data = base64.b64decode(response.image_data)
                with open(output_path, "wb") as f:
                    f.write(image_data)
                print(f"📁 Also saved to: {output_path}")
                
                print(f"📊 Metadata:")
                for key, value in response.metadata.items():
                    print(f"   {key}: {value}")
                
                print(f"\n💭 Generated with prompt technique:")
                print(f"   Reference image + your style specifications")
                print(f"   Text: 'THE NEXT MOST POWERFUL' + 'SUPER HERO' in red banner")
                
                return str(file_path)
                
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
    print("🖼️ Superhero YouTube Thumbnail Generator")
    print("=" * 50)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set")
        return
    
    print("🎯 Creating: 'The Next Most Powerful Super Hero' thumbnail")
    print("🎨 Style: Person on right, white text on left, red banner")
    print()
    
    asyncio.run(generate_superhero_thumbnail())


if __name__ == "__main__":
    main()