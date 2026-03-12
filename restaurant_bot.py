#!/usr/bin/env python3
# python-telegram-bot 22.6
# Для Railway/сервера - токен берётся из переменной окружения

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Токен берётся из переменной окружения (для Railway)
# Если запускаешь локально — замени на свой токен в кавычках
BOT_TOKEN = os.environ.get("BOT_TOKEN", "ВСТАВЬ_ТОКЕН_ЗДЕСЬ") 
ADMIN_ID = 5660517750

KITCHEN_INFO = {
    "name": "Ошхонаи ЗЕБО",
    "address": "Бозори марказии шаҳри Исфара дар зери маҷмуаи Зебо",
    "phone": "+992 025971616",
    "hours": "Вақти корӣ: 7:00 - 17:00",
    "location_lat": 40.12498,
    "location_lon": 70.62566,
}

MENU = {
    "Хӯришҳо": [
        {"name": "Цезарь бо гушти мург", "price": 5, "desc": "Гӯшти мурғ, барги салат, нончаҳои биреншуда(croutons), панири (parmesan), майонез ё зардии тухм, сир, шарбати лимӯ, равғани зайтун, панири пармезан, намак ва қаламфури сиёҳ", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Caesar_salad_%281%29.jpg/800px-Caesar_salad_%281%29.jpg"},
        {"name": "Хӯриши Юнонӣ", "price": 5, "desc": "Сабзавои тару тоза, Зайтун, панири фета", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Greek_salad.jpg/800px-Greek_salad.jpg"},
        {"name": "Алевия бо гушти мург", "price": 5, "desc": "Гӯшти мурғ, картошка, сабзӣ, тухм, бодиринги намакӣ, нахӯди консервашуда, майонез", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Caesar_salad_%281%29.jpg/800px-Caesar_salad_%281%29.jpg"},
        {"name": "Хуриши Агарот", "price": 5, "desc": "Бодиринги тару тоза, помидор, карам, сабзӣ,қаламфури булғорӣ, кабудиҳо(шибит ва петрушка), намак, равғани растанӣ, сирко е шарбати лимӯ", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Greek_salad.jpg/800px-Greek_salad.jpg"},
    ],
    "Хӯрокҳои гарм": [
        {"name": "Хом Шӯрбо бо гушти гов", "price": 12, "desc": "Гӯшти гови устухондор, сабзӣ, картошка, дунба ё равған, помидор", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Fresh_made_Carbonara_from_Rome.jpg/800px-Fresh_made_Carbonara_from_Rome.jpg"},
        {"name": "Ҷаварӣ", "price": 12, "desc": "Гӯшти қима ва гов, Донагиҳо ( мош, лубие ё фасол), сабзавот, равған", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Grilled-chicken.jpg/800px-Grilled-chicken.jpg"},
        {"name": "Мастова", "price": 12, "desc": "Гӯшти гов ё гӯсфанд, биринҷ, сабзавот, равган", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Borscht_served_in_Minsk%2C_Belarus.jpg/800px-Borscht_served_in_Minsk%2C_Belarus.jpg"},
        {"name": "Хом Шӯрбо бо гушти гӯсфанд", "price": 12, "desc": "Гӯшти гӯсфанди и устухондор, сабзӣ, картошка, дунба ё равған, помидор", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Fresh_made_Carbonara_from_Rome.jpg/800px-Fresh_made_Carbonara_from_Rome.jpg"},
        {"name": "Рассолник", "price": 12, "desc": "Гӯшти қима ва гов, бодиринги намакӣ, сабзавот, ҷави марворид (перловка), биринҷ", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Grilled-chicken.jpg/800px-Grilled-chicken.jpg"},  
    ],
    "Хӯрокҳои дуюм": [
        {"name": "Картошка бирен", "price": 12, "desc": "Картошка, равған, намак", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/800px-Eq_it-na_pizza-margherita_sep2005_sml.jpg"},
        {"name": "Картошка пюре", "price": 12, "desc": "картошка, равғани маска, намак", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Supreme_pizza.jpg/800px-Supreme_pizza.jpg"},
        {"name": "Макарон", "price": 12, "desc": "Макарон, равған, намак, об", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/800px-Eq_it-na_pizza-margherita_sep2005_sml.jpg"},
        {"name": "Марҷумак (гречка)", "price": 12, "desc": "Марҷумак (гречка), об, намак, равғани маска", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Supreme_pizza.jpg/800px-Supreme_pizza.jpg"},
    ],
    "Напитки": [
        {"name": "Соки натуралӣ", "price": 3, "desc": "олуча / зардолу / шафтолу", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/OrangeJuice.jpg/800px-OrangeJuice.jpg"},
        {"name": "Чойҳо", "price": 2, "desc": "Горячие напитки на выбор", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/A_small_cup_of_coffee.JPG/800px-A_small_cup_of_coffee.JPG"},
        {"name": "Обҳои газнок", "price": 13, "desc": "Горячие напитки на выбор", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/A_small_cup_of_coffee.JPG/800px-A_small_cup_of_coffee.JPG"},
    ],
}

ENTER_NAME, ENTER_PHONE, ENTER_ADDRESS = range(3)
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)


def main_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Меню", callback_data="menu")],
        [InlineKeyboardButton("Корзина", callback_data="cart")],
        [InlineKeyboardButton("Наш адрес", callback_data="location")],
        [InlineKeyboardButton("Контакты", callback_data="contacts")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        f"Добро пожаловать в {KITCHEN_INFO['name']}!\n\nВыберите раздел:",
        reply_markup=main_kb()
    )


async def cb_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(
        f"Добро пожаловать в {KITCHEN_INFO['name']}!\n\nВыберите раздел:",
        reply_markup=main_kb()
    )


async def cb_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    kb = [[InlineKeyboardButton(cat, callback_data="cat|" + cat)] for cat in MENU]
    kb.append([InlineKeyboardButton("Главное меню", callback_data="main_menu")])
    await q.edit_message_text("Выберите категорию:", reply_markup=InlineKeyboardMarkup(kb))


async def cb_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    category = q.data.split("|", 1)[1]
    context.user_data["cat"] = category
    dishes = MENU[category]
    kb = [[InlineKeyboardButton(f"{d['name']} - {d['price']} руб.", callback_data=f"dish|{i}")] for i, d in enumerate(dishes)]
    kb.append([InlineKeyboardButton("Назад", callback_data="menu")])
    await q.edit_message_text(f"{category}\n\nВыберите блюдо:", reply_markup=InlineKeyboardMarkup(kb))


async def cb_dish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    idx = int(q.data.split("|")[1])
    category = context.user_data.get("cat", "")
    dish = MENU[category][idx]
    context.user_data["dish"] = dish
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("В корзину", callback_data=f"add|{idx}")],
        [InlineKeyboardButton("Назад", callback_data="cat|" + category)],
    ])
    caption = f"{dish['name']}\n\n{dish['desc']}\n\nЦена: {dish['price']} руб."
    try:
        await q.message.reply_photo(photo=dish["photo_url"], caption=caption, reply_markup=kb)
        await q.message.delete()
    except Exception as e:
        logging.error(f"Photo error: {e}")
        await q.edit_message_text(caption, reply_markup=kb)


async def cb_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer("Добавлено в корзину!")
    dish = context.user_data.get("dish")
    if not dish:
        return
    cart = context.user_data.setdefault("cart", [])
    for item in cart:
        if item["name"] == dish["name"]:
            item["qty"] += 1
            break
    else:
        cart.append({"name": dish["name"], "price": dish["price"], "qty": 1})
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("Корзина", callback_data="cart")],
        [InlineKeyboardButton("Продолжить", callback_data="menu")],
    ])
    try:
        await q.edit_message_caption(caption=f"{dish['name']} добавлен!\n\nЧто дальше?", reply_markup=kb)
    except Exception:
        await q.edit_message_text(f"{dish['name']} добавлен!\n\nЧто дальше?", reply_markup=kb)


async def cb_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    cart = context.user_data.get("cart", [])
    if not cart:
        await q.edit_message_text("Корзина пуста.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("В меню", callback_data="menu")],
                [InlineKeyboardButton("Главное меню", callback_data="main_menu")],
            ]))
        return
    text = "Ваша корзина:\n\n"
    total = 0
    for i, item in enumerate(cart):
        sub = item["price"] * item["qty"]
        total += sub
        text += f"{i+1}. {item['name']} x{item['qty']} = {sub} руб.\n"
    text += f"\nИтого: {total} руб."
    await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("Оформить заказ", callback_data="checkout")],
        [InlineKeyboardButton("Очистить", callback_data="clear_cart")],
        [InlineKeyboardButton("Продолжить", callback_data="menu")],
        [InlineKeyboardButton("Главное меню", callback_data="main_menu")],
    ]))


async def cb_clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer("Корзина очищена")
    context.user_data["cart"] = []
    await q.edit_message_text("Корзина очищена.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("В меню", callback_data="menu")]]))


async def cb_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text("Оформление заказа\n\nВведите ваше имя:")
    return ENTER_NAME


async def enter_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["order_name"] = update.message.text
    await update.message.reply_text("Введите номер телефона:")
    return ENTER_PHONE


async def enter_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["order_phone"] = update.message.text
    await update.message.reply_text("Выберите способ получения:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Самовывоз", callback_data="pickup")],
            [InlineKeyboardButton("Доставка", callback_data="delivery")],
        ]))
    return ENTER_ADDRESS


async def choose_delivery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "pickup":
        context.user_data["order_addr"] = "Самовывоз - " + KITCHEN_INFO["address"]
        await do_finalize(q, context)
        return ConversationHandler.END
    await q.edit_message_text("Введите адрес доставки:")
    return ENTER_ADDRESS


async def enter_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["order_addr"] = "Доставка: " + update.message.text
    await do_finalize(update, context)
    return ConversationHandler.END


async def do_finalize(src, context):
    cart = context.user_data.get("cart", [])
    total = sum(i["price"] * i["qty"] for i in cart)
    name = context.user_data.get("order_name", "-")
    phone = context.user_data.get("order_phone", "-")
    addr = context.user_data.get("order_addr", "-")
    text = f"Заказ принят!\n\nИмя: {name}\nТелефон: {phone}\n{addr}\n\nСостав:\n"
    for item in cart:
        text += f"- {item['name']} x{item['qty']} = {item['price']*item['qty']} руб.\n"
    text += f"\nИтого: {total} руб.\n\nМы свяжемся с вами. Спасибо!"
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("Главное меню", callback_data="main_menu")]])
    if hasattr(src, "data"):
        await src.edit_message_text(text, reply_markup=kb)
    else:
        await src.message.reply_text(text, reply_markup=kb)
    context.user_data["cart"] = []
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text="🔔 ЯНГИ ФАРМОИШ!\n\n" + text)
    except Exception:
        pass


async def cb_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_location(latitude=KITCHEN_INFO["location_lat"], longitude=KITCHEN_INFO["location_lon"])
    await q.message.reply_text(
        f"{KITCHEN_INFO['name']}\n\nАдрес: {KITCHEN_INFO['address']}\nРежим работы: {KITCHEN_INFO['hours']}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Главное меню", callback_data="main_menu")]])
    )
    await q.message.delete()


async def cb_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(
        f"Контакты {KITCHEN_INFO['name']}\n\nТелефон: {KITCHEN_INFO['phone']}\nАдрес: {KITCHEN_INFO['address']}\nРежим работы: {KITCHEN_INFO['hours']}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Главное меню", callback_data="main_menu")]])
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отменено.", reply_markup=main_kb())
    return ConversationHandler.END


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(cb_checkout, pattern="^checkout$")],
        states={
            ENTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_name)],
            ENTER_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_phone)],
            ENTER_ADDRESS: [
                CallbackQueryHandler(choose_delivery, pattern="^(pickup|delivery)$"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, enter_address),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=False,
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(cb_main_menu, pattern="^main_menu$"))
    app.add_handler(CallbackQueryHandler(cb_menu,      pattern="^menu$"))
    app.add_handler(CallbackQueryHandler(cb_category,  pattern="^cat\\|"))
    app.add_handler(CallbackQueryHandler(cb_dish,      pattern="^dish\\|"))
    app.add_handler(CallbackQueryHandler(cb_add,       pattern="^add\\|"))
    app.add_handler(CallbackQueryHandler(cb_cart,      pattern="^cart$"))
    app.add_handler(CallbackQueryHandler(cb_clear,     pattern="^clear_cart$"))
    app.add_handler(CallbackQueryHandler(cb_location,  pattern="^location$"))
    app.add_handler(CallbackQueryHandler(cb_contacts,  pattern="^contacts$"))
    print("Бот запущен!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
