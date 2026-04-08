"""Core image generation service using OpenAI gpt-image-1."""

import asyncio
import base64
import io
import logging

import aiohttp
from openai import AsyncOpenAI
from PIL import Image

from .config import settings
from .models import (
    BatchGenerationRequest,
    BatchGenerationResponse,
    ContentType,
    GenerateImageRequest,
    ImageGenerationResponse,
    OptimizeForPlatformRequest,
)
from .prompt_optimizer import PromptOptimizer
from .utils import validate_image_data

logger = logging.getLogger(__name__)


class ImageGenerationService:
    """Service for generating images using OpenAI image models."""

    def __init__(self):
        """Initialize the image generation service."""
        self.client = AsyncOpenAI(**settings.openai_client_config)
        self.prompt_optimizer = PromptOptimizer()
        self._session: aiohttp.ClientSession | None = None

    async def __aenter__(self):
        """Async context manager entry."""
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._session:
            await self._session.close()

    async def generate_image(self, request: GenerateImageRequest) -> ImageGenerationResponse:
        """Generate a single image based on the request."""
        try:
            # Optimize the prompt based on content type and requirements
            optimized_prompt = await self.prompt_optimizer.optimize_prompt(request)
            logger.info(f"Optimized prompt: {optimized_prompt[:100]}...")

            # Check if reference image is provided
            if request.reference_image and request.reference_image.strip():
                logger.info(f"Using reference image generation (image data length: {len(request.reference_image)})")
                response = await self._generate_with_reference_image(request, optimized_prompt)
            elif request.content_type == ContentType.YOUTUBE_THUMBNAIL:
                logger.info("Using YouTube thumbnail generation")
                response = await self._generate_youtube_thumbnail(request, optimized_prompt)
            else:
                logger.info("Using generic image generation")
                response = await self._generate_generic_image(request, optimized_prompt)

            return response

        except Exception as e:
            logger.error(f"Image generation failed: {str(e)}")
            return ImageGenerationResponse(
                success=False,
                error=str(e),
                suggestions=[
                    "Try simplifying the prompt",
                    "Check if all required parameters are provided",
                    "Ensure the content type is appropriate for the request"
                ]
            )

    async def _generate_youtube_thumbnail(
        self, request: GenerateImageRequest, optimized_prompt: str
    ) -> ImageGenerationResponse:
        """Generate a YouTube thumbnail optimized for engagement."""
        try:
            # Add text overlay if requested
            if request.include_text_overlay and request.text_overlay:
                optimized_prompt += f"\n\nInclude the text '{request.text_overlay}' prominently in the image with high contrast and readability."

            # Add brand colors if provided
            if request.brand_colors:
                color_text = ", ".join(request.brand_colors)
                optimized_prompt += f"\n\nUse these brand colors prominently: {color_text}"

            # Use Image API directly for YouTube thumbnails
            size = request.size or "1792x1024"

            # Handle quality parameter based on model
            if settings.image_model == "gpt-image-1":
                # gpt-image-1 doesn't use quality/detail parameters
                quality_param = {}
            elif settings.image_model == "dall-e-3":
                quality = "hd" if request.quality in ["high", "auto"] else "standard"
                quality_param = {"quality": quality}
            else:
                quality_param = {"quality": "standard"}

            # Build parameters dynamically based on model
            params = {
                "model": settings.image_model,
                "prompt": optimized_prompt,
                "n": 1,
                **quality_param
            }

            # Add parameters based on model support
            if settings.image_model in ["dall-e-2", "dall-e-3"]:
                params["size"] = size
                params["response_format"] = "b64_json"

            result = await self.client.images.generate(**params)

            image_data = result.data[0].b64_json

            # Post-process for YouTube optimization
            processed_image = await self._post_process_youtube_thumbnail(
                image_data, request
            )

            return ImageGenerationResponse(
                success=True,
                image_data=processed_image,
                revised_prompt=getattr(result.data[0], 'revised_prompt', optimized_prompt),
                metadata={
                    "content_type": request.content_type,
                    "size": size,
                    "quality": request.quality,
                    "model_used": settings.image_model,
                    "optimized_for": "youtube",
                    "processing_applied": ["contrast_enhancement", "readability_optimization"]
                }
            )

        except Exception as e:
            logger.error(f"YouTube thumbnail generation failed: {str(e)}")
            # Try fallback method
            return await self._generate_with_fallback(request, optimized_prompt)

    async def _generate_generic_image(
        self, request: GenerateImageRequest, optimized_prompt: str
    ) -> ImageGenerationResponse:
        """Generate a generic image using the Image API."""
        try:
            # Use Image API for direct generation
            size = request.size or "1024x1024"

            # Handle quality parameter based on model
            if settings.image_model == "gpt-image-1":
                # gpt-image-1 doesn't use quality/detail parameters
                quality_param = {}
            elif settings.image_model == "dall-e-3":
                quality = "hd" if request.quality in ["high", "auto"] else "standard"
                quality_param = {"quality": quality}
            else:
                # dall-e-2 only supports standard quality
                quality_param = {"quality": "standard"}

            # Build parameters dynamically based on model
            params = {
                "model": settings.image_model,
                "prompt": optimized_prompt,
                "n": 1,
                **quality_param
            }

            # Add parameters based on model support
            if settings.image_model in ["dall-e-2", "dall-e-3"]:
                params["size"] = size
                params["response_format"] = "b64_json"

            result = await self.client.images.generate(**params)

            image_data = result.data[0].b64_json

            # Post-process based on content type
            if request.content_type in [ContentType.BLOG_HEADER, ContentType.BLOG_FEATURED]:
                processed_image = await self._post_process_blog_image(image_data, request)
            else:
                processed_image = image_data

            return ImageGenerationResponse(
                success=True,
                image_data=processed_image,
                revised_prompt=getattr(result.data[0], 'revised_prompt', optimized_prompt),
                metadata={
                    "content_type": request.content_type,
                    "size": request.size,
                    "quality": request.quality,
                    "model_used": settings.image_model
                }
            )

        except Exception as e:
            logger.error(f"Generic image generation failed: {str(e)}")
            return await self._generate_with_fallback(request, optimized_prompt)

    async def _generate_with_reference_image(
        self, request: GenerateImageRequest, optimized_prompt: str
    ) -> ImageGenerationResponse:
        """Generate image using a reference image for guidance using Image API edit endpoint."""
        try:
            # Create specialized prompt for reference-based generation
            if request.content_type == ContentType.YOUTUBE_THUMBNAIL:
                reference_prompt = self._create_reference_thumbnail_prompt(request, optimized_prompt)
            else:
                reference_prompt = self._create_reference_prompt(request, optimized_prompt)

            # Convert base64 back to BytesIO for Image API
            import base64
            import io
            reference_bytes = base64.b64decode(request.reference_image)
            reference_file = io.BytesIO(reference_bytes)

            # Use Image API edit endpoint for reference-based generation
            params = {
                "model": settings.image_model,  # Use configured image model
                "image": reference_file,
                "prompt": reference_prompt,
            }

            # Add size if specified (Image API edit only supports specific sizes)
            if request.content_type == ContentType.YOUTUBE_THUMBNAIL:
                params["size"] = "1536x1024"  # Closest supported size for YouTube
            elif request.size:
                # Map unsupported sizes to supported ones
                size_mapping = {
                    "1792x1024": "1536x1024",
                    "1920x1080": "1536x1024"
                }
                params["size"] = size_mapping.get(request.size, request.size)

            # Add quality if supported by the model
            if request.quality and request.quality != "auto":
                if settings.image_model == "gpt-image-1":
                    # Map quality values for gpt-image-1 (supports low, medium, high, auto)
                    quality_mapping = {
                        "standard": "medium",
                        "low": "low",
                        "medium": "medium",
                        "high": "high"
                    }
                    params["quality"] = quality_mapping.get(request.quality, "medium")

            result = await self.client.images.edit(**params)

            image_data = result.data[0].b64_json
            revised_prompt = getattr(result.data[0], 'revised_prompt', reference_prompt)

            # Post-process if YouTube thumbnail
            if request.content_type == ContentType.YOUTUBE_THUMBNAIL:
                processed_image = await self._post_process_youtube_thumbnail(image_data, request)
            else:
                processed_image = image_data

            return ImageGenerationResponse(
                success=True,
                image_data=processed_image,
                revised_prompt=revised_prompt,
                metadata={
                    "content_type": request.content_type,
                    "model_used": settings.image_model,
                    "reference_image_used": True,
                    "generation_method": "image_api_edit"
                }
            )

        except Exception as e:
            logger.error(f"Reference image generation failed: {str(e)}")
            # Fallback to regular generation without reference
            logger.info("Falling back to generation without reference image")
            if request.content_type == ContentType.YOUTUBE_THUMBNAIL:
                return await self._generate_youtube_thumbnail(request, optimized_prompt)
            else:
                return await self._generate_generic_image(request, optimized_prompt)

    async def _generate_with_fallback(
        self, request: GenerateImageRequest, optimized_prompt: str
    ) -> ImageGenerationResponse:
        """Generate image using fallback model."""
        try:
            logger.info(f"Using fallback model for image generation: {settings.fallback_model}")

            # Handle quality parameter for fallback model
            if settings.fallback_model == "gpt-image-1":
                quality_param = {}  # gpt-image-1 doesn't use quality parameters
            elif settings.fallback_model == "dall-e-3":
                quality_param = {"quality": "standard"}
            else:
                quality_param = {"quality": "standard"}

            params = {
                "model": settings.fallback_model,
                "prompt": optimized_prompt,
                "n": 1,
                **quality_param
            }

            # Add parameters based on model support
            if settings.fallback_model in ["dall-e-2", "dall-e-3"]:
                params["size"] = request.size or "1024x1024"
                params["response_format"] = "b64_json"

            result = await self.client.images.generate(**params)

            return ImageGenerationResponse(
                success=True,
                image_data=result.data[0].b64_json,
                revised_prompt=optimized_prompt,
                metadata={
                    "content_type": request.content_type,
                    "model_used": settings.fallback_model,
                    "fallback_used": True
                }
            )

        except Exception as e:
            logger.error(f"Fallback generation failed: {str(e)}")
            return ImageGenerationResponse(
                success=False,
                error=f"All generation methods failed: {str(e)}",
                suggestions=[
                    "Check your OpenAI API key and credits",
                    "Simplify the prompt",
                    "Try again later"
                ]
            )

    async def _post_process_youtube_thumbnail(
        self, image_data: str, request: GenerateImageRequest
    ) -> str:
        """Post-process image for YouTube thumbnail optimization."""
        try:
            # Decode image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))

            # Ensure correct size for YouTube - use 1280x720 for smaller file size
            target_size = (1280, 720)
            if image.size != target_size:
                image = image.resize(target_size, Image.Resampling.LANCZOS)

            # Enhance contrast for better visibility
            from PIL import ImageEnhance
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.2)  # Increase contrast by 20%

            # Convert back to base64 with PNG compression for smaller file size
            output_buffer = io.BytesIO()
            # Use PNG with maximum compression for smallest file size
            image.save(output_buffer, format='PNG', optimize=True, compress_level=9)

            # If still too large, try additional size reduction
            if len(output_buffer.getvalue()) > 2000000:  # If over 2MB
                # Try smaller resolution
                smaller_image = image.resize((1024, 576), Image.Resampling.LANCZOS)
                output_buffer = io.BytesIO()
                smaller_image.save(output_buffer, format='PNG', optimize=True, compress_level=9)

            processed_data = base64.b64encode(output_buffer.getvalue()).decode()

            return processed_data

        except Exception as e:
            logger.warning(f"Post-processing failed, returning original: {str(e)}")
            return image_data

    async def _post_process_blog_image(
        self, image_data: str, request: GenerateImageRequest
    ) -> str:
        """Post-process image for blog optimization."""
        try:
            # Decode image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))

            # Optimize for web (compress if needed)
            if len(image_bytes) > settings.max_image_size_mb * 1024 * 1024:
                # Compress image
                output_buffer = io.BytesIO()
                image.save(output_buffer, format='JPEG', quality=85, optimize=True)
                processed_data = base64.b64encode(output_buffer.getvalue()).decode()
                return processed_data

            return image_data

        except Exception as e:
            logger.warning(f"Blog post-processing failed, returning original: {str(e)}")
            return image_data

    async def optimize_for_platform(self, request: OptimizeForPlatformRequest) -> ImageGenerationResponse:
        """Optimize an existing image for a specific platform."""
        try:
            # Validate input image
            if not validate_image_data(request.image_data):
                raise ValueError("Invalid image data provided")

            # Use the configured model with the original image to create an optimized version
            optimization_prompt = self._create_optimization_prompt(request)

            tools = [
                {
                    "type": "image_generation",
                    "input_fidelity": "high"
                }
            ]

            # Determine optimal size for platform (using OpenAI supported sizes)
            platform_sizes = {
                "youtube": "1792x1024",
                "instagram": "1024x1024",
                "twitter": "1792x1024",
                "facebook": "1792x1024",
                "blog": "1792x1024"
            }

            tools[0]["size"] = platform_sizes.get(request.target_platform, "1024x1024")

            response = await self.client.responses.create(
                model=settings.default_model,
                input=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": optimization_prompt},
                            {
                                "type": "input_image",
                                "image_url": f"data:image/jpeg;base64,{request.image_data}"
                            }
                        ]
                    }
                ],
                tools=tools
            )

            # Extract optimized image
            image_generation_calls = [
                output for output in response.output
                if output.type == "image_generation_call"
            ]

            if not image_generation_calls:
                raise ValueError("No optimized image was generated")

            return ImageGenerationResponse(
                success=True,
                image_data=image_generation_calls[0].result,
                revised_prompt=optimization_prompt,
                metadata={
                    "optimized_for": request.target_platform,
                    "optimization_focus": request.optimization_focus,
                    "original_provided": True
                }
            )

        except Exception as e:
            logger.error(f"Platform optimization failed: {str(e)}")
            return ImageGenerationResponse(
                success=False,
                error=str(e),
                suggestions=[
                    "Ensure the input image is valid",
                    "Try a different target platform",
                    "Check the optimization focus parameters"
                ]
            )

    def _create_optimization_prompt(self, request: OptimizeForPlatformRequest) -> str:
        """Create optimization prompt for platform-specific requirements."""
        platform_requirements = {
            "youtube": "Optimize this image as a YouTube thumbnail. Enhance contrast, make text more readable, ensure faces are prominent, and create visual elements that encourage clicks. The thumbnail should be eye-catching and stand out in YouTube's browsing interface.",
            "instagram": "Optimize this image for Instagram. Ensure it looks great in a square format, enhance colors for mobile viewing, and make it visually appealing for social media engagement.",
            "twitter": "Optimize this image for Twitter posts. Ensure good readability at small sizes, maintain aspect ratio for timeline display, and enhance visual impact for social sharing.",
            "facebook": "Optimize this image for Facebook posts. Enhance for newsfeed visibility, ensure good readability across devices, and optimize for social media engagement.",
            "blog": "Optimize this image for blog content. Ensure professional appearance, good readability, and visual appeal that complements written content."
        }

        base_prompt = platform_requirements.get(
            request.target_platform,
            f"Optimize this image for {request.target_platform} platform."
        )

        if request.content_type:
            base_prompt += f" The content is {request.content_type} related."

        if request.optimization_focus:
            focus_areas = ", ".join(request.optimization_focus)
            base_prompt += f" Focus particularly on: {focus_areas}."

        return base_prompt

    async def generate_batch(self, request: BatchGenerationRequest) -> BatchGenerationResponse:
        """Generate multiple images concurrently."""
        start_time = asyncio.get_event_loop().time()

        # Limit concurrent requests
        semaphore = asyncio.Semaphore(
            min(request.max_concurrent, settings.max_concurrent_generations)
        )

        async def generate_single(single_request: GenerateImageRequest):
            async with semaphore:
                return await self.generate_image(single_request)

        # Execute all requests concurrently
        results = await asyncio.gather(
            *[generate_single(req) for req in request.requests],
            return_exceptions=True
        )

        # Process results and handle exceptions
        processed_results = []
        successful = 0
        failed = 0

        for result in results:
            if isinstance(result, Exception):
                processed_results.append(
                    ImageGenerationResponse(
                        success=False,
                        error=str(result)
                    )
                )
                failed += 1
            elif result.success:
                processed_results.append(result)
                successful += 1
            else:
                processed_results.append(result)
                failed += 1

        processing_time = asyncio.get_event_loop().time() - start_time

        return BatchGenerationResponse(
            results=processed_results,
            total_successful=successful,
            total_failed=failed,
            processing_time=processing_time
        )

    def _create_reference_thumbnail_prompt(self, request: GenerateImageRequest, base_prompt: str) -> str:
        """Create optimized prompt for reference-based YouTube thumbnail generation."""

        # Check for creative mode or flexible layout
        if request.creative_mode or request.layout_freedom in ["flexible", "experimental"]:
            return self._create_creative_reference_prompt(request, base_prompt)

        # Standard/rigid layout mode (original behavior)
        style_prompt = f"""Create a professional YouTube thumbnail using the person from the reference image.

Composition:
- Position the person on the RIGHT side of the thumbnail (40% of image width)
- Person should have a confident, engaging expression looking at the camera
- Left side: Large, bold WHITE text on dark background
- Use a RED rectangular banner for secondary text
- Dark professional background (black/dark gray)
- High contrast design for maximum visibility

Text Layout:
- Main headline: "{request.text_overlay or 'MAIN TEXT'}" in large white font
- Secondary text in red banner if provided
- Ensure text is highly readable and prominent

Style Requirements:
- Professional headshot style for the person
- Dark clothing to match the aesthetic
- High contrast colors throughout
- YouTube thumbnail optimized (1792x1024)
- Authoritative and trustworthy appearance

Additional Context: {base_prompt}"""

        # Add brand colors if specified
        if request.brand_colors:
            color_text = ", ".join(request.brand_colors)
            style_prompt += f"\n\nUse these brand colors where appropriate: {color_text}"

        # Add topic-specific elements if provided
        if request.topic:
            style_prompt += f"\n\nThe thumbnail is about: {request.topic}"

        return style_prompt

    def _create_creative_reference_prompt(self, request: GenerateImageRequest, base_prompt: str) -> str:
        """Create flexible, creative prompt for reference-based generation."""

        # Base creative prompt
        creative_prompt = f"""Create a compelling YouTube thumbnail using the person from the reference image.

Creative Direction:
- Incorporate the person naturally and creatively into the composition
- Feel free to experiment with positioning, angles, and layouts
- Maintain high visual impact and thumbnail appeal
- Preserve the person's facial features and appearance from reference
- {base_prompt}

Creative Parameters:"""

        # Add composition style if specified
        if request.composition_style:
            if request.composition_style == "centered":
                creative_prompt += "\n- Center the person prominently in the composition"
            elif request.composition_style == "dynamic":
                creative_prompt += "\n- Use dynamic, energetic positioning and angles"
            elif request.composition_style == "creative":
                creative_prompt += "\n- Experiment with creative, artistic composition techniques"
            else:
                creative_prompt += f"\n- Position the person on the {request.composition_style} side"

        # Layout freedom level
        if request.layout_freedom == "experimental":
            creative_prompt += "\n- Complete creative freedom with layout, colors, and styling"
            creative_prompt += "\n- Experiment with unconventional thumbnail designs"
        elif request.layout_freedom == "flexible":
            creative_prompt += "\n- Some creative flexibility while maintaining thumbnail best practices"

        # Add text handling
        if request.include_text_overlay and request.text_overlay:
            if request.layout_freedom == "experimental":
                creative_prompt += f"\n- Creatively integrate the text '{request.text_overlay}' in an impactful way"
            else:
                creative_prompt += f"\n- Include the text '{request.text_overlay}' prominently with high contrast"

        # Add brand colors if specified (but more flexibly)
        if request.brand_colors:
            color_text = ", ".join(request.brand_colors)
            creative_prompt += f"\n- Incorporate these brand colors creatively: {color_text}"

        # Add topic context
        if request.topic:
            creative_prompt += f"\n- Topic: {request.topic}"

        # Add style preferences
        if request.style:
            creative_prompt += f"\n- Overall style: {request.style}"

        if request.emotional_tone:
            creative_prompt += f"\n- Emotional tone: {request.emotional_tone}"

        return creative_prompt

    def _create_reference_prompt(self, request: GenerateImageRequest, base_prompt: str) -> str:
        """Create prompt for reference-based image generation (non-thumbnail)."""
        reference_prompt = f"""Create an image incorporating the person/subject from the reference image.

Instructions:
- Preserve the key features and appearance of the person/subject from the reference
- Use high input fidelity to maintain facial features and important details
- {base_prompt}
        """

        # Add specific positioning if YouTube thumbnail
        if request.content_type == ContentType.YOUTUBE_THUMBNAIL:
            reference_prompt += "\n- Position the person prominently in the composition"

        # Add text overlay instructions
        if request.include_text_overlay and request.text_overlay:
            reference_prompt += f"\n- Include the text '{request.text_overlay}' prominently with high contrast"

        # Add style preferences
        if request.style:
            reference_prompt += f"\n- Style: {request.style}"

        if request.emotional_tone:
            reference_prompt += f"\n- Emotional tone: {request.emotional_tone}"

        return reference_prompt
