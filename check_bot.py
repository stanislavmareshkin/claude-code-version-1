#!/usr/bin/env python3
"""
Диагностический скрипт для проверки Telegram-бота @AstrologLamabot
Запустите: python3 check_bot.py
"""

import urllib.request
import json
import sys

BOT_TOKEN = "8741884500:AAH_dNb192db7gM7ZpmA7LzHljGFX_nJKMU"
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"


def api_call(method):
    """Вызов метода Telegram Bot API."""
    url = f"{API_BASE}/{method}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return {"ok": False, "error": f"HTTP {e.code}", "description": body}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def main():
    print("=" * 50)
    print("Диагностика бота @AstrologLamabot")
    print("=" * 50)

    # 1. Проверка токена (getMe)
    print("\n1. Проверка токена (getMe)...")
    result = api_call("getMe")
    if result.get("ok"):
        bot = result["result"]
        print(f"   ✅ Токен валиден")
        print(f"   Имя бота: {bot.get('first_name')}")
        print(f"   Username: @{bot.get('username')}")
        print(f"   Bot ID: {bot.get('id')}")
    else:
        print(f"   ❌ Токен невалиден или бот заблокирован!")
        print(f"   Ошибка: {result.get('error', '')} {result.get('description', '')}")
        print("\n   Возможные причины:")
        print("   - Токен был отозван через @BotFather")
        print("   - Бот был удалён")
        print("   Решение: Создайте новый токен через @BotFather -> /mybots -> @AstrologLamabot -> API Token -> Revoke/Generate")
        sys.exit(1)

    # 2. Проверка webhook
    print("\n2. Проверка Webhook (getWebhookInfo)...")
    result = api_call("getWebhookInfo")
    if result.get("ok"):
        info = result["result"]
        webhook_url = info.get("url", "")
        if webhook_url:
            print(f"   Webhook URL: {webhook_url}")
            print(f"   Ожидающие обновления: {info.get('pending_update_count', 0)}")
            last_error = info.get("last_error_message")
            last_error_date = info.get("last_error_date")
            if last_error:
                print(f"   ❌ Последняя ошибка: {last_error}")
                print(f"   Дата ошибки: {last_error_date}")
                print("\n   Возможные причины:")
                print("   - Webhook URL недоступен (сервер выключен, SSL-сертификат истёк)")
                print("   - Сервер отвечает ошибкой (500, 502, etc.)")
                print("   Решение: Проверьте, что сервер запущен и доступен по указанному URL")
            else:
                print("   ✅ Webhook работает без ошибок")
        else:
            print("   ℹ️  Webhook не установлен (бот использует polling или не настроен)")
            print("   Если бот должен работать через webhook — его нужно установить заново")
    else:
        print(f"   Ошибка: {result}")

    # 3. Проверка получения обновлений (только если нет webhook)
    if not webhook_url:
        print("\n3. Проверка обновлений (getUpdates)...")
        result = api_call("getUpdates?limit=3&timeout=3")
        if result.get("ok"):
            updates = result.get("result", [])
            print(f"   Получено обновлений: {len(updates)}")
            if updates:
                for upd in updates[-3:]:
                    msg = upd.get("message", {})
                    text = msg.get("text", "(нет текста)")
                    user = msg.get("from", {}).get("first_name", "?")
                    print(f"   - От {user}: {text[:50]}")
            print("   ✅ Бот может получать сообщения через polling")
        else:
            print(f"   ❌ Не удалось получить обновления: {result}")

    # 4. Тест отправки сообщения самому себе
    print("\n4. Попытка отправить тестовое сообщение...")
    print("   ℹ️  Для теста отправьте /start боту, затем запустите скрипт снова")

    print("\n" + "=" * 50)
    print("Диагностика завершена")
    print("=" * 50)
    print("\nОсновные причины, почему бот может не работать:")
    print("1. Сервер/хостинг, на котором работает бот, выключен или упал")
    print("2. Процесс бота остановился (ошибка в коде, нехватка памяти)")
    print("3. Webhook URL стал недоступен (истёк SSL, сменился IP)")
    print("4. Токен был отозван или изменён")
    print("5. Бот заблокирован Telegram за нарушение правил")


if __name__ == "__main__":
    main()
