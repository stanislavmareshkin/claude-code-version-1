"""
Main entry point for the social media automation + lead outreach system.

Usage:
    python main.py post                    # schedule posts
    python main.py post --immediate        # publish now
    python main.py outreach --csv leads.csv  # cold outreach
    python main.py outreach --dry-run      # preview without sending
    python main.py follow-up               # send follow-ups
    python main.py funnel                  # show lead funnel
    python main.py report                  # performance report
    python main.py continuous              # run both continuously
"""
import argparse
import os
import sys
from pathlib import Path

# Run via: python run.py (from repo root)
# The package uses relative imports — run.py bootstraps the package.
try:
    from ai_social_media_post_automation.orchestrator import SocialMediaOrchestrator
except ImportError:
    # Fallback for direct execution with package dir on sys.path
    from orchestrator import SocialMediaOrchestrator  # type: ignore


def _build_credentials() -> dict:
    """Build credentials dict from environment variables."""
    creds = {}
    # Telegram
    tg_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    tg_chat = os.environ.get("TELEGRAM_CHAT_ID", "")
    if tg_token and tg_chat:
        creds["telegram"] = {"bot_token": tg_token, "chat_id": tg_chat}
    # VK
    vk_token = os.environ.get("VK_ACCESS_TOKEN", "")
    vk_group = os.environ.get("VK_GROUP_ID", "")
    if vk_token and vk_group:
        creds["vk"] = {"access_token": vk_token, "group_id": vk_group}
    # Email
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_pass = os.environ.get("SMTP_PASSWORD", "")
    if smtp_user and smtp_pass:
        creds["email"] = {
            "smtp_host": os.environ.get("SMTP_HOST", "smtp.gmail.com"),
            "smtp_port": int(os.environ.get("SMTP_PORT", "587")),
            "smtp_user": smtp_user,
            "smtp_password": smtp_pass,
            "from_name": os.environ.get("EMAIL_FROM_NAME", ""),
            "from_email": smtp_user,
        }
    return creds


def cmd_post(orchestrator: SocialMediaOrchestrator, args):
    """Generate and publish social media posts."""
    if not orchestrator.adapters:
        print("No platforms authenticated. Check your .env credentials.")
        return

    print(f"Platforms: {', '.join(orchestrator.adapters.keys())}")

    if args.immediate:
        platform = args.platform or list(orchestrator.adapters.keys())[0]
        print(f"\nPublishing immediately to {platform}...")
        result = orchestrator.publish_immediately(platform, theme=args.theme)
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Published! Post ID: {result.get('post_id')}")
    else:
        count = args.count or 3
        print(f"\nScheduling {count} posts...")
        batch = orchestrator.generate_and_schedule_batch(count=count)
        print(f"Scheduled {batch['scheduled_count']} posts")
        for p in batch["posts"]:
            print(f"  - {p['platform']} at {p['scheduled_time']}")


def cmd_outreach(orchestrator: SocialMediaOrchestrator, args):
    """Run cold outreach campaign."""
    manager = orchestrator.create_outreach_manager()

    # Import leads if CSV provided
    if args.csv:
        count = manager.import_leads_csv(args.csv)
        print(f"Imported {count} leads from {args.csv}")

    # Show funnel
    stats = manager.storage.get_funnel_stats()
    print(f"\nFunnel: {stats}")

    ready = manager.storage.get_ready_for_outreach()
    print(f"Ready for outreach: {len(ready)} leads")

    if not ready:
        print("No leads ready. Import a CSV with --csv or add leads manually.")
        return

    if args.dry_run:
        print("\n[DRY RUN] Would send proposals to:")
        for lead in ready[:args.limit]:
            print(f"  - {lead.display_name} <{lead.email}>")
        return

    # Run batch
    print(f"\nSending proposals (max {args.limit})...")
    result = manager.run_outreach_batch(max_sends=args.limit, template=args.template)
    print(f"\nResults: {result['sent']} sent, {result['failed']} failed "
          f"(out of {result['total_ready']} ready)")


def cmd_follow_up(orchestrator: SocialMediaOrchestrator, _args):
    """Send follow-ups to non-responsive leads."""
    manager = orchestrator.create_outreach_manager()
    eligible = manager.storage.get_ready_for_follow_up()
    print(f"Leads eligible for follow-up: {len(eligible)}")

    if not eligible:
        return

    result = manager.run_follow_up_batch()
    print(f"Follow-ups sent: {result['sent']}/{result['eligible']}")


def cmd_funnel(orchestrator: SocialMediaOrchestrator, _args):
    """Show lead funnel statistics."""
    manager = orchestrator.create_outreach_manager()
    report = manager.get_funnel_report()

    print("\n=== Lead Funnel ===")
    for status, count in report["funnel"].items():
        bar = "#" * count
        print(f"  {status:20s} | {count:4d} {bar}")

    if report["recent_sends"]:
        print(f"\nRecent sends ({len(report['recent_sends'])}):")
        for r in report["recent_sends"][-5:]:
            print(f"  {r['timestamp'][:16]} | {r['status']:6s} | {r['lead']}")


def cmd_report(orchestrator: SocialMediaOrchestrator, args):
    """Show posting performance report."""
    days = args.days or 30
    report = orchestrator.get_performance_report(days=days)
    print(f"\n=== Performance Report ({days} days) ===")
    for platform, stats in report["platforms"].items():
        print(f"\n  {platform.upper()}:")
        print(f"    Posts: {stats['total_posts']}, Engagement: {stats['engagement_rate']:.2%}")
        print(f"    Avg likes: {stats['average_likes']:.0f}, Avg views: {stats['average_views']:.0f}")

    recs = orchestrator.optimize_content_strategy()
    if recs["suggestions"]:
        print("\nRecommendations:")
        for s in recs["suggestions"]:
            print(f"  - {s}")


def cmd_continuous(orchestrator: SocialMediaOrchestrator, args):
    """Run both posting and outreach continuously."""
    print("Starting continuous mode (posting + outreach)...")
    orchestrator.run_continuous_mode(check_interval_minutes=args.interval or 180)


def main():
    parser = argparse.ArgumentParser(
        description="AI Social Media Automation + Cold Outreach",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # post
    p_post = subparsers.add_parser("post", help="Generate and publish posts")
    p_post.add_argument("--immediate", "-i", action="store_true", help="Publish now")
    p_post.add_argument("--platform", "-p", help="Target platform")
    p_post.add_argument("--theme", "-t", help="Content theme")
    p_post.add_argument("--count", "-c", type=int, help="Number of posts to schedule")

    # outreach
    p_out = subparsers.add_parser("outreach", help="Cold outreach campaign")
    p_out.add_argument("--csv", help="Path to CSV with leads")
    p_out.add_argument("--limit", type=int, default=10, help="Max proposals to send")
    p_out.add_argument("--template", default="", help="Proposal template key")
    p_out.add_argument("--dry-run", action="store_true", help="Preview without sending")

    # follow-up
    subparsers.add_parser("follow-up", help="Send follow-ups")

    # funnel
    subparsers.add_parser("funnel", help="Show lead funnel stats")

    # report
    p_rep = subparsers.add_parser("report", help="Show performance report")
    p_rep.add_argument("--days", type=int, default=30)

    # continuous
    p_cont = subparsers.add_parser("continuous", help="Run continuously")
    p_cont.add_argument("--interval", type=int, default=180, help="Check interval (minutes)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Load .env if python-dotenv available
    try:
        from dotenv import load_dotenv
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            load_dotenv(env_path)
    except ImportError:
        pass

    credentials = _build_credentials()
    orchestrator = SocialMediaOrchestrator(credentials)

    commands = {
        "post": cmd_post,
        "outreach": cmd_outreach,
        "follow-up": cmd_follow_up,
        "funnel": cmd_funnel,
        "report": cmd_report,
        "continuous": cmd_continuous,
    }

    handler = commands.get(args.command)
    if handler:
        handler(orchestrator, args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
