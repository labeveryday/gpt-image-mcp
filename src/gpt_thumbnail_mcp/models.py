"""Simplified Pydantic models for image generation requests and responses."""

from typing import Any, Dict, List, Optional
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
    size: Optional[str] = None
    quality: str = "auto"
    style: Optional[str] = None
    emotional_tone: Optional[str] = None
    include_text_overlay: bool = False
    text_overlay: Optional[str] = None
    brand_colors: Optional[List[str]] = None
    topic: Optional[str] = None
    target_audience: Optional[str] = None


class OptimizeForPlatformRequest(BaseModel):
    """Request to optimize an image for a platform."""
    
    image_data: str
    target_platform: str
    content_type: Optional[str] = None
    optimization_focus: Optional[List[str]] = None


class ImageAnalysisRequest(BaseModel):
    """Request to analyze an image."""
    
    image_data: str
    platform: str = "youtube"
    content_category: Optional[str] = None


class ImageGenerationResponse(BaseModel):
    """Response from image generation."""
    
    success: bool
    image_data: Optional[str] = None
    revised_prompt: Optional[str] = None
    metadata: Dict[str, Any] = {}
    error: Optional[str] = None
    suggestions: Optional[List[str]] = None


class ImageAnalysisResponse(BaseModel):
    """Response from image analysis."""
    
    success: bool
    effectiveness_score: Optional[float] = None
    analysis: Optional[Dict[str, Any]] = None
    suggestions: Optional[List[str]] = None
    error: Optional[str] = None


class BatchGenerationRequest(BaseModel):
    """Request for batch image generation."""
    
    requests: List[GenerateImageRequest]
    max_concurrent: int = 3


class BatchGenerationResponse(BaseModel):
    """Response from batch image generation."""
    
    results: List[ImageGenerationResponse]
    total_successful: int
    total_failed: int
    processing_time: float