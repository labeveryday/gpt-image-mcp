"""FastMCP server for GPT-powered image generation."""

import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP

# Handle both direct execution and module import
if __name__ == "__main__":
    # Add the src directory to the path for direct execution
    src_path = Path(__file__).parent.parent
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

# Ensure environment variables are loaded before importing settings
try:
    from .config import settings
    from .file_manager import temp_image_manager
    from .image_generator import ImageGenerationService
    from .models import (
        BatchGenerationRequest,
        ContentType,
        GenerateImageRequest,
        ImageAnalysisRequest,
        OptimizeForPlatformRequest,
    )
    from .prompt_optimizer import PromptOptimizer
    from .thumbnail_analyzer import ThumbnailAnalyzer
except ImportError:
    # Direct execution fallback
    from gpt_thumbnail_mcp.config import settings
    from gpt_thumbnail_mcp.file_manager import temp_image_manager
    from gpt_thumbnail_mcp.image_generator import ImageGenerationService
    from gpt_thumbnail_mcp.models import (
        BatchGenerationRequest,
        ContentType,
        GenerateImageRequest,
        ImageAnalysisRequest,
        OptimizeForPlatformRequest,
    )
    from gpt_thumbnail_mcp.prompt_optimizer import PromptOptimizer
    from gpt_thumbnail_mcp.thumbnail_analyzer import ThumbnailAnalyzer

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastMCP server
mcp = FastMCP(settings.server_name)


@mcp.resource("gpt://image-generation/templates")
def get_templates() -> str:
    """Get image generation templates for different content types."""
    templates = {
        "youtube_thumbnail": {
            "description": "Template for YouTube thumbnails",
            "default_size": "1792x1024",
            "recommended_style": ["dramatic", "professional", "entertainment"],
            "best_practices": [
                "Include expressive faces",
                "Use high contrast colors",
                "Add compelling text overlays",
                "Create emotional reactions"
            ]
        },
        "blog_header": {
            "description": "Template for blog header images",
            "default_size": "1792x1024",
            "recommended_style": ["professional", "minimalist"],
            "best_practices": [
                "Maintain professional appearance",
                "Ensure relevance to content",
                "Use landscape orientation",
                "Keep composition clean"
            ]
        },
        "social_media": {
            "description": "Template for social media posts",
            "default_size": "1080x1080",
            "recommended_style": ["casual", "vibrant"],
            "best_practices": [
                "Use bright, engaging colors",
                "Optimize for mobile viewing",
                "Create scroll-stopping content",
                "Include shareable elements"
            ]
        }
    }
    return json.dumps(templates, indent=2)


@mcp.resource("gpt://image-generation/best-practices")
def get_best_practices() -> str:
    """Get best practices for different platforms and content types."""
    best_practices = {
        "youtube": {
            "thumbnail_specs": {
                "size": "1920x1080 pixels",
                "aspect_ratio": "16:9",
                "file_size": "Under 2MB",
                "formats": ["JPG", "PNG", "GIF"]
            },
            "design_principles": [
                "Follow the 0.3 second rule - make it instantly understandable",
                "Use high contrast for visibility",
                "Include expressive human faces when relevant",
                "Create emotional connection with viewers",
                "Use vibrant, eye-catching colors",
                "Ensure text is large and readable",
                "Maintain consistent branding across videos"
            ],
            "common_mistakes": [
                "Too much text or clutter",
                "Low contrast that's hard to see",
                "Misleading thumbnails that don't match content",
                "Inconsistent branding",
                "Poor image quality or resolution"
            ]
        },
        "blog": {
            "header_images": {
                "recommended_size": "1536x1024 pixels",
                "aspect_ratio": "3:2",
                "optimization": "Web-optimized for fast loading"
            },
            "design_principles": [
                "Maintain professional appearance",
                "Ensure clear relevance to article content",
                "Use high-quality, crisp imagery",
                "Consider SEO implications",
                "Optimize for various device sizes",
                "Incorporate brand elements subtly"
            ]
        }
    }
    return json.dumps(best_practices, indent=2)


@mcp.resource("gpt://image-generation/examples")
def get_examples() -> str:
    """Get example prompts and generated images."""
    examples = {
        "youtube_thumbnails": [
            {
                "content_type": "tech_tutorial",
                "prompt": "Create a YouTube thumbnail for a Python programming tutorial. Show an excited programmer's face with Python code in the background, bright colors, professional but approachable style",
                "style": "professional",
                "emotional_tone": "excited"
            },
            {
                "content_type": "fitness",
                "prompt": "Design a YouTube thumbnail for a home workout video. Feature a confident person in workout clothes, energetic pose, bright motivational colors",
                "style": "energetic",
                "emotional_tone": "confident"
            }
        ],
        "blog_images": [
            {
                "content_type": "business_article",
                "prompt": "Create a professional blog header image about digital marketing trends. Modern, clean design with abstract business graphics",
                "topic": "digital marketing",
                "target_audience": "business professionals"
            }
        ]
    }
    return json.dumps(examples, indent=2)


@mcp.tool()
async def generate_image(
    prompt: str,
    content_type: str = "general",
    size: str = "auto",
    quality: str = "auto",
    style: Optional[str] = None,
    emotional_tone: Optional[str] = None,
    include_text_overlay: bool = False,
    text_overlay: Optional[str] = None,
    brand_colors: Optional[List[str]] = None,
    topic: Optional[str] = None,
    target_audience: Optional[str] = None,
    avoid_elements: Optional[List[str]] = None,
    emphasis_elements: Optional[List[str]] = None
) -> str:
    """Generate images using GPT-5 for YouTube thumbnails, blog images, and social media content.
    
    Args:
        prompt: Description of the image to generate
        content_type: Type of content (youtube_thumbnail, blog_header, blog_featured, social_media, general)
        size: Image dimensions (auto-selected based on content_type if not provided)
        quality: Image quality level (low, medium, high, auto)
        style: Visual style (professional, casual, dramatic, minimalist, educational, entertainment)
        emotional_tone: Emotional tone (excited, curious, confident, surprised, serious, friendly, dramatic)
        include_text_overlay: Whether to include text overlay on the image
        text_overlay: Text to overlay on the image
        brand_colors: Brand colors to use (hex codes)
        topic: Topic or subject matter for the image
        target_audience: Target audience for the content
        avoid_elements: Elements to avoid in the generated image
        emphasis_elements: Elements to emphasize in the generated image
    """
    try:
        # Create request model with proper defaults for MCP compatibility
        request_data = {
            "prompt": prompt,
            "content_type": content_type,
            "include_text_overlay": include_text_overlay
        }
        
        # Only include non-None optional values
        if size and size != "auto":
            request_data["size"] = size
        if quality and quality != "auto":
            request_data["quality"] = quality  
        if style:
            request_data["style"] = style
        if emotional_tone:
            request_data["emotional_tone"] = emotional_tone
        if text_overlay:
            request_data["text_overlay"] = text_overlay
        if brand_colors:
            request_data["brand_colors"] = brand_colors
        if topic:
            request_data["topic"] = topic
        if target_audience:
            request_data["target_audience"] = target_audience
        if avoid_elements:
            request_data["avoid_elements"] = avoid_elements
        if emphasis_elements:
            request_data["emphasis_elements"] = emphasis_elements
            
        request = GenerateImageRequest(**request_data)
        
        # Generate image
        async with ImageGenerationService() as service:
            response = await service.generate_image(request)
        
        if response.success:
            # Save image to temporary file instead of returning base64 data
            try:
                file_path = temp_image_manager.save_image(response.image_data, "png")
                result = {
                    "success": True,
                    "file_path": file_path,
                    "revised_prompt": response.revised_prompt,
                    "metadata": response.metadata,
                    "message": "Image generated and saved successfully!"
                }
                
                if response.suggestions:
                    result["suggestions"] = response.suggestions
            except Exception as e:
                logger.error(f"Failed to save image file: {str(e)}")
                result = {
                    "success": False,
                    "error": f"Image generated but failed to save: {str(e)}",
                    "suggestions": ["Try generating the image again"]
                }
        else:
            result = {
                "success": False,
                "error": response.error,
                "suggestions": response.suggestions or []
            }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Image generation failed: {str(e)}")
        return json.dumps({
            "success": False,
            "error": str(e),
            "suggestions": [
                "Check that your prompt is valid",
                "Ensure all parameters are correct",
                "Try again with a simpler request"
            ]
        }, indent=2)


@mcp.tool()
async def optimize_for_platform(
    image_data: str,
    target_platform: str,
    content_type: Optional[str] = None,
    optimization_focus: Optional[List[str]] = None
) -> str:
    """Optimize an existing image for a specific platform.
    
    Args:
        image_data: Base64 encoded image data
        target_platform: Target platform (youtube, instagram, twitter, facebook, blog)
        content_type: Type of content (e.g., tutorial, entertainment, news)
        optimization_focus: Areas to focus optimization on
    """
    try:
        # Create request with proper None handling
        request_data = {
            "image_data": image_data,
            "target_platform": target_platform
        }
        
        if content_type:
            request_data["content_type"] = content_type
        if optimization_focus:
            request_data["optimization_focus"] = optimization_focus
            
        request = OptimizeForPlatformRequest(**request_data)
        
        async with ImageGenerationService() as service:
            response = await service.optimize_for_platform(request)
        
        if response.success:
            # Save optimized image to temporary file
            try:
                file_path = temp_image_manager.save_image(response.image_data, "png")
                result = {
                    "success": True,
                    "optimized_image_path": file_path,
                    "optimized_for": request.target_platform,
                    "metadata": response.metadata,
                    "message": f"Image optimized for {request.target_platform} and saved"
                }
            except Exception as e:
                logger.error(f"Failed to save optimized image: {str(e)}")
                result = {
                    "success": False,
                    "error": f"Image optimized but failed to save: {str(e)}",
                    "suggestions": ["Try the optimization again"]
                }
        else:
            result = {
                "success": False,
                "error": response.error,
                "suggestions": response.suggestions or []
            }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Platform optimization failed: {str(e)}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


@mcp.tool()
async def analyze_thumbnail(
    image_data: str,
    platform: str = "youtube",
    content_category: Optional[str] = None
) -> str:
    """Analyze a thumbnail's effectiveness and provide improvement suggestions.
    
    Args:
        image_data: Base64 encoded image data
        platform: Platform for analysis (youtube, instagram, twitter, facebook, blog)
        content_category: Content category (e.g., education, entertainment, tech)
    """
    try:
        # Create request with proper None handling
        request_data = {
            "image_data": image_data,
            "platform": platform
        }
        
        if content_category:
            request_data["content_category"] = content_category
            
        request = ImageAnalysisRequest(**request_data)
        
        analyzer = ThumbnailAnalyzer()
        response = await analyzer.analyze_image(request)
        
        if response.success:
            result = {
                "success": True,
                "effectiveness_score": response.effectiveness_score,
                "analysis": response.analysis,
                "suggestions": response.suggestions,
                "message": "Thumbnail analysis completed successfully!"
            }
        else:
            result = {
                "success": False,
                "error": response.error
            }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Thumbnail analysis failed: {str(e)}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


@mcp.tool()
async def generate_batch(
    requests: List[Dict[str, Any]],
    max_concurrent: int = 3
) -> str:
    """Generate multiple images at once with different parameters.
    
    Args:
        requests: List of image generation requests (each with prompt, content_type, etc.)
        max_concurrent: Maximum number of concurrent generations (1-10)
    """
    try:
        # Convert dict requests to proper request models
        generation_requests = []
        for req_dict in requests:
            req = GenerateImageRequest(**req_dict)
            generation_requests.append(req)
        
        batch_request = BatchGenerationRequest(
            requests=generation_requests,
            max_concurrent=min(max(max_concurrent, 1), 10)  # Clamp between 1-10
        )
        
        async with ImageGenerationService() as service:
            response = await service.generate_batch(batch_request)
        
        # Format results for output
        results_summary = {
            "total_successful": response.total_successful,
            "total_failed": response.total_failed,
            "processing_time": f"{response.processing_time:.2f} seconds",
            "results": []
        }
        
        for i, result in enumerate(response.results):
            result_data = {
                "index": i,
                "success": result.success
            }
            
            if result.success:
                # Save each batch image to temporary file
                try:
                    file_path = temp_image_manager.save_image(result.image_data, "png")
                    result_data.update({
                        "image_generated": True,
                        "file_path": file_path,
                        "metadata": result.metadata
                    })
                except Exception as e:
                    logger.error(f"Failed to save batch image {i}: {str(e)}")
                    result_data.update({
                        "success": False,
                        "error": f"Image generated but failed to save: {str(e)}",
                        "suggestions": ["Try generating this image individually"]
                    })
            else:
                result_data.update({
                    "error": result.error,
                    "suggestions": result.suggestions
                })
            
            results_summary["results"].append(result_data)
        
        return json.dumps(results_summary, indent=2)
        
    except Exception as e:
        logger.error(f"Batch generation failed: {str(e)}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


@mcp.tool()
async def get_prompt_suggestions(
    content_type: str,
    current_prompt: Optional[str] = None
) -> str:
    """Get suggestions for improving image generation prompts.
    
    Args:
        content_type: Type of content (youtube_thumbnail, blog_header, blog_featured, social_media, general)
        current_prompt: Current prompt to analyze and improve (optional)
    """
    try:
        content_type_enum = ContentType(content_type)
        
        optimizer = PromptOptimizer()
        
        # Get general suggestions for content type
        suggestions = optimizer.get_prompt_suggestions(content_type_enum)
        
        result = {
            "content_type": content_type_enum.value,
            "suggestions": suggestions
        }
        
        # Analyze current prompt if provided
        if current_prompt:
            analysis = optimizer.analyze_prompt_quality(current_prompt)
            result["prompt_analysis"] = analysis
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Prompt suggestions failed: {str(e)}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


@mcp.resource("gpt://temp-files/info")
def get_temp_files_info() -> str:
    """Get information about temporary files storage."""
    info = temp_image_manager.get_temp_dir_info()
    return json.dumps(info, indent=2)


@mcp.tool()
async def cleanup_temp_files() -> str:
    """Clean up old temporary files."""
    try:
        cleaned_count = temp_image_manager.cleanup_old_files()
        return json.dumps({
            "success": True,
            "files_cleaned": cleaned_count,
            "message": f"Successfully cleaned up {cleaned_count} old image files"
        }, indent=2)
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")
        return json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2)


def main():
    """Main entry point for the FastMCP server."""
    logger.info(f"Starting {settings.server_name} v{settings.server_version}")
    
    # Validate configuration
    if not settings.openai_api_key:
        logger.error("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        return
    
    # Clean up old temporary files on startup
    try:
        cleaned_count = temp_image_manager.cleanup_old_files()
        if cleaned_count > 0:
            logger.info(f"Cleaned up {cleaned_count} old temporary files on startup")
    except Exception as e:
        logger.warning(f"Failed to clean up temporary files on startup: {str(e)}")
    
    # Run the FastMCP server
    mcp.run()


if __name__ == "__main__":
    main()