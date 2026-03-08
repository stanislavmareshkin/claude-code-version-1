# Social Media Automation System

A comprehensive AI-powered social media automation system that generates, schedules, and publishes content across multiple platforms.

## Features

- 🤖 **AI Content Generation**: Uses GPT-4/GPT-3.5 to generate platform-optimized content
- 📸 **Image Generation**: Creates visuals using DALL-E 3 or Stable Diffusion
- 📅 **Smart Scheduling**: Automatically schedules posts at optimal times for each platform
- 📊 **Analytics & Optimization**: Tracks performance and optimizes content strategy
- 🔌 **Multi-Platform Support**: Extensible adapter system for various social media platforms

## Supported Platforms

- ✅ Telegram
- 🔄 Twitter/X (adapter structure ready)
- 🔄 Yandex Dzen
- 🔄 WordPress
- 🔄 Instagram
- 🔄 Facebook

## Installation

1. **Clone or navigate to the project directory**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
# Required for AI content generation
export OPENAI_API_KEY="your-openai-api-key"

# Platform credentials
export TELEGRAM_BOT_TOKEN="your-telegram-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"
export VK_ACCESS_TOKEN="your-vk-access-token"
export VK_GROUP_ID="your-group-id"
```

## Quick Start

### Basic Usage

```python
from social_media_automation.orchestrator import SocialMediaOrchestrator

# Set up credentials
credentials = {
    "telegram": {
        "bot_token": "your-bot-token",
        "chat_id": "your-chat-id",
    },
    "vk": {
        "access_token": "your-access-token",
        "group_id": "your-group-id",
    },
}

# Initialize
orchestrator = SocialMediaOrchestrator(credentials)

# Generate and schedule posts
orchestrator.generate_and_schedule_batch(count=10)

# Publish immediately
orchestrator.publish_immediately("telegram", theme="business_tips")

# Get performance report
report = orchestrator.get_performance_report(days=30)
print(report)
```

### Running the Main Script

```bash
python -m social_media_automation.main
```

### Continuous Automation Mode

```python
# Run continuously, generating content every 3 hours
orchestrator.run_continuous_mode(check_interval_minutes=180)
```

## Architecture

```
social_media_automation/
├── config.py                 # Configuration settings
├── ai_content_generator.py   # AI content generation
├── scheduler.py              # Content scheduling
├── analytics.py             # Performance tracking
├── orchestrator.py           # Main coordinator
├── main.py                   # Entry point
└── platform_adapters/
    ├── base.py               # Base adapter class
    ├── telegram_adapter.py   # Telegram implementation
    ├── vk_adapter.py         # VK implementation
    └── ...                   # Other platform adapters
```

## Key Components

### 1. AI Content Generator
- Generates platform-optimized text content
- Creates images using AI
- Adapts content between platforms
- Optimizes based on performance data

### 2. Platform Adapters
- Abstract base class for extensibility
- Platform-specific implementations
- Handles authentication and publishing
- Fetches analytics data

### 3. Scheduler
- Smart scheduling based on optimal posting times
- Batch content generation
- Queue management
- Persistent storage

### 4. Analytics Tracker
- Performance metrics tracking
- Platform statistics
- Theme performance analysis
- Top content identification

### 5. Orchestrator
- Coordinates all components
- Manages platform connections
- Generates content batches
- Provides optimization recommendations

## Configuration

Edit `config.py` to customize:

- **Content themes**: Types of content to generate
- **Posting frequency**: Posts per day
- **Platform settings**: Character limits, optimal times
- **AI models**: Which models to use
- **Scheduling**: Timezone, intervals

## Adding New Platforms

1. Create a new adapter class inheriting from `PlatformAdapter`:

```python
from platform_adapters.base import PlatformAdapter

class NewPlatformAdapter(PlatformAdapter):
    def authenticate(self) -> bool:
        # Implement authentication
        pass
    
    def publish_post(self, text, images, scheduled_time):
        # Implement publishing
        pass
    
    def get_analytics(self, post_id, start_date, end_date):
        # Implement analytics fetching
        pass
```

2. Register it in `orchestrator.py`:

```python
adapter_classes = {
    "newplatform": NewPlatformAdapter,
    # ...
}
```

## API Keys Required

- **OpenAI API**: For content generation (GPT-4, DALL-E 3)
- **Platform APIs**: Each platform requires its own credentials
  - Telegram: Bot token from @BotFather
  - VK: Access token from VK API
  - Twitter: API keys from Twitter Developer Portal
  - etc.

## Cost Considerations

- **OpenAI API**: ~$0.03-0.06 per post (GPT-4) or ~$0.002 (GPT-3.5)
- **DALL-E 3**: ~$0.04-0.08 per image
- **Platform APIs**: Most are free, some have rate limits

For 10 posts/day with images: ~$0.50-1.00/day or ~$15-30/month

## Advanced Features

### Custom Content Themes
Add new themes in `config.py` and the AI will generate content accordingly.

### Performance-Based Optimization
The system automatically identifies:
- Best performing platforms
- Best performing content themes
- Optimal posting times
- Content style preferences

### Multi-Language Support
The AI generator can create content in any language by adjusting prompts.

## Limitations & Notes

1. **Rate Limits**: Each platform has API rate limits
2. **Content Quality**: AI-generated content may need human review
3. **Compliance**: Ensure content complies with platform policies
4. **Instagram**: May have restrictions in some regions
5. **Scheduling**: Some platforms don't support native scheduling (requires external scheduler)

## Future Enhancements

- [ ] Web dashboard for management
- [ ] Database storage instead of JSON
- [ ] Video content generation
- [ ] A/B testing framework
- [ ] Multi-language content
- [ ] Integration with more platforms
- [ ] Advanced analytics dashboard
- [ ] Content calendar visualization

## License

This is a template/example implementation. Customize as needed for your use case.

## Support

For issues or questions, refer to the platform-specific API documentation:
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [VK API](https://dev.vk.com/api)
- [Twitter API](https://developer.twitter.com/en/docs)
- [OpenAI API](https://platform.openai.com/docs)



