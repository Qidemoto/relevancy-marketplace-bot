# 🛍️ МаркетБот — Telegram-бот для поиска лучших товаров

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![Aiogram](https://img.shields.io/badge/aiogram-3.x-blueviolet?style=flat-square)
![Mistral AI](https://img.shields.io/badge/Mistral-AI-orange?style=flat-square)

**МаркетБот** — это интеллектуальный Telegram-бот, который поможет тебе быстро найти лучшие товары на маркетплейсах.  
На текущий момент поддерживается Wildberries. В будущем планируется добавление Ozon и Яндекс.Маркета.

## 🚀 Возможности

- 🔍 Поиск товаров по запросу
- 🧠 Выбор наилучшего варианта с помощью модели от Mistral AI
- 📊 Учет рейтинга, отзывов, бренда и цены
- 📦 Быстрая ссылка на карточку товара

## 📸 Примеры использования

```
/start

солнцезащитный крем
```

Бот ответит:
```
Бренд: Nivea
Цена: 399.00 ₽ (до скидки: 599.00 ₽)
Рейтинг: 4.8⭐
(3124 отзывов)

Причина: самый высокий рейтинг при низкой цене, подходит под запрос
[Открыть на Wildberries]
```

## 🛠️ Технологии

- Python 3.10+
- [Aiogram 3](https://github.com/aiogram/aiogram)
- [Mistral API](https://docs.mistral.ai)
- Wildberries API (неофициальный)
- dotenv для хранения конфигурации

## 🔧 Установка и запуск

1. Клонируй репозиторий:
   ```bash
   git clone https://github.com/Qidemoto/relevancy-marketplace-bot
   cd relevancy-marketplace-bot
   ```

2. Установи зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Создай `.env` файл и добавь свои ключи:
   ```dotenv
   TOKEN=твой_telegram_token
   MISTRAL_API_KEY=твой_mistral_api_key
   ```

4. Запусти бота:
   ```bash
   python main.py
   ```

## 📁 Структура проекта

```
.
├── main.py                # Основной бот
├── mistral_api.py         # Обращение к Mistral для оценки товаров
├── .env                   # Переменные окружения
├── README.md              # Описание проекта
└── requirements.txt       # Зависимости
```

## 📌 Планы

* ✅ Поиск по Wildberries
* 🔄 Добавление Яндекс.Маркета
* 🔄 Добавление Ozon
* 🔄 Отслеживание цен и уведомления
* 🔄 Отображение графика изменения цены

## 🤝 Контакты

---

> Проект в активной разработке 🚧
