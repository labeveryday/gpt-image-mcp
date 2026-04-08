"""Utility functions for image processing and validation."""

import base64
import io
import logging

from PIL import Image

logger = logging.getLogger(__name__)


def validate_image_data(image_data: str) -> bool:
    """Validate base64 encoded image data."""
    try:
        # Try to decode the base64 string
        image_bytes = base64.b64decode(image_data)

        # Try to open as an image
        image = Image.open(io.BytesIO(image_bytes))

        # Verify it's a valid image format
        if image.format not in ['PNG', 'JPEG', 'JPG', 'WEBP', 'GIF']:
            return False

        # Check image dimensions (reasonable limits)
        width, height = image.size
        if width > 4096 or height > 4096 or width < 64 or height < 64:
            return False

        return True

    except Exception as e:
        logger.warning(f"Image validation failed: {str(e)}")
        return False


def encode_image(image_path: str) -> str | None:
    """Encode an image file to base64 string."""
    try:
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
            return base64.b64encode(image_data).decode('utf-8')
    except Exception as e:
        logger.error(f"Failed to encode image {image_path}: {str(e)}")
        return None


def decode_image(image_data: str) -> Image.Image | None:
    """Decode base64 image data to PIL Image."""
    try:
        image_bytes = base64.b64decode(image_data)
        return Image.open(io.BytesIO(image_bytes))
    except Exception as e:
        logger.error(f"Failed to decode image: {str(e)}")
        return None


def resize_image(image_data: str, target_size: tuple[int, int], maintain_aspect_ratio: bool = True) -> str | None:
    """Resize an image and return as base64 string."""
    try:
        # Decode image
        image = decode_image(image_data)
        if not image:
            return None

        # Resize image
        if maintain_aspect_ratio:
            image.thumbnail(target_size, Image.Resampling.LANCZOS)
        else:
            image = image.resize(target_size, Image.Resampling.LANCZOS)

        # Encode back to base64
        output_buffer = io.BytesIO()
        format = image.format or 'PNG'
        image.save(output_buffer, format=format)
        encoded_image = base64.b64encode(output_buffer.getvalue()).decode('utf-8')

        return encoded_image

    except Exception as e:
        logger.error(f"Failed to resize image: {str(e)}")
        return None


def compress_image(image_data: str, quality: int = 85, format: str = 'JPEG') -> str | None:
    """Compress an image and return as base64 string."""
    try:
        # Decode image
        image = decode_image(image_data)
        if not image:
            return None

        # Convert to RGB if saving as JPEG
        if format.upper() == 'JPEG' and image.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
            image = background

        # Compress and save
        output_buffer = io.BytesIO()
        image.save(output_buffer, format=format, quality=quality, optimize=True)
        encoded_image = base64.b64encode(output_buffer.getvalue()).decode('utf-8')

        return encoded_image

    except Exception as e:
        logger.error(f"Failed to compress image: {str(e)}")
        return None


def get_image_info(image_data: str) -> dict | None:
    """Get information about an image."""
    try:
        image = decode_image(image_data)
        if not image:
            return None

        # Calculate file size
        image_bytes = base64.b64decode(image_data)
        file_size = len(image_bytes)

        return {
            'width': image.width,
            'height': image.height,
            'format': image.format,
            'mode': image.mode,
            'size_bytes': file_size,
            'size_mb': file_size / (1024 * 1024),
            'aspect_ratio': image.width / image.height
        }

    except Exception as e:
        logger.error(f"Failed to get image info: {str(e)}")
        return None


def create_thumbnail_preview(image_data: str, size: tuple[int, int] = (200, 200)) -> str | None:
    """Create a small preview thumbnail of an image."""
    try:
        image = decode_image(image_data)
        if not image:
            return None

        # Create thumbnail
        image.thumbnail(size, Image.Resampling.LANCZOS)

        # Convert to base64
        output_buffer = io.BytesIO()
        format = 'PNG' if image.mode == 'RGBA' else 'JPEG'
        image.save(output_buffer, format=format)
        encoded_thumbnail = base64.b64encode(output_buffer.getvalue()).decode('utf-8')

        return encoded_thumbnail

    except Exception as e:
        logger.error(f"Failed to create thumbnail: {str(e)}")
        return None


def validate_image_dimensions(image_data: str, min_size: tuple[int, int], max_size: tuple[int, int]) -> bool:
    """Validate that image dimensions are within specified bounds."""
    try:
        image = decode_image(image_data)
        if not image:
            return False

        width, height = image.size
        min_width, min_height = min_size
        max_width, max_height = max_size

        return (min_width <= width <= max_width and
                min_height <= height <= max_height)

    except Exception as e:
        logger.warning(f"Dimension validation failed: {str(e)}")
        return False


def calculate_optimal_dimensions(content_type: str, platform: str = None) -> tuple[int, int]:
    """Calculate optimal dimensions for different content types and platforms."""
    # Platform-specific dimensions
    platform_dimensions = {
        'youtube': (1920, 1080),
        'instagram': (1080, 1080),
        'twitter': (1200, 675),
        'facebook': (1200, 630),
        'linkedin': (1200, 627),
        'pinterest': (735, 1102)
    }

    # Content type dimensions
    content_dimensions = {
        'youtube_thumbnail': (1920, 1080),
        'blog_header': (1536, 1024),
        'blog_featured': (1024, 1536),
        'social_media': (1080, 1080),
        'general': (1024, 1024)
    }

    # First try platform-specific
    if platform and platform.lower() in platform_dimensions:
        return platform_dimensions[platform.lower()]

    # Then try content type
    if content_type.lower() in content_dimensions:
        return content_dimensions[content_type.lower()]

    # Default
    return (1024, 1024)


def enhance_image_contrast(image_data: str, factor: float = 1.2) -> str | None:
    """Enhance image contrast for better visibility."""
    try:
        from PIL import ImageEnhance

        image = decode_image(image_data)
        if not image:
            return None

        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        enhanced_image = enhancer.enhance(factor)

        # Convert back to base64
        output_buffer = io.BytesIO()
        format = image.format or 'PNG'
        enhanced_image.save(output_buffer, format=format)
        encoded_image = base64.b64encode(output_buffer.getvalue()).decode('utf-8')

        return encoded_image

    except Exception as e:
        logger.error(f"Failed to enhance contrast: {str(e)}")
        return None


def add_watermark(image_data: str, watermark_text: str, position: str = 'bottom-right', opacity: float = 0.5) -> str | None:
    """Add a text watermark to an image."""
    try:
        from PIL import ImageDraw, ImageFont

        image = decode_image(image_data)
        if not image:
            return None

        # Create a copy to work with
        watermarked = image.copy()

        # Create drawing context
        draw = ImageDraw.Draw(watermarked)

        # Try to use a nice font, fall back to default
        try:
            font = ImageFont.truetype("Arial.ttf", 36)
        except OSError:
            font = ImageFont.load_default()

        # Get text dimensions
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Calculate position
        img_width, img_height = watermarked.size

        position_coords = {
            'top-left': (20, 20),
            'top-right': (img_width - text_width - 20, 20),
            'bottom-left': (20, img_height - text_height - 20),
            'bottom-right': (img_width - text_width - 20, img_height - text_height - 20),
            'center': ((img_width - text_width) // 2, (img_height - text_height) // 2)
        }

        x, y = position_coords.get(position, position_coords['bottom-right'])

        # Add semi-transparent watermark
        watermark_color = (255, 255, 255, int(255 * opacity))
        draw.text((x, y), watermark_text, font=font, fill=watermark_color)

        # Convert back to base64
        output_buffer = io.BytesIO()
        format = 'PNG'  # Use PNG to preserve transparency
        watermarked.save(output_buffer, format=format)
        encoded_image = base64.b64encode(output_buffer.getvalue()).decode('utf-8')

        return encoded_image

    except Exception as e:
        logger.error(f"Failed to add watermark: {str(e)}")
        return None


def merge_images(image_data_list: list, layout: str = 'horizontal', spacing: int = 10, background_color: tuple = (255, 255, 255)) -> str | None:
    """Merge multiple images into a single image."""
    try:
        if not image_data_list or len(image_data_list) < 2:
            return None

        # Decode all images
        images = []
        for data in image_data_list:
            img = decode_image(data)
            if img:
                images.append(img)

        if len(images) < 2:
            return None

        # Calculate dimensions for merged image
        if layout == 'horizontal':
            total_width = sum(img.width for img in images) + spacing * (len(images) - 1)
            total_height = max(img.height for img in images)
        else:  # vertical
            total_width = max(img.width for img in images)
            total_height = sum(img.height for img in images) + spacing * (len(images) - 1)

        # Create new image
        merged_image = Image.new('RGB', (total_width, total_height), background_color)

        # Paste images
        if layout == 'horizontal':
            x_offset = 0
            for img in images:
                y_offset = (total_height - img.height) // 2  # Center vertically
                merged_image.paste(img, (x_offset, y_offset))
                x_offset += img.width + spacing
        else:  # vertical
            y_offset = 0
            for img in images:
                x_offset = (total_width - img.width) // 2  # Center horizontally
                merged_image.paste(img, (x_offset, y_offset))
                y_offset += img.height + spacing

        # Convert to base64
        output_buffer = io.BytesIO()
        merged_image.save(output_buffer, format='PNG')
        encoded_image = base64.b64encode(output_buffer.getvalue()).decode('utf-8')

        return encoded_image

    except Exception as e:
        logger.error(f"Failed to merge images: {str(e)}")
        return None
