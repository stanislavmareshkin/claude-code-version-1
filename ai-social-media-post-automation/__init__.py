"""
Social Media Automation + Cold Outreach System
"""
from .orchestrator import SocialMediaOrchestrator
from .ai_content_generator import AIContentGenerator
from .scheduler import ContentScheduler
from .analytics import AnalyticsTracker
from .leads import OutreachManager, LeadStorage, Lead

__version__ = "2.0.0"
__all__ = [
    "SocialMediaOrchestrator",
    "AIContentGenerator",
    "ContentScheduler",
    "AnalyticsTracker",
    "OutreachManager",
    "LeadStorage",
    "Lead",
]


