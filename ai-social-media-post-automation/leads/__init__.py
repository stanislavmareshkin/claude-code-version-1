"""
Lead management and cold outreach module.
"""
from .models import Lead, LeadStatus
from .storage import LeadStorage
from .outreach_manager import OutreachManager

__all__ = ["Lead", "LeadStatus", "OutreachManager", "LeadStorage"]
