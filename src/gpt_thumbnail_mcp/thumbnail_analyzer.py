"""Thumbnail analysis service for evaluating image effectiveness."""

import logging
from typing import Dict, List, Optional

from openai import AsyncOpenAI

from .config import settings
from .models import ImageAnalysisRequest, ImageAnalysisResponse
from .utils import decode_image, get_image_info

logger = logging.getLogger(__name__)


class ThumbnailAnalyzer:
    """Service for analyzing thumbnail effectiveness."""

    def __init__(self):
        """Initialize the thumbnail analyzer."""
        self.client = AsyncOpenAI(**settings.openai_client_config)

    async def analyze_image(self, request: ImageAnalysisRequest) -> ImageAnalysisResponse:
        """Analyze a thumbnail image and provide effectiveness scoring and suggestions."""
        try:
            # First, validate the image
            if not self._validate_image(request.image_data):
                return ImageAnalysisResponse(
                    success=False,
                    error="Invalid image data provided"
                )

            # Get basic image information
            image_info = get_image_info(request.image_data)
            if not image_info:
                return ImageAnalysisResponse(
                    success=False,
                    error="Unable to process image data"
                )

            # Perform AI-powered analysis
            analysis_result = await self._perform_ai_analysis(request, image_info)
            
            # Calculate effectiveness score
            effectiveness_score = self._calculate_effectiveness_score(
                analysis_result, 
                request.platform, 
                image_info
            )

            # Generate improvement suggestions
            suggestions = self._generate_suggestions(
                analysis_result, 
                request.platform, 
                image_info
            )

            return ImageAnalysisResponse(
                success=True,
                effectiveness_score=effectiveness_score,
                analysis=analysis_result,
                suggestions=suggestions
            )

        except Exception as e:
            logger.error(f"Thumbnail analysis failed: {str(e)}")
            return ImageAnalysisResponse(
                success=False,
                error=str(e)
            )

    def _validate_image(self, image_data: str) -> bool:
        """Validate the provided image data."""
        try:
            image = decode_image(image_data)
            return image is not None
        except Exception:
            return False

    async def _perform_ai_analysis(self, request: ImageAnalysisRequest, image_info: Dict) -> Dict:
        """Perform AI-powered analysis of the thumbnail."""
        try:
            # Create analysis prompt based on platform
            analysis_prompt = self._create_analysis_prompt(request.platform, request.content_category)

            # Use GPT-4o for image analysis
            response = await self.client.chat.completions.create(
                model=settings.analysis_model,
                messages=[
                    {
                        "role": "system",
                        "content": analysis_prompt
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Analyze this {request.platform or 'thumbnail'} image. Provide detailed feedback on its effectiveness."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{request.image_data}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.3
            )

            # Parse the analysis response
            analysis_text = response.choices[0].message.content
            
            # Structure the analysis results
            analysis_result = {
                "ai_analysis": analysis_text,
                "technical_specs": image_info,
                "platform": request.platform or "general",
                "content_category": request.content_category,
                "dimension_analysis": self._analyze_dimensions(image_info, request.platform),
                "quality_assessment": self._assess_technical_quality(image_info)
            }

            return analysis_result

        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            return {
                "error": f"AI analysis failed: {str(e)}",
                "technical_specs": image_info,
                "platform": request.platform or "general"
            }

    def _create_analysis_prompt(self, platform: Optional[str], content_category: Optional[str]) -> str:
        """Create an analysis prompt based on platform and content category."""
        base_prompt = """You are an expert in visual design and thumbnail optimization. 
        Analyze the provided image and evaluate its effectiveness as a thumbnail.

        Please evaluate the following aspects:
        1. Visual Impact: How eye-catching and attention-grabbing is the image?
        2. Clarity: How clear and easy to understand is the main subject?
        3. Composition: How well is the image composed (rule of thirds, balance, etc.)?
        4. Color Usage: How effective is the color scheme and contrast?
        5. Text Readability: If there's text, how readable is it?
        6. Emotional Appeal: Does the image evoke the intended emotional response?
        7. Brand Consistency: Does it maintain consistent visual branding?
        8. Platform Optimization: How well is it optimized for the target platform?

        Provide specific, actionable feedback for each aspect."""

        # Add platform-specific analysis requirements
        if platform == "youtube":
            base_prompt += """

            For YouTube thumbnails, specifically evaluate:
            - Adherence to the 0.3-second rule (instantly understandable)
            - Face visibility and expression quality
            - Contrast and visibility at small sizes
            - Clickthrough potential and engagement factors
            - Mobile viewing optimization"""

        elif platform == "instagram":
            base_prompt += """

            For Instagram posts, specifically evaluate:
            - Square format optimization
            - Mobile-first design approach
            - Visual storytelling effectiveness
            - Feed integration and aesthetic consistency"""

        elif platform == "blog":
            base_prompt += """

            For blog images, specifically evaluate:
            - Professional appearance and quality
            - Content relevance and context
            - SEO and accessibility considerations
            - Web optimization and loading performance"""

        # Add content category considerations
        if content_category:
            base_prompt += f"""

            Content Category: {content_category}
            Consider how well the image serves this specific content category and its typical audience expectations."""

        return base_prompt

    def _calculate_effectiveness_score(self, analysis: Dict, platform: Optional[str], image_info: Dict) -> float:
        """Calculate an overall effectiveness score from 0-10."""
        try:
            base_score = 5.0  # Start with middle score
            
            # Technical quality factors
            if image_info.get("width", 0) >= 1000 and image_info.get("height", 0) >= 500:
                base_score += 0.5  # Good resolution
            
            if image_info.get("size_mb", 0) < 2.0:
                base_score += 0.3  # Reasonable file size
            
            # Platform-specific scoring
            if platform == "youtube":
                # Check for YouTube optimal dimensions
                width = image_info.get("width", 0)
                height = image_info.get("height", 0)
                aspect_ratio = width / height if height > 0 else 0
                
                if 1.7 <= aspect_ratio <= 1.8:  # Close to 16:9
                    base_score += 0.7
                elif width == 1920 and height == 1080:
                    base_score += 1.0  # Perfect YouTube dimensions
            
            # AI analysis influence (parse keywords from analysis)
            ai_analysis = analysis.get("ai_analysis", "").lower()
            
            positive_indicators = [
                "eye-catching", "clear", "good contrast", "effective", "engaging",
                "well-composed", "professional", "vibrant", "readable"
            ]
            
            negative_indicators = [
                "cluttered", "unclear", "poor contrast", "blurry", "confusing",
                "unprofessional", "difficult to read", "low quality"
            ]
            
            for indicator in positive_indicators:
                if indicator in ai_analysis:
                    base_score += 0.2
            
            for indicator in negative_indicators:
                if indicator in ai_analysis:
                    base_score -= 0.3
            
            # Clamp score between 0 and 10
            return max(0.0, min(10.0, base_score))
            
        except Exception as e:
            logger.warning(f"Score calculation failed: {str(e)}")
            return 5.0  # Return neutral score on error

    def _generate_suggestions(self, analysis: Dict, platform: Optional[str], image_info: Dict) -> List[str]:
        """Generate improvement suggestions based on analysis."""
        suggestions = []
        
        try:
            # Technical suggestions
            if image_info.get("width", 0) < 1000:
                suggestions.append("Consider using a higher resolution image for better clarity")
            
            if image_info.get("size_mb", 0) > 2.0:
                suggestions.append("Optimize image file size for faster loading")
            
            # Platform-specific suggestions
            if platform == "youtube":
                width = image_info.get("width", 0)
                height = image_info.get("height", 0)
                
                if width != 1920 or height != 1080:
                    suggestions.append("Use 1920x1080 pixels for optimal YouTube thumbnail display")
                
                suggestions.extend([
                    "Ensure faces are clearly visible and expressive",
                    "Use high contrast colors for better visibility",
                    "Add compelling text overlay if appropriate",
                    "Test readability at small thumbnail sizes",
                    "Consider emotional impact and click-through potential"
                ])
            
            elif platform == "instagram":
                aspect_ratio = image_info.get("aspect_ratio", 1)
                if abs(aspect_ratio - 1.0) > 0.1:
                    suggestions.append("Consider using square aspect ratio (1:1) for Instagram posts")
                
                suggestions.extend([
                    "Optimize for mobile viewing experience",
                    "Ensure colors are vibrant and engaging",
                    "Consider how the image fits with your feed aesthetic"
                ])
            
            elif platform == "blog":
                suggestions.extend([
                    "Ensure the image clearly relates to your content",
                    "Maintain professional image quality",
                    "Consider SEO implications and alt text",
                    "Optimize for web loading speeds"
                ])
            
            # Parse AI analysis for specific suggestions
            ai_analysis = analysis.get("ai_analysis", "")
            if "contrast" in ai_analysis.lower() and ("low" in ai_analysis.lower() or "poor" in ai_analysis.lower()):
                suggestions.append("Increase contrast between elements for better visibility")
            
            if "text" in ai_analysis.lower() and ("small" in ai_analysis.lower() or "difficult" in ai_analysis.lower()):
                suggestions.append("Make text larger and more readable")
            
            if "cluttered" in ai_analysis.lower():
                suggestions.append("Simplify composition and remove unnecessary elements")
            
            # Remove duplicates while preserving order
            seen = set()
            unique_suggestions = []
            for suggestion in suggestions:
                if suggestion not in seen:
                    seen.add(suggestion)
                    unique_suggestions.append(suggestion)
            
            return unique_suggestions[:10]  # Limit to top 10 suggestions
            
        except Exception as e:
            logger.warning(f"Suggestion generation failed: {str(e)}")
            return ["Unable to generate specific suggestions due to analysis error"]

    def _analyze_dimensions(self, image_info: Dict, platform: Optional[str]) -> Dict:
        """Analyze image dimensions for platform compatibility."""
        width = image_info.get("width", 0)
        height = image_info.get("height", 0)
        aspect_ratio = width / height if height > 0 else 0
        
        analysis = {
            "current_dimensions": f"{width}x{height}",
            "aspect_ratio": round(aspect_ratio, 2),
            "platform_optimal": False,
            "recommendations": []
        }
        
        # Platform-specific dimension analysis
        if platform == "youtube":
            analysis["platform_optimal"] = (width == 1920 and height == 1080)
            analysis["target_dimensions"] = "1920x1080"
            analysis["target_aspect_ratio"] = 1.78
            
            if not analysis["platform_optimal"]:
                analysis["recommendations"].append("Resize to 1920x1080 for optimal YouTube display")
        
        elif platform == "instagram":
            analysis["platform_optimal"] = abs(aspect_ratio - 1.0) < 0.1
            analysis["target_dimensions"] = "1080x1080"
            analysis["target_aspect_ratio"] = 1.0
            
            if not analysis["platform_optimal"]:
                analysis["recommendations"].append("Use square format (1:1) for Instagram")
        
        elif platform == "blog":
            # Blog images are flexible, but landscape is often preferred for headers
            analysis["platform_optimal"] = aspect_ratio > 1.2
            analysis["target_dimensions"] = "1536x1024 (for headers)"
            analysis["target_aspect_ratio"] = 1.5
        
        return analysis

    def _assess_technical_quality(self, image_info: Dict) -> Dict:
        """Assess technical quality of the image."""
        assessment = {
            "resolution": "Unknown",
            "file_size": "Unknown",
            "format": image_info.get("format", "Unknown"),
            "quality_rating": "Unknown",
            "recommendations": []
        }
        
        try:
            width = image_info.get("width", 0)
            height = image_info.get("height", 0)
            total_pixels = width * height
            
            # Resolution assessment
            if total_pixels >= 2073600:  # 1920x1080
                assessment["resolution"] = "Excellent"
            elif total_pixels >= 1048576:  # 1024x1024
                assessment["resolution"] = "Good"
            elif total_pixels >= 307200:  # 640x480
                assessment["resolution"] = "Acceptable"
            else:
                assessment["resolution"] = "Poor"
                assessment["recommendations"].append("Use higher resolution image")
            
            # File size assessment
            size_mb = image_info.get("size_mb", 0)
            if size_mb <= 0.5:
                assessment["file_size"] = "Excellent"
            elif size_mb <= 2.0:
                assessment["file_size"] = "Good"
            elif size_mb <= 5.0:
                assessment["file_size"] = "Acceptable"
            else:
                assessment["file_size"] = "Too Large"
                assessment["recommendations"].append("Optimize file size for web use")
            
            # Overall quality rating
            if assessment["resolution"] in ["Excellent", "Good"] and assessment["file_size"] in ["Excellent", "Good"]:
                assessment["quality_rating"] = "High"
            elif assessment["resolution"] != "Poor" and assessment["file_size"] != "Too Large":
                assessment["quality_rating"] = "Medium"
            else:
                assessment["quality_rating"] = "Low"
        
        except Exception as e:
            logger.warning(f"Technical assessment failed: {str(e)}")
            assessment["recommendations"].append("Unable to assess technical quality")
        
        return assessment