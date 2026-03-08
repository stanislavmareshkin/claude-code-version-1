"""
Base class for social media platform adapters.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path
from PIL import Image


class PlatformAdapter(ABC):
    """
    Abstract base class for platform-specific adapters.
    """
    
    def __init__(self, credentials: Dict[str, Any]):
        """
        Initialize platform adapter.
        
        Args:
            credentials: Platform-specific credentials (API keys, tokens, etc.)
        """
        self.credentials = credentials
        self.platform_name = self.__class__.__name__.lower().replace("adapter", "")
        self.last_post_time = None
    
    @abstractmethod
    def authenticate(self) -> bool:
        """
        Authenticate with the platform.
        
        Returns:
            True if authentication successful
        """
        pass
    
    @abstractmethod
    def publish_post(
        self,
        text: str,
        images: Optional[List[Image.Image]] = None,
        scheduled_time: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Publish a post to the platform.
        
        Args:
            text: Post text content
            images: Optional list of images
            scheduled_time: Optional scheduled publication time
            
        Returns:
            Dictionary with post ID and metadata
        """
        pass
    
    @abstractmethod
    def get_analytics(
        self,
        post_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Get analytics for a published post.
        
        Args:
            post_id: Post identifier
            start_date: Start date for analytics
            end_date: End date for analytics
            
        Returns:
            Dictionary with analytics data
        """
        pass
    
    @abstractmethod
    def validate_content(self, text: str, images: Optional[List[Image.Image]] = None) -> Tuple[bool, Optional[str]]:
        """
        Validate content before publishing.
        
        Args:
            text: Post text
            images: Optional images
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        pass
    
    def format_text(self, text: str) -> str:
        """
        Format text according to platform-specific rules.
        
        Args:
            text: Raw text
            
        Returns:
            Formatted text
        """
        return text
    
    def save_image(self, image: Image.Image, filename: str) -> Path:
        """
        Save image to local storage.
        
        Args:
            image: PIL Image object
            filename: Filename
            
        Returns:
            Path to saved image
        """
        from ..config import CONTENT_DIR
        CONTENT_DIR.mkdir(parents=True, exist_ok=True)
        
        image_path = CONTENT_DIR / f"{self.platform_name}_{filename}"
        image.save(image_path)
        return image_path

