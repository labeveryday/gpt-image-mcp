"""Tests for ImageGenerationService with mocked OpenAI client."""

import base64
import io
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from PIL import Image

from gpt_image_mcp.image_generator import ImageGenerationService
from gpt_image_mcp.models import ContentType, GenerateImageRequest


def _fake_b64_png(width: int = 64, height: int = 64) -> str:
    img = Image.new("RGB", (width, height), color="blue")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


def _fake_openai_response(b64: str, revised: str = "revised prompt"):
    return SimpleNamespace(
        data=[SimpleNamespace(b64_json=b64, revised_prompt=revised)]
    )


@pytest.mark.asyncio
async def test_generate_generic_image_success():
    fake_b64 = _fake_b64_png()
    service = ImageGenerationService()
    service.client = SimpleNamespace(
        images=SimpleNamespace(generate=AsyncMock(return_value=_fake_openai_response(fake_b64)))
    )

    request = GenerateImageRequest(prompt="A cat astronaut", content_type=ContentType.GENERAL)
    response = await service.generate_image(request)

    assert response.success is True
    assert response.image_data is not None
    assert response.metadata["model_used"] == "gpt-image-1"
    service.client.images.generate.assert_awaited_once()


@pytest.mark.asyncio
async def test_generate_youtube_thumbnail_post_processed():
    fake_b64 = _fake_b64_png(1792, 1024)
    service = ImageGenerationService()
    service.client = SimpleNamespace(
        images=SimpleNamespace(generate=AsyncMock(return_value=_fake_openai_response(fake_b64)))
    )

    request = GenerateImageRequest(
        prompt="Awesome video",
        content_type=ContentType.YOUTUBE_THUMBNAIL,
        include_text_overlay=True,
        text_overlay="WATCH NOW",
    )
    response = await service.generate_image(request)

    assert response.success is True
    assert response.metadata["optimized_for"] == "youtube"


@pytest.mark.asyncio
async def test_generate_image_failure_returns_error():
    service = ImageGenerationService()
    service.client = SimpleNamespace(
        images=SimpleNamespace(generate=AsyncMock(side_effect=RuntimeError("api boom")))
    )

    request = GenerateImageRequest(prompt="x", content_type=ContentType.GENERAL)
    response = await service.generate_image(request)

    # Falls back, fallback also fails -> success False
    assert response.success is False
    assert "boom" in (response.error or "")
