# Инструкция по импорту blueprint в Make.com

## Схема сценария

```
[Scheduler] → [Claude Sonnet 4.6] → [Parse Claude] → [Parse Post JSON] → [Imagen 3.0] → [Parse Image] → [Router]
                 (Anthropic API)                                            (Google AI)                      ├── Telegram (sendPhoto + текст)
                                                                                                             ├── VK (wall.post)
                                                                                                             ├── VC.ru (entry/create)
                                                                                                             └── Яндекс Дзен (publication)
```

## Используемые AI-модели

| Задача | Модель | API |
|---|---|---|
| Генерация текста | **Claude Sonnet 4.6** | Anthropic API (`claude-sonnet-4-6`) |
| Генерация картинок | **Imagen 3.0 (Nano Banana 2)** | Google Generative Language API |

## Шаг 1: Импорт blueprint

1. Откройте [Make.com](https://make.com) → **Scenarios** → **Create a new scenario**
2. Нажмите **"..."** (три точки внизу) → **Import Blueprint**
3. Загрузите файл `make-blueprint-autoposting.json`

## Шаг 2: Настройка переменных сценария

Перейдите в **Scenario settings** → **Variables** и создайте:

| Переменная | Описание | Где получить |
|---|---|---|
| `ANTHROPIC_API_KEY` | Ключ Anthropic API (Claude) | https://console.anthropic.com/settings/keys |
| `GOOGLE_AI_API_KEY` | Ключ Google AI (Imagen) | https://aistudio.google.com/apikey |
| `TELEGRAM_BOT_TOKEN` | Токен Telegram бота | @BotFather в Telegram |
| `TELEGRAM_CHAT_ID` | ID канала/чата | Бот @userinfobot или @getmyid_bot |
| `VK_ACCESS_TOKEN` | Токен VK API | https://dev.vk.com → Мои приложения |
| `VK_GROUP_ID` | ID группы ВК | В URL группы или через API |
| `VC_API_TOKEN` | Токен vc.ru | Настройки профиля → API |
| `VC_SUBSITE_ID` | ID подсайта | В URL вашего блога на vc.ru |
| `DZEN_API_TOKEN` | Токен Дзен | Яндекс Вебмастер → Дзен API |

## Шаг 4: Как работает сценарий

1. **Scheduler** запускает сценарий каждые 3 часа
2. **Claude Sonnet 4.6** генерирует текст поста (заголовок, короткий/длинный текст, хештеги, промпт для картинки)
3. **Imagen 3.0** генерирует картинку по промпту из Claude
4. **Router** параллельно отправляет пост на все 4 платформы:
   - **Telegram** — фото + подпись (sendPhoto API)
   - **VK** — текстовый пост (wall.post)
   - **VC.ru** — статья (entry/create)
   - **Яндекс Дзен** — публикация (article)

## Шаг 4: Тестирование

1. Нажмите **Run once** для тестового запуска
2. Проверьте, что Claude возвращает валидный JSON
3. Проверьте, что Imagen генерирует картинку
4. Проверьте каждую ветку роутера

## Шаг 5: Активация

1. Убедитесь, что тест прошёл
2. Включите **Scheduling** (по умолчанию: каждые 3 часа)
3. Нажмите **ON**

## Примечания

- Claude Sonnet 4.6 генерирует `image_prompt` на английском — это промпт для Imagen
- VK: для постинга с картинкой потребуется дополнительный модуль загрузки фото через `photos.getWallUploadServer`
- VC.ru и Дзен используют HTTP-модули, нативных модулей Make для них нет
- API-ключи хранятся в переменных сценария Make.com для безопасности
