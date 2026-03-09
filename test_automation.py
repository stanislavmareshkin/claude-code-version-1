"""
Tests for the AI Social Media Automation + Cold Outreach system.
"""
import csv
import json
import sys
import tempfile
import types
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock

# Bootstrap package
_pkg_dir = Path(__file__).resolve().parent / "ai-social-media-post-automation"
_pkg_name = "ai_social_media_post_automation"
if _pkg_name not in sys.modules:
    pkg = types.ModuleType(_pkg_name)
    pkg.__path__ = [str(_pkg_dir)]
    pkg.__package__ = _pkg_name
    pkg.__file__ = str(_pkg_dir / "__init__.py")
    sys.modules[_pkg_name] = pkg

from ai_social_media_post_automation.leads.models import Lead, LeadStatus
from ai_social_media_post_automation.leads.storage import LeadStorage
from ai_social_media_post_automation.leads.outreach_manager import OutreachManager
from ai_social_media_post_automation.ai_content_generator import AIContentGenerator
from ai_social_media_post_automation.platform_adapters.vk_adapter import VKAdapter
from ai_social_media_post_automation.platform_adapters.email_adapter import EmailAdapter
from ai_social_media_post_automation.platform_adapters.telegram_adapter import TelegramAdapter
from ai_social_media_post_automation.config import SUPPORTED_PLATFORMS, LEAD_CONFIG


def _tmpfile(suffix=".json"):
    f = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    f.close()
    return Path(f.name)


# ── 1. Lead Model ──────────────────────────────────────────────────

def test_lead_model():
    print("TEST: Lead model...", end=" ")
    lead = Lead(
        company="TestCo",
        contact_name="Ivan",
        email="ivan@test.com",
        industry="IT",
    )
    assert lead.status == LeadStatus.NEW
    assert lead.display_name == "Ivan (TestCo)"
    assert lead.proposals_sent == 0

    # to_dict / from_dict roundtrip
    d = lead.to_dict()
    assert d["status"] == "new"
    assert d["company"] == "TestCo"

    lead2 = Lead.from_dict(d)
    assert lead2.company == "TestCo"
    assert lead2.status == LeadStatus.NEW
    assert lead2.email == "ivan@test.com"

    print("PASS")


# ── 2. Lead Storage ────────────────────────────────────────────────

def test_lead_storage():
    print("TEST: LeadStorage CRUD...", end=" ")
    fp = _tmpfile()
    storage = LeadStorage(filepath=fp)

    # Add
    lead = Lead(company="Alpha", contact_name="Anna", email="anna@alpha.com")
    added = storage.add(lead)
    assert added is lead
    assert len(storage.leads) == 1

    # Dedup
    dup = Lead(company="Alpha", contact_name="Anna", email="anna@alpha.com")
    added2 = storage.add(dup)
    assert added2 is lead  # returned existing
    assert len(storage.leads) == 1

    # Find
    found = storage.find_by_email("anna@alpha.com")
    assert found is not None
    assert found.company == "Alpha"

    found_none = storage.find_by_email("nobody@test.com")
    assert found_none is None

    # Update
    storage.update("anna@alpha.com", industry="Retail", status=LeadStatus.ENRICHED)
    assert storage.leads[0].industry == "Retail"
    assert storage.leads[0].status == LeadStatus.ENRICHED

    # Filter
    enriched = storage.filter_by_status(LeadStatus.ENRICHED)
    assert len(enriched) == 1

    # Persistence
    storage2 = LeadStorage(filepath=fp)
    assert len(storage2.leads) == 1
    assert storage2.leads[0].industry == "Retail"

    # Delete
    assert storage.delete("anna@alpha.com")
    assert len(storage.leads) == 0
    assert not storage.delete("nonexistent@test.com")

    # Cleanup
    fp.unlink(missing_ok=True)
    print("PASS")


# ── 3. CSV Import ──────────────────────────────────────────────────

def test_csv_import():
    print("TEST: CSV import...", end=" ")
    csv_file = _tmpfile(suffix=".csv")
    leads_file = _tmpfile()

    # Write test CSV
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["company", "contact_name", "email", "industry", "website"])
        writer.writerow(["CompA", "Petr", "petr@compa.com", "Fintech", "https://compa.com"])
        writer.writerow(["CompB", "Maria", "maria@compb.com", "E-commerce", "https://compb.com"])
        writer.writerow(["CompC", "", "admin@compc.com", "SaaS", ""])  # no contact_name
        writer.writerow(["", "Nobody", "", "", ""])  # missing required fields

    storage = LeadStorage(filepath=leads_file)
    count = storage.import_csv(str(csv_file))

    assert count == 3, f"Expected 3 imports, got {count}"
    assert len(storage.leads) == 3

    # Check contact_name fallback
    compc = storage.find_by_email("admin@compc.com")
    assert compc is not None
    assert compc.contact_name == "CompC"  # falls back to company name

    # Check all sources set
    assert all(l.source == "csv" for l in storage.leads)

    # Re-import — dedup should prevent new adds
    count2 = storage.import_csv(str(csv_file))
    assert count2 == 0
    assert len(storage.leads) == 3

    csv_file.unlink(missing_ok=True)
    leads_file.unlink(missing_ok=True)
    print("PASS")


# ── 4. Funnel Stats ────────────────────────────────────────────────

def test_funnel_stats():
    print("TEST: Funnel stats...", end=" ")
    fp = _tmpfile()
    storage = LeadStorage(filepath=fp)

    for i in range(5):
        storage.add(Lead(company=f"Co{i}", contact_name=f"P{i}", email=f"p{i}@test.com"))

    storage.update_status("p0@test.com", LeadStatus.ENRICHED)
    storage.update_status("p1@test.com", LeadStatus.PROPOSAL_SENT)
    storage.update_status("p2@test.com", LeadStatus.PROPOSAL_SENT)

    stats = storage.get_funnel_stats()
    assert stats["total"] == 5
    assert stats["new"] == 2
    assert stats["enriched"] == 1
    assert stats["proposal_sent"] == 2

    ready = storage.get_ready_for_outreach()
    assert len(ready) == 3  # new(2) + enriched(1)

    follow_ups = storage.get_ready_for_follow_up()
    assert len(follow_ups) == 2  # proposal_sent(2)

    fp.unlink(missing_ok=True)
    print("PASS")


# ── 5. AIContentGenerator (mocked) ─────────────────────────────────

def test_ai_content_generator_mocked():
    print("TEST: AIContentGenerator (mocked)...", end=" ")
    gen = AIContentGenerator()

    mock_response = {
        "content": [{"text": "Test post about AI"}]
    }

    with patch("requests.post") as mock_post:
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: mock_response,
            raise_for_status=lambda: None,
        )

        text = gen.generate_post_text(platform="telegram", theme="AI и автоматизация")
        assert text == "Test post about AI"
        assert mock_post.called

    # Test proposal generation
    mock_proposal = {
        "content": [{"text": '{"subject": "AI для вашего бизнеса", "body": "Здравствуйте, Иван!"}'}]
    }
    with patch("requests.post") as mock_post:
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: mock_proposal,
            raise_for_status=lambda: None,
        )

        proposal = gen.generate_proposal(
            lead_name="Иван",
            company="TestCo",
            industry="IT",
        )
        assert proposal["subject"] == "AI для вашего бизнеса"
        assert "Иван" in proposal["body"] or "Здравствуйте" in proposal["body"]

    # Test follow-up generation
    mock_followup = {
        "content": [{"text": '{"subject": "Re: AI для вашего бизнеса", "body": "Добрый день!"}'}]
    }
    with patch("requests.post") as mock_post:
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: mock_followup,
            raise_for_status=lambda: None,
        )

        followup = gen.generate_follow_up(
            lead_name="Иван",
            company="TestCo",
            previous_subject="AI для вашего бизнеса",
            follow_up_number=1,
        )
        assert "Re:" in followup["subject"] or "AI" in followup["subject"]

    print("PASS")


# ── 6. OutreachManager Pipeline ─────────────────────────────────────

def test_outreach_pipeline():
    print("TEST: OutreachManager pipeline...", end=" ")
    leads_fp = _tmpfile()
    storage = LeadStorage(filepath=leads_fp)

    # Add leads
    storage.add(Lead(company="Acme", contact_name="Bob", email="bob@acme.com", industry="Retail"))
    storage.add(Lead(company="Beta", contact_name="Eve", email="eve@beta.com", industry="SaaS"))

    sent_log = []

    def mock_send(lead, subject, body):
        sent_log.append({"email": lead.email, "subject": subject})
        return True

    gen = AIContentGenerator()

    mock_response = {
        "content": [{"text": '{"subject": "Предложение для Acme", "body": "Тело КП"}'}]
    }

    manager = OutreachManager(
        storage=storage,
        content_generator=gen,
        send_callback=mock_send,
    )

    with patch("requests.post") as mock_post:
        mock_post.return_value = MagicMock(
            status_code=200,
            json=lambda: mock_response,
            raise_for_status=lambda: None,
        )

        result = manager.run_outreach_batch(max_sends=2, delay_seconds=0)

    assert result["sent"] == 2
    assert result["failed"] == 0
    assert len(sent_log) == 2

    # Check leads updated
    acme = storage.find_by_email("bob@acme.com")
    assert acme.status == LeadStatus.PROPOSAL_SENT
    assert acme.proposals_sent == 1

    leads_fp.unlink(missing_ok=True)
    print("PASS")


# ── 7. VK Adapter ──────────────────────────────────────────────────

def test_vk_adapter():
    print("TEST: VKAdapter...", end=" ")
    adapter = VKAdapter({"access_token": "test_token", "group_id": "123456"})

    # Test validation
    valid, err = adapter.validate_content("Тестовый пост")
    assert valid
    assert err is None

    valid, err = adapter.validate_content("")
    assert not valid

    valid, err = adapter.validate_content("x" * 16000)
    assert not valid

    # Test auth
    with patch("requests.get") as mock_get:
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {"response": [{"id": 123}]},
        )
        assert adapter.authenticate()

    # Test publish (VK API uses GET for wall.post via _api_call)
    with patch("requests.get") as mock_get:
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {"response": {"post_id": 456}},
        )
        result = adapter.publish_post("Test post")
        assert result["success"]
        assert result["post_id"] == "456"

    print("PASS")


# ── 8. Email Adapter ───────────────────────────────────────────────

def test_email_adapter():
    print("TEST: EmailAdapter...", end=" ")
    adapter = EmailAdapter({
        "smtp_host": "smtp.test.com",
        "smtp_port": 587,
        "smtp_user": "test@test.com",
        "smtp_password": "pass",
        "from_name": "Test",
        "from_email": "test@test.com",
    })

    # Test validation
    valid, err = adapter.validate_content("Hello body")
    assert valid

    valid, err = adapter.validate_content("")
    assert not valid

    valid, err = adapter.validate_content("   ")
    assert not valid

    # Test send_email (mocked SMTP)
    with patch("smtplib.SMTP") as mock_smtp_class:
        mock_server = MagicMock()
        mock_smtp_class.return_value.__enter__ = MagicMock(return_value=mock_server)
        mock_smtp_class.return_value.__exit__ = MagicMock(return_value=False)

        result = adapter.send_email(
            to_email="client@example.com",
            subject="Тест КП",
            body="Здравствуйте!",
            to_name="Клиент",
        )
        assert result["success"]
        assert result["platform"] == "email"
        assert "client@example.com" in result["to"]

    print("PASS")


# ── 9. Telegram Adapter ────────────────────────────────────────────

def test_telegram_adapter():
    print("TEST: TelegramAdapter...", end=" ")
    adapter = TelegramAdapter({
        "bot_token": "000:XXX",
        "chat_id": "-100123",
    })

    valid, err = adapter.validate_content("Hello")
    assert valid

    valid, err = adapter.validate_content("x" * 5000)
    assert not valid

    print("PASS")


# ── 10. CLI --help ──────────────────────────────────────────────────

def test_cli_help():
    print("TEST: CLI --help...", end=" ")
    from ai_social_media_post_automation.main import main
    import io
    from contextlib import redirect_stdout, redirect_stderr

    old_argv = sys.argv
    sys.argv = ["main.py"]

    out = io.StringIO()
    try:
        with redirect_stdout(out):
            main()
    except SystemExit:
        pass
    finally:
        sys.argv = old_argv

    output = out.getvalue()
    assert "post" in output or "outreach" in output or "usage" in output.lower()
    print("PASS")


# ── Run All ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING ALL TESTS")
    print("=" * 60)

    tests = [
        test_lead_model,
        test_lead_storage,
        test_csv_import,
        test_funnel_stats,
        test_ai_content_generator_mocked,
        test_outreach_pipeline,
        test_vk_adapter,
        test_email_adapter,
        test_telegram_adapter,
        test_cli_help,
    ]

    passed = 0
    failed = 0
    errors = []

    for test_fn in tests:
        try:
            test_fn()
            passed += 1
        except Exception as e:
            failed += 1
            errors.append((test_fn.__name__, str(e)))
            print(f"FAIL: {e}")

    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(tests)}")
    if errors:
        print("\nFailed tests:")
        for name, err in errors:
            print(f"  {name}: {err}")
    print("=" * 60)

    sys.exit(1 if failed > 0 else 0)
