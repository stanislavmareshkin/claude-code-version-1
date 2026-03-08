"""
Platform adapters for social media automation.
"""
from .base import PlatformAdapter
from .telegram_adapter import TelegramAdapter
from .vk_adapter import VKAdapter
from .email_adapter import EmailAdapter

__all__ = [
    "PlatformAdapter",
    "TelegramAdapter",
    "VKAdapter",
    "EmailAdapter",
]


