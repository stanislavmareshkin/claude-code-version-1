"""
Main orchestrator for the social media automation system.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
import random
from .config import (
    SUPPORTED_PLATFORMS,
    CONTENT_GENERATION,
    PLATFORM_CONFIGS,
)
from .ai_content_generator import AIContentGenerator
from .scheduler import ContentScheduler
from .analytics import AnalyticsTracker
from .platform_adapters import PlatformAdapter, TelegramAdapter, VKAdapter


class SocialMediaOrchestrator:
    """
    Main orchestrator that coordinates all components.
    """
    
    def __init__(self, credentials: Dict[str, Dict], data_dir: Optional[Path] = None):
        """
        Initialize the orchestrator.
        
        Args:
            credentials: Dictionary mapping platform names to their credentials
            data_dir: Directory for data storage
        """
        from config import DATA_DIR
        
        self.data_dir = Path(data_dir) if data_dir else DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.content_generator = AIContentGenerator()
        self.scheduler = ContentScheduler()
        self.analytics = AnalyticsTracker(self.data_dir / "analytics")
        
        # Initialize platform adapters
        self.adapters: Dict[str, PlatformAdapter] = {}
        self._initialize_adapters(credentials)
        
        # Register platform callbacks
        self._register_platform_callbacks()
    
    def _initialize_adapters(self, credentials: Dict[str, Dict]):
        """Initialize platform adapters based on credentials."""
        adapter_classes = {
            "telegram": TelegramAdapter,
            "vk": VKAdapter,
            # Add more adapters as they're implemented
        }
        
        for platform, creds in credentials.items():
            if platform in adapter_classes:
                try:
                    adapter = adapter_classes[platform](creds)
                    if adapter.authenticate():
                        self.adapters[platform] = adapter
                        print(f"✓ Connected to {platform.upper()}")
                    else:
                        print(f"⚠️ Failed to authenticate {platform.upper()}")
                except Exception as e:
                    print(f"❌ Error initializing {platform}: {str(e)}")
    
    def _register_platform_callbacks(self):
        """Register publish callbacks for each platform."""
        for platform, adapter in self.adapters.items():
            def make_callback(plat, adpt):
                def callback(text, images, scheduled_time):
                    result = adpt.publish_post(text, images, scheduled_time)
                    
                    # Record in analytics
                    if result.get("success"):
                        self.analytics.record_post_publication(
                            result.get("post_id"),
                            plat,
                            text,
                            published_at=datetime.now(),
                        )
                    
                    return result
                return callback
            
            self.scheduler.register_platform_callback(platform, make_callback(platform, adapter))
    
    def generate_and_schedule_batch(
        self,
        platforms: Optional[List[str]] = None,
        themes: Optional[List[str]] = None,
        count: Optional[int] = None,
    ) -> Dict:
        """
        Generate and schedule a batch of posts.
        
        Args:
            platforms: List of platforms (None for all)
            themes: List of themes (None for random)
            count: Number of posts to generate (None for default)
            
        Returns:
            Batch generation result
        """
        if platforms is None:
            platforms = list(self.adapters.keys())
        
        if themes is None:
            themes = CONTENT_GENERATION["content_themes"]
        
        if count is None:
            count = CONTENT_GENERATION["max_posts_per_day"]
        
        scheduled_posts = []
        
        for i in range(count):
            platform = random.choice(platforms)
            theme = random.choice(themes)
            
            # Generate content
            config = PLATFORM_CONFIGS.get(platform, {})
            max_length = config.get("max_text_length")
            
            text = self.content_generator.generate_post_text(
                platform=platform,
                theme=theme,
                max_length=max_length,
            )
            
            # Generate image if enabled
            images = None
            if CONTENT_GENERATION["image_generation"]:
                image_prompt = f"{theme} social media post, professional, modern design"
                image = self.content_generator.generate_image(image_prompt)
                if image:
                    images = [image]
            
            # Schedule post
            result = self.scheduler.schedule_post(
                platform=platform,
                text=text,
                images=images,
                theme=theme,
            )
            
            scheduled_posts.append(result)
        
        return {
            "success": True,
            "scheduled_count": len(scheduled_posts),
            "posts": scheduled_posts,
        }
    
    def publish_immediately(
        self,
        platform: str,
        theme: Optional[str] = None,
    ) -> Dict:
        """
        Generate and publish a post immediately.
        
        Args:
            platform: Target platform
            theme: Content theme (None for random)
            
        Returns:
            Publishing result
        """
        if platform not in self.adapters:
            return {"error": f"Platform {platform} not available"}
        
        if theme is None:
            theme = random.choice(CONTENT_GENERATION["content_themes"])
        
        # Generate content
        config = PLATFORM_CONFIGS.get(platform, {})
        max_length = config.get("max_text_length")
        
        text = self.content_generator.generate_post_text(
            platform=platform,
            theme=theme,
            max_length=max_length,
        )
        
        # Generate image if enabled
        images = None
        if CONTENT_GENERATION["image_generation"]:
            image_prompt = f"{theme} social media post, professional, modern design"
            image = self.content_generator.generate_image(image_prompt)
            if image:
                images = [image]
        
        # Publish
        result = self.scheduler.publish_immediately(
            platform=platform,
            text=text,
            images=images,
        )
        
        return result
    
    def update_analytics(self, platform: str):
        """
        Update analytics for a platform by fetching latest metrics.
        
        Args:
            platform: Platform name
        """
        if platform not in self.adapters:
            return
        
        adapter = self.adapters[platform]
        
        # Get recent posts from analytics
        platform_posts = self.analytics.metrics.get(platform, [])
        
        for post in platform_posts[-10:]:  # Update last 10 posts
            post_id = post["post_id"]
            try:
                metrics = adapter.get_analytics(post_id)
                if metrics and "error" not in metrics:
                    self.analytics.update_post_metrics(platform, post_id, metrics)
            except Exception as e:
                print(f"⚠️ Error updating analytics for {post_id}: {str(e)}")
    
    def get_performance_report(self, days: int = 30) -> Dict:
        """
        Generate a performance report.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Performance report
        """
        report = {
            "period_days": days,
            "platforms": {},
            "top_posts": [],
            "theme_performance": {},
        }
        
        # Platform statistics
        for platform in self.adapters.keys():
            report["platforms"][platform] = self.analytics.get_platform_statistics(
                platform, days
            )
        
        # Top performing posts
        report["top_posts"] = self.analytics.identify_top_performing_content(limit=10)
        
        # Theme performance
        for theme in CONTENT_GENERATION["content_themes"]:
            report["theme_performance"][theme] = self.analytics.get_theme_performance(
                theme, days
            )
        
        return report
    
    def optimize_content_strategy(self) -> Dict:
        """
        Analyze performance and suggest content strategy optimizations.
        
        Returns:
            Optimization recommendations
        """
        report = self.get_performance_report(days=30)
        
        recommendations = {
            "best_performing_platforms": [],
            "best_performing_themes": [],
            "suggestions": [],
        }
        
        # Find best platforms
        platform_scores = [
            (platform, stats["engagement_rate"])
            for platform, stats in report["platforms"].items()
        ]
        platform_scores.sort(key=lambda x: x[1], reverse=True)
        recommendations["best_performing_platforms"] = [
            platform for platform, _ in platform_scores[:3]
        ]
        
        # Find best themes
        theme_scores = [
            (theme, perf["average_engagement"])
            for theme, perf in report["theme_performance"].items()
        ]
        theme_scores.sort(key=lambda x: x[1], reverse=True)
        recommendations["best_performing_themes"] = [
            theme for theme, _ in theme_scores[:3]
        ]
        
        # Generate suggestions
        if platform_scores:
            best_platform = platform_scores[0][0]
            recommendations["suggestions"].append(
                f"Focus more content on {best_platform.upper()} - highest engagement rate"
            )
        
        if theme_scores:
            best_theme = theme_scores[0][0]
            recommendations["suggestions"].append(
                f"Increase {best_theme} content - performs best with audience"
            )
        
        return recommendations
    
    def run_continuous_mode(self, check_interval_minutes: int = 60):
        """
        Run in continuous mode, generating and scheduling content automatically.
        
        Args:
            check_interval_minutes: How often to check and generate new content
        """
        print("🚀 Starting continuous automation mode...")
        print(f"📅 Will generate content every {check_interval_minutes} minutes")
        
        # Initial batch
        self.generate_and_schedule_batch()
        
        # Schedule periodic generation
        import schedule
        schedule.every(check_interval_minutes).minutes.do(
            self.generate_and_schedule_batch
        )
        
        # Run scheduler
        self.scheduler.run_scheduler(interval_seconds=60)

