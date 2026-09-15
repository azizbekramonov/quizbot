
import asyncio
import os
import threading
from flask import Flask
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# <<< TOKENNI KOD ICHIGA YOZMANG — Render'ning Environment Variables bo'limiga qo'shing
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

QUESTION = "O'zbekiston poytaxti qaysi shahar?"
CORRECT_ANSWER = "toshkent"


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer(f"Savol: {QUESTION}")


@dp.message()
async def answer_handler(message: types.Message):
    user_answer = message.text.strip().lower()

    if user_answer == CORRECT_ANSWER:
        await message.answer("✅ To'g'ri javob! Barakalla.")
    else:
        await message.answer("❌ Noto'g'ri. Yana urinib ko'ring.")


# ---------------------------------------------------------------------------
# FLASK — RENDER UCHUN HEALTH-CHECK SERVER (UptimeRobot shu manzilga ping yuboradi)
# ---------------------------------------------------------------------------

app = Flask(__name__)


@app.route("/")
def home():
    return "OK"


def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)


async def main():
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())