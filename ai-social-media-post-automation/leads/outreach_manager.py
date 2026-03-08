"""
Outreach Manager — orchestrates the cold outreach pipeline.
"""
import time
from datetime import datetime
from typing import Dict, List, Optional

from .models import Lead, LeadStatus
from .storage import LeadStorage
from ..ai_content_generator import AIContentGenerator
from ..config import LEAD_CONFIG, PLATFORM_CONFIGS


class OutreachManager:
    """
    Manages the full cold outreach lifecycle:
    1. Import leads
    2. Enrich (via AI or external data)
    3. Generate personalized proposals
    4. Send via email / Telegram
    5. Track funnel
    6. Auto follow-up
    """

    def __init__(
        self,
        storage: Optional[LeadStorage] = None,
        content_generator: Optional[AIContentGenerator] = None,
        send_callback=None,
    ):
        self.storage = storage or LeadStorage()
        self.generator = content_generator or AIContentGenerator()
        self.send_callback = send_callback  # function(lead, subject, body) -> bool
        self.results: List[Dict] = []

    # ── Pipeline Steps ──────────────────────────────────────────────

    def import_leads_csv(self, csv_path: str) -> int:
        """Import leads from CSV."""
        count = self.storage.import_csv(csv_path)
        print(f"Imported {count} new leads from {csv_path}")
        return count

    def enrich_lead(self, lead: Lead, website_text: str = "") -> Lead:
        """
        Enrich a lead with AI-generated insights.

        Args:
            lead: The lead to enrich
            website_text: Optional scraped text from lead's website (via Firecrawl)
        """
        if not website_text and not lead.industry:
            # Minimal enrichment — just mark as enriched
            self.storage.update_status(lead.email, LeadStatus.ENRICHED)
            return lead

        # Use AI to extract pain points from website or industry
        system = (
            "Проанализируй компанию и определи 3-5 потенциальных болей, "
            "которые можно решить с помощью AI-автоматизации. "
            "Ответь JSON-списком строк. Только JSON-массив, без пояснений."
        )
        context = f"Компания: {lead.company}, отрасль: {lead.industry}"
        if website_text:
            context += f"\nТекст с сайта: {website_text[:2000]}"

        try:
            raw = self.generator._call_claude(system, context, max_tokens=512)
            clean = raw.strip()
            if clean.startswith("```"):
                clean = clean.split("\n", 1)[1].rsplit("```", 1)[0]
            import json
            pain_points = json.loads(clean)
            if isinstance(pain_points, list):
                lead.pain_points = [str(p) for p in pain_points[:5]]
        except Exception:
            pass

        self.storage.update(lead.email, pain_points=lead.pain_points, status=LeadStatus.ENRICHED)
        return lead

    def generate_proposal(self, lead: Lead, template: str = "") -> Dict[str, str]:
        """Generate a personalized proposal for a lead."""
        tmpl = template or LEAD_CONFIG["default_template"]
        proposal = self.generator.generate_proposal(
            lead_name=lead.contact_name,
            company=lead.company,
            industry=lead.industry or "Бизнес",
            pain_points=lead.pain_points,
            template=tmpl,
        )
        return proposal

    def send_proposal(self, lead: Lead, proposal: Dict[str, str]) -> bool:
        """Send the proposal and update lead status."""
        if not self.send_callback:
            print(f"No send callback configured. Proposal for {lead.display_name} NOT sent.")
            return False

        success = self.send_callback(lead, proposal["subject"], proposal["body"])

        if success:
            self.storage.update(
                lead.email,
                status=LeadStatus.PROPOSAL_SENT,
                proposals_sent=lead.proposals_sent + 1,
                last_proposal_date=datetime.now().isoformat(),
                last_proposal_subject=proposal["subject"],
            )
            self.results.append({
                "lead": lead.display_name,
                "email": lead.email,
                "subject": proposal["subject"],
                "status": "sent",
                "timestamp": datetime.now().isoformat(),
            })
            print(f"Sent proposal to {lead.display_name}")
            return True
        else:
            self.results.append({
                "lead": lead.display_name,
                "email": lead.email,
                "status": "failed",
                "timestamp": datetime.now().isoformat(),
            })
            return False

    def send_follow_up(self, lead: Lead) -> bool:
        """Generate and send a follow-up for a non-responsive lead."""
        follow_up = self.generator.generate_follow_up(
            lead_name=lead.contact_name,
            company=lead.company,
            previous_subject=lead.last_proposal_subject,
            follow_up_number=lead.follow_ups_sent + 1,
        )

        if not self.send_callback:
            print(f"No send callback. Follow-up for {lead.display_name} NOT sent.")
            return False

        success = self.send_callback(lead, follow_up["subject"], follow_up["body"])
        if success:
            self.storage.update(
                lead.email,
                follow_ups_sent=lead.follow_ups_sent + 1,
            )
            print(f"Sent follow-up #{lead.follow_ups_sent + 1} to {lead.display_name}")
            return True
        return False

    # ── Batch Operations ────────────────────────────────────────────

    def run_outreach_batch(
        self,
        max_sends: Optional[int] = None,
        template: str = "",
        delay_seconds: int = 5,
    ) -> Dict:
        """
        Run a batch outreach: generate proposals and send to all ready leads.

        Args:
            max_sends: Max proposals to send in this batch
            template: Proposal template key
            delay_seconds: Delay between sends to avoid rate limits

        Returns:
            Batch result summary
        """
        ready = self.storage.get_ready_for_outreach()
        limit = max_sends or LEAD_CONFIG["max_proposals_per_day"]
        batch = ready[:limit]

        sent = 0
        failed = 0

        for lead in batch:
            proposal = self.generate_proposal(lead, template)
            if self.send_proposal(lead, proposal):
                sent += 1
            else:
                failed += 1

            if delay_seconds > 0 and sent + failed < len(batch):
                time.sleep(delay_seconds)

        return {
            "total_ready": len(ready),
            "attempted": len(batch),
            "sent": sent,
            "failed": failed,
        }

    def run_follow_up_batch(self, delay_seconds: int = 5) -> Dict:
        """Send follow-ups to all eligible leads."""
        leads = self.storage.get_ready_for_follow_up(
            max_follow_ups=len(LEAD_CONFIG.get("follow_up_days", [3, 7, 14]))
        )
        sent = 0
        for lead in leads:
            if self.send_follow_up(lead):
                sent += 1
            if delay_seconds > 0:
                time.sleep(delay_seconds)

        return {"eligible": len(leads), "sent": sent}

    def get_funnel_report(self) -> Dict:
        """Get the current funnel statistics."""
        stats = self.storage.get_funnel_stats()
        return {
            "funnel": stats,
            "recent_sends": self.results[-20:],
        }
