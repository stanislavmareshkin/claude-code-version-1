"""
Configuration for the social media automation and lead outreach system.
"""
import os
from pathlib import Path

# === Directories ===

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CONTENT_DIR = DATA_DIR / "content"
LEADS_DIR = DATA_DIR / "leads"
ANALYTICS_DIR = DATA_DIR / "analytics"

for d in [DATA_DIR, CONTENT_DIR, LEADS_DIR, ANALYTICS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# === AI Models ===

AI_CONFIG = {
    "anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY", ""),
    "model": os.environ.get("AI_MODEL", "claude-sonnet-4-20250514"),
    "max_tokens": 2048,
    "temperature": 0.7,
}

# === Supported Platforms ===

SUPPORTED_PLATFORMS = ["telegram", "vk", "email"]

# === Content Generation ===

CONTENT_GENERATION = {
    "content_themes": [
        "AI и автоматизация",
        "Маркетинг и продвижение",
        "Бизнес и стартапы",
        "Технологии и тренды",
        "Продуктивность",
        "Кейсы и результаты",
    ],
    "max_posts_per_day": 3,
    "image_generation": False,  # Enable when DALL-E/Midjourney configured
    "default_language": "ru",
}

# === Platform Configs ===

PLATFORM_CONFIGS = {
    "telegram": {
        "max_text_length": 4096,
        "max_caption_length": 1024,
        "max_images": 10,
        "optimal_post_time": "09:00-12:00, 18:00-21:00",
        "supports_scheduling": False,
        "supports_markdown": True,
    },
    "vk": {
        "max_text_length": 15895,
        "max_images": 10,
        "optimal_post_time": "10:00-13:00, 19:00-22:00",
        "supports_scheduling": True,
        "api_version": "5.199",
    },
    "email": {
        "max_subject_length": 78,
        "optimal_send_time": "09:00-11:00, 14:00-16:00",
        "batch_size": 50,
        "delay_between_emails_sec": 5,
    },
}

# === Scheduling ===

SCHEDULING = {
    "check_interval_seconds": 60,
    "max_posts_per_day_per_platform": 3,
    "min_interval_between_posts_hours": 2,
}

# === Analytics ===

ANALYTICS = {
    "retention_days": 90,
    "update_interval_hours": 6,
}

# === Lead Outreach ===

LEAD_CONFIG = {
    "statuses": ["new", "enriched", "proposal_sent", "opened", "replied", "deal", "rejected"],
    "max_proposals_per_day": 50,
    "follow_up_days": [3, 7, 14],
    "proposal_templates": {
        "b2b_services": "Предлагаем автоматизацию процессов с помощью AI",
        "b2b_marketing": "Увеличьте конверсию с AI-контентом для соцсетей",
        "b2b_consulting": "Консультация по внедрению AI в бизнес-процессы",
    },
    "default_template": "b2b_services",
}

# === Email SMTP ===

EMAIL_CONFIG = {
    "smtp_host": os.environ.get("SMTP_HOST", "smtp.gmail.com"),
    "smtp_port": int(os.environ.get("SMTP_PORT", "587")),
    "smtp_user": os.environ.get("SMTP_USER", ""),
    "smtp_password": os.environ.get("SMTP_PASSWORD", ""),
    "from_name": os.environ.get("EMAIL_FROM_NAME", ""),
    "from_email": os.environ.get("SMTP_USER", ""),
    "reply_to": os.environ.get("EMAIL_REPLY_TO", ""),
}
