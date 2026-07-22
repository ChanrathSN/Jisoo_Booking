import asyncio
import logging
import json

from pathlib import Path
from datetime import datetime

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
    FSInputFile
)

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# ==================================================
# CONFIGURATION
# ==================================================

# IMPORTANT:
# Use your real BotFather token here.
# If this token has already been shared publicly,
# generate a new token from BotFather.
BOT_TOKEN = "8274446621:AAH6ItCjsHzle6GebZsGGHSbmGqyfRE7S0I"


# Your GitHub Pages Mini App URL
MINI_APP_URL = (
    "https://chanrathsn.github.io/"
    "Jisoo_Booking/"
    "telegram-mini-app/"
    "frontend/"
)


# ==================================================
# PROJECT FOLDERS
# ==================================================

# Current file:
#
# Jisoo_Booking/
# └── backend/
#     └── bot.py
#
# Parent folder:
#
# Jisoo_Booking/
#
BASE_DIR = Path(__file__).resolve().parent.parent


# PDF output folder:
#
# Jisoo_Booking/
# └── out/
#
OUT_DIR = BASE_DIR / "out"


# Automatically create the out folder
OUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ==================================================
# AQUALIFE PRODUCT CATALOG
# ==================================================

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
        "name": "MINI-S (HWC)",
        "price": 1188
    },

    "MINI-S (HW)": {
        "name": "MINI-S (HW)",
        "price": 1188
    },

    "JS-V2": {
        "name": "NOVA",
        "price": 199
    }

}


# ==================================================
# BOT SETUP
# ==================================================

bot = Bot(
    token=BOT_TOKEN
)

dp = Dispatcher()


# ==================================================
# PRICE FORMAT
# ==================================================

def format_price(
    amount
):

    return (
        f"${amount:,.2f}"
    )


# ==================================================
# CREATE PDF RECEIPT
# ==================================================

def create_sample_receipt(
    customer_name,
    products,
    total,
    order_number
):

    # Save PDF inside:
    #
    # Jisoo_Booking/out/
    #
    pdf_path = (

        OUT_DIR /

        f"sample_receipt_"
        f"{order_number}.pdf"

    )


    # Create PDF

    pdf = canvas.Canvas(

        str(pdf_path),

        pagesize=A4

    )


    width, height = A4


    y = height - 50


    # ==============================================
    # HEADER
    # ==============================================

    pdf.setFont(

        "Helvetica-Bold",

        20

    )


    pdf.drawCentredString(

        width / 2,

        y,

        "AQUALIFE CAMBODIA"

    )


    y -= 30


    pdf.setFont(

        "Helvetica-Bold",

        16

    )


    pdf.drawCentredString(

        width / 2,

        y,

        "SAMPLE RECEIPT"

    )


    y -= 40


    # ==============================================
    # CUSTOMER INFORMATION
    # ==============================================

    pdf.setFont(

        "Helvetica",

        10

    )


    pdf.drawString(

        50,

        y,

        f"Customer: {customer_name}"

    )


    y -= 18


    pdf.drawString(

        50,

        y,

        f"Order No: {order_number}"

    )


    y -= 18


    pdf.drawString(

        50,

        y,

        (

            "Date: "

            f"{datetime.now().strftime("
            "'%Y-%m-%d %H:%M')"

        )

    )


    y -= 35


    # ==============================================
    # TABLE HEADER
    # ==============================================

    pdf.setFont(

        "Helvetica-Bold",

        10

    )


    pdf.drawString(

        50,

        y,

        "Product"

    )


    pdf.drawString(

        300,

        y,

        "Qty"

    )


    pdf.drawString(

        360,

        y,

        "Unit Price"

    )


    pdf.drawString(

        470,

        y,

        "Total"

    )


    y -= 20


    pdf.line(

        50,

        y,

        545,

        y

    )


    y -= 20


    # ==============================================
    # PRODUCTS
    # ==============================================

    pdf.setFont(

        "Helvetica",

        10

    )


    for item in products:


        name = item["name"]


        quantity = item["quantity"]


        price = item["price"]


        item_total = (

            price *

            quantity

        )


        pdf.drawString(

            50,

            y,

            name[:35]

        )


        pdf.drawString(

            300,

            y,

            str(quantity)

        )


        pdf.drawString(

            360,

            y,

            format_price(price)

        )


        pdf.drawString(

            470,

            y,

            format_price(item_total)

        )


        y -= 20


    # ==============================================
    # TOTAL
    # ==============================================

    y -= 15


    pdf.line(

        50,

        y,

        545,

        y

    )


    y -= 30


    pdf.setFont(

        "Helvetica-Bold",

        14

    )


    pdf.drawString(

        350,

        y,

        "TOTAL:"

    )


    pdf.drawString(

        470,

        y,

        format_price(total)

    )


    y -= 50


    # ==============================================
    # FOOTER
    # ==============================================

    pdf.setFont(

        "Helvetica-Oblique",

        10

    )


    pdf.drawCentredString(

        width / 2,

        y,

        "This is a sample receipt."

    )


    y -= 16


    pdf.drawCentredString(

        width / 2,

        y,

        "Official invoice will be issued later."

    )


    # Save PDF

    pdf.save()


    return pdf_path


# ==================================================
# /START COMMAND
# ==================================================

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

            "Welcome to AquaLife Cambodia 💧\n\n"

            "Choose your products, "

            "add them to your cart, "

            "and confirm your order."

        ),

        reply_markup=keyboard

    )


# ==================================================
# RECEIVE ORDER FROM MINI APP
# ==================================================

@dp.message(

    F.web_app_data

)

async def handle_mini_app_data(

    message: types.Message

):


    try:


        # ==========================================
        # READ DATA FROM MINI APP
        # ==========================================

        raw_data = (

            message.web_app_data.data

        )


        order_data = json.loads(

            raw_data

        )


        products = (

            order_data.get(

                "products",

                []

            )

        )


        if not products:


            await message.answer(

                "⚠️ Your cart is empty."

            )


            return


        # ==========================================
        # CUSTOMER INFORMATION
        # ==========================================

        customer_name = (

            message.from_user.full_name

        )


        username = (

            f"@{message.from_user.username}"

            if message.from_user.username

            else "No username"

        )


        # ==========================================
        # ORDER NUMBER
        # ==========================================

        order_number = (

            datetime.now().strftime(

                "AL-%Y%m%d-%H%M%S"

            )

        )


        # ==========================================
        # CALCULATE ORDER
        # ==========================================

        calculated_total = 0


        calculated_items = 0


        verified_products = []


        order_lines = []


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


            # Find product from our official catalog

            product = (

                PRODUCT_CATALOG.get(

                    product_id

                )

            )


            if not product:


                continue


            product_name = (

                product["name"]

            )


            product_price = (

                product["price"]

            )


            item_total = (

                product_price *

                quantity

            )


            calculated_total += (

                item_total

            )


            calculated_items += (

                quantity

            )


            verified_products.append(

                {

                    "id": product_id,

                    "name": product_name,

                    "price": product_price,

                    "quantity": quantity,

                    "total": item_total

                }

            )


            order_lines.append(

                (

                    f"• <b>{product_name}</b>\n"

                    f"  Code: {product_id}\n"

                    f"  Qty: {quantity}\n"

                    f"  Unit Price: "

                    f"{format_price(product_price)}\n"

                    f"  Total: "

                    f"{format_price(item_total)}"

                )

            )


        if not verified_products:


            await message.answer(

                "❌ No valid products found."

            )


            return


        # ==========================================
        # CREATE ORDER SUMMARY
        # ==========================================

        order_summary = (

            "\n\n".join(

                order_lines

            )

        )


        order_time = (

            datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            )

        )


        # ==========================================
        # SEND ORDER DETAILS TO TELEGRAM
        # ==========================================

        response_message = (

            "🛒 <b>NEW CUSTOMER ORDER</b>\n\n"

            f"🧾 <b>Order No:</b> "

            f"{order_number}\n"

            f"👤 <b>Customer:</b> "

            f"{customer_name}\n"

            f"📱 <b>Username:</b> "

            f"{username}\n"

            f"🕒 <b>Time:</b> "

            f"{order_time}\n\n"

            "📦 <b>ORDER DETAILS</b>\n\n"

            f"{order_summary}\n\n"

            "━━━━━━━━━━━━━━\n"

            f"🧮 <b>Total Items:</b> "

            f"{calculated_items}\n"

            f"💰 <b>GRAND TOTAL:</b> "

            f"{format_price(calculated_total)}"

        )


        await message.answer(

            response_message,

            parse_mode="HTML"

        )


        # ==========================================
        # CREATE PDF IN OUT FOLDER
        # ==========================================

        pdf_path = (

            create_sample_receipt(

                customer_name,

                verified_products,

                calculated_total,

                order_number

            )

        )


        # ==========================================
        # SEND PDF TO TELEGRAM
        # ==========================================

        document = FSInputFile(

            str(pdf_path)

        )


        await message.answer_document(

            document,

            caption=(

                "🧾 <b>SAMPLE RECEIPT</b>\n\n"

                f"Order No: "

                f"{order_number}\n\n"

                "The PDF was generated "

                "automatically from your order."

            ),

            parse_mode="HTML"

        )


        print(

            "\nPDF SAVED TO:\n"

            f"{pdf_path}\n"

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

            f"Error processing order: "

            f"{error}"

        )


        await message.answer(

            (

                "❌ Error processing your order.\n\n"

                f"Error: {error}"

            )

        )


# ==================================================
# MAIN RUNNER
# ==================================================

async def main():


    logging.basicConfig(

        level=logging.INFO

    )


    # Remove old pending Telegram updates

    await bot.delete_webhook(

        drop_pending_updates=True

    )


    print(

        "===================================="

    )


    print(

        " AquaLife Telegram Store Online 💧"

    )


    print(

        "===================================="

    )


    print(

        f"PDF folder: {OUT_DIR}"

    )


    await dp.start_polling(

        bot

    )


# ==================================================
# START BOT
# ==================================================

if __name__ == "__main__":


    asyncio.run(

        main()

    )
