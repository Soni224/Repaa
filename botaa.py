import asyncio
import logging
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from uvicorn import Config, Server

# --- НАСТРОЙКИ ---
TOKEN = "ТВОЙ_ТОКЕН_БОТА"
# Для теста укажи любой URL, например свой локальный или google.com
APP_URL = "https://google.com" 

app = FastAPI()
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- ЛОГИКА БОТА ---
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    # Создаем кнопку, которая откроет Mini App
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть Mini App", web_app=WebAppInfo(url=APP_URL))]
    ])
    await message.answer("Привет! Нажми кнопку, чтобы открыть интерфейс:", reply_markup=kb)

# Обработчик данных, которые придут из Mini App через метод sendData
@dp.message(F.web_app_data)
async def get_web_data(message: types.Message):
    await message.answer(f"Бот получил данные: {message.web_app_data.data}")

# --- API ДЛЯ MINI APP (FastAPI) ---
@app.get("/")
async def read_root():
    return {"status": "Server is running"}

@app.post("/update_data")
async def update_data(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    action = data.get("action")
    
    # Бот реагирует на действие в Mini App
    await bot.send_message(user_id, f"Вы нажали кнопку '{action}' внутри Mini App!")
    return {"ok": True}

# --- ЗАПУСК ВСЕГО ВМЕСТЕ ---
async def main():
    # Запускаем бота в фоне
    asyncio.create_task(dp.start_polling(bot))
    
    # Запускаем FastAPI сервер
    config = Config(app=app, host="0.0.0.0", port=8000)
    server = Server(config)
    await server.serve()

if name == "main":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())