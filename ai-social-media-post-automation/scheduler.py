"""
Content scheduling and publishing system.
"""
import schedule
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from pathlib import Path
import json
from .config import SCHEDULING, PLATFORM_CONFIGS


class ContentScheduler:
    """
    Manages content scheduling and automated publishing.
    """
    
    def __init__(self):
        self.scheduled_posts = []
        self.publishing_queue = []
        self.post_history = []
        self.callbacks = {}  # Platform-specific publish callbacks
    
    def register_platform_callback(self, platform: str, callback: Callable):
        """
        Register a callback function for publishing to a platform.
        
        Args:
            platform: Platform name
            callback: Function that takes (text, images, scheduled_time) and returns result
        """
        self.callbacks[platform] = callback
    
    def schedule_post(
        self,
        platform: str,
        text: str,
        images: Optional[List] = None,
        scheduled_time: Optional[datetime] = None,
        theme: Optional[str] = None,
    ) -> Dict:
        """
        Schedule a post for publication.
        
        Args:
            platform: Target platform
            text: Post text
            images: Optional images
            scheduled_time: When to publish (default: next optimal time)
            theme: Content theme
            
        Returns:
            Scheduling result
        """
        if scheduled_time is None:
            scheduled_time = self._get_next_optimal_time(platform)
        
        post_data = {
            "platform": platform,
            "text": text,
            "images": images,
            "scheduled_time": scheduled_time,
            "theme": theme,
            "status": "scheduled",
            "created_at": datetime.now().isoformat(),
        }
        
        self.scheduled_posts.append(post_data)
        self.scheduled_posts.sort(key=lambda x: x["scheduled_time"])
        
        # Schedule using schedule library
        schedule.every().day.at(scheduled_time.strftime("%H:%M")).do(
            self._publish_scheduled_post,
            post_data
        )
        
        return {
            "success": True,
            "post_id": len(self.scheduled_posts),
            "scheduled_time": scheduled_time.isoformat(),
            "platform": platform,
        }
    
    def _get_next_optimal_time(self, platform: str) -> datetime:
        """
        Get the next optimal posting time for a platform.
        
        Args:
            platform: Platform name
            
        Returns:
            Next optimal datetime
        """
        from .config import PLATFORM_CONFIGS
        
        config = PLATFORM_CONFIGS.get(platform, {})
        optimal_times = config.get("optimal_post_time", "09:00-12:00, 18:00-21:00")
        
        # Parse optimal times (simple implementation)
        # In production, use more sophisticated scheduling
        now = datetime.now()
        
        # Try to schedule within next 24 hours at optimal times
        optimal_hours = [9, 10, 11, 12, 18, 19, 20, 21]
        
        for hour in optimal_hours:
            candidate = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            if candidate > now:
                return candidate
        
        # If no optimal time today, schedule for tomorrow at 9 AM
        tomorrow = now + timedelta(days=1)
        return tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
    
    def _publish_scheduled_post(self, post_data: Dict):
        """Internal method to publish a scheduled post."""
        platform = post_data["platform"]
        callback = self.callbacks.get(platform)
        
        if not callback:
            print(f"❌ No callback registered for platform: {platform}")
            return
        
        try:
            scheduled_time = datetime.fromisoformat(post_data["scheduled_time"])
            result = callback(
                post_data["text"],
                post_data.get("images"),
                scheduled_time,
            )
            
            post_data["status"] = "published"
            post_data["published_at"] = datetime.now().isoformat()
            post_data["result"] = result
            
            self.post_history.append(post_data)
            
            # Remove from scheduled list
            if post_data in self.scheduled_posts:
                self.scheduled_posts.remove(post_data)
            
            print(f"✓ Published post to {platform}: {result.get('post_id', 'unknown')}")
            
        except Exception as e:
            print(f"❌ Error publishing scheduled post: {str(e)}")
            post_data["status"] = "failed"
            post_data["error"] = str(e)
    
    def publish_immediately(
        self,
        platform: str,
        text: str,
        images: Optional[List] = None,
    ) -> Dict:
        """
        Publish a post immediately.
        
        Args:
            platform: Target platform
            text: Post text
            images: Optional images
            
        Returns:
            Publishing result
        """
        callback = self.callbacks.get(platform)
        if not callback:
            return {"error": f"No callback registered for platform: {platform}"}
        
        try:
            result = callback(text, images, None)
            
            post_data = {
                "platform": platform,
                "text": text,
                "images": images,
                "status": "published",
                "published_at": datetime.now().isoformat(),
                "result": result,
            }
            
            self.post_history.append(post_data)
            return result
            
        except Exception as e:
            return {"error": f"Failed to publish: {str(e)}"}
    
    def get_scheduled_posts(self, platform: Optional[str] = None) -> List[Dict]:
        """Get list of scheduled posts."""
        if platform:
            return [p for p in self.scheduled_posts if p["platform"] == platform]
        return self.scheduled_posts
    
    def cancel_post(self, post_id: int) -> bool:
        """Cancel a scheduled post."""
        if 0 <= post_id < len(self.scheduled_posts):
            post = self.scheduled_posts[post_id]
            post["status"] = "cancelled"
            self.scheduled_posts.remove(post)
            return True
        return False
    
    def run_scheduler(self, interval_seconds: int = 60):
        """
        Run the scheduler loop.
        
        Args:
            interval_seconds: How often to check for scheduled posts
        """
        print(f"🕐 Scheduler started. Checking every {interval_seconds} seconds...")
        
        while True:
            schedule.run_pending()
            time.sleep(interval_seconds)
    
    def save_schedule(self, filepath: Path):
        """Save scheduled posts to file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.scheduled_posts, f, indent=2, ensure_ascii=False)
    
    def load_schedule(self, filepath: Path):
        """Load scheduled posts from file."""
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                self.scheduled_posts = json.load(f)

