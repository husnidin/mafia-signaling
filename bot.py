import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command  # ✅ bu muhim

API_TOKEN = "7865563534:AAEDVqfbfco1ifRwlaI_iMIGGlOQ3QdVoTc"
WEBAPP_URL = "https://polite-piroshki-407252.netlify.app/"

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("start"))  # ✅ YANGI USLUB
async def cmd_start(message: types.Message):
    web_app = WebAppInfo(url=f"{WEBAPP_URL}?user_id={message.from_user.id}")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔗 Kirish", web_app=web_app)]],
        resize_keyboard=True
    )
    await message.answer("Mafia o'yiniga kirish uchun tugmani bosing:", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())