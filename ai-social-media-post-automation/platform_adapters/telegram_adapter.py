"""
Telegram platform adapter.
"""
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from PIL import Image
import requests
from pathlib import Path
from .base import PlatformAdapter


class TelegramAdapter(PlatformAdapter):
    """
    Adapter for Telegram platform.
    """
    
    def __init__(self, credentials: Dict[str, Any]):
        super().__init__(credentials)
        self.bot_token = credentials.get("bot_token")
        self.chat_id = credentials.get("chat_id")
        self.api_base = f"https://api.telegram.org/bot{self.bot_token}"
        self.authenticated = False
    
    def authenticate(self) -> bool:
        """Authenticate with Telegram API."""
        try:
            response = requests.get(f"{self.api_base}/getMe")
            if response.status_code == 200:
                self.authenticated = True
                return True
        except Exception as e:
            print(f"❌ Telegram authentication failed: {str(e)}")
        return False
    
    def publish_post(
        self,
        text: str,
        images: Optional[List[Image.Image]] = None,
        scheduled_time: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Publish post to Telegram channel/group.
        
        Note: Telegram doesn't support native scheduling, so we'd need
        to use a scheduler service or bot framework for that.
        """
        if not self.authenticated:
            if not self.authenticate():
                return {"error": "Authentication failed"}
        
        try:
            if images and len(images) > 0:
                # Send photo with caption
                image_path = self.save_image(images[0], f"telegram_{datetime.now().timestamp()}.jpg")
                
                with open(image_path, 'rb') as photo:
                    files = {'photo': photo}
                    data = {
                        'chat_id': self.chat_id,
                        'caption': text[:1024],  # Telegram caption limit
                    }
                    response = requests.post(
                        f"{self.api_base}/sendPhoto",
                        files=files,
                        data=data
                    )
                
                image_path.unlink()  # Clean up
            else:
                # Send text message
                response = requests.post(
                    f"{self.api_base}/sendMessage",
                    json={
                        'chat_id': self.chat_id,
                        'text': text,
                        'parse_mode': 'Markdown',  # Supports Markdown formatting
                    }
                )
            
            if response.status_code == 200:
                result = response.json()
                self.last_post_time = datetime.now()
                return {
                    "success": True,
                    "post_id": str(result.get("result", {}).get("message_id")),
                    "platform": "telegram",
                    "timestamp": datetime.now().isoformat(),
                }
            else:
                return {"error": f"API error: {response.text}"}
                
        except Exception as e:
            return {"error": f"Failed to publish: {str(e)}"}
    
    def get_analytics(
        self,
        post_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Get analytics for Telegram post.
        
        Note: Telegram Bot API has limited analytics. For full analytics,
        you'd need to use Telegram Analytics or track manually.
        """
        # Basic implementation - Telegram Bot API doesn't provide detailed analytics
        return {
            "post_id": post_id,
            "platform": "telegram",
            "views": None,  # Not available via Bot API
            "likes": None,
            "shares": None,
            "comments": None,
            "note": "Full analytics require Telegram Analytics or manual tracking",
        }
    
    def validate_content(self, text: str, images: Optional[List[Image.Image]] = None) -> Tuple[bool, Optional[str]]:
        """Validate content for Telegram."""
        if len(text) > 4096:
            return False, "Text exceeds Telegram's 4096 character limit"
        
        if images and len(images) > 10:
            return False, "Telegram supports up to 10 images per message"
        
        return True, None
    
    def format_text(self, text: str) -> str:
        """Format text with Telegram Markdown support."""
        # Basic formatting - can be enhanced
        return text

