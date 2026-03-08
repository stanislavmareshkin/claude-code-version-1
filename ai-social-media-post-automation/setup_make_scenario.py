#!/usr/bin/env python3
"""
Скрипт автоматической настройки сценария Make.com
Создаёт сценарий, импортирует blueprint и настраивает переменные.

Запуск:
  python3 setup_make_scenario.py
"""

import json
import sys
import os
import urllib.request
import urllib.error

# Загрузка .env файла
def load_dotenv(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key.strip(), value)

load_dotenv()

# ============================================================
# КОНФИГУРАЦИЯ — заполните свои значения
# ============================================================

MAKE_API_TOKEN = os.getenv("MAKE_API_TOKEN", "")
MAKE_ZONE = os.getenv("MAKE_ZONE", "eu2")

# API-ключи загружаются из .env файла (см. .env.example)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GOOGLE_AI_API_KEY = os.getenv("GOOGLE_AI_API_KEY", "")

# Telegram (обязательно)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# VK (опционально)
VK_ACCESS_TOKEN = os.getenv("VK_ACCESS_TOKEN", "")
VK_GROUP_ID = os.getenv("VK_GROUP_ID", "")

# VC.ru (опционально)
VC_API_TOKEN = os.getenv("VC_API_TOKEN", "")
VC_SUBSITE_ID = os.getenv("VC_SUBSITE_ID", "")

# Яндекс Дзен (опционально)
DZEN_API_TOKEN = os.getenv("DZEN_API_TOKEN", "")

# ============================================================

BASE_URL = f"https://{MAKE_ZONE}.make.com/api/v2"
HEADERS = {
    "Authorization": f"Token {MAKE_API_TOKEN}",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}


def api_request(method, path, data=None):
    """Выполняет запрос к Make.com API."""
    url = f"{BASE_URL}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"  Ошибка {e.code}: {error_body}")
        sys.exit(1)


def main():
    print("=" * 50)
    print("  Настройка сценария Make.com")
    print("=" * 50)

    # 1. Получаем организацию и команду
    print("\n[1/5] Получаю информацию об аккаунте...")
    orgs = api_request("GET", "/organizations")
    if not orgs.get("organizations"):
        print("  Не найдено организаций. Проверьте токен и регион.")
        sys.exit(1)
    org_id = orgs["organizations"][0]["id"]
    print(f"  Организация: {orgs['organizations'][0]['name']} (ID: {org_id})")

    teams = api_request("GET", f"/organizations/{org_id}/teams")
    team_id = teams["teams"][0]["id"]
    print(f"  Команда ID: {team_id}")

    # 2. Создаём сценарий
    print("\n[2/5] Создаю сценарий...")

    # Загружаем blueprint из файла
    blueprint_path = os.path.join(os.path.dirname(__file__), "make-blueprint-autoposting.json")
    with open(blueprint_path, "r", encoding="utf-8") as f:
        blueprint = json.load(f)

    scenario_data = {
        "teamId": team_id,
        "name": blueprint["name"],
        "blueprint": json.dumps(blueprint),
        "scheduling": {
            "type": "interval",
            "interval": 180
        }
    }
    result = api_request("POST", "/scenarios", scenario_data)
    scenario = result.get("scenario", result)
    scenario_id = scenario["id"]
    print(f"  Сценарий создан: ID {scenario_id}")
    print(f"  URL: https://{MAKE_ZONE}.make.com/scenarios/{scenario_id}")

    # 3. Настраиваем переменные (Data Stores / Keys)
    print("\n[3/5] Настраиваю переменные сценария...")

    variables = {
        "ANTHROPIC_API_KEY": ANTHROPIC_API_KEY,
        "GOOGLE_AI_API_KEY": GOOGLE_AI_API_KEY,
        "TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN,
        "TELEGRAM_CHAT_ID": TELEGRAM_CHAT_ID,
        "VK_ACCESS_TOKEN": VK_ACCESS_TOKEN,
        "VK_GROUP_ID": VK_GROUP_ID,
        "VC_API_TOKEN": VC_API_TOKEN,
        "VC_SUBSITE_ID": VC_SUBSITE_ID,
        "DZEN_API_TOKEN": DZEN_API_TOKEN,
    }

    # Фильтруем пустые
    active_vars = {k: v for k, v in variables.items() if v}

    if active_vars:
        var_update = {
            "blueprint": json.dumps({
                **blueprint,
                "metadata": {
                    **blueprint.get("metadata", {}),
                    "variables": [
                        {"name": k, "value": v}
                        for k, v in active_vars.items()
                    ]
                }
            })
        }
        api_request("PATCH", f"/scenarios/{scenario_id}", var_update)
        print(f"  Установлено {len(active_vars)} переменных:")
        for k in active_vars:
            masked = active_vars[k][:8] + "..." if len(active_vars[k]) > 8 else "***"
            print(f"    - {k}: {masked}")
    else:
        print("  Переменные не заданы — заполните их в скрипте!")

    # 4. Проверяем статус
    print("\n[4/5] Проверяю сценарий...")
    check = api_request("GET", f"/scenarios/{scenario_id}")
    scenario_info = check.get("scenario", check)
    print(f"  Статус: {scenario_info.get('islinked', 'unknown')}")
    print(f"  Модулей: {scenario_info.get('usedPackages', 'N/A')}")

    # 5. Готово
    print("\n[5/5] Готово!")
    print(f"\n  Откройте сценарий в браузере:")
    print(f"  https://{MAKE_ZONE}.make.com/scenarios/{scenario_id}")
    print(f"\n  Следующие шаги:")
    print(f"  1. Откройте сценарий и проверьте модули")
    print(f"  2. Заполните пустые переменные (если есть)")
    print(f"  3. Нажмите 'Run once' для тестового запуска")
    print(f"  4. Включите сценарий (ON)")
    print("=" * 50)


if __name__ == "__main__":
    main()
