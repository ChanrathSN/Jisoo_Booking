import asyncio
import logging
import json
from datetime import datetime

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

BOT_TOKEN = "8274446621:AAH6ItCjsHzle6GebZsGGHSbmGqyfRE7S0I"


MINI_APP_URL = (
    "https://chanrathsn.github.io/"
    "Jisoo_Booking/"
    "telegram-mini-app/"
    "frontend/"
)


# ==========================================
# AQUALIFE PRODUCT CATALOG
# ==========================================

PRODUCT_CATALOG = {


    "SU-G": {

        "name": "SAENG SU (TT)",

        "price": 449

    },


    "SU(FS)-G": {

        "name": "SAENG SU (FS)",

        "price": 499

    },


    "MNL(FS)-W": {

        "name": "MNL(FS) - WHITE",

        "price": 799

    },


    "SC": {

        "name": "SUPER COOLING",

        "price": 1188

    },


    "JS-V3": {

        "name": "JICO",

        "price": 219

    },


    "RKT5000": {

        "name": "ROKKET 5000",

        "price": 399

    },


    "RKT8000": {

        "name": "ROKKET 8000",

        "price": 449

    },


    "RKT10000": {

        "name": "ROKKET 10000",

        "price": 549

    },


    "CANNON": {

        "name": "CANNON",

        "price": 249

    },


    "JS-VT": {

        "name": "TRICO",

        "price": 219

    },


    "MINI-S (HWC)": {

        "name": "MINI-S(HWC)",

        "price": 1188

    },


    "MINI-S (HW)": {

        "name": "MINI-S(HW)",

        "price": 1188

    },


    "JS-V2": {

        "name": "NOVA",

        "price": 199

    }

}


# ==========================================
# BOT SETUP
# ==========================================

bot = Bot(

    token=BOT_TOKEN

)


dp = Dispatcher()


# ==========================================
# FORMAT MONEY
# ==========================================

def format_price(

    amount

):


    return (

        f"${amount:,.2f}"

    )


# ==========================================
# START COMMAND
# ==========================================

@dp.message(

    CommandStart()

)

async def cmd_start(

    message: types.Message

):


    keyboard = InlineKeyboardMarkup(

        inline_keyboard=[

            [

                InlineKeyboardButton(

                    text=(

                        "Open AquaLife Store 🛒"

                    ),

                    web_app=WebAppInfo(

                        url=MINI_APP_URL

                    )

                )

            ]

        ]

    )


    await message.answer(

        (

            f"Hello "

            f"{message.from_user.first_name}"

            "! 👋\n\n"

            "Welcome to the "

            "AquaLife Product Store 💧\n\n"

            "Choose your products and "

            "add them to your cart.\n\n"

            "Tap below to start shopping:"

        ),

        reply_markup=keyboard

    )


# ==========================================
# RECEIVE CUSTOMER ORDER
# ==========================================

@dp.message(

    F.web_app_data

)

async def handle_mini_app_data(

    message: types.Message

):


    try:


        # Read Mini App data

        raw_data = (

            message.web_app_data.data

        )


        # Convert JSON

        order_data = json.loads(

            raw_data

        )


        # Get products

        products = (

            order_data.get(

                "products",

                []

            )

        )


        # Check empty order

        if not products:


            await message.answer(

                "⚠️ Your cart is empty."

            )


            return


        # Order information

        order_lines = []


        calculated_total = 0


        calculated_items = 0


        # Process each product

        for item in products:


            product_id = str(

                item.get(

                    "id"

                )

            )


            quantity = int(

                item.get(

                    "quantity",

                    1

                )

            )


            # Get official catalog data

            product = (

                PRODUCT_CATALOG.get(

                    product_id

                )

            )


            if not product:


                continue


            name = product["name"]


            price = product["price"]


            item_total = (

                price *

                quantity

            )


            calculated_total += (

                item_total

            )


            calculated_items += (

                quantity

            )


            order_lines.append(

                (

                    f"• <b>{name}</b>\n"

                    f"  Code: {product_id}\n"

                    f"  Qty: {quantity}\n"

                    f"  Unit Price: "

                    f"{format_price(price)}\n"

                    f"  Total: "

                    f"{format_price(item_total)}"

                )

            )


        # Create order summary

        order_summary = (

            "\n\n".join(

                order_lines

            )

        )


        # Current time

        order_time = (

            datetime.now()

            .strftime(

                "%Y-%m-%d %H:%M:%S"

            )

        )


        # Customer details

        customer_name = (

            message.from_user.full_name

        )


        username = (

            f"@{message.from_user.username}"

            if message.from_user.username

            else "No username"

        )


        # Final message

        response_message = (

            "🛒 <b>NEW CUSTOMER ORDER</b>\n"

            "\n"

            f"👤 <b>Customer:</b> "

            f"{customer_name}\n"

            f"📱 <b>Username:</b> "

            f"{username}\n"

            f"🕒 <b>Time:</b> "

            f"{order_time}\n"

            "\n"

            "📦 <b>ORDER DETAILS</b>\n"

            "\n"

            f"{order_summary}\n"

            "\n"

            "━━━━━━━━━━━━━━\n"

            f"🧮 <b>Total Items:</b> "

            f"{calculated_items}\n"

            f"💰 <b>GRAND TOTAL:</b> "

            f"{format_price(calculated_total)}"

        )


        # Send order to Telegram

        await message.answer(

            response_message,

            parse_mode="HTML"

        )


    except json.JSONDecodeError:


        logging.exception(

            "Invalid JSON received."

        )


        await message.answer(

            "❌ Invalid order data received."

        )


    except Exception as error:


        logging.exception(

            f"Order processing error: "

            f"{error}"

        )


        await message.answer(

            "❌ Error processing your order."

        )


# ==========================================
# MAIN
# ==========================================

async def main():


    logging.basicConfig(

        level=logging.INFO

    )


    # Clear pending updates

    await bot.delete_webhook(

        drop_pending_updates=True

    )


    print(

        "==================================="

    )


    print(

        " AquaLife Telegram Store Online 💧"

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


    asyncio.run(

        main()

    )
