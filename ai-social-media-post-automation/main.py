"""
Main entry point for the social media automation system.
"""
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from social_media_automation.orchestrator import SocialMediaOrchestrator
from social_media_automation.config import DATA_DIR


def main():
    """
    Main function to run the social media automation system.
    
    Example usage:
    1. Set up credentials for platforms
    2. Initialize orchestrator
    3. Generate and schedule content
    4. Run scheduler
    """
    
    # Example credentials (in production, use environment variables or secure storage)
    credentials = {
        "telegram": {
            "bot_token": os.environ.get("TELEGRAM_BOT_TOKEN", ""),
            "chat_id": os.environ.get("TELEGRAM_CHAT_ID", ""),
        },
        "vk": {
            "access_token": os.environ.get("VK_ACCESS_TOKEN", ""),
            "group_id": os.environ.get("VK_GROUP_ID", ""),
        },
    }
    
    # Initialize orchestrator
    orchestrator = SocialMediaOrchestrator(credentials)
    
    if not orchestrator.adapters:
        print("❌ No platforms authenticated. Please check your credentials.")
        return
    
    print(f"✓ Initialized with {len(orchestrator.adapters)} platform(s)")
    
    # Example: Generate and schedule a batch of posts
    print("\n📝 Generating content batch...")
    batch_result = orchestrator.generate_and_schedule_batch(count=5)
    print(f"✓ Scheduled {batch_result['scheduled_count']} posts")
    
    # Example: Publish one post immediately
    print("\n🚀 Publishing immediate post...")
    if orchestrator.adapters:
        platform = list(orchestrator.adapters.keys())[0]
        immediate_result = orchestrator.publish_immediately(platform)
        if "error" not in immediate_result:
            print(f"✓ Published to {platform}")
        else:
            print(f"❌ Error: {immediate_result.get('error')}")
    
    # Get performance report
    print("\n📊 Generating performance report...")
    report = orchestrator.get_performance_report(days=7)
    print(f"✓ Analyzed {sum(s['total_posts'] for s in report['platforms'].values())} posts")
    
    # Get optimization recommendations
    print("\n💡 Getting optimization recommendations...")
    recommendations = orchestrator.optimize_content_strategy()
    print("Recommendations:")
    for suggestion in recommendations.get("suggestions", []):
        print(f"  • {suggestion}")
    
    # Uncomment to run in continuous mode:
    # print("\n🔄 Starting continuous mode...")
    # orchestrator.run_continuous_mode(check_interval_minutes=180)


if __name__ == "__main__":
    main()

