import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")  # Ключ в .env
API_URL = "https://api.mistral.ai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {MISTRAL_API_KEY}",
    "Content-Type": "application/json"
}

def build_prompt(query, products):
    prompt = (
        f"Ты — помощник, который оценивает товары по запросу пользователя.\n"
        f"Запрос: \"{query}\"\n"
        f"Вот список товаров с характеристиками:\n"
    )
    for i, p in enumerate(products):
        prompt += (
            f"{i} - Название: {p['title']}\n"
            f"    Бренд: {p['brand']}\n"
            f"    Цена: {p['price']:.2f} ₽ (до скидки: {p['full_price']:.2f} ₽)\n"
            f"    Рейтинг: {p['rating']}⭐\n"
            f"    Отзывы: {p['reviews']}\n"
        )
    prompt += (
        "Проанализируй товары и выбери лучший, учитывая, что он должен быть в первую очередь дешевле аналогов,"
        "название должно логически соответствать запросу и бренду, много отзывов (лучше - больше), хороший рейтинг.\n"
        "Ответ напиши строго и только в формате:\n"
        "<ID товара> - Причина: <объективная и краткая причина>\n"
    )
    return prompt

def query_mistral(prompt, retries=3, delay=1):
    body = {
        "model": "open-mistral-nemo",
        "messages": [
            {"role": "system", "content": "Ты эксперт по выбору товаров."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "top_p": 0.9
    }
    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=HEADERS, json=body)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise e

def parse_response(response_text, products):
    """
    Парсим ответ вида: 'id - комментарий'
    Возвращаем индекс товара и комментарий, если корректно, иначе None
    """
    if '-' not in response_text:
        return None, None
    parts = response_text.split('-', 1)
    id_part = parts[0].strip()
    comment_part = parts[1].strip()
    if not id_part.isdigit():
        return None, None
    index = int(id_part)
    if index < 0 or index >= len(products):
        return None, None
    return index, comment_part

def get_best_product_with_comment(query, products, max_attempts=5):
    prompt = build_prompt(query, products)
    for attempt in range(max_attempts):
        response = query_mistral(prompt)
        index, comment = parse_response(response, products)
        if index is not None:
            return products[index], comment
        time.sleep(2)  # Ждём перед повтором
    # Если не удалось получить корректный ответ - возвращаем первый товар и пустой комментарий
    return products[0], "Не удалось получить корректный комментарий от модели."
