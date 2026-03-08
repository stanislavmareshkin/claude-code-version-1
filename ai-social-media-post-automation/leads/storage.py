"""
Lead storage — JSON file-based CRM.
Supports import from CSV / manual add / Firecrawl results.
"""
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from .models import Lead, LeadStatus
from ..config import LEADS_DIR


class LeadStorage:
    """Persist leads to a JSON file. Lightweight alternative to a full DB."""

    def __init__(self, filepath: Optional[Path] = None):
        self.filepath = filepath or (LEADS_DIR / "leads.json")
        self.leads: List[Lead] = []
        self._load()

    # ── CRUD ────────────────────────────────────────────────────────

    def add(self, lead: Lead) -> Lead:
        """Add a lead (dedup by email)."""
        existing = self.find_by_email(lead.email)
        if existing:
            return existing
        self.leads.append(lead)
        self._save()
        return lead

    def update(self, email: str, **fields) -> Optional[Lead]:
        """Update lead fields by email."""
        lead = self.find_by_email(email)
        if not lead:
            return None
        for key, value in fields.items():
            if hasattr(lead, key):
                setattr(lead, key, value)
        lead.updated_at = datetime.now().isoformat()
        self._save()
        return lead

    def update_status(self, email: str, status: LeadStatus) -> Optional[Lead]:
        """Advance lead through the funnel."""
        return self.update(email, status=status)

    def delete(self, email: str) -> bool:
        lead = self.find_by_email(email)
        if lead:
            self.leads.remove(lead)
            self._save()
            return True
        return False

    # ── Queries ─────────────────────────────────────────────────────

    def find_by_email(self, email: str) -> Optional[Lead]:
        email_lower = email.lower()
        for lead in self.leads:
            if lead.email.lower() == email_lower:
                return lead
        return None

    def filter_by_status(self, status: LeadStatus) -> List[Lead]:
        return [l for l in self.leads if l.status == status]

    def get_ready_for_outreach(self) -> List[Lead]:
        """Leads that are enriched but haven't received a proposal yet."""
        return [
            l for l in self.leads
            if l.status in (LeadStatus.NEW, LeadStatus.ENRICHED)
            and l.proposals_sent == 0
        ]

    def get_ready_for_follow_up(self, max_follow_ups: int = 3) -> List[Lead]:
        """Leads that received a proposal but didn't respond."""
        return [
            l for l in self.leads
            if l.status == LeadStatus.PROPOSAL_SENT
            and l.follow_ups_sent < max_follow_ups
        ]

    def get_funnel_stats(self) -> Dict[str, int]:
        """Return counts per status."""
        stats: Dict[str, int] = {}
        for status in LeadStatus:
            stats[status.value] = sum(1 for l in self.leads if l.status == status)
        stats["total"] = len(self.leads)
        return stats

    # ── Import ──────────────────────────────────────────────────────

    def import_csv(self, csv_path: str, column_map: Optional[Dict[str, str]] = None) -> int:
        """
        Import leads from a CSV file.

        Args:
            csv_path: Path to CSV
            column_map: Optional mapping {csv_column: lead_field}
                        Default expects: company, contact_name, email, industry, website, phone

        Returns:
            Number of new leads imported
        """
        default_map = {
            "company": "company",
            "contact_name": "contact_name",
            "name": "contact_name",
            "email": "email",
            "industry": "industry",
            "website": "website",
            "phone": "phone",
            "telegram": "telegram",
            "city": "city",
        }
        mapping = column_map or default_map

        count = 0
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                lead_data: Dict = {"source": "csv"}
                for csv_col, lead_field in mapping.items():
                    val = row.get(csv_col, "").strip()
                    if val:
                        lead_data[lead_field] = val

                if not lead_data.get("email") or not lead_data.get("company"):
                    continue

                if not lead_data.get("contact_name"):
                    lead_data["contact_name"] = lead_data["company"]

                lead = Lead(**{k: v for k, v in lead_data.items() if k in Lead.__dataclass_fields__})
                added = self.add(lead)
                if added is lead:  # wasn't a duplicate
                    count += 1

        return count

    # ── Persistence ─────────────────────────────────────────────────

    def _save(self):
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([l.to_dict() for l in self.leads], f, indent=2, ensure_ascii=False)

    def _load(self):
        if self.filepath.exists():
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.leads = [Lead.from_dict(d) for d in data]
