#!/usr/bin/env python3
"""
Demonstrate the creative mode prompt differences without generating images.
"""

import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from gpt_image_mcp.image_generator import ImageGenerationService
from gpt_image_mcp.models import GenerateImageRequest, ContentType


def demonstrate_creative_modes():
    """Show the different prompts generated for each mode."""
    print("🎨 Creative Mode Prompt Comparison")
    print("=" * 60)
    
    # Mock request for demonstration
    base_request = GenerateImageRequest(
        prompt="Professional YouTube thumbnail about AI technology",
        content_type=ContentType.YOUTUBE_THUMBNAIL,
        reference_image="dummy_base64",
        include_text_overlay=True,
        text_overlay="AI REVOLUTION",
        topic="artificial intelligence",
        style="professional",
        emotional_tone="confident"
    )
    
    service = ImageGenerationService()
    base_prompt = "Professional YouTube thumbnail about AI technology"
    
    modes = [
        {
            "name": "🔒 STANDARD MODE (Original Rigid Layout)",
            "creative_mode": False,
            "layout_freedom": "standard", 
            "composition_style": None
        },
        {
            "name": "🎨 FLEXIBLE CREATIVE MODE",
            "creative_mode": True,
            "layout_freedom": "flexible",
            "composition_style": "dynamic"
        },
        {
            "name": "🚀 EXPERIMENTAL MODE (Full Freedom)",
            "creative_mode": True,
            "layout_freedom": "experimental", 
            "composition_style": "creative"
        },
        {
            "name": "📍 CENTERED COMPOSITION",
            "creative_mode": True,
            "layout_freedom": "flexible",
            "composition_style": "centered"
        }
    ]
    
    for mode in modes:
        print(f"\n{mode['name']}")
        print("=" * 60)
        
        # Update request parameters
        base_request.creative_mode = mode['creative_mode']
        base_request.layout_freedom = mode['layout_freedom']
        base_request.composition_style = mode['composition_style']
        
        # Generate prompt
        prompt = service._create_reference_thumbnail_prompt(base_request, base_prompt)
        
        # Show the prompt
        print(prompt)
        print("\n" + "-" * 60)
    
    print(f"\n✨ KEY DIFFERENCES:")
    print("🔒 Standard: Rigid positioning (person on right, text on left, red banner)")
    print("🎨 Flexible: Creative freedom while maintaining best practices")
    print("🚀 Experimental: Complete creative freedom with unconventional designs")
    print("📍 Centered: Person prominently centered in composition")


def show_usage_examples():
    """Show how to use the new creative parameters."""
    print(f"\n📋 USAGE EXAMPLES")
    print("=" * 50)
    
    examples = [
        {
            "title": "Consistent Branding (Default)",
            "code": '''generate_image(
    prompt="Professional YouTube thumbnail about Python",
    reference_image="base64_image_data",
    text_overlay="PYTHON MASTERY"
    # creative_mode=False (default)
    # layout_freedom="standard" (default)
)'''
        },
        {
            "title": "Creative with Some Structure", 
            "code": '''generate_image(
    prompt="Creative coding tutorial thumbnail",
    reference_image="base64_image_data", 
    text_overlay="CODE CREATIVELY",
    creative_mode=True,
    layout_freedom="flexible",
    composition_style="dynamic"
)'''
        },
        {
            "title": "Full Creative Freedom",
            "code": '''generate_image(
    prompt="Artistic tech thumbnail",
    reference_image="base64_image_data",
    text_overlay="TECH ART",
    creative_mode=True,
    layout_freedom="experimental",
    composition_style="creative"
)'''
        },
        {
            "title": "Centered Personal Brand",
            "code": '''generate_reference_thumbnail(
    reference_image="base64_image_data",
    main_text="MY TECH JOURNEY", 
    creative_mode=True,
    composition_style="centered",
    layout_freedom="flexible"
)'''
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['title']}")
        print("-" * 30)
        print(example['code'])


def main():
    """Main function."""
    print("🖼️ Creative Mode Demo - Prompt Analysis")
    print("=" * 60)
    print("This shows how different creative modes generate different prompts")
    print("without actually calling the OpenAI API.\n")
    
    demonstrate_creative_modes()
    show_usage_examples()
    
    print(f"\n🎯 READY TO USE:")
    print("• Standard mode: Perfect for consistent branding")
    print("• Creative modes: Perfect for experimentation and variety")
    print("• All modes preserve your face from the reference image!")


if __name__ == "__main__":
    main()