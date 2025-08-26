#!/usr/bin/env python3
"""
Practical example: Generate a thumbnail with your reference image.

This will create an actual thumbnail using your screenshot as a reference.
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


def encode_image(image_path: str) -> str:
    """Encode an image file to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


async def generate_example_thumbnail():
    """Generate a real thumbnail using the reference image from your screenshot."""
    print("🎯 Generating Real Thumbnail with Reference Image")
    print("=" * 50)
    
    # Use your screenshot as reference (we'll extract the person from it)
    reference_path = "/var/folders/_t/prj2v87x0vdbqql0dk02jvvc0000gn/T/TemporaryItems/NSIRD_screencaptureui_XIM2Gx/Screenshot 2025-08-25 at 3.42.01 PM.png"
    
    if not os.path.exists(reference_path):
        print(f"❌ Reference image not found at: {reference_path}")
        print("📝 Please update the path to your reference image")
        return
    
    print(f"📸 Using reference image: {Path(reference_path).name}")
    reference_image_b64 = encode_image(reference_path)
    
    # Example: Generate a new thumbnail with different topic
    example = {
        "main_text": "5 PYTHON SECRETS",
        "secondary_text": "THAT CHANGED MY CAREER", 
        "topic": "Python programming tips"
    }
    
    print(f"🔄 Generating: {example['topic']}")
    print(f"   Main Text: '{example['main_text']}'")
    print(f"   Secondary: '{example['secondary_text']}'")
    print(f"   🤖 This will take 30-60 seconds...")
    
    try:
        async with ImageGenerationService() as service:
            # Create request with your reference image
            request = GenerateImageRequest(
                prompt=f"Professional YouTube thumbnail about {example['topic']} in the exact style of the reference image",
                content_type=ContentType.YOUTUBE_THUMBNAIL,
                reference_image=reference_image_b64,
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
            
            response = await service.generate_image(request)
            
            if response.success:
                print(f"   ✅ Success! Thumbnail generated")
                
                # Save the generated image
                output_dir = Path(__file__).parent.parent / "output"
                output_dir.mkdir(exist_ok=True)
                
                # Decode and save
                image_data = base64.b64decode(response.image_data)
                output_path = output_dir / f"reference_thumbnail_example.png"
                
                with open(output_path, "wb") as f:
                    f.write(image_data)
                
                print(f"   💾 Saved to: {output_path}")
                print(f"   📊 Metadata: {json.dumps(response.metadata, indent=2)}")
                print(f"   💭 Revised Prompt: {response.revised_prompt[:200]}...")
                
            else:
                print(f"   ❌ Generation failed: {response.error}")
                if response.suggestions:
                    print("   💡 Suggestions:")
                    for suggestion in response.suggestions:
                        print(f"      • {suggestion}")
                        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("💡 Make sure you have:")
        print("   • OPENAI_API_KEY environment variable set")
        print("   • Valid OpenAI credits")
        print("   • Internet connection")


if __name__ == "__main__":
    print("🖼️ Generate Thumbnail with Reference Image")
    print("=" * 50)
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set")
        print("   Please set it with: export OPENAI_API_KEY='your-key-here'")
    else:
        print("✅ OpenAI API key found")
        asyncio.run(generate_example_thumbnail())