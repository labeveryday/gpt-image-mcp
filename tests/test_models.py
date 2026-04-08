"""Tests for simplified Pydantic models."""


from gpt_image_mcp.models import GenerateImageRequest


def test_generate_image_request_basic():
    """Test basic GenerateImageRequest creation."""
    request = GenerateImageRequest(prompt="Test image for demo")

    assert request.prompt == "Test image for demo"
    assert request.content_type == "general"


def test_generate_image_request_youtube():
    """Test YouTube-specific request."""
    request = GenerateImageRequest(
        prompt="YouTube thumbnail",
        content_type="youtube_thumbnail",
        style="professional",
        emotional_tone="excited",
        include_text_overlay=True,
        text_overlay="Amazing Video!"
    )

    assert request.content_type == "youtube_thumbnail"
    assert request.style == "professional"
    assert request.emotional_tone == "excited"
    assert request.include_text_overlay is True
    assert request.text_overlay == "Amazing Video!"


def test_brand_colors():
    """Test brand colors field."""
    request = GenerateImageRequest(
        prompt="Test brand colors image",
        brand_colors=["#FF0000", "#00FF00", "#0000FF"]
    )

    assert len(request.brand_colors) == 3
    assert "#FF0000" in request.brand_colors


def test_optional_fields():
    """Test that all optional fields work correctly."""
    request = GenerateImageRequest(
        prompt="Test social media image",
        content_type="social_media",
        size="1024x1024",
        quality="high",
        style="minimalist",
        emotional_tone="friendly",
        topic="test topic",
        target_audience="developers"
    )

    assert request.topic == "test topic"
    assert request.target_audience == "developers"
    assert request.size == "1024x1024"
