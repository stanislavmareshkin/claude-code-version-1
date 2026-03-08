"""
Lead data models.
"""
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class LeadStatus(str, Enum):
    NEW = "new"
    ENRICHED = "enriched"
    PROPOSAL_SENT = "proposal_sent"
    OPENED = "opened"
    REPLIED = "replied"
    DEAL = "deal"
    REJECTED = "rejected"


@dataclass
class Lead:
    """A single lead in the outreach pipeline."""

    # Required
    company: str
    contact_name: str
    email: str

    # Optional enrichment
    industry: str = ""
    website: str = ""
    phone: str = ""
    telegram: str = ""
    city: str = ""
    pain_points: List[str] = field(default_factory=list)
    notes: str = ""

    # Pipeline state
    status: LeadStatus = LeadStatus.NEW
    source: str = ""  # csv, google_sheets, manual, firecrawl
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    # Outreach history
    proposals_sent: int = 0
    last_proposal_date: Optional[str] = None
    last_proposal_subject: str = ""
    follow_ups_sent: int = 0
    channel: str = "email"  # email, telegram

    # Tracking
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        d = asdict(self)
        d["status"] = self.status.value
        return d

    @classmethod
    def from_dict(cls, data: Dict) -> "Lead":
        data = data.copy()
        if "status" in data:
            data["status"] = LeadStatus(data["status"])
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    @property
    def display_name(self) -> str:
        return f"{self.contact_name} ({self.company})"
