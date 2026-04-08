"""Tests for utility functions."""

import base64
import io

import pytest
from PIL import Image

from gpt_image_mcp.utils import (
    calculate_optimal_dimensions,
    get_image_info,
    resize_image,
    validate_image_data,
)


def create_test_image(width=100, height=100, format='PNG'):
    """Create a test image and return as base64."""
    image = Image.new('RGB', (width, height), color='red')
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    return base64.b64encode(buffer.getvalue()).decode('utf-8')


def test_validate_image_data_valid():
    """Test validation with valid image data."""
    image_data = create_test_image()
    assert validate_image_data(image_data) is True


def test_validate_image_data_invalid():
    """Test validation with invalid data."""
    assert validate_image_data("invalid_base64") is False
    assert validate_image_data("") is False


def test_get_image_info():
    """Test getting image information."""
    image_data = create_test_image(200, 150)
    info = get_image_info(image_data)

    assert info is not None
    assert info['width'] == 200
    assert info['height'] == 150
    assert info['format'] == 'PNG'
    assert info['aspect_ratio'] == pytest.approx(200/150)


def test_resize_image():
    """Test image resizing."""
    image_data = create_test_image(400, 300)
    resized_data = resize_image(image_data, (200, 150), maintain_aspect_ratio=False)

    assert resized_data is not None

    # Check the resized image dimensions
    resized_info = get_image_info(resized_data)
    assert resized_info['width'] == 200
    assert resized_info['height'] == 150


def test_calculate_optimal_dimensions():
    """Test optimal dimension calculation."""
    # YouTube
    dims = calculate_optimal_dimensions("youtube_thumbnail")
    assert dims == (1920, 1080)

    # Instagram
    dims = calculate_optimal_dimensions("social_media", "instagram")
    assert dims == (1080, 1080)

    # Blog
    dims = calculate_optimal_dimensions("blog_header")
    assert dims == (1536, 1024)

    # Default
    dims = calculate_optimal_dimensions("unknown")
    assert dims == (1024, 1024)


def test_image_too_large():
    """Test validation rejects overly large images."""
    # This would create a very large image that should be rejected
    image_data = create_test_image(5000, 5000)
    assert validate_image_data(image_data) is False


def test_image_too_small():
    """Test validation rejects very small images."""
    image_data = create_test_image(50, 50)
    assert validate_image_data(image_data) is False
