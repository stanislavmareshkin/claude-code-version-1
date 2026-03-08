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
| Генерация текста | **Claude Sonnet** | Anthropic API (`claude-sonnet-4-5-20241022`) |
| Генерация картинок | **DALL-E 3** | OpenAI API (возвращает URL картинки) |

## Шаг 1: Импорт blueprint

1. Откройте [Make.com](https://make.com) → **Scenarios** → **Create a new scenario**
2. Нажмите **"..."** (три точки внизу) → **Import Blueprint**
3. Загрузите файл `make-blueprint-autoposting.json`

## Шаг 2: Настройка переменных сценария

Перейдите в **Scenario settings** → **Variables** и создайте:

| Переменная | Описание | Где получить |
|---|---|---|
| `ANTHROPIC_API_KEY` | Ключ Anthropic API (Claude) | https://console.anthropic.com/settings/keys |
| `OPENAI_API_KEY` | Ключ OpenAI (DALL-E 3) | https://platform.openai.com/api-keys |
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

- Claude генерирует `image_prompt` на английском — это промпт для DALL-E 3, который возвращает URL картинки
- VK: для постинга с картинкой потребуется дополнительный модуль загрузки фото через `photos.getWallUploadServer`
- VC.ru и Дзен используют HTTP-модули, нативных модулей Make для них нет
- API-ключи хранятся в переменных сценария Make.com для безопасности

---

# Дополнительные сценарии (отдельные blueprint'ы)

Помимо основного сценария, в репозитории есть 3 отдельных blueprint'а для каждой платформы.

## Сценарий 1: Автопост VK (`make-blueprint-vk-clean.json`)

```
[Inoreader RSS] → [HTML→Text] → [GPT: пост 500 симв.] → [GPT: промпт Midjourney] → [Midjourney] → [Sleep 300с] → [Status] → [Random 1-4] → [Upscale] → [Sleep 60с] → [Status] → [Router]
                                                                                                                                                                                          └── [GPT: пост VK 1200 симв.] → [Скачать картинку] → [VK: getWallUploadServer] → [Upload фото] → [saveWallPhoto] → [wall.post]
```

**Что делает:** Читает новости из Inoreader (папка RSS), суммаризирует через GPT-4o-mini, генерирует картинку через Midjourney (userapi.ai), загружает фото в VK и публикует пост от имени группы.

**Требуемые подключения (Connections):**
- Inoreader
- OpenAI (GPT-4o-mini)
- UserAPI.ai (Midjourney)

**Плейсхолдеры для замены:**
- `YOUR_USER_ID` / `YOUR_FOLDER` — ID пользователя и папки в Inoreader
- `YOUR_VK_GROUP_ID` — ID группы ВКонтакте
- `YOUR_VK_ACCESS_TOKEN` — токен доступа VK API

## Сценарий 2: Автопост VC.ru (`make-blueprint-vc-webhook-clean.json`)

```
[Google Sheets: тема A1] → [Google Sheets: ключи B1] → [Perplexity: статья 8-12K] → [GPT: редактор] → [Markdown→HTML] → [GPT: description]
                                                          ↓                                                                       ↓
                                                     [GPT: промпт] → [Midjourney] → [Sleep 200с] → [Status] → [Random] → [Upscale] → [Sleep 60с] → [Status] → [Скачать] → [Placid: обложка] → [Скачать обложку]
                                                                                                                                                                                                         ↓
                                                                                                                                                                              [GPT: заголовок] → [GPT: лид] → [HTTP POST → VC webhook]
```

**Что делает:** Берёт тему и ключевые слова из Google Sheets, генерирует статью через Perplexity AI, редактирует через GPT, создаёт обложку через Midjourney + Placid, публикует на VC.ru через webhook.

**Требуемые подключения (Connections):**
- Google Sheets (OAuth)
- Perplexity AI
- OpenAI (GPT-4o-mini)
- UserAPI.ai (Midjourney)
- Placid (генерация обложки из шаблона)

**Плейсхолдеры для замены:**
- `YOUR_SPREADSHEET_ID` — ID Google Sheets таблицы
- `YOUR-VC-PUBLISHER-ENDPOINT` — URL вашего webhook-эндпоинта для публикации на VC.ru
- Placid template ID (`5bjy4n310nocu`) — замените на свой шаблон

## Сценарий 3: Автопост Дзен через WordPress (`make-blueprint-dzen-wordpress-clean.json`)

```
[Google Sheets: тема A1] → [Google Sheets: ключи B1] → [Perplexity: статья] → [GPT: редактор] → [GPT: промпты 20шт] → [Markdown→HTML ×2]
                                                                                                                              ↓
                                                          [GPT: description] → [GPT: промпт фольклор] → [Midjourney] → [Sleep 210с] → [Status] → [Random] → [Upscale] → [Sleep 40с] → [Status] → [Скачать]
                                                                                                                                                                                                      ↓
                                                                                                                                              [GPT: имя файла] → [WordPress: загрузить медиа] → [WordPress: создать пост] → [Google Sheets: удалить строку]
```

**Что делает:** Берёт тему из Google Sheets, генерирует статью через Perplexity + GPT, создаёт обложку в стиле русского фольклора через Midjourney, публикует на WordPress. Через RSS WordPress → контент попадает в Яндекс Дзен. После публикации удаляет использованную строку из таблицы.

**Требуемые подключения (Connections):**
- Google Sheets (OAuth)
- Perplexity AI
- OpenAI (GPT-4o-mini)
- UserAPI.ai (Midjourney)
- WordPress (REST API)

**Плейсхолдеры для замены:**
- `YOUR_SPREADSHEET_ID` — ID Google Sheets таблицы
- WordPress connection — настроить подключение к вашему сайту

## Импорт дополнительных сценариев

Для каждого сценария:
1. Make.com → **Scenarios** → **Create a new scenario**
2. **"..."** → **Import Blueprint**
3. Загрузите соответствующий `.json` файл
4. Настройте все **Connections** (подключения к сервисам)
5. Замените плейсхолдеры (`YOUR_*`) на реальные значения
6. **Run once** для тестирования
7. Включите расписание
