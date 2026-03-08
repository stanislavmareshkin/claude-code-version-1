"""
AI Content Generator using Claude API.
Generates social media posts and commercial proposals.
"""
import json
import os
from typing import Dict, List, Optional
from pathlib import Path

import requests

from .config import AI_CONFIG, PLATFORM_CONFIGS, CONTENT_GENERATION


class AIContentGenerator:
    """
    Generates content using Claude API (Anthropic).
    Supports social media posts and personalized commercial proposals.
    """

    def __init__(self):
        self.api_key = AI_CONFIG["anthropic_api_key"]
        self.model = AI_CONFIG["model"]
        self.api_url = "https://api.anthropic.com/v1/messages"

    def _call_claude(self, system_prompt: str, user_prompt: str, max_tokens: int = 2048) -> str:
        """Send a request to Claude API and return the text response."""
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
        }

        resp = requests.post(self.api_url, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data["content"][0]["text"]

    # ── Social Media Posts ──────────────────────────────────────────

    def generate_post_text(
        self,
        platform: str,
        theme: str,
        max_length: Optional[int] = None,
        tone: str = "professional",
        language: str = "ru",
    ) -> str:
        """
        Generate a social media post.

        Args:
            platform: Target platform (telegram, vk, etc.)
            theme: Content theme
            max_length: Max characters (default from platform config)
            tone: Writing tone
            language: Output language

        Returns:
            Generated post text
        """
        if max_length is None:
            config = PLATFORM_CONFIGS.get(platform, {})
            max_length = config.get("max_text_length", 2000)

        system_prompt = (
            f"Ты — профессиональный SMM-копирайтер. "
            f"Пиши посты на языке: {language}. "
            f"Тон: {tone}. Платформа: {platform}. "
            f"Максимальная длина: {max_length} символов. "
            f"Пост должен быть вовлекающим, с призывом к действию. "
            f"Добавь 3-5 релевантных хэштегов в конце."
        )

        user_prompt = f"Напиши пост на тему: {theme}"

        return self._call_claude(system_prompt, user_prompt, max_tokens=1024)

    def generate_image(self, prompt: str) -> Optional[Path]:
        """
        Generate an image for a post.
        Currently a placeholder — integrate DALL-E or Midjourney via Make.com.
        """
        # TODO: integrate OpenAI DALL-E or UserAPI.ai (Midjourney)
        return None

    # ── Commercial Proposals ────────────────────────────────────────

    def generate_proposal(
        self,
        lead_name: str,
        company: str,
        industry: str,
        pain_points: Optional[List[str]] = None,
        our_services: Optional[str] = None,
        template: str = "b2b_services",
        language: str = "ru",
    ) -> Dict[str, str]:
        """
        Generate a personalized commercial proposal.

        Args:
            lead_name: Contact person name
            company: Company name
            industry: Company industry
            pain_points: Known pain points (from enrichment)
            our_services: Description of our services
            template: Proposal template key
            language: Output language

        Returns:
            Dict with 'subject' and 'body' keys
        """
        pains_text = ""
        if pain_points:
            pains_text = f"Известные боли клиента: {', '.join(pain_points)}. "

        services_text = our_services or (
            "AI-автоматизация маркетинга и контента, "
            "чат-боты, автопостинг в соцсетях, аналитика"
        )

        system_prompt = (
            f"Ты — эксперт по B2B-продажам и AI-автоматизации. "
            f"Язык: {language}. "
            f"Пиши кратко, персонализированно, без воды. "
            f"Формат ответа — JSON с полями: subject (тема письма, до 78 символов), "
            f"body (тело письма/сообщения, 150-300 слов). "
            f"Наши услуги: {services_text}."
        )

        user_prompt = (
            f"Составь персонализированное коммерческое предложение.\n"
            f"Имя контакта: {lead_name}\n"
            f"Компания: {company}\n"
            f"Отрасль: {industry}\n"
            f"{pains_text}"
            f"Шаблон стиля: {template}\n"
            f"Отвечай ТОЛЬКО валидным JSON."
        )

        raw = self._call_claude(system_prompt, user_prompt, max_tokens=1024)

        # Parse JSON from response
        try:
            # Handle markdown code blocks
            clean = raw.strip()
            if clean.startswith("```"):
                clean = clean.split("\n", 1)[1].rsplit("```", 1)[0]
            result = json.loads(clean)
            return {"subject": result.get("subject", ""), "body": result.get("body", "")}
        except (json.JSONDecodeError, IndexError):
            # Fallback: use raw text as body
            return {"subject": f"Предложение для {company}", "body": raw}

    def generate_follow_up(
        self,
        lead_name: str,
        company: str,
        previous_subject: str,
        follow_up_number: int = 1,
    ) -> Dict[str, str]:
        """
        Generate a follow-up message for a lead that didn't respond.

        Args:
            lead_name: Contact name
            company: Company name
            previous_subject: Subject of the original proposal
            follow_up_number: Which follow-up (1st, 2nd, 3rd)

        Returns:
            Dict with 'subject' and 'body'
        """
        system_prompt = (
            "Ты — эксперт по follow-up письмам в B2B-продажах. "
            "Пиши кратко, вежливо, с ценностью. Не давай, не навязывай. "
            "Формат ответа — JSON: {\"subject\": \"...\", \"body\": \"...\"}. "
            "Тело письма — 50-100 слов максимум."
        )

        user_prompt = (
            f"Follow-up #{follow_up_number} для {lead_name} из {company}.\n"
            f"Предыдущая тема: {previous_subject}\n"
            f"Отвечай ТОЛЬКО валидным JSON."
        )

        raw = self._call_claude(system_prompt, user_prompt, max_tokens=512)
        try:
            clean = raw.strip()
            if clean.startswith("```"):
                clean = clean.split("\n", 1)[1].rsplit("```", 1)[0]
            result = json.loads(clean)
            return {"subject": result.get("subject", ""), "body": result.get("body", "")}
        except (json.JSONDecodeError, IndexError):
            return {
                "subject": f"Re: {previous_subject}",
                "body": raw,
            }
