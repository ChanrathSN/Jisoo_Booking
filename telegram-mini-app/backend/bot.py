import asyncio
import logging
import json

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)


# ==========================================
# CONFIGURATION
# ==========================================

# Paste your real BotFather token here
BOT_TOKEN = "8274446621:AAH6ItCjsHzle6GebZsGGHSbmGqyfRE7S0I"


# GitHub Pages Mini App URL
MINI_APP_URL = (
    "https://chanrathsn.github.io/"
    "Jisoo_Booking/telegram-mini-app/frontend/"
)


# ==========================================
# AQUALIFE PRODUCT CATALOG
# ==========================================

PRODUCT_CATALOG = {

    "1": {
        "name": "ROKKET Outdoor Filter",
        "price": "$99"
    },

    "2": {
        "name": "NOVA Water Purifier",
        "price": "Contact Us"
    },

    "3": {
        "name": "TRICO Water Purifier",
        "price": "Contact Us"
    },

    "4": {
        "name": "Filter Cartridge",
        "price": "Contact Us"
    },

    "5": {
        "name": "Aqualife Accessories",
        "price": "Contact Us"
    },

    "6": {
        "name": "ROKKET Service Package",
        "price": "Contact Us"
    }

}


# ==========================================
# BOT SETUP
# ==========================================

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()


# ==========================================
# /START COMMAND
# ==========================================

@dp.message(CommandStart())
async def cmd_start(message: types.Message):

    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [

                InlineKeyboardButton(

                    text="Open Aqualife Store 🛒",

                    web_app=WebAppInfo(

                        url=MINI_APP_URL

                    )

                )

            ]

        ]

    )


    await message.reply(

        f"Hello {message.from_user.first_name}! 👋\n\n"

        f"Welcome to the AquaLife Product Store 💧\n\n"

        f"Tap the button below to browse our products:",

        reply_markup=keyboard

    )


# ==========================================
# RECEIVE MINI APP ORDER
# ==========================================

@dp.message(F.web_app_data)
async def handle_mini_app_data(message: types.Message):

    try:

        # Get data from Mini App

        raw_data = message.web_app_data.data


        # Convert JSON into Python dictionary

        order_data = json.loads(raw_data)


        # Get product list

        products = order_data.get("products", [])


        # Check empty order

        if not products:

            await message.reply(

                "⚠️ Your order is empty."

            )

            return


        # Create order lines

        order_lines = []


        for item in products:


            product_id = str(

                item.get("id")

            )


            quantity = int(

                item.get("quantity", 1)

            )


            # Get product information

            product_info = PRODUCT_CATALOG.get(

                product_id,

                {

                    "name": item.get(

                        "name",

                        f"Product #{product_id}"

                    ),

                    "price": item.get(

                        "price",

                        "N/A"

                    )

                }

            )


            product_name = product_info["name"]

            product_price = product_info["price"]


            order_lines.append(

                f"• {product_name}\n"

                f"  Quantity: {quantity}\n"

                f"  Price: {product_price}"

            )


        # Join all products

        order_summary = "\n\n".join(

            order_lines

        )


        # Final message

        response_message = (

            "✅ <b>Order Received Successfully!</b>\n\n"

            f"<b>Customer:</b> "

            f"{message.from_user.full_name}\n\n"

            "<b>Order Details:</b>\n"

            f"{order_summary}\n\n"

            "Thank you for shopping with "

            "AquaLife Cambodia! 💧"

        )


        # Send order confirmation

        await message.reply(

            response_message,

            parse_mode="HTML"

        )


    except json.JSONDecodeError:


        logging.error(

            "Invalid JSON received from Mini App"

        )


        await message.reply(

            "❌ Invalid order data received."

        )


    except Exception as error:


        logging.exception(

            f"Error processing order: {error}"

        )


        await message.reply(

            "❌ An error occurred while processing "

            "your order."

        )


# ==========================================
# MAIN RUNNER
# ==========================================

async def main():

    logging.basicConfig(

        level=logging.INFO

    )


    # Remove old pending updates

    await bot.delete_webhook(

        drop_pending_updates=True

    )


    print(

        "==================================="

    )

    print(

        " AquaLife Telegram Bot Online 💧"

    )

    print(

        "==================================="


    )


    await dp.start_polling(

        bot

    )


# ==========================================
# START BOT
# ==========================================

if __name__ == "__main__":

    asyncio.run(main())
