"""Simplified Pydantic models for image generation requests and responses."""

from typing import Any

from pydantic import BaseModel


# Simple content types
class ContentType:
    YOUTUBE_THUMBNAIL = "youtube_thumbnail"
    BLOG_HEADER = "blog_header"
    BLOG_FEATURED = "blog_featured"
    SOCIAL_MEDIA = "social_media"
    GENERAL = "general"


class GenerateImageRequest(BaseModel):
    """Simple request for image generation."""

    prompt: str
    content_type: str = "general"
    size: str | None = None
    quality: str = "auto"
    style: str | None = None
    emotional_tone: str | None = None
    include_text_overlay: bool = False
    text_overlay: str | None = None
    brand_colors: list[str] | None = None
    topic: str | None = None
    target_audience: str | None = None
    reference_image: str | None = None
    avoid_elements: list[str] | None = None
    emphasis_elements: list[str] | None = None
    creative_mode: bool = False
    composition_style: str | None = None
    layout_freedom: str = "standard"


class OptimizeForPlatformRequest(BaseModel):
    """Request to optimize an image for a platform."""

    image_data: str
    target_platform: str
    content_type: str | None = None
    optimization_focus: list[str] | None = None


class ImageAnalysisRequest(BaseModel):
    """Request to analyze an image."""

    image_data: str
    platform: str = "youtube"
    content_category: str | None = None


class ImageGenerationResponse(BaseModel):
    """Response from image generation."""

    success: bool
    image_data: str | None = None
    revised_prompt: str | None = None
    metadata: dict[str, Any] = {}
    error: str | None = None
    suggestions: list[str] | None = None


class ImageAnalysisResponse(BaseModel):
    """Response from image analysis."""

    success: bool
    effectiveness_score: float | None = None
    analysis: dict[str, Any] | None = None
    suggestions: list[str] | None = None
    error: str | None = None


class BatchGenerationRequest(BaseModel):
    """Request for batch image generation."""

    requests: list[GenerateImageRequest]
    max_concurrent: int = 3


class BatchGenerationResponse(BaseModel):
    """Response from batch image generation."""

    results: list[ImageGenerationResponse]
    total_successful: int
    total_failed: int
    processing_time: float
