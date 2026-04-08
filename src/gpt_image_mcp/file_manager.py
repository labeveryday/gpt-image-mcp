"""File management utilities for temporary image storage."""

import base64
import logging
import tempfile
import uuid
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


class TempImageManager:
    """Manages temporary storage of generated images."""

    def __init__(self, cleanup_age_hours: int = 24):
        """Initialize the temp image manager.

        Args:
            cleanup_age_hours: Age in hours after which files are cleaned up
        """
        self.temp_dir = Path(tempfile.gettempdir()) / "gpt-image-mcp"
        self.temp_dir.mkdir(exist_ok=True)
        self.cleanup_age_hours = cleanup_age_hours

    def save_image(self, image_data: str, file_extension: str = "png") -> str:
        """Save base64 image data to a temporary file.

        Args:
            image_data: Base64 encoded image data
            file_extension: File extension (without dot)

        Returns:
            Absolute path to the saved file
        """
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            filename = f"image_{timestamp}_{unique_id}.{file_extension}"
            file_path = self.temp_dir / filename

            # Decode and save image
            image_bytes = base64.b64decode(image_data)
            with open(file_path, 'wb') as f:
                f.write(image_bytes)

            logger.info(f"Saved image to: {file_path}")
            return str(file_path)

        except Exception as e:
            logger.error(f"Failed to save image: {str(e)}")
            raise

    def cleanup_old_files(self) -> int:
        """Clean up old temporary files.

        Returns:
            Number of files cleaned up
        """
        if not self.temp_dir.exists():
            return 0

        cutoff_time = datetime.now() - timedelta(hours=self.cleanup_age_hours)
        cleaned_count = 0

        try:
            for file_path in self.temp_dir.glob("image_*.png"):
                if file_path.stat().st_mtime < cutoff_time.timestamp():
                    file_path.unlink()
                    cleaned_count += 1
                    logger.debug(f"Cleaned up old file: {file_path}")

            for file_path in self.temp_dir.glob("image_*.jpg"):
                if file_path.stat().st_mtime < cutoff_time.timestamp():
                    file_path.unlink()
                    cleaned_count += 1
                    logger.debug(f"Cleaned up old file: {file_path}")

        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

        if cleaned_count > 0:
            logger.info(f"Cleaned up {cleaned_count} old image files")

        return cleaned_count

    def get_temp_dir_info(self) -> dict:
        """Get information about the temporary directory.

        Returns:
            Dictionary with temp directory statistics
        """
        if not self.temp_dir.exists():
            return {"exists": False, "path": str(self.temp_dir)}

        files = list(self.temp_dir.glob("image_*"))
        total_size = sum(f.stat().st_size for f in files if f.is_file())

        return {
            "exists": True,
            "path": str(self.temp_dir),
            "file_count": len(files),
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "cleanup_age_hours": self.cleanup_age_hours
        }


# Global instance
temp_image_manager = TempImageManager()
