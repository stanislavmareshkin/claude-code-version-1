"""
Analytics and performance tracking module.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
import json
from collections import defaultdict
from .config import ANALYTICS


class AnalyticsTracker:
    """
    Tracks and analyzes social media post performance.
    """
    
    def __init__(self, data_dir: Path):
        """
        Initialize analytics tracker.
        
        Args:
            data_dir: Directory to store analytics data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.metrics = defaultdict(list)
        self.performance_cache = {}
    
    def record_post_publication(
        self,
        post_id: str,
        platform: str,
        text: str,
        theme: Optional[str] = None,
        published_at: Optional[datetime] = None,
    ):
        """
        Record a post publication.
        
        Args:
            post_id: Post identifier
            platform: Platform name
            text: Post text
            theme: Content theme
            published_at: Publication timestamp
        """
        record = {
            "post_id": post_id,
            "platform": platform,
            "text": text[:200],  # Store preview
            "theme": theme,
            "published_at": (published_at or datetime.now()).isoformat(),
            "metrics": {},
        }
        
        self.metrics[platform].append(record)
        self._save_metrics()
    
    def update_post_metrics(
        self,
        platform: str,
        post_id: str,
        metrics: Dict[str, float],
    ):
        """
        Update metrics for a published post.
        
        Args:
            platform: Platform name
            post_id: Post identifier
            metrics: Dictionary of metrics (likes, shares, views, etc.)
        """
        # Find the post in metrics
        for post in self.metrics[platform]:
            if post["post_id"] == post_id:
                post["metrics"].update(metrics)
                post["last_updated"] = datetime.now().isoformat()
                break
        
        self._save_metrics()
    
    def get_post_performance(
        self,
        post_id: str,
        platform: str,
    ) -> Optional[Dict]:
        """
        Get performance data for a specific post.
        
        Args:
            post_id: Post identifier
            platform: Platform name
            
        Returns:
            Performance data dictionary
        """
        for post in self.metrics[platform]:
            if post["post_id"] == post_id:
                return post
        return None
    
    def get_platform_statistics(
        self,
        platform: str,
        days: int = 30,
    ) -> Dict:
        """
        Get aggregated statistics for a platform.
        
        Args:
            platform: Platform name
            days: Number of days to analyze
            
        Returns:
            Statistics dictionary
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        platform_posts = [
            p for p in self.metrics[platform]
            if datetime.fromisoformat(p["published_at"]) >= cutoff_date
        ]
        
        if not platform_posts:
            return {
                "platform": platform,
                "total_posts": 0,
                "average_likes": 0,
                "average_shares": 0,
                "average_views": 0,
                "engagement_rate": 0,
            }
        
        total_likes = sum(p["metrics"].get("likes", 0) for p in platform_posts)
        total_shares = sum(p["metrics"].get("shares", 0) for p in platform_posts)
        total_views = sum(p["metrics"].get("views", 0) for p in platform_posts)
        total_posts = len(platform_posts)
        
        avg_likes = total_likes / total_posts if total_posts > 0 else 0
        avg_shares = total_shares / total_posts if total_posts > 0 else 0
        avg_views = total_views / total_posts if total_posts > 0 else 0
        
        # Calculate engagement rate (likes + shares + comments) / views
        total_engagement = sum(
            p["metrics"].get("likes", 0) +
            p["metrics"].get("shares", 0) +
            p["metrics"].get("comments", 0)
            for p in platform_posts
        )
        engagement_rate = (total_engagement / total_views) if total_views > 0 else 0
        
        return {
            "platform": platform,
            "total_posts": total_posts,
            "average_likes": avg_likes,
            "average_shares": avg_shares,
            "average_views": avg_views,
            "engagement_rate": engagement_rate,
            "period_days": days,
        }
    
    def get_theme_performance(
        self,
        theme: str,
        days: int = 30,
    ) -> Dict:
        """
        Analyze performance by content theme.
        
        Args:
            theme: Content theme
            days: Number of days to analyze
            
        Returns:
            Theme performance statistics
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        
        theme_posts = []
        for platform_posts in self.metrics.values():
            for post in platform_posts:
                if (post.get("theme") == theme and
                    datetime.fromisoformat(post["published_at"]) >= cutoff_date):
                    theme_posts.append(post)
        
        if not theme_posts:
            return {
                "theme": theme,
                "total_posts": 0,
                "average_engagement": 0,
            }
        
        total_engagement = sum(
            p["metrics"].get("likes", 0) +
            p["metrics"].get("shares", 0) +
            p["metrics"].get("comments", 0)
            for p in theme_posts
        )
        
        return {
            "theme": theme,
            "total_posts": len(theme_posts),
            "average_engagement": total_engagement / len(theme_posts),
            "period_days": days,
        }
    
    def identify_top_performing_content(
        self,
        platform: Optional[str] = None,
        metric: str = "engagement",
        limit: int = 10,
    ) -> List[Dict]:
        """
        Identify top performing posts.
        
        Args:
            platform: Filter by platform (None for all)
            metric: Metric to rank by (engagement, likes, shares, views)
            limit: Number of top posts to return
            
        Returns:
            List of top performing posts
        """
        posts_to_analyze = []
        
        if platform:
            posts_to_analyze = self.metrics[platform]
        else:
            for platform_posts in self.metrics.values():
                posts_to_analyze.extend(platform_posts)
        
        # Calculate engagement score
        for post in posts_to_analyze:
            metrics = post.get("metrics", {})
            if metric == "engagement":
                post["_score"] = (
                    metrics.get("likes", 0) +
                    metrics.get("shares", 0) * 2 +  # Shares weighted higher
                    metrics.get("comments", 0) * 1.5
                )
            else:
                post["_score"] = metrics.get(metric, 0)
        
        # Sort by score
        top_posts = sorted(
            posts_to_analyze,
            key=lambda x: x.get("_score", 0),
            reverse=True
        )[:limit]
        
        # Remove temporary score
        for post in top_posts:
            post.pop("_score", None)
        
        return top_posts
    
    def _save_metrics(self):
        """Save metrics to disk."""
        metrics_file = self.data_dir / "analytics.json"
        with open(metrics_file, 'w', encoding='utf-8') as f:
            json.dump(dict(self.metrics), f, indent=2, ensure_ascii=False)
    
    def _load_metrics(self):
        """Load metrics from disk."""
        metrics_file = self.data_dir / "analytics.json"
        if metrics_file.exists():
            with open(metrics_file, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                self.metrics = defaultdict(list, loaded)

