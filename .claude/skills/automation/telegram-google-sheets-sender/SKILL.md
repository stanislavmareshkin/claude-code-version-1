---
name: telegram-google-sheets-sender
description: Рассылка сообщений через Telegram Bot API с данными из Google Sheets (service account). Читает строки из таблицы, отправляет сообщения, записывает статусы обратно.
---

# Telegram Google Sheets Sender

Автоматизация рассылки сообщений в Telegram с использованием Google Sheets как источника данных.

## Возможности

- Чтение получателей и текстов из Google Таблицы
- Отправка через Telegram Bot API (sendMessage)
- Поддержка Parse_Mode (MarkdownV2, HTML)
- Запись статусов (sent / error) обратно в таблицу
- Пропуск уже отправленных строк
- Режим DRY_RUN для тестирования без отправки
- Задержка между сообщениями для соблюдения rate limits

## Предварительная настройка

### Google Cloud

1. Создать проект в Google Cloud Console
2. Включить **Google Sheets API**
3. Включить **Google Drive API**
4. Создать **Service Account**
5. Скачать JSON-ключ

### Google Таблица

Поделиться таблицей с `client_email` из JSON-файла service account (роль: Редактор).

Обязательные колонки в первой строке:

| Колонка | Обязательная | Описание |
|---------|-------------|----------|
| `Chat_ID` | да | Telegram chat ID получателя |
| `Message` | да | Текст сообщения (до 4096 символов) |
| `Parse_Mode` | нет | `MarkdownV2` или `HTML` |
| `Status` | нет | Заполняется скриптом: `sent` / `error` |
| `Sent_At` | нет | Заполняется скриптом: дата и время отправки |
| `Last_Error` | нет | Заполняется скриптом: текст ошибки |

### Telegram

- Создать бота через [@BotFather](https://t.me/BotFather)
- Получатели должны первыми написать боту `/start`

## Использование

```bash
# Установка зависимостей
pip install gspread requests

# Запуск
export TELEGRAM_BOT_TOKEN="123456789:ABCDEF..."
export GOOGLE_SHEET_URL="https://docs.google.com/spreadsheets/d/..."
python .claude/skills/automation/telegram-google-sheets-sender/scripts/sender_google_sheet.py
```

## Переменные окружения

| Переменная | Обязательная | По умолчанию | Описание |
|-----------|-------------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | да | — | Токен Telegram-бота |
| `GOOGLE_SHEET_URL` | да | — | URL Google Таблицы |
| `GOOGLE_WORKSHEET_NAME` | нет | `Sheet1` | Имя листа |
| `GOOGLE_SERVICE_ACCOUNT_FILE` | нет | `service_account.json` | Путь к JSON-ключу |
| `DELAY_BETWEEN_MESSAGES` | нет | `1` | Задержка между сообщениями (секунды) |
| `REQUEST_TIMEOUT` | нет | `15` | Таймаут HTTP-запросов (секунды) |
| `SKIP_ALREADY_SENT` | нет | `true` | Пропускать строки со статусом `sent` |
| `DRY_RUN` | нет | `false` | Тестовый прогон без реальной отправки |

## Безопасность

- Не коммитьте `service_account.json` и токен бота в репозиторий
- Используйте переменные окружения или `.env` файл (добавлен в `.gitignore`)
- Service account ключи должны храниться в безопасном месте
