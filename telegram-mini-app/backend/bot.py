import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# ==========================================
# CONFIGURATION
# ==========================================
BOT_TOKEN = "8274446621:AAH6ItCjsHzle6GebZsGGHSbmGqyfRE7S0I"  # Replace with your BotFather token

# Your full GitHub Pages URL pointing to the frontend folder
MINI_APP_URL = "https://chanrathsn.github.io/Jisoo_Booking/telegram-mini-app/frontend/"

# Catalog mapping (IDs match the ones used in index.html)
PRODUCT_CATALOG = {
    "1": {"name": "Cake", "price": "$1.00"},
    "2": {"name": "Burger", "price": "$4.99"},
    "3": {"name": "Fries", "price": "$1.49"},
    "4": {"name": "Hotdog", "price": "$3.49"},
    "5": {"name": "Taco", "price": "$3.99"},
    "6": {"name": "Pizza", "price": "$7.99"},
}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ==========================================
# HANDLERS
# ==========================================

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    """Handles the /start command and yields an inline keyboard button launching the Mini App."""
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Open Store 🛒",
                web_app=WebAppInfo(url=MINI_APP_URL)
            )
        ]
    ])
    await message.reply(
        f"Hello {message.from_user.first_name}! 👋\n\n"
        f"Tap the button below to browse products and place your order:",
        reply_markup=kb
    )


@dp.message(F.web_app_data)
async def handle_mini_app_data(message: types.Message):
    """Intercepts incoming JSON cart payload pushed back from frontend via tg.sendData()."""
    try:
        raw_data = message.web_app_data.data
        cart = json.loads(raw_data)  # Format expected: {"1": 2, "2": 1}
        
        if not cart:
            await message.reply("⚠️ Received an empty cart payload.")
            return

        order_lines = []
        
        # Build human-readable receipt
        for item_id, quantity in cart.items():
            product_info = PRODUCT_CATALOG.get(str(item_id), {"name": f"Item #{item_id}", "price": "N/A"})
            order_lines.append(f"• **{product_info['name']}** × {quantity} ({product_info['price']})")
        
        order_summary = "\n".join(order_lines)
        
        response_msg = (
            f"✅ **Order Received Successfully!**\n\n"
            f"**Customer:** {message.from_user.full_name}\n"
            f"**Order Details:**\n{order_summary}\n\n"
            f"Thank you for shopping with AquaLife! ❤️"
        )
        
        await message.reply(response_msg, parse_mode="Markdown")

    except Exception as e:
        logging.error(f"Error parsing web app payload: {e}")
        await message.reply("❌ An error occurred while processing your order.")


# ==========================================
# MAIN RUNNER
# ==========================================

async def main():
    logging.basicConfig(level=logging.INFO)
    
    # Cleans up old pending updates before polling starts
    await bot.delete_webhook(drop_pending_updates=True)
    
    print("===================================")
    print(" Telegram Bot Online and Listening ")
    print("===================================")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
