import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command  # ✅ bu muhim

API_TOKEN = "7865563534:AAEDVqfbfco1ifRwlaI_iMIGGlOQ3QdVoTc"
WEBAPP_URL = "https://scintillating-narwhal-e24493.netlify.app/"

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    creator_id = message.from_user.id
    room_id = f"room_{creator_id}"

    web_app = WebAppInfo(url=f"{WEBAPP_URL}?room_id={room_id}&user_id={creator_id}")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔗 Kirish", web_app=web_app)]],
        resize_keyboard=True
    )

    invite_link = f"{WEBAPP_URL}?room_id={room_id}"
    await message.answer(
        f"Mafia o'yin xonasi yaratildi!\n\n"
        f"🧑‍💼 Sizning Room ID: <code>{room_id}</code>\n"
        f"👥 Do‘stlaringizga ushbu havolani yuboring: \n<code>{invite_link}</code>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )



async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())