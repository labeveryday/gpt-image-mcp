#!/usr/bin/env python3
"""
Test the new creative mode functionality for reference thumbnails.
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

from gpt_image_mcp.image_generator import ImageGenerationService
from gpt_image_mcp.models import GenerateImageRequest, ContentType
from gpt_image_mcp.file_manager import temp_image_manager


def encode_image(image_path: str) -> str:
    """Encode an image file to base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


async def test_creative_modes():
    """Test different creative modes with the superhero sample."""
    print("🎨 Testing Creative Mode Functionality")
    print("=" * 50)
    
    # Use the superhero sample as reference
    image_path = "examples/sample-images/black_superhero_sample.png"
    
    if not os.path.exists(image_path):
        print(f"❌ Reference image not found: {image_path}")
        return
    
    print(f"📸 Using reference: {Path(image_path).name}")
    reference_image_b64 = encode_image(image_path)
    
    # Define test cases for different creative modes
    test_cases = [
        {
            "name": "Standard Mode (Original)",
            "params": {
                "creative_mode": False,
                "layout_freedom": "standard",
                "composition_style": None
            },
            "description": "Rigid layout with person on right, text on left, red banner"
        },
        {
            "name": "Flexible Creative Mode", 
            "params": {
                "creative_mode": True,
                "layout_freedom": "flexible",
                "composition_style": "dynamic"
            },
            "description": "Some creative flexibility while maintaining best practices"
        },
        {
            "name": "Experimental Mode",
            "params": {
                "creative_mode": True, 
                "layout_freedom": "experimental",
                "composition_style": "creative"
            },
            "description": "Full creative freedom with unconventional designs"
        },
        {
            "name": "Centered Composition",
            "params": {
                "creative_mode": True,
                "layout_freedom": "flexible", 
                "composition_style": "centered"
            },
            "description": "Creative mode with person centered prominently"
        }
    ]
    
    try:
        async with ImageGenerationService() as service:
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n🔄 Test {i}: {test_case['name']}")
                print(f"   📝 {test_case['description']}")
                print(f"   ⚙️ Parameters: {test_case['params']}")
                print("   🤖 Generating... (30-60 seconds)")
                
                # Create request with test parameters
                request = GenerateImageRequest(
                    prompt="Professional YouTube thumbnail about cutting-edge AI technology",
                    content_type=ContentType.YOUTUBE_THUMBNAIL,
                    reference_image=reference_image_b64,
                    include_text_overlay=True,
                    text_overlay="AI REVOLUTION",
                    style="professional",
                    emotional_tone="confident",
                    quality="high",
                    brand_colors=["#FF0000"] if not test_case['params']['creative_mode'] else ["#00FF88", "#FF6B6B"],
                    topic="artificial intelligence",
                    **test_case['params']  # Unpack creative mode parameters
                )
                
                response = await service.generate_image(request)
                
                if response.success:
                    print(f"   ✅ Success! Generated with {response.metadata.get('generation_method', 'unknown method')}")
                    
                    # Save the result
                    file_path = temp_image_manager.save_image(response.image_data, "png")
                    
                    # Also save to examples directory with descriptive name
                    safe_name = test_case['name'].lower().replace(" ", "_").replace("(", "").replace(")", "")
                    output_path = Path(f"examples/sample-images/creative_test_{safe_name}.png")
                    image_data = base64.b64decode(response.image_data)
                    with open(output_path, "wb") as f:
                        f.write(image_data)
                    
                    print(f"   💾 Saved to: {output_path}")
                    
                else:
                    print(f"   ❌ Generation failed: {response.error}")
                    if response.suggestions:
                        for suggestion in response.suggestions:
                            print(f"      💡 {suggestion}")
                            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


async def demonstrate_creative_prompts():
    """Show the different prompts generated for each mode."""
    print(f"\n📋 Creative Prompt Examples")
    print("=" * 40)
    
    # Mock request for demonstration
    base_request = GenerateImageRequest(
        prompt="Professional YouTube thumbnail about AI",
        content_type=ContentType.YOUTUBE_THUMBNAIL,
        reference_image="dummy_base64",
        include_text_overlay=True,
        text_overlay="AI REVOLUTION",
        topic="artificial intelligence"
    )
    
    service = ImageGenerationService()
    
    modes = [
        ("Standard Mode", False, "standard", None),
        ("Creative Flexible", True, "flexible", "dynamic"), 
        ("Experimental", True, "experimental", "creative")
    ]
    
    for mode_name, creative, freedom, composition in modes:
        print(f"\n🎯 {mode_name}:")
        
        # Update request parameters
        base_request.creative_mode = creative
        base_request.layout_freedom = freedom
        base_request.composition_style = composition
        
        # Generate prompt (this calls the internal method)
        prompt = service._create_reference_thumbnail_prompt(base_request, "base prompt context")
        
        # Show first few lines of the prompt
        lines = prompt.split('\n')[:8]
        for line in lines:
            print(f"   {line}")
        print("   ...")


def main():
    """Main function."""
    print("🖼️ Creative Mode Testing Suite")
    print("=" * 50)
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set")
        return
    
    print("🎨 This will test different creative modes:")
    print("   • Standard: Your original rigid layout")
    print("   • Flexible: Some creative freedom with best practices") 
    print("   • Experimental: Full creative freedom")
    print("   • Centered: Creative with centered composition")
    print()
    
    # Run the tests
    asyncio.run(test_creative_modes())
    
    # Show prompt examples
    asyncio.run(demonstrate_creative_prompts())


if __name__ == "__main__":
    main()