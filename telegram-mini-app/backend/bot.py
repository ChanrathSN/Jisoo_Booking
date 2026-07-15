import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Replace with the exact token BotFather handed to you
BOT_TOKEN = "8274446621:AAH6ItCjsHzle6GebZsGGHSbmGqyfRE7S0I"
# Replace with the live HTTPS URL where your frontend index.html is deployed
MINI_APP_URL = "https://your-deployed-frontend.vercel.app"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    """Handles the /start command and yields an inline keyboard button launching the Mini App."""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Open Product Shop 🛒",
                web_app=WebAppInfo(url=MINI_APP_URL)
            )
        ]
    ])
    await message.reply(
        f"Hello {message.from_user.first_name}! Use the button below to browse products natively:",
        reply_markup=kb
    )

@dp.message(lambda message: message.web_app_data is not None)
async def handle_mini_app_data(message: types.Message):
    """Intercepts incoming JSON string payloads pushed back from the frontend via tg.sendData()."""
    try:
        raw_data = message.web_app_data.data
        data = json.loads(raw_data)
        
        product_name = data.get("product", "Unknown Item")
        
        await message.reply(
            f"✅ **Order Received!**\n\n"
            f"Product: {product_name}\n"
            f"Status: Processing setup."
        )
    except Exception as e:
        await message.reply("Processed application window closing, but structure validation skipped.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
