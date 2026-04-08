"""Configuration management for the GPT Image MCP server."""

from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra='ignore'  # Ignore extra fields from environment
    )

    # OpenAI Configuration
    openai_api_key: str = Field(default="", description="OpenAI API key")
    openai_base_url: str | None = Field(
        default=None,
        description="OpenAI API base URL (for custom endpoints)"
    )
    openai_organization: str | None = Field(
        default=None,
        description="OpenAI organization ID"
    )

    # Model Configuration
    default_model: str = Field(
        default="gpt-image-1",
        description="Primary model for image generation - OpenAI's best image model"
    )
    image_model: str = Field(
        default="gpt-image-1",
        description="Model for direct image generation via Image API"
    )
    fallback_model: str = Field(
        default="dall-e-3",
        description="Fallback model if primary models fail"
    )

    # Generation Settings
    max_retries: int = Field(default=3, description="Maximum retries for failed generations")
    timeout_seconds: int = Field(default=120, description="Request timeout in seconds")
    max_concurrent_generations: int = Field(
        default=5,
        description="Maximum concurrent image generations"
    )

    # Image Settings
    default_quality: str = Field(default="auto", description="Default image quality")
    default_size: str = Field(default="auto", description="Default image size")
    max_image_size_mb: float = Field(default=10.0, description="Maximum image size in MB")

    # YouTube Thumbnail Optimization
    youtube_thumbnail_size: str = Field(
        default="1792x1024",
        description="Standard YouTube thumbnail size (OpenAI API compatible)"
    )
    youtube_best_practices: dict[str, str] = Field(
        default_factory=lambda: {
            "contrast": "high",
            "text_size": "large",
            "face_visibility": "prominent",
            "color_scheme": "vibrant",
            "composition": "rule_of_thirds"
        }
    )

    # Blog Image Settings
    blog_header_sizes: list[str] = Field(
        default_factory=lambda: ["1792x1024", "1024x1024", "1024x1792"]
    )
    blog_featured_size: str = Field(default="1024x1792", description="Blog featured image size")

    # Brand Guidelines
    default_brand_colors: list[str] = Field(
        default_factory=lambda: ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]
    )
    brand_fonts: list[str] = Field(
        default_factory=lambda: ["Arial", "Helvetica", "Open Sans", "Roboto", "Montserrat"]
    )

    # Content Analysis
    enable_content_analysis: bool = Field(
        default=True,
        description="Enable content analysis for optimization suggestions"
    )
    analysis_model: str = Field(
        default="gpt-4o",
        description="Model for content analysis"
    )

    # Performance Settings
    enable_caching: bool = Field(default=True, description="Enable response caching")
    cache_ttl_minutes: int = Field(default=60, description="Cache TTL in minutes")
    enable_compression: bool = Field(default=True, description="Enable image compression")

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    enable_detailed_logging: bool = Field(
        default=False,
        description="Enable detailed request/response logging"
    )

    # Security
    rate_limit_per_minute: int = Field(
        default=30,
        description="Rate limit per minute per client"
    )
    enable_content_filtering: bool = Field(
        default=True,
        description="Enable content filtering for generated images"
    )

    # MCP Server Settings
    server_name: str = Field(
        default="gpt-image-mcp",
        description="MCP server name"
    )
    server_version: str = Field(default="0.1.0", description="MCP server version")

    # Platform-specific templates
    youtube_prompt_template: str = Field(
        default="""Create a compelling YouTube thumbnail for {content_type} content about '{topic}'.
        The image should be eye-catching, follow the {style} style, and convey a {emotional_tone} tone.
        Ensure high contrast, readable text if included, and engaging visual elements that encourage clicks.
        {additional_requirements}""",
        description="Template for YouTube thumbnail prompts"
    )

    blog_prompt_template: str = Field(
        default="""Generate a professional blog {image_type} image for an article about '{topic}'
        targeting {target_audience}. The image should be visually appealing, relevant to the content,
        and suitable for {format} format. Style should be {style} with {emotional_tone} mood.
        {additional_requirements}""",
        description="Template for blog image prompts"
    )

    @property
    def openai_client_config(self) -> dict[str, str]:
        """Get OpenAI client configuration."""
        config = {"api_key": self.openai_api_key}
        if self.openai_base_url:
            config["base_url"] = self.openai_base_url
        if self.openai_organization:
            config["organization"] = self.openai_organization
        return config


# Global settings instance
settings = Settings()
