"""
VK (VKontakte) platform adapter.
"""
import io
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from PIL import Image
import requests

from .base import PlatformAdapter


class VKAdapter(PlatformAdapter):
    """
    Adapter for VK (VKontakte) platform.
    Uses VK API v5.199.
    """

    API_BASE = "https://api.vk.com/method"
    API_VERSION = "5.199"

    def __init__(self, credentials: Dict[str, Any]):
        super().__init__(credentials)
        self.access_token = credentials.get("access_token")
        self.group_id = credentials.get("group_id")  # without minus sign
        self.authenticated = False

    def _api_call(self, method: str, params: Optional[Dict] = None) -> Dict:
        """Make a VK API call."""
        params = params or {}
        params.update({
            "access_token": self.access_token,
            "v": self.API_VERSION,
        })
        resp = requests.get(f"{self.API_BASE}/{method}", params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        if "error" in data:
            raise RuntimeError(f"VK API error: {data['error'].get('error_msg', data['error'])}")
        return data.get("response", data)

    def authenticate(self) -> bool:
        """Authenticate by checking token validity."""
        if not self.access_token or not self.group_id:
            return False
        try:
            result = self._api_call("groups.getById", {"group_id": self.group_id})
            if result:
                self.authenticated = True
                return True
        except Exception as e:
            print(f"VK auth failed: {e}")
        return False

    def _upload_photo(self, image: Image.Image) -> Optional[str]:
        """
        Upload a photo to VK wall.

        Returns:
            Photo attachment string like 'photo-12345_67890'
        """
        # Step 1: Get upload URL
        upload_info = self._api_call(
            "photos.getWallUploadServer",
            {"group_id": self.group_id},
        )
        upload_url = upload_info["upload_url"]

        # Step 2: Upload image bytes
        buf = io.BytesIO()
        image.save(buf, format="JPEG")
        buf.seek(0)
        resp = requests.post(upload_url, files={"photo": ("post.jpg", buf, "image/jpeg")}, timeout=60)
        resp.raise_for_status()
        upload_result = resp.json()

        # Step 3: Save photo on VK
        saved = self._api_call("photos.saveWallPhoto", {
            "group_id": self.group_id,
            "photo": upload_result["photo"],
            "server": upload_result["server"],
            "hash": upload_result["hash"],
        })
        if saved:
            photo = saved[0]
            return f"photo{photo['owner_id']}_{photo['id']}"
        return None

    def publish_post(
        self,
        text: str,
        images: Optional[List[Image.Image]] = None,
        scheduled_time: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Publish a post to VK community wall."""
        if not self.authenticated:
            if not self.authenticate():
                return {"error": "VK authentication failed"}

        params = {
            "owner_id": f"-{self.group_id}",
            "from_group": 1,
            "message": text,
        }

        # Upload images
        attachments = []
        if images:
            for img in images[:10]:
                att = self._upload_photo(img)
                if att:
                    attachments.append(att)
            if attachments:
                params["attachments"] = ",".join(attachments)

        # Schedule if needed
        if scheduled_time and scheduled_time > datetime.now():
            params["publish_date"] = int(scheduled_time.timestamp())

        try:
            result = self._api_call("wall.post", params)
            post_id = result.get("post_id")
            self.last_post_time = datetime.now()
            return {
                "success": True,
                "post_id": str(post_id),
                "platform": "vk",
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"error": f"VK publish failed: {e}"}

    def get_analytics(
        self,
        post_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Get analytics for a VK post."""
        try:
            posts = self._api_call("wall.getById", {
                "posts": f"-{self.group_id}_{post_id}",
            })
            if posts:
                post = posts[0]
                return {
                    "post_id": post_id,
                    "platform": "vk",
                    "views": post.get("views", {}).get("count", 0),
                    "likes": post.get("likes", {}).get("count", 0),
                    "shares": post.get("reposts", {}).get("count", 0),
                    "comments": post.get("comments", {}).get("count", 0),
                }
        except Exception as e:
            return {"error": f"VK analytics error: {e}"}
        return {"post_id": post_id, "platform": "vk"}

    def validate_content(
        self, text: str, images: Optional[List[Image.Image]] = None
    ) -> Tuple[bool, Optional[str]]:
        """Validate content for VK."""
        if not text or not text.strip():
            return False, "Post text cannot be empty"
        if len(text) > 15895:
            return False, "Text exceeds VK's 15895 character limit"
        if images and len(images) > 10:
            return False, "VK supports up to 10 images per post"
        return True, None
