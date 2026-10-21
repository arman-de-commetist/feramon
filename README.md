# MONA Pheromone — сайт на Django

## Запуск (Windows)

```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python manage.py migrate
.venv\Scripts\python manage.py createsuperuser
.venv\Scripts\python manage.py runserver
```

- Сайт: http://127.0.0.1:8000/
- Админка: http://127.0.0.1:8000/admin/ — цены, объёмы, ноты, отзывы, заказы и их статусы.

## Страницы

- Магазин: `/` главная, `/aromaty/` каталог, `/aromat/<slug>/` аромат, `/obemy/` сравнение объёмов,
  `/test/` тест «какой аромат ваш», `/zakaz/` выбор аромата и подарка, `/korzina/` корзина,
  `/oformlenie/` оформление, `/spasibo/<id>/` спасибо за заказ
- Подарки: `/akcii/`, `/dyson-airwrap/`, `/podarki/` и `/podarki/<slug>/`
- О нас: `/o-brende/`, `/feromony/`, `/otzyvy/` (с формой), `/galereya/`, `/blog/` и `/blog/<slug>/`
- Покупателям: `/dostavka-i-oplata/`, `/oplata/`, `/garantiya-i-vozvrat/`, `/voprosy/`, `/kontakty/`
- Документы: `/politika-konfidencialnosti/`, `/oferta/` (черновики — заполните реквизиты в `shop/templates/shop/legal/`)

## Цены и подарки (админка → Парфюмы → Варианты)

- У каждого объёма: цена, старая цена, тип подарка и количество.
- 30 мл — 1 французский парфюм, 50 мл — 2 парфюма, 100 мл — Dyson Airwrap (цвет + имя на корпусе).
- Подарочные парфюмы — админка → «Парфюмы в подарок». Отзывы с сайта приходят скрытыми — опубликуйте в админке.
- Статьи блога и фото галереи — админка → «Блог» и «Галерея».

## Языки (RU / EN / ҚАЗ)

- Переключатель в шапке, выбор запоминается в cookie; по умолчанию — русский.
- Названия, описания и ноты ароматов переводятся в админке (блоки «English» и «Қазақша»).
- Тексты страниц — в `locale/en/LC_MESSAGES/django.po` и `locale/kk/LC_MESSAGES/django.po`.
  После правки выполните `python manage.py compiletranslations` и перезапустите сервер.

## Структура

- `mona/` — настройки проекта
- `shop/models.py` — Парфюм, Варианты (объём/цена в ₸), Ноты, Отзывы, Заказы
- `shop/templates/shop/` — HTML-шаблоны
- `shop/static/shop/` — стили и JS
- `shop/migrations/0002_seed_data.py` — начальные данные (ноты, цены, отзывы)

## Менеджеры и WhatsApp

- Админка → «Менеджеры»: имя, телефон/WhatsApp, фото, языки, часы. Галочка «Получает новых клиентов» — очередь.
- Заказы и чаты с сайта распределяются по очереди; у заказа видно назначенного менеджера.
- Кнопки «Написать менеджеру» открывают WhatsApp с готовым текстом по странице (`/napisat/`).

## Уведомления о заказах в Telegram (необязательно)

1. Создайте бота через @BotFather и получите токен.
2. Напишите боту любое сообщение, узнайте свой chat_id (например, через @userinfobot).
3. Задайте переменные окружения и проверьте:

```bash
set TELEGRAM_BOT_TOKEN=123456:ABC...
set TELEGRAM_CHAT_ID=123456789
python manage.py testtelegram
```

## Запуск в интернете (хостинг)

Проект готов к Railway / Render / любому VPS: есть `Procfile`, сервер `gunicorn`, статика через WhiteNoise.

Переменные окружения:

| Переменная | Значение |
|---|---|
| `DJANGO_DEBUG` | `0` |
| `DJANGO_SECRET_KEY` | длинная случайная строка — без неё сайт специально не запустится |
| `DJANGO_ALLOWED_HOSTS` | `mona.kz,www.mona.kz` |
| `DJANGO_CSRF_ORIGINS` | `https://mona.kz,https://www.mona.kz` |
| `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` | для уведомлений о заказах (необязательно) |
| `DJANGO_SSL_REDIRECT` | `0`, только если хостинг сам не даёт HTTPS |
| `DJANGO_SERVE_MEDIA` | `0`, если фото из `media/` раздаёт nginx |

При каждом выпуске (`release` в Procfile) выполняются миграции, сборка переводов и `collectstatic`.
Важно: база `db.sqlite3` и папка `media/` должны лежать на постоянном диске хостинга (volume),
иначе заказы и загруженные фото пропадут при перезапуске. Для большого магазина лучше PostgreSQL.

Сгенерировать секретный ключ:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

## SEO

- `/sitemap.xml` и `/robots.txt` — отправьте карту сайта в Google Search Console и Яндекс.Вебмастер.
- У каждой страницы есть превью для WhatsApp/Instagram (фото, название), у ароматов — данные о цене для Google.
- Сайт можно «установить» на телефон как приложение (иконка MONA).
