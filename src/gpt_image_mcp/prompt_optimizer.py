"""Prompt optimization service for generating effective image generation prompts."""

import logging

from .models import ContentType, GenerateImageRequest

logger = logging.getLogger(__name__)


class PromptOptimizer:
    """Service for optimizing prompts for image generation."""

    def __init__(self):
        """Initialize the prompt optimizer."""
        self.youtube_best_practices = {
            "contrast": "Use high contrast elements and colors",
            "readability": "Ensure any text is large and easily readable",
            "faces": "Include expressive human faces when relevant",
            "emotion": "Convey clear emotional reactions or expressions",
            "composition": "Use rule of thirds and dynamic composition",
            "colors": "Use vibrant, eye-catching colors",
            "clarity": "Avoid clutter and maintain visual clarity"
        }

        self.blog_best_practices = {
            "professionalism": "Maintain a professional and polished appearance",
            "relevance": "Ensure clear relevance to the blog topic",
            "quality": "Use high-quality, crisp imagery",
            "branding": "Incorporate subtle branding elements when appropriate",
            "appeal": "Create visual appeal that complements written content"
        }

    async def optimize_prompt(self, request: GenerateImageRequest) -> str:
        """Optimize the base prompt for better image generation results."""
        try:
            base_prompt = request.prompt.strip()

            # Apply content-type specific optimizations
            if request.content_type == ContentType.YOUTUBE_THUMBNAIL:
                return await self._optimize_for_youtube(base_prompt, request)
            elif request.content_type in [ContentType.BLOG_HEADER, ContentType.BLOG_FEATURED]:
                return await self._optimize_for_blog(base_prompt, request)
            elif request.content_type == ContentType.SOCIAL_MEDIA:
                return await self._optimize_for_social_media(base_prompt, request)
            else:
                return await self._optimize_general(base_prompt, request)

        except Exception as e:
            logger.warning(f"Prompt optimization failed, using original: {str(e)}")
            return request.prompt

    async def _optimize_for_youtube(self, base_prompt: str, request: GenerateImageRequest) -> str:
        """Optimize prompt specifically for YouTube thumbnails."""
        optimized_parts = [base_prompt]

        # Add style-specific enhancements
        if request.style:
            style_enhancements = {
                "professional": "professional, clean, corporate style with polished visuals",
                "casual": "casual, friendly, approachable style with natural lighting",
                "dramatic": "dramatic lighting, bold contrasts, cinematic composition",
                "minimalist": "clean, minimalist design with plenty of white space",
                "educational": "educational, informative style with clear visual hierarchy",
                "entertainment": "fun, energetic, vibrant colors with dynamic composition"
            }
            if request.style and request.style in style_enhancements:
                optimized_parts.append(style_enhancements[request.style])

        # Add emotional tone
        if request.emotional_tone:
            tone_enhancements = {
                "excited": "with excited, enthusiastic expressions and bright, energetic colors",
                "curious": "with curious, intrigued expressions that spark interest",
                "confident": "with confident, authoritative presence and strong composition",
                "surprised": "with surprised, amazed expressions and dynamic elements",
                "serious": "with serious, professional tone and muted color palette",
                "friendly": "with warm, welcoming expressions and inviting colors",
                "dramatic": "with intense, dramatic expressions and bold visual elements"
            }
            if request.emotional_tone and request.emotional_tone in tone_enhancements:
                optimized_parts.append(tone_enhancements[request.emotional_tone])

        # Add YouTube-specific requirements
        youtube_requirements = [
            "designed as a YouTube thumbnail",
            "high contrast for visibility",
            "eye-catching and click-worthy",
            "clear focal point",
            "vibrant colors that stand out",
            "readable at small sizes"
        ]

        # Add face requirements by default
        youtube_requirements.append("expressive human faces prominently featured")

        # Add text overlay requirements
        if request.include_text_overlay and request.text_overlay:
            youtube_requirements.append(f"bold, readable text saying '{request.text_overlay}'")

        # Add brand color requirements
        if request.brand_colors:
            color_list = ", ".join(request.brand_colors)
            youtube_requirements.append(f"incorporating brand colors: {color_list}")

        # Skip emphasis elements (removed in simplified model)

        # Combine all parts
        optimized_parts.extend(youtube_requirements)

        # Add quality specifications
        quality_specs = [
            "ultra-high resolution",
            "professional photography quality",
            "sharp focus",
            "perfect lighting"
        ]
        optimized_parts.extend(quality_specs)

        return ". ".join(optimized_parts) + "."

    async def _optimize_for_blog(self, base_prompt: str, request: GenerateImageRequest) -> str:
        """Optimize prompt for blog images."""
        optimized_parts = [base_prompt]

        # Add blog-specific requirements
        blog_type = "header" if request.content_type == ContentType.BLOG_HEADER else "featured"
        optimized_parts.append(f"designed as a professional blog {blog_type} image")

        # Add topic-specific enhancements
        if request.topic:
            optimized_parts.append(f"clearly related to {request.topic}")

        # Add target audience considerations
        if request.target_audience:
            optimized_parts.append(f"appealing to {request.target_audience}")

        # Add style requirements
        if request.style:
            optimized_parts.append(f"{request.style} style")

        # Add emotional tone
        if request.emotional_tone:
            optimized_parts.append(f"conveying a {request.emotional_tone} mood")

        # Add blog-specific requirements
        blog_requirements = [
            "professional and polished appearance",
            "high-quality photography style",
            "suitable for web publishing",
            "visually appealing composition",
            "clear and focused subject matter"
        ]

        if request.content_type == ContentType.BLOG_HEADER:
            blog_requirements.extend([
                "suitable as a blog header",
                "landscape orientation",
                "space for text overlay if needed"
            ])

        optimized_parts.extend(blog_requirements)

        return ". ".join(optimized_parts) + "."

    async def _optimize_for_social_media(self, base_prompt: str, request: GenerateImageRequest) -> str:
        """Optimize prompt for social media posts."""
        optimized_parts = [base_prompt]

        # Add social media specific requirements
        social_requirements = [
            "designed for social media sharing",
            "eye-catching and engaging",
            "optimized for mobile viewing",
            "vibrant colors",
            "clear composition"
        ]

        # Add emotional engagement
        if request.emotional_tone:
            social_requirements.append(f"{request.emotional_tone} emotional appeal")

        optimized_parts.extend(social_requirements)

        return ". ".join(optimized_parts) + "."

    async def _optimize_general(self, base_prompt: str, request: GenerateImageRequest) -> str:
        """Apply general optimizations to the prompt."""
        optimized_parts = [base_prompt]

        # Add quality specifications
        quality_specs = [
            "high-quality",
            "professional",
            "well-composed"
        ]

        # Add emotional tone if specified
        if request.emotional_tone:
            quality_specs.append(f"{request.emotional_tone} mood")

        # Add style if specified
        if request.style:
            quality_specs.append(f"{request.style} style")

        optimized_parts.extend(quality_specs)

        return ". ".join(optimized_parts) + "."

    def get_prompt_suggestions(self, content_type: ContentType) -> list[str]:
        """Get prompt suggestions for a specific content type."""
        suggestions = {
            ContentType.YOUTUBE_THUMBNAIL: [
                "Include expressive human faces for better engagement",
                "Use high contrast colors and bold typography",
                "Create a clear focal point that draws attention",
                "Add emotional expressions or reactions",
                "Include relevant visual metaphors or symbols",
                "Use the rule of thirds for composition",
                "Ensure the image tells a story at a glance"
            ],
            ContentType.BLOG_HEADER: [
                "Choose images that clearly relate to your content topic",
                "Maintain a professional and polished appearance",
                "Use landscape orientation for better header fit",
                "Include relevant symbols or metaphors",
                "Keep the composition clean and uncluttered",
                "Use colors that complement your brand"
            ],
            ContentType.BLOG_FEATURED: [
                "Select images that capture the essence of your article",
                "Use high-quality, engaging visuals",
                "Ensure the image works well at different sizes",
                "Consider your target audience's preferences",
                "Include visual elements that encourage clicks"
            ],
            ContentType.SOCIAL_MEDIA: [
                "Create visually striking content that stops the scroll",
                "Use bright, engaging colors",
                "Keep important elements large and clear",
                "Consider how the image will look on mobile devices",
                "Include elements that encourage sharing"
            ]
        }

        return suggestions.get(content_type, [
            "Use clear, descriptive language in your prompts",
            "Specify the style and mood you want",
            "Include details about composition and colors",
            "Consider the context where the image will be used"
        ])

    def analyze_prompt_quality(self, prompt: str) -> dict[str, any]:
        """Analyze the quality of a prompt and provide improvement suggestions."""
        analysis = {
            "length": len(prompt),
            "word_count": len(prompt.split()),
            "has_style_descriptor": any(word in prompt.lower() for word in [
                "professional", "casual", "dramatic", "minimalist", "artistic"
            ]),
            "has_emotion_descriptor": any(word in prompt.lower() for word in [
                "excited", "happy", "serious", "confident", "friendly", "dramatic"
            ]),
            "has_composition_terms": any(word in prompt.lower() for word in [
                "centered", "close-up", "wide-angle", "portrait", "landscape", "composition"
            ]),
            "has_quality_terms": any(word in prompt.lower() for word in [
                "high-quality", "professional", "sharp", "clear", "detailed"
            ]),
            "suggestions": []
        }

        # Generate suggestions based on analysis
        if analysis["length"] < 50:
            analysis["suggestions"].append("Consider adding more descriptive details")

        if not analysis["has_style_descriptor"]:
            analysis["suggestions"].append("Add style descriptors (e.g., professional, artistic, modern)")

        if not analysis["has_emotion_descriptor"]:
            analysis["suggestions"].append("Include emotional tone (e.g., friendly, confident, excited)")

        if not analysis["has_composition_terms"]:
            analysis["suggestions"].append("Specify composition preferences (e.g., close-up, wide shot)")

        if not analysis["has_quality_terms"]:
            analysis["suggestions"].append("Add quality specifications (e.g., high-resolution, professional)")

        return analysis
