import os
import requests
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import mistral_api  # импортируем наш модуль

load_dotenv()
logging.basicConfig(level=logging.INFO)

bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher()


def search_wb(query):
    url = (
        "https://search.wb.ru/exactmatch/ru/common/v4/search"
        f"?query={query}&resultset=catalog&sort=popular&limit=30"
        f"&curr=rub&locale=ru&lang=ru&dest=12358512"
    )
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        return resp.json().get("data", {}).get("products", [])
    except Exception as e:
        print(f"Ошибка поиска: {e}")
        return []


@dp.message(CommandStart())
async def cmd_start(msg: types.Message):
    text = (
        "<b>👋 Привет!</b>\n\n"
        "🤖 Я — бот, который поможет тебе найти <u>лучший товар</u> по твоему запросу.\n\n"
        "🧪 Сейчас я работаю в <b>тестовом режиме</b> и ищу товары только на <b>Wildberries</b>.\n\n"
        "🔍 Просто отправь название товара, например:\n"
        "<i>солнцезащитный крем</i> или <i>беспроводные наушники</i> — и я подберу лучший вариант по рейтингу, отзывам и цене! 💡"
    )
    await msg.answer(text, parse_mode=ParseMode.HTML)


@dp.message(F.text == "/about")
async def cmd_about(msg: types.Message):
    text = (
        "<b>ℹ️ О боте</b>\n\n"
        "🔍 Бот использует алгоритм на базе нейросетевой модель для оценки релевантности, цены, отзывов и рейтинга товаров.\n\n"
        "🧠 Технологии:\n"
        "• Python + Aiogram\n"
        "• Модель для анализа товаров"
        "\n"
        "• Wildberries API для получения товаров"
    )
    await msg.answer(text, parse_mode=ParseMode.HTML)



@dp.message(F.text)
async def handle_message(msg: types.Message):
    query = msg.text.strip()
    products_raw = search_wb(query)

    if not products_raw:
        await msg.answer("По вашему запросу ничего не найдено.")
        return

    products = []
    for p in products_raw:
        products.append({
            "id": p.get("id"),
            "title": p.get("name", ""),
            "brand": p.get("brand", "?"),
            "price": p.get("salePriceU", 0) / 100,
            "full_price": p.get("priceU", 0) / 100,
            "rating": p.get("reviewRating", 0),
            "reviews": p.get("feedbacks", 0),
            "url": f"https://www.wildberries.ru/catalog/{p.get('id')}/detail.aspx"
        })

    try:
        best_product, mistral_comment = mistral_api.get_best_product_with_comment(query, products)
    except Exception as e:
        await msg.answer(f"Ошибка при обращении к Mistral: {e}")
        return

    text = (
        f"<b>{best_product['title']}</b>\n"
        f"Бренд: {best_product['brand']}\n"
        f"Цена: {best_product['price']:.2f} ₽ (до скидки: {best_product['full_price']:.2f} ₽)\n"
        f"Рейтинг: {best_product['rating']}⭐\n({best_product['reviews']} отзывов)"
    )
    if mistral_comment:
        text += f"\n\n<i>{mistral_comment}</i>"

    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text="Открыть на Wildberries",
            url=best_product["url"]
        )
    )

    await msg.answer(text, parse_mode=ParseMode.HTML, reply_markup=kb.as_markup())


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
