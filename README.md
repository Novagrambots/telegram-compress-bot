# bot_4_compress — Telegram-бот для сжатия видео и фотографий

Бот для сжатия медиафайлов через Telegram.
Aiogram 3 + SQLAlchemy + PostgreSQL + ffmpeg + Pillow + Local Bot API.

## Возможности

- 🎬 Сжатие видео (H.265 / libx265, MP4)
- 📷 Сжатие фотографий (JPEG, с поддержкой HEIC на входе)
- 🚀 **Файлы до 2 ГБ** через Local Bot API
- ⚖️ Три пресета сжатия:
  - **Слабое** — CRF 28, без даунскейла, без изменения FPS
  - **Среднее** — CRF 32, даунскейл до 720p, FPS до 30
  - **Сильное** — CRF 38, даунскейл до 480p, FPS до 30
- 🖼 Для фото — JPEG quality 85 / 70 / 50 по пресету
- 🔄 EXIF auto-rotate, RGBA → RGB на белом фоне, прогрессивный JPEG
- 🏷 Рекламная подпись `🤖 Сжато ботом @username` под каждым результатом
- 📢 Обязательная подписка на каналы (middleware)
- 👨‍💼 Админ-панель: статистика, управление каналами, рассылка (text/photo/video)
- 🌐 Мультиязычность: 🇷🇺 Русский · 🇺🇿 O'zbek (latin) · 🇺🇿 Ўзбек (kirill) · 🇬🇧 English
- ⏱ Rate limit — 5 запросов/мин на юзера (in-memory, с фоновой очисткой)
- 🧹 Фоновая очистка `/tmp/compress_bot` (старше 30 мин) и `bot-api-data` (старше 1 часа) каждые 5 минут
- 🔒 Защита от двойного клика на кнопку пресета через per-user `asyncio.Lock`
- ⚙️ Семафор на 2 параллельных libx265-задачи (CPU-bound, без GPU)
- ⚡ `uvloop` для ускорения asyncio в 2-4 раза

## Деплой (Docker)

```bash
# 1. Склонировать и настроить
cp .env.example .env
# заполнить .env (BOT_TOKEN, API_ID, API_HASH, DB_*, ADMIN_IDS)

# 2. Запустить
docker compose up -d --build

# 3. Логи
docker compose logs -f bot
```

### Сервисы docker-compose

| Сервис     | Образ                             | Назначение                                  |
|------------|-----------------------------------|---------------------------------------------|
| `bot`      | собирается из `Dockerfile`        | Python-приложение                           |
| `bot-api`  | `aiogram/telegram-bot-api:latest` | Local Bot API — файлы до 2 ГБ (порт `8081`) |
| `postgres` | `postgres:16-alpine`              | База данных (порт `5432`)                   |
| `autoheal` | `willfarrell/autoheal:latest`     | Авто-рестарт unhealthy контейнеров (opt-in label) |

## Локальная разработка

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# заполнить .env
python -m bot.main
```

Для локального запуска `bot-api` не обязателен (бот будет работать через
обычный Bot API с лимитом 20 МБ на входной файл).

## Переменные окружения (`.env`)

| Переменная                  | Описание                                                             | Обязательно |
|-----------------------------|----------------------------------------------------------------------|-------------|
| `BOT_TOKEN`                 | Токен от @BotFather                                                  | ✅          |
| `BOT_USERNAME`              | Юзернейм бота без `@`. Если не задан — определяется автоматически через `get_me()` | ❌ |
| `API_ID`, `API_HASH`        | Креды с https://my.telegram.org — **нужны только для Local Bot API** | ✅ (если поднят `bot-api`) |
| `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` | Параметры PostgreSQL                            | ✅          |
| `ADMIN_IDS`                 | Telegram-ID админов через запятую (доступ к /admin)                  | ❌          |
| `ADMIN_USERNAME`            | Username админа для контакта в справке                               | ❌          |

**`BOT_API_URL`** задаётся напрямую в `docker-compose.yml`
(`environment.BOT_API_URL=http://bot-api:8081`) — это тех-параметр обвязки,
а не настройка бизнес-логики.

## Структура проекта

```
bot/
├── main.py              — entrypoint, роутеры, мидлвари, фоновая очистка
├── config.py            — pydantic-settings из .env
├── i18n.py              — переводы (ru/uz_latn/uz_cyrl/en) + detect_language()
├── emojis.py            — премиум-эмодзи (E_ID и E)
├── database/
│   ├── __init__.py      — engine + async_session
│   ├── models.py        — User / Channel
│   └── crud.py          — все запросы к БД
├── handlers/
│   ├── start.py         — /start, главное меню, смена языка, профиль, подписка
│   ├── compress.py      — приём файла, выбор пресета, сжатие, отправка результата
│   └── admin.py         — /admin: статистика, каналы, рассылка
├── middlewares/
│   ├── subscription.py  — обязательная подписка на каналы
│   └── rate_limit.py    — 5 запросов/мин + фоновая очистка
├── keyboards/
│   ├── inline.py        — пользовательские клавиатуры
│   └── admin.py         — админские клавиатуры
├── services/
│   └── compressor.py    — ffmpeg/Pillow, пресеты, classify_error()
└── utils/
    ├── commands.py      — персональные и глобальные меню команд Telegram
    └── fsm_cleanup.py   — очистка tmp_dir + сброс FSM
```

## Docker-образ

`python:3.12-slim` + `ffmpeg` (libx265 / AAC) + `libheif-dev` (для pillow-heif).

## Python-зависимости

- `aiogram==3.26.0` — Telegram Bot API
- `SQLAlchemy==2.0.38` + `asyncpg==0.30.0` — PostgreSQL async ORM
- `pillow==11.2.1` + `pillow-heif==0.22.0` — обработка изображений (HEIC, JPEG)
- `pydantic-settings==2.8.1` — конфигурация из `.env`
- `alembic==1.14.1` — миграции БД (пока не используется, таблицы создаются через `create_all()`)
- `uvloop==0.22.1` — ускорение asyncio

## Команды бота

| Команда     | Доступ  | Описание                                   |
|-------------|---------|--------------------------------------------|
| `/start`    | Все     | Запуск бота, приветствие, главное меню     |
| `/menu`     | Все     | Главное меню                               |
| `/profile`  | Все     | Профиль юзера (ID, счётчик сжатий)         |
| `/help`     | Все     | Справка                                    |
| `/language` | Все     | Смена языка                                |
| `/cancel`   | Все     | Сбросить текущее состояние FSM             |
| `/admin`    | Админы  | Админ-панель                               |

## Полезные команды для диагностики

```bash
# логи бота
docker compose logs -f bot

# использование дисков (tmp + Local Bot API)
docker compose exec bot du -sh /tmp/compress_bot /var/lib/telegram-bot-api

# перезапуск только бота после изменений
docker compose up -d --build bot

# выполнение ffprobe внутри контейнера
docker compose exec bot ffprobe -v error -show_format -show_streams /path/to/file.mp4
```
