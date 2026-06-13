#!/usr/bin/env python3
"""
SkillHunt Telegram Bot — API сервер + бот для мини-приложения
=============================================================
Запуск:
  export BOT_TOKEN="YOUR_BOT_TOKEN"
  export WEBAPP_URL="https://yourdomain.com"  # URL мини-приложения
  export API_SECRET="your-random-secret"      # Секрет для API
  python bot.py

Архитектура:
  - aiohttp сервер обслуживает API + отдаёт HTML мини-приложения
  - aiogram бот обрабатывает Telegram команды
  - SQLite хранит данные пользователей, заказов, откликов
  - Мини-приложение получает данные через API и tg.initDataUnsafe
"""

import os
import json
import time
import hashlib
import hmac
import asyncio
import logging
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

from aiohttp import web
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    WebAppInfo, Message
)

# ── Конфигурация ──
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
WEBAPP_URL = os.environ.get("WEBAPP_URL", "http://localhost:8080")
API_SECRET = os.environ.get("API_SECRET", "skillhunt-secret-key")
API_PORT = int(os.environ.get("API_PORT", "8080"))
DB_PATH = os.environ.get("DB_PATH", "skillhunt.db")
ADMIN_IDS = [int(x) for x in os.environ.get("ADMIN_IDS", "").split(",") if x.strip()]

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("skillhunt")

# ── База данных ──
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            photo_url TEXT,
            language_code TEXT DEFAULT 'ru',
            spec TEXT DEFAULT '',
            about TEXT DEFAULT '',
            timezone TEXT DEFAULT '',
            rate REAL DEFAULT 0,
            balance INTEGER DEFAULT 0,
            subscription_plan TEXT DEFAULT 'free',
            subscription_started_at TEXT,
            trial_started_at TEXT,
            trial_offer_shown INTEGER DEFAULT 0,
            monthly_app_count INTEGER DEFAULT 0,
            monthly_app_reset TEXT,
            ai_proposal_count INTEGER DEFAULT 0,
            saved_count INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now')),
            last_active_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            budget_min INTEGER DEFAULT 0,
            budget_max INTEGER DEFAULT 0,
            currency TEXT DEFAULT 'USD',
            client_name TEXT,
            client_rating REAL DEFAULT 0,
            client_orders INTEGER DEFAULT 0,
            posted_at TEXT DEFAULT (datetime('now')),
            match_score INTEGER DEFAULT 0,
            level TEXT DEFAULT 'middle',
            job_type TEXT DEFAULT 'remote',
            skills TEXT DEFAULT '[]',
            description TEXT DEFAULT '',
            is_active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            job_id INTEGER NOT NULL,
            cover_letter TEXT DEFAULT '',
            ai_generated INTEGER DEFAULT 0,
            status TEXT DEFAULT 'sent',
            applied_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (job_id) REFERENCES jobs(id),
            UNIQUE(user_id, job_id)
        );

        CREATE TABLE IF NOT EXISTS saved_jobs (
            user_id INTEGER NOT NULL,
            job_id INTEGER NOT NULL,
            saved_at TEXT DEFAULT (datetime('now')),
            PRIMARY KEY (user_id, job_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        );

        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            progress INTEGER DEFAULT 50,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );

        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT DEFAULT '',
            skills TEXT DEFAULT '',
            color TEXT DEFAULT 'primary',
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );

        CREATE TABLE IF NOT EXISTS templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            text TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );

        CREATE TABLE IF NOT EXISTS support_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            topic TEXT DEFAULT '',
            description TEXT DEFAULT '',
            status TEXT DEFAULT 'open',
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS exchange_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_currency TEXT DEFAULT 'USD',
            to_currency TEXT DEFAULT 'RUB',
            rate REAL NOT NULL,
            updated_at TEXT DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_jobs_active ON jobs(is_active);
        CREATE INDEX IF NOT EXISTS idx_jobs_category ON jobs(category);
        CREATE INDEX IF NOT EXISTS idx_apps_user ON applications(user_id);
        CREATE INDEX IF NOT EXISTS idx_apps_status ON applications(status);
        CREATE INDEX IF NOT EXISTS idx_saved_user ON saved_jobs(user_id);
        CREATE INDEX IF NOT EXISTS idx_skills_user ON skills(user_id);
        CREATE INDEX IF NOT EXISTS idx_portfolio_user ON portfolio(user_id);
    """)
    conn.commit()
    conn.close()
    log.info("Database initialized")

def seed_jobs_if_empty():
    """Заполнить таблицу заказов начальными данными, если она пуста."""
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
    if count > 0:
        conn.close()
        return

    jobs_data = [
        ("Разработка ML-модели для рекомендаций", "ai", 3000, 8000, "Дмитрий К.", 4.8, 34, 94, "senior", "remote", '["Python","TensorFlow","PyTorch","NLP"]', "Необходима разработка ML-модели рекомендательной системы для e-commerce платформы."),
        ("UI/UX дизайн мобильного приложения", "design", 1500, 4000, "Елена М.", 4.9, 56, 87, "middle", "remote", '["Figma","Prototyping","User Research","Design Systems"]', "Ищем UX/UI дизайнера для создания дизайна мобильного приложения в сфере финтех."),
        ("Backend разработка на Node.js", "dev", 2000, 5000, "Артём В.", 4.5, 22, 82, "middle", "remote", '["Node.js","PostgreSQL","Redis","Docker"]', "Разработка высоконагруженного backend-сервиса для обработки платежей."),
        ("Написание SEO-статей для блога", "writing", 200, 500, "Мария С.", 4.7, 89, 73, "junior", "remote", '["SEO","Copywriting","Content Marketing","Research"]', "Необходимы 10 SEO-оптимизированных статей для корпоративного блога."),
        ("Настройка CI/CD пайплайна", "devops", 800, 2000, "Игорь Л.", 4.6, 15, 68, "senior", "remote", '["Docker","Kubernetes","GitHub Actions","Terraform"]', "Настроить полный CI/CD пайплайн для микросервисного проекта."),
        ("Анализ данных клиентов с ML", "data", 5000, 12000, "Ольга П.", 5.0, 41, 91, "senior", "hybrid", '["Python","Pandas","Scikit-learn","SQL","Visualization"]', "Провести комплексный анализ клиентской базы с использованием ML-методов."),
        ("Разработка чат-бота на GPT API", "ai", 1000, 3000, "Андрей Б.", 4.3, 18, 89, "middle", "remote", '["OpenAI API","Python","NLP","Telegram API"]', "Разработка интеллектуального чат-бота для клиентской поддержки."),
        ("SMM-стратегия для стартапа", "marketing", 500, 1500, "Наталья К.", 4.4, 27, 56, "middle", "remote", '["Social Media","Content Strategy","Analytics","Branding"]', "Разработка полной SMM-стратегии для IT-стартапа."),
        ("Дизайн лендинга для SaaS-продукта", "design", 800, 2500, "Сергей Д.", 4.7, 63, 78, "middle", "remote", '["Figma","Web Design","Animation","Conversion Optimization"]', "Разработка дизайна лендинга для B2B SaaS-продукта."),
        ("React Native мобильное приложение", "dev", 5000, 15000, "Виктория Р.", 4.9, 45, 85, "senior", "remote", '["React Native","TypeScript","Firebase","Redux"]', "Разработка кроссплатформенного мобильного приложения."),
        ("Fine-tuning LLM для юридических текстов", "ai", 8000, 15000, "Алексей Т.", 4.8, 12, 96, "lead", "remote", '["LLM","Fine-tuning","RAG","Legal Tech"]', "Необходим fine-tuning большой языковой модели для юридических документов."),
        ("Техническая документация API", "writing", 300, 800, "Павел Н.", 4.2, 31, 62, "middle", "remote", '["Technical Writing","API Documentation","Markdown","Swagger"]', "Написание полной технической документации для REST API."),
        ("Миграция инфраструктуры в облако", "devops", 3000, 7000, "Роман Ш.", 4.6, 19, 71, "senior", "hybrid", '["AWS","Terraform","Ansible","Docker","Monitoring"]', "Миграция on-premise инфраструктуры в AWS."),
        ("Анализ конкурентов рынка EdTech", "marketing", 1000, 3000, "Юлия Г.", 4.5, 38, 53, "middle", "office", '["Market Research","Competitive Analysis","Data Analysis","Presentation"]', "Комплексный анализ конкурентов на рынке EdTech."),
        ("Computer Vision для контроля качества", "ai", 10000, 15000, "Михаил Ф.", 4.9, 8, 88, "lead", "hybrid", '["Computer Vision","OpenCV","PyTorch","Edge AI","YOLO"]', "Разработка системы компьютерного зрения для контроля качества."),
    ]

    for j in jobs_data:
        conn.execute("""
            INSERT INTO jobs (title, category, budget_min, budget_max, client_name, client_rating,
                            client_orders, match_score, level, job_type, skills, description, posted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now', '-' || abs(random()) % 172800 || ' seconds'))
        """, j)

    # Seed exchange rate
    conn.execute("""
        INSERT INTO exchange_rates (from_currency, to_currency, rate, updated_at)
        VALUES ('USD', 'RUB', 92.5, datetime('now'))
    """)

    conn.commit()
    conn.close()
    log.info(f"Seeded {len(jobs_data)} jobs and exchange rate")

def ensure_user(user_id: int, first_name: str = "", last_name: str = "",
                username: str = "", photo_url: str = "", language_code: str = "ru"):
    """Создать или обновить пользователя в БД."""
    conn = get_db()
    existing = conn.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,)).fetchone()
    if existing:
        conn.execute("""
            UPDATE users SET first_name=?, last_name=?, username=?, photo_url=?,
                           language_code=?, last_active_at=datetime('now')
            WHERE user_id=?
        """, (first_name, last_name, username, photo_url, language_code, user_id))
    else:
        conn.execute("""
            INSERT INTO users (user_id, username, first_name, last_name, photo_url, language_code,
                             monthly_app_reset)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, username, first_name, last_name, photo_url, language_code,
              datetime.now().strftime("%Y-%m")))
    conn.commit()
    conn.close()

# ── Проверка подписи Telegram initData ──
def validate_init_data(init_data: str) -> dict | None:
    """Проверить подпись Telegram WebApp initData."""
    if not init_data:
        return None
    try:
        vals = {}
        for pair in init_data.split("&"):
            k, v = pair.split("=", 1)
            vals[k] = v

        hash_val = vals.pop("hash", None)
        if not hash_val:
            return None

        check_string = "\n".join(f"{k}={v}" for k, v in sorted(vals.items()))
        secret_key = hmac.new(
            b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256
        ).digest()
        computed = hmac.new(
            secret_key, check_string.encode(), hashlib.sha256
        ).hexdigest()

        if computed != hash_val:
            return None

        # Parse user JSON
        user_data = json.loads(vals.get("user", "{}"))
        return {**vals, "user": user_data}
    except Exception as e:
        log.warning(f"initData validation failed: {e}")
        return None

def get_user_id_from_request(request: web.Request) -> int | None:
    """Извлечь user_id из initData или заголовка."""
    # Try initData first
    init_data = request.query.get("init_data", "") or request.headers.get("X-Init-Data", "")
    if init_data:
        parsed = validate_init_data(init_data)
        if parsed and "user" in parsed:
            return parsed["user"].get("id")

    # Fallback: user_id parameter
    uid = request.query.get("user_id", "")
    if uid.isdigit():
        return int(uid)

    return None


# ═══════════════════════════════════════════════════════════
# API маршруты
# ═══════════════════════════════════════════════════════════

async def api_index(request: web.Request):
    """Отдать HTML мини-приложения с инжектированными данными пользователя."""
    init_data = request.query.get("init_data", "")
    tg_user = None
    user_id = None

    if init_data:
        parsed = validate_init_data(init_data)
        if parsed and "user" in parsed:
            tg_user = parsed["user"]
            user_id = tg_user.get("id")

    if user_id:
        ensure_user(
            user_id,
            first_name=tg_user.get("first_name", ""),
            last_name=tg_user.get("last_name", ""),
            username=tg_user.get("username", ""),
            photo_url=tg_user.get("photo_url", ""),
            language_code=tg_user.get("language_code", "ru"),
        )

    # Read and inject user data into HTML
    html_path = Path(__file__).parent / "index.html"
    if not html_path.exists():
        return web.Response(text="Mini app HTML not found", status=404)

    html = html_path.read_text(encoding="utf-8")

    # Inject server config and user data as a script tag before </head>
    inject_data = {
        "SERVER_URL": WEBAPP_URL,
        "USER_ID": user_id,
        "TG_USER": tg_user,
    }
    inject_script = f'<script id="__SH_SERVER_DATA__" type="application/json">{json.dumps(inject_data, ensure_ascii=False)}</script>'

    html = html.replace("</head>", inject_script + "\n</head>", 1)

    return web.Response(text=html, content_type="text/html", charset="utf-8")


async def api_jobs(request: web.Request):
    """GET /api/jobs — список заказов."""
    user_id = get_user_id_from_request(request)
    conn = get_db()

    # Если пользователь авторизован, обновим last_active
    if user_id:
        conn.execute("UPDATE users SET last_active_at=datetime('now') WHERE user_id=?", (user_id,))

    category = request.query.get("category", "all")
    level = request.query.get("level", "any")
    job_type = request.query.get("type", "all")
    search = request.query.get("q", "")
    sort = request.query.get("sort", "relevance")

    query = "SELECT * FROM jobs WHERE is_active = 1"
    params = []

    if category and category != "all":
        query += " AND category = ?"
        params.append(category)
    if level and level != "any":
        query += " AND level = ?"
        params.append(level)
    if job_type and job_type != "all":
        query += " AND job_type = ?"
        params.append(job_type)
    if search:
        query += " AND (title LIKE ? OR description LIKE ? OR skills LIKE ?)"
        params.extend([f"%{search}%"] * 3)

    if sort == "relevance":
        query += " ORDER BY match_score DESC, posted_at DESC"
    elif sort == "budget_high":
        query += " ORDER BY budget_max DESC"
    elif sort == "budget_low":
        query += " ORDER BY budget_min ASC"
    elif sort == "newest":
        query += " ORDER BY posted_at DESC"

    rows = conn.execute(query, params).fetchall()
    conn.close()

    jobs = []
    for r in rows:
        posted_at = r["posted_at"]
        # Compute human-readable "posted" time
        try:
            dt = datetime.fromisoformat(posted_at)
            diff = datetime.now() - dt
            if diff.total_seconds() < 60:
                posted = "только что"
            elif diff.total_seconds() < 3600:
                posted = f"{int(diff.total_seconds()/60)} мин"
            elif diff.total_seconds() < 86400:
                posted = f"{int(diff.total_seconds()/3600)}ч"
            else:
                days = int(diff.total_seconds() / 86400)
                posted = f"{days}д"
        except:
            posted = posted_at

        jobs.append({
            "id": r["id"],
            "title": r["title"],
            "category": r["category"],
            "budgetMin": r["budget_min"],
            "budgetMax": r["budget_max"],
            "currency": r["currency"],
            "clientName": r["client_name"],
            "clientRating": r["client_rating"],
            "clientOrders": r["client_orders"],
            "posted": posted,
            "postedAt": posted_at,
            "match": r["match_score"],
            "level": r["level"],
            "type": r["job_type"],
            "skills": json.loads(r["skills"]) if r["skills"] else [],
            "description": r["description"],
        })

    return web.json_response({"jobs": jobs, "total": len(jobs)})


async def api_profile_get(request: web.Request):
    """GET /api/profile?user_id=X — профиль пользователя."""
    user_id = get_user_id_from_request(request)
    if not user_id:
        return web.json_response({"error": "unauthorized"}, status=401)

    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()

    if not row:
        return web.json_response({"error": "user not found"}, status=404)

    return web.json_response({
        "user_id": row["user_id"],
        "name": row["first_name"] or "",
        "username": row["username"] or "",
        "last_name": row["last_name"] or "",
        "photo_url": row["photo_url"] or "",
        "spec": row["spec"] or "",
        "about": row["about"] or "",
        "timezone": row["timezone"] or "",
        "rate": row["rate"] or 0,
        "balance": row["balance"] or 0,
        "subscription_plan": row["subscription_plan"] or "free",
        "trial_started_at": row["trial_started_at"],
        "trial_offer_shown": bool(row["trial_offer_shown"]),
        "monthly_app_count": row["monthly_app_count"] or 0,
        "ai_proposal_count": row["ai_proposal_count"] or 0,
        "saved_count": row["saved_count"] or 0,
    })


async def api_profile_update(request: web.Request):
    """POST /api/profile — обновить профиль."""
    user_id = get_user_id_from_request(request)
    if not user_id:
        return web.json_response({"error": "unauthorized"}, status=401)

    data = await request.json()
    conn = get_db()

    fields = []
    values = []
    for key in ["spec", "about", "timezone", "rate"]:
        if key in data:
            fields.append(f"{key} = ?")
            values.append(data[key])
    if "name" in data:
        fields.append("first_name = ?")
        values.append(data["name"])

    if fields:
        values.append(user_id)
        conn.execute(f"UPDATE users SET {', '.join(fields)} WHERE user_id = ?", values)
        conn.commit()

    conn.close()
    return web.json_response({"ok": True})


async def api_balance(request: web.Request):
    """GET /api/balance?user_id=X — баланс пользователя."""
    user_id = get_user_id_from_request(request)
    if not user_id:
        return web.json_response({"balance": 0})

    conn = get_db()
    row = conn.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()

    return web.json_response({"balance": row["balance"] if row else 0})


async def api_balance_add(request: web.Request):
    """POST /api/balance — добавить токены."""
    user_id = get_user_id_from_request(request)
    if not user_id:
        return web.json_response({"error": "unauthorized"}, status=401)

    data = await request.json()
    amount = data.get("amount", 0)
    if not isinstance(amount, int) or amount <= 0:
        return web.json_response({"error": "invalid amount"}, status=400)

    conn = get_db()
    conn.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
    row = conn.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.commit()
    conn.close()

    return web.json_response({"balance": row["balance"] if row else 0})


async def api_applications_get(request: web.Request):
    """GET /api/applications?user_id=X — отклики пользователя."""
    user_id = get_user_id_from_request(request)
    if not user_id:
        return web.json_response({"applications": []})

    conn = get_db()
    rows = conn.execute("""
        SELECT a.*, j.title as job_title, j.category, j.budget_min, j.budget_max,
               j.client_name, j.match_score
        FROM applications a
        LEFT JOIN jobs j ON a.job_id = j.id
        WHERE a.user_id = ?
        ORDER BY a.applied_at DESC
    """, (user_id,)).fetchall()
    conn.close()

    apps = []
    for r in rows:
        # Auto-update statuses based on time elapsed
        status = r["status"]
        try:
            dt = datetime.fromisoformat(r["applied_at"])
            hours = (datetime.now() - dt).total_seconds() / 3600
            if status == "sent" and hours > 48:
                status = "viewed"
            if status == "viewed" and hours > 96 and r["job_id"] % 2 == 0:
                status = "replied"
        except:
            pass

        apps.append({
            "id": r["id"],
            "jobId": r["job_id"],
            "jobTitle": r["job_title"] or "",
            "category": r["category"] or "",
            "budgetMin": r["budget_min"] or 0,
            "budgetMax": r["budget_max"] or 0,
            "clientName": r["client_name"] or "",
            "match": r["match_score"] or 0,
            "coverLetter": r["cover_letter"] or "",
            "aiGenerated": bool(r["ai_generated"]),
            "status": status,
            "date": r["applied_at"],
        })

    return web.json_response({"applications": apps})


async def api_application_create(request: web.Request):
    """POST /api/applications — создать отклик."""
    user_id = get_user_id_from_request(request)
    if not user_id:
        return web.json_response({"error": "unauthorized"}, status=401)

    data = await request.json()
    job_id = data.get("job_id")
    cover_letter = data.get("cover_letter", "")
    ai_generated = data.get("ai_generated", False)

    if not job_id:
        return web.json_response({"error": "job_id required"}, status=400)

    conn = get_db()

    # Check subscription limits
    user = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    if not user:
        conn.close()
        return web.json_response({"error": "user not found"}, status=404)

    plan = user["subscription_plan"]
    if plan not in ("pro", "trial"):
        # Reset monthly count if new month
        current_month = datetime.now().strftime("%Y-%m")
        if user["monthly_app_reset"] != current_month:
            conn.execute("UPDATE users SET monthly_app_count=0, monthly_app_reset=? WHERE user_id=?",
                        (current_month, user_id))
            monthly_count = 0
        else:
            monthly_count = user["monthly_app_count"] or 0

        if monthly_count >= 3:  # FREE_APP_LIMIT
            conn.close()
            return web.json_response({"error": "limit_reached", "limit": 3}, status=403)

    # Check if already applied
    existing = conn.execute("SELECT id FROM applications WHERE user_id=? AND job_id=?",
                           (user_id, job_id)).fetchone()
    if existing:
        conn.close()
        return web.json_response({"error": "already_applied"}, status=409)

    conn.execute("""
        INSERT INTO applications (user_id, job_id, cover_letter, ai_generated, status)
        VALUES (?, ?, ?, ?, 'sent')
    """, (user_id, job_id, cover_letter, ai_generated))

    # Increment monthly app count
    conn.execute("UPDATE users SET monthly_app_count = monthly_app_count + 1 WHERE user_id = ?",
                (user_id,))
    conn.commit()
    conn.close()

    return web.json_response({"ok": True})


async def api_saved_get(request: web.Request):
    """GET /api/saved?user_id=X — сохранённые заказы."""
    user_id = get_user_id_from_request(request)
    if not user_id:
        return web.json_response({"saved": []})

    conn = get_db()
    rows = conn.execute("""
        SELECT s.job_id, s.saved_at, j.title, j.category, j.budget_min, j.budget_max,
               j.client_name, j.match_score, j.level, j.job_type, j.skills, j.description,
               j.posted_at, j.client_rating, j.client_orders
        FROM saved_jobs s
        LEFT JOIN jobs j ON s.job_id = j.id
        WHERE s.user_id = ?
        ORDER BY s.saved_at DESC
    """, (user_id,)).fetchall()
    conn.close()

    saved = []
    for r in rows:
        saved.append({
            "jobId": r["job_id"],
            "savedAt": r["saved_at"],
            "title": r["title"] or "",
            "category": r["category"] or "",
            "budgetMin": r["budget_min"] or 0,
            "budgetMax": r["budget_max"] or 0,
            "clientName": r["client_name"] or "",
            "match": r["match_score"] or 0,
            "level": r["level"] or "middle",
            "type": r["job_type"] or "remote",
            "skills": json.loads(r["skills"]) if r["skills"] else [],
            "description": r["description"] or "",
        })

    return web.json_response({"saved": saved})


async def api_saved_add(request: web.Request):
    """POST /api/saved — сохранить заказ."""
    user_id = get_user_id_from_request(request)
    if not user_id:
        return web.json_response({"error": "unauthorized"}, status=401)

    data = await request.json()
    job_id = data.get("job_id")
    if not job_id:
        return web.json_response({"error": "job_id required"}, status=400)

    conn = get_db()
    try:
        conn.execute("INSERT INTO saved_jobs (user_id, job_id) VALUES (?, ?)", (user_id, job_id))
        conn.execute("UPDATE users SET saved_count = saved_count + 1 WHERE user_id = ?", (user_id,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Already saved
    conn.close()

    return web.json_response({"ok": True})


async def api_saved_remove(request: web.Request):
    """DELETE /api/saved — убрать из сохранённых."""
    user_id = get_user_id_from_request(request)
    if not user_id:
        return web.json_response({"error": "unauthorized"}, status=401)

    data = await request.json()
    job_id = data.get("job_id")
    if not job_id:
        return web.json_response({"error": "job_id required"}, status=400)

    conn = get_db()
    conn.execute("DELETE FROM saved_jobs WHERE user_id=? AND job_id=?", (user_id, job_id))
    conn.execute("UPDATE users SET saved_count = MAX(0, saved_count - 1) WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

    return web.json_response({"ok": True})


async def api_skills_get(request: web.Request):
    """GET /api/skills?user_id=X — навыки пользователя."""
    user_id = get_user_id_from_request(request)
    if not user_id:
        return web.json_response({"skills": []})

    conn = get_db()
    rows = conn.execute("SELECT * FROM skills WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()

    return web.json_response({"skills": [
        {"id": r["id"], "name": r["name"], "progress": r["progress"]}
        for r in rows
    ]})


async def api_skills_add(request: web.Request):
    """POST /api/skills — добавить навык."""
    user_id = get_user_id_from_request(request)
    if not user_id:
        return web.json_response({"error": "unauthorized"}, status=401)

    data = await request.json()
    name = data.get("name", "").strip()
    if not name:
        return web.json_response({"error": "name required"}, status=400)

    progress = data.get("progress", 50)

    conn = get_db()
    conn.execute("INSERT INTO skills (user_id, name, progress) VALUES (?, ?, ?)",
                (user_id, name, progress))
    conn.commit()
    conn.close()

    return web.json_response({"ok": True})


async def api_portfolio_get(request: web.Request):
    """GET /api/portfolio?user_id=X — портфолио пользователя."""
    user_id = get_user_id_from_request(request)
    if not user_id:
        return web.json_response({"portfolio": []})

    conn = get_db()
    rows = conn.execute("SELECT * FROM portfolio WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()

    return web.json_response({"portfolio": [
        {"id": r["id"], "name": r["name"], "description": r["description"],
         "skills": r["skills"], "color": r["color"]}
        for r in rows
    ]})


async def api_portfolio_add(request: web.Request):
    """POST /api/portfolio — добавить проект в портфолио."""
    user_id = get_user_id_from_request(request)
    if not user_id:
        return web.json_response({"error": "unauthorized"}, status=401)

    data = await request.json()
    name = data.get("name", "").strip()
    if not name:
        return web.json_response({"error": "name required"}, status=400)

    desc = data.get("description", "")
    skills = data.get("skills", "")
    color = data.get("color", "primary")

    conn = get_db()
    conn.execute("INSERT INTO portfolio (user_id, name, description, skills, color) VALUES (?, ?, ?, ?, ?)",
                (user_id, name, desc, skills, color))
    conn.commit()
    conn.close()

    return web.json_response({"ok": True})


async def api_portfolio_delete(request: web.Request):
    """DELETE /api/portfolio — удалить проект из портфолио."""
    user_id = get_user_id_from_request(request)
    if not user_id:
        return web.json_response({"error": "unauthorized"}, status=401)

    data = await request.json()
    item_id = data.get("id")
    if not item_id:
        return web.json_response({"error": "id required"}, status=400)

    conn = get_db()
    conn.execute("DELETE FROM portfolio WHERE id=? AND user_id=?", (item_id, user_id))
    conn.commit()
    conn.close()

    return web.json_response({"ok": True})


async def api_templates_get(request: web.Request):
    """GET /api/templates?user_id=X — шаблоны пользователя."""
    user_id = get_user_id_from_request(request)
    if not user_id:
        return web.json_response({"templates": []})

    conn = get_db()
    rows = conn.execute("SELECT * FROM templates WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()

    return web.json_response({"templates": [
        {"id": r["id"], "title": r["title"], "text": r["text"], "createdAt": r["created_at"]}
        for r in rows
    ]})


async def api_templates_add(request: web.Request):
    """POST /api/templates — создать шаблон."""
    user_id = get_user_id_from_request(request)
    if not user_id:
        return web.json_response({"error": "unauthorized"}, status=401)

    data = await request.json()
    title = data.get("title", "").strip()
    text = data.get("text", "").strip()
    if not title or not text:
        return web.json_response({"error": "title and text required"}, status=400)

    conn = get_db()
    conn.execute("INSERT INTO templates (user_id, title, text) VALUES (?, ?, ?)",
                (user_id, title, text))
    conn.commit()
    conn.close()

    return web.json_response({"ok": True})


async def api_subscription(request: web.Request):
    """GET /api/subscription?user_id=X — статус подписки."""
    user_id = get_user_id_from_request(request)
    if not user_id:
        return web.json_response({"plan": "free"})

    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()

    if not row:
        return web.json_response({"plan": "free"})

    plan = row["subscription_plan"]
    trial_days_left = 0
    trial_hours_left = 0

    if plan == "trial" and row["trial_started_at"]:
        try:
            start = datetime.fromisoformat(row["trial_started_at"])
            trial_duration = timedelta(days=3)
            elapsed = datetime.now() - start
            if elapsed >= trial_duration:
                # Trial expired - downgrade to free
                conn = get_db()
                conn.execute("UPDATE users SET subscription_plan='free' WHERE user_id=?", (user_id,))
                conn.commit()
                conn.close()
                plan = "free"
            else:
                remaining = trial_duration - elapsed
                trial_days_left = remaining.days
                trial_hours_left = int(remaining.total_seconds() / 3600)
        except:
            pass

    # Reset monthly app count if new month
    current_month = datetime.now().strftime("%Y-%m")
    if row["monthly_app_reset"] != current_month:
        conn = get_db()
        conn.execute("UPDATE users SET monthly_app_count=0, monthly_app_reset=? WHERE user_id=?",
                    (current_month, user_id))
        conn.commit()
        conn.close()

    is_pro = plan in ("pro", "trial")

    return web.json_response({
        "plan": plan,
        "isPro": is_pro,
        "trialDaysLeft": trial_days_left,
        "trialHoursLeft": trial_hours_left,
        "monthlyAppCount": row["monthly_app_count"] or 0,
        "monthlyAppLimit": 999 if is_pro else 3,
        "aiProposalCount": row["ai_proposal_count"] or 0,
        "savedCount": row["saved_count"] or 0,
        "savedLimit": 999 if is_pro else 3,
        "trialOfferShown": bool(row["trial_offer_shown"]),
    })


async def api_subscription_update(request: web.Request):
    """POST /api/subscription — обновить подписку (начать триал, перейти на Pro)."""
    user_id = get_user_id_from_request(request)
    if not user_id:
        return web.json_response({"error": "unauthorized"}, status=401)

    data = await request.json()
    action = data.get("action", "")

    conn = get_db()
    if action == "start_trial":
        conn.execute("""
            UPDATE users SET subscription_plan='trial', trial_started_at=datetime('now'),
                           monthly_app_count=0, ai_proposal_count=0
            WHERE user_id=?
        """, (user_id,))
    elif action == "subscribe_pro":
        conn.execute("""
            UPDATE users SET subscription_plan='pro', trial_started_at=NULL
            WHERE user_id=?
        """, (user_id,))
    elif action == "skip_trial":
        conn.execute("UPDATE users SET trial_offer_shown=1 WHERE user_id=?", (user_id,))
    elif action == "downgrade":
        conn.execute("UPDATE users SET subscription_plan='free' WHERE user_id=?", (user_id,))

    conn.commit()
    conn.close()

    return web.json_response({"ok": True})


async def api_exchange_rate(request: web.Request):
    """GET /api/exchange-rate — текущий курс USD→RUB."""
    conn = get_db()
    row = conn.execute("""
        SELECT rate, updated_at FROM exchange_rates
        WHERE from_currency='USD' AND to_currency='RUB'
        ORDER BY updated_at DESC LIMIT 1
    """).fetchone()
    conn.close()

    if row:
        return web.json_response({"rate": row["rate"], "updatedAt": row["updated_at"]})

    # Fallback default
    return web.json_response({"rate": 92.5, "updatedAt": None})


async def api_support_create(request: web.Request):
    """POST /api/support — создать тикет поддержки."""
    user_id = get_user_id_from_request(request)
    if not user_id:
        return web.json_response({"error": "unauthorized"}, status=401)

    data = await request.json()
    topic = data.get("topic", "")
    description = data.get("description", "")

    conn = get_db()
    cursor = conn.execute("""
        INSERT INTO support_tickets (user_id, topic, description) VALUES (?, ?, ?)
    """, (user_id, topic, description))
    ticket_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return web.json_response({"ok": True, "ticketId": f"SH-{1000 + ticket_id}"})


async def api_stats(request: web.Request):
    """GET /api/stats?user_id=X — агрегированная статистика для hero-метрик."""
    user_id = get_user_id_from_request(request)
    if not user_id:
        return web.json_response({
            "potentialIncome": 0,
            "conversion": "0 из 0",
            "newJobs": 0,
            "totalJobs": 0,
            "applicationsCount": 0,
        })

    conn = get_db()

    # Exchange rate
    rate_row = conn.execute("""
        SELECT rate FROM exchange_rates
        WHERE from_currency='USD' AND to_currency='RUB'
        ORDER BY updated_at DESC LIMIT 1
    """).fetchone()
    exchange_rate = rate_row["rate"] if rate_row else 92.5

    # User's applications with job budgets
    apps = conn.execute("""
        SELECT a.status, j.budget_max
        FROM applications a
        LEFT JOIN jobs j ON a.job_id = j.id
        WHERE a.user_id = ?
    """, (user_id,)).fetchall()

    total_earnings_usd = sum(a["budget_max"] or 0 for a in apps)
    total_earnings_rub = int(total_earnings_usd * exchange_rate)

    sent = sum(1 for a in apps if a["status"] == "sent")
    viewed = sum(1 for a in apps if a["status"] == "viewed")
    replied = sum(1 for a in apps if a["status"] == "replied")

    # New jobs (posted within last 2 hours)
    new_jobs = conn.execute("""
        SELECT COUNT(*) as cnt FROM jobs
        WHERE is_active=1 AND posted_at >= datetime('now', '-2 hours')
    """).fetchone()["cnt"]

    total_jobs = conn.execute("SELECT COUNT(*) as cnt FROM jobs WHERE is_active=1").fetchone()["cnt"]

    # User subscription info
    user = conn.execute("SELECT subscription_plan FROM users WHERE user_id=?", (user_id,)).fetchone()
    is_pro = user["subscription_plan"] in ("pro", "trial") if user else False

    # Potential income based on visible jobs
    if total_earnings_rub > 0:
        potential_income = total_earnings_rub
    else:
        if is_pro:
            potential = conn.execute("SELECT SUM(budget_max) as s FROM jobs WHERE is_active=1").fetchone()["s"] or 0
        else:
            potential = conn.execute("SELECT SUM(budget_max) as s FROM jobs WHERE is_active=1 LIMIT 6").fetchone()["s"] or 0
        potential_income = int(potential * exchange_rate)

    conn.close()

    return web.json_response({
        "potentialIncome": potential_income,
        "exchangeRate": exchange_rate,
        "conversion": f"{replied} из {len(apps)}",
        "newJobs": new_jobs,
        "totalJobs": total_jobs,
        "applicationsCount": len(apps),
        "sent": sent,
        "viewed": viewed,
        "replied": replied,
    })


# ═══════════════════════════════════════════════════════════
# Telegram Bot
# ═══════════════════════════════════════════════════════════

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, bot: Bot):
    ensure_user(
        message.from_user.id,
        first_name=message.from_user.first_name or "",
        last_name=message.from_user.last_name or "",
        username=message.from_user.username or "",
        language_code=message.from_user.language_code or "ru",
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🚀 Открыть SkillHunt",
            web_app=WebAppInfo(url=f"{WEBAPP_URL}/?tgWebAppStartParam=1")
        )]
    ])

    await message.answer(
        "Привет! 👋\n\n"
        "SkillHunt — AI-платформа для фрилансеров.\n"
        "Находите заказы, откликайтесь и зарабатывайте.\n\n"
        "Нажмите кнопку ниже, чтобы начать:",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "🆘 Помощь по SkillHunt\n\n"
        "/start — Открыть мини-приложение\n"
        "/profile — Ваш профиль\n"
        "/stats — Статистика\n"
        "/subscribe — Управление подпиской\n\n"
        "Если возникли проблемы — напишите в поддержку через приложение.",
    )


@router.message(Command("profile"))
async def cmd_profile(message: Message):
    user_id = message.from_user.id
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()

    if not user:
        await message.answer("Профиль не найден. Откройте мини-приложение через /start")
        return

    plan_emoji = {"free": "🆓", "trial": "⭐", "pro": "💎"}.get(user["subscription_plan"], "🆓")
    plan_name = {"free": "Free", "trial": "Pro (триал)", "pro": "Pro"}.get(user["subscription_plan"], "Free")

    text = (
        f"👤 Профиль SkillHunt\n\n"
        f"Имя: {user['first_name'] or 'Не указано'}\n"
        f"Специализация: {user['spec'] or 'Не указана'}\n"
        f"Ставка: ${user['rate'] or 0}/час\n"
        f"Баланс: {user['balance'] or 0} токенов\n"
        f"Подписка: {plan_emoji} {plan_name}\n"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🚀 Открыть SkillHunt",
            web_app=WebAppInfo(url=f"{WEBAPP_URL}/")
        )]
    ])
    await message.answer(text, reply_markup=keyboard)


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    user_id = message.from_user.id
    conn = get_db()

    apps_count = conn.execute("SELECT COUNT(*) FROM applications WHERE user_id=?", (user_id,)).fetchone()[0]
    saved_count = conn.execute("SELECT COUNT(*) FROM saved_jobs WHERE user_id=?", (user_id,)).fetchone()[0]
    total_jobs = conn.execute("SELECT COUNT(*) FROM jobs WHERE is_active=1").fetchone()[0]

    conn.close()

    text = (
        f"📊 Статистика SkillHunt\n\n"
        f"Всего заказов: {total_jobs}\n"
        f"Отправлено откликов: {apps_count}\n"
        f"Сохранённых заказов: {saved_count}\n"
    )
    await message.answer(text)


@router.message(Command("subscribe"))
async def cmd_subscribe(message: Message, bot: Bot):
    user_id = message.from_user.id
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()

    plan = user["subscription_plan"] if user else "free"

    if plan == "pro":
        await message.answer("💎 У вас уже активна Pro подписка!")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="💎 Оформить Pro",
            web_app=WebAppInfo(url=f"{WEBAPP_URL}/?action=subscribe")
        )]
    ])

    if plan == "trial":
        await message.answer("⭐ У вас активен пробный период Pro", reply_markup=keyboard)
    else:
        await message.answer(
            "🆓 У вас Free-план\n\n"
            "Ограничения Free:\n"
            "• 3 отклика в месяц\n"
            "• 3 сохранённых заказа\n"
            "• Только 6 заказов из ленты\n\n"
            "💎 Pro — без ограничений!",
            reply_markup=keyboard,
        )


# Handle web_app_data (when mini app sends data back)
@router.message(F.web_app_data)
async def handle_web_app_data(message: Message):
    data = message.web_app_data.data
    log.info(f"WebApp data from {message.from_user.id}: {data}")
    await message.answer(f"Данные получены: {data}")


# ── Admin: add jobs ──
@router.message(Command("addjob"))
async def cmd_add_job(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Нет прав для этой команды")
        return

    # Parse: /addjob title|category|min|max|level|type|skills|description
    parts = message.text.split("|")
    if len(parts) < 3:
        await message.answer("Формат: /addjob Заголовок|категория|мин_бюджет|макс_бюджет|уровень|тип|навыки|описание")
        return

    title = parts[0].replace("/addjob", "").strip()
    category = parts[1].strip() if len(parts) > 1 else "dev"
    budget_min = int(parts[2].strip()) if len(parts) > 2 and parts[2].strip().isdigit() else 0
    budget_max = int(parts[3].strip()) if len(parts) > 3 and parts[3].strip().isdigit() else 0
    level = parts[4].strip() if len(parts) > 4 else "middle"
    job_type = parts[5].strip() if len(parts) > 5 else "remote"
    skills = parts[6].strip() if len(parts) > 6 else "[]"
    description = parts[7].strip() if len(parts) > 7 else ""

    conn = get_db()
    conn.execute("""
        INSERT INTO jobs (title, category, budget_min, budget_max, level, job_type, skills, description,
                        client_name, client_rating, client_orders, match_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Заказчик', 4.5, 10, 70)
    """, (title, category, budget_min, budget_max, level, job_type, skills, description))
    conn.commit()
    conn.close()

    await message.answer(f"✅ Заказ добавлен: {title}")


# Need to import Command
from aiogram.filters import Command

# ═══════════════════════════════════════════════════════════
# Сервер
# ═══════════════════════════════════════════════════════════

def create_app():
    app = web.Application()

    # Serve mini app HTML
    app.router.add_get("/", api_index)

    # API endpoints
    app.router.add_get("/api/jobs", api_jobs)
    app.router.add_get("/api/profile", api_profile_get)
    app.router.add_post("/api/profile", api_profile_update)
    app.router.add_get("/api/balance", api_balance)
    app.router.add_post("/api/balance", api_balance_add)
    app.router.add_get("/api/applications", api_applications_get)
    app.router.add_post("/api/applications", api_application_create)
    app.router.add_get("/api/saved", api_saved_get)
    app.router.add_post("/api/saved", api_saved_add)
    app.router.add_delete("/api/saved", api_saved_remove)
    app.router.add_get("/api/skills", api_skills_get)
    app.router.add_post("/api/skills", api_skills_add)
    app.router.add_get("/api/portfolio", api_portfolio_get)
    app.router.add_post("/api/portfolio", api_portfolio_add)
    app.router.add_delete("/api/portfolio", api_portfolio_delete)
    app.router.add_get("/api/templates", api_templates_get)
    app.router.add_post("/api/templates", api_templates_add)
    app.router.add_get("/api/subscription", api_subscription)
    app.router.add_post("/api/subscription", api_subscription_update)
    app.router.add_get("/api/exchange-rate", api_exchange_rate)
    app.router.add_post("/api/support", api_support_create)
    app.router.add_get("/api/stats", api_stats)

    # Health check
    app.router.add_get("/health", lambda r: web.json_response({"status": "ok"}))

    return app


async def main():
    # Init database
    init_db()
    seed_jobs_if_empty()

    if not BOT_TOKEN:
        log.warning("BOT_TOKEN not set! Bot commands will not work. API server only.")

    # Create aiohttp app
    app = create_app()

    # Setup aiogram bot and dispatcher
    if BOT_TOKEN:
        bot = Bot(
            token=BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        dp = Dispatcher()
        dp.include_router(router)

        # Start polling in background
        asyncio.create_task(dp.start_polling(bot))
        log.info("Telegram bot started")

    # Start aiohttp server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", API_PORT)
    await site.start()
    log.info(f"API server started on port {API_PORT}")

    # Keep running
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
