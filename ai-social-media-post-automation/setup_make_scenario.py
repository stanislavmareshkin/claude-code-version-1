#!/usr/bin/env python3
"""
Скрипт автоматической настройки ВСЕХ сценариев Make.com
Создаёт сценарии из всех blueprint-файлов, импортирует их и настраивает переменные.

Запуск:
  python3 setup_make_scenario.py          # все blueprint'ы
  python3 setup_make_scenario.py --only autoposting cold-outreach  # выборочно
"""

import glob
import json
import sys
import os
import time
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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

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

# Email SMTP
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

# ============================================================

# Все blueprint-файлы и их настройки интервалов (в минутах)
BLUEPRINTS = [
    {"file": "make-blueprint-autoposting.json",           "interval": 180},
    {"file": "make-blueprint-vk-clean.json",              "interval": 180},
    {"file": "make-blueprint-vc-webhook-clean.json",      "interval": 0},    # webhook, без интервала
    {"file": "make-blueprint-dzen-wordpress-clean.json",   "interval": 360},
    {"file": "make-blueprint-cold-outreach.json",          "interval": 60},
    {"file": "make-blueprint-follow-up.json",              "interval": 1440}, # раз в сутки
]

BASE_URL = f"https://{MAKE_ZONE}.make.com/api/v2"
HEADERS = {
    "Authorization": f"Token {MAKE_API_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

MAX_RETRIES = 4
RETRY_DELAYS = [2, 4, 8, 16]


def api_request(method, path, data=None):
    """Выполняет запрос к Make.com API с повторными попытками при сетевых ошибках."""
    url = f"{BASE_URL}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)

    for attempt in range(MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            if e.code == 401:
                print(f"  Ошибка 401: Неверный API-токен Make.com.")
                print(f"  Текущий токен: {MAKE_API_TOKEN[:12]}...")
                print()
                print("  Как получить правильный токен:")
                print(f"  1. Откройте https://{MAKE_ZONE}.make.com")
                print("  2. Войдите в аккаунт")
                print("  3. Нажмите на аватар (внизу слева) → Profile")
                print("  4. Перейдите во вкладку API Access")
                print("  5. Нажмите 'Add token', выберите нужные scopes (все), нажмите Save")
                print("  6. Скопируйте токен и вставьте в .env файл как MAKE_API_TOKEN=...")
                sys.exit(1)
            elif e.code == 403:
                print(f"  Ошибка 403: Доступ запрещён.")
                try:
                    err = json.loads(error_body)
                    if err.get("code") == 1010 or "cloudflare" in error_body.lower():
                        print("  Запрос заблокирован Cloudflare.")
                        print(f"  Проверьте, что регион MAKE_ZONE={MAKE_ZONE} указан верно.")
                except (json.JSONDecodeError, KeyError):
                    pass
                print(f"  Ответ: {error_body}")
                sys.exit(1)
            else:
                raise RuntimeError(f"HTTP {e.code}: {error_body}")
        except (urllib.error.URLError, ConnectionError, OSError) as e:
            if attempt < MAX_RETRIES:
                delay = RETRY_DELAYS[attempt]
                print(f"  Сетевая ошибка: {e}. Повтор через {delay}с ({attempt + 1}/{MAX_RETRIES})...")
                time.sleep(delay)
            else:
                print(f"  Сетевая ошибка после {MAX_RETRIES} попыток: {e}")
                sys.exit(1)


def validate_config():
    """Проверяет конфигурацию перед запуском."""
    if not MAKE_API_TOKEN:
        print("  ОШИБКА: MAKE_API_TOKEN не задан в .env файле.")
        print(f"  Получите токен: https://{MAKE_ZONE}.make.com → Profile → API Access")
        sys.exit(1)

    import re
    if re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', MAKE_API_TOKEN, re.IGNORECASE):
        print("  ПРЕДУПРЕЖДЕНИЕ: MAKE_API_TOKEN похож на UUID, а не на токен Make.com.")
        print("  Токены Make.com обычно длиннее и имеют другой формат.")
        print(f"  Получите правильный токен: https://{MAKE_ZONE}.make.com → Profile → API Access")
        print()

    if not ANTHROPIC_API_KEY:
        print("  ПРЕДУПРЕЖДЕНИЕ: ANTHROPIC_API_KEY не задан — Claude не будет работать в сценариях.")
    if not GOOGLE_AI_API_KEY:
        print("  ПРЕДУПРЕЖДЕНИЕ: GOOGLE_AI_API_KEY не задан — генерация изображений не будет работать.")
    if not TELEGRAM_BOT_TOKEN:
        print("  ПРЕДУПРЕЖДЕНИЕ: TELEGRAM_BOT_TOKEN не задан — Telegram-публикация не будет работать.")


def get_variables():
    """Возвращает словарь всех непустых переменных для инъекции в blueprint."""
    all_vars = {
        "ANTHROPIC_API_KEY": ANTHROPIC_API_KEY,
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "GOOGLE_AI_API_KEY": GOOGLE_AI_API_KEY,
        "TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN,
        "TELEGRAM_CHAT_ID": TELEGRAM_CHAT_ID,
        "VK_ACCESS_TOKEN": VK_ACCESS_TOKEN,
        "VK_GROUP_ID": VK_GROUP_ID,
        "VC_API_TOKEN": VC_API_TOKEN,
        "VC_SUBSITE_ID": VC_SUBSITE_ID,
        "DZEN_API_TOKEN": DZEN_API_TOKEN,
        "SMTP_HOST": SMTP_HOST,
        "SMTP_USER": SMTP_USER,
        "SMTP_PASSWORD": SMTP_PASSWORD,
    }
    return {k: v for k, v in all_vars.items() if v}


def deploy_blueprint(team_id, bp_config, active_vars, index, total):
    """Разворачивает один blueprint как сценарий Make.com."""
    filename = bp_config["file"]
    interval = bp_config["interval"]
    blueprint_path = os.path.join(os.path.dirname(__file__), filename)

    if not os.path.exists(blueprint_path):
        print(f"  ПРОПУСК: файл {filename} не найден")
        return None

    with open(blueprint_path, "r", encoding="utf-8") as f:
        blueprint = json.load(f)

    name = blueprint.get("name", filename)
    print(f"\n{'─' * 50}")
    print(f"  [{index}/{total}] {name}")
    print(f"  Файл: {filename}")

    # Настраиваем scheduling
    if interval > 0:
        scheduling = {"type": "interval", "interval": interval}
    else:
        scheduling = {"type": "indefinitely"}

    # Создаём сценарий
    scenario_data = {
        "teamId": team_id,
        "name": name,
        "blueprint": json.dumps(blueprint),
        "scheduling": scheduling,
    }

    try:
        result = api_request("POST", "/scenarios", scenario_data)
    except RuntimeError as e:
        print(f"  ОШИБКА при создании: {e}")
        return None

    scenario = result.get("scenario", result)
    scenario_id = scenario["id"]
    print(f"  Создан: ID {scenario_id}")

    # Инъекция переменных в blueprint
    if active_vars:
        updated_blueprint = json.loads(json.dumps(blueprint))
        if "metadata" not in updated_blueprint:
            updated_blueprint["metadata"] = {}
        updated_blueprint["metadata"]["variables"] = [
            {"name": k, "value": v}
            for k, v in active_vars.items()
        ]
        try:
            api_request("PATCH", f"/scenarios/{scenario_id}", {
                "blueprint": json.dumps(updated_blueprint)
            })
            print(f"  Переменных: {len(active_vars)}")
        except RuntimeError as e:
            print(f"  ПРЕДУПРЕЖДЕНИЕ: не удалось обновить переменные: {e}")

    url = f"https://{MAKE_ZONE}.make.com/scenarios/{scenario_id}"
    print(f"  URL: {url}")
    return {"id": scenario_id, "name": name, "url": url, "file": filename}


def main():
    # Парсим аргументы --only
    only_filter = None
    if "--only" in sys.argv:
        idx = sys.argv.index("--only")
        only_filter = sys.argv[idx + 1:]
        if not only_filter:
            print("  Использование: python3 setup_make_scenario.py --only autoposting cold-outreach")
            sys.exit(1)

    print("=" * 50)
    print("  Размещение ВСЕХ сценариев на Make.com")
    print("=" * 50)

    validate_config()

    # Фильтруем blueprint'ы если указан --only
    blueprints = BLUEPRINTS
    if only_filter:
        blueprints = [
            bp for bp in BLUEPRINTS
            if any(keyword in bp["file"] for keyword in only_filter)
        ]
        if not blueprints:
            print(f"  Не найдено blueprint'ов, подходящих под фильтр: {only_filter}")
            sys.exit(1)
        print(f"\n  Фильтр: {only_filter}")

    print(f"  Blueprint'ов к развёртыванию: {len(blueprints)}")

    # 1. Получаем организацию и команду
    print("\n[1/3] Получаю информацию об аккаунте...")
    orgs = api_request("GET", "/organizations")
    if not orgs.get("organizations"):
        print("  Не найдено организаций. Проверьте токен и регион.")
        sys.exit(1)
    org_id = orgs["organizations"][0]["id"]
    print(f"  Организация: {orgs['organizations'][0]['name']} (ID: {org_id})")

    teams = api_request("GET", f"/organizations/{org_id}/teams")
    team_id = teams["teams"][0]["id"]
    print(f"  Команда ID: {team_id}")

    # 2. Разворачиваем все blueprint'ы
    print(f"\n[2/3] Создаю {len(blueprints)} сценариев...")

    active_vars = get_variables()
    results = []

    for i, bp_config in enumerate(blueprints, 1):
        result = deploy_blueprint(team_id, bp_config, active_vars, i, len(blueprints))
        if result:
            results.append(result)

    # 3. Итоговый отчёт
    print(f"\n{'=' * 50}")
    print(f"[3/3] ГОТОВО! Создано сценариев: {len(results)}/{len(blueprints)}")
    print(f"{'=' * 50}")

    if results:
        print("\n  Созданные сценарии:")
        for r in results:
            print(f"    ✓ {r['name']}")
            print(f"      {r['url']}")

    failed = len(blueprints) - len(results)
    if failed:
        print(f"\n  Не удалось создать: {failed}")

    print(f"\n  Следующие шаги:")
    print(f"  1. Откройте каждый сценарий и проверьте модули")
    print(f"  2. Настройте подключения (connections) для каждого модуля")
    print(f"  3. Нажмите 'Run once' для тестового запуска")
    print(f"  4. Включите сценарии (ON)")
    print("=" * 50)


if __name__ == "__main__":
    main()
