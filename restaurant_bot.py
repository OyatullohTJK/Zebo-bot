#!/usr/bin/env python3
# python-telegram-bot 22.6

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

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
        {"name": "Цезарь бо гушти мург", "price": 5, "desc": "Гӯшти мурғ, барги салат, нончаҳои биреншуда, панири parmesan, майонез, сир, шарбати лимӯ, равғани зайтун, намак ва қаламфури сиёҳ", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Caesar_salad_%281%29.jpg/800px-Caesar_salad_%281%29.jpg"},
        {"name": "Хӯриши Юнонӣ", "price": 5, "desc": "Сабзавои тару тоза, Зайтун, панири фета", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Greek_salad.jpg/800px-Greek_salad.jpg"},
        {"name": "Алевия бо гушти мург", "price": 5, "desc": "Гӯшти мурғ, картошка, сабзӣ, тухм, бодиринги намакӣ, нахӯди консервашуда, майонез", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Caesar_salad_%281%29.jpg/800px-Caesar_salad_%281%29.jpg"},
        {"name": "Хуриши Агарот", "price": 5, "desc": "Бодиринги тару тоза, помидор, карам, сабзӣ, қаламфури булғорӣ, кабудиҳо, намак, равғани растанӣ, сирко е шарбати лимӯ", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Greek_salad.jpg/800px-Greek_salad.jpg"},
    ],
    "Хӯрокҳои гарм": [
        {"name": "Хом Шӯрбо бо гушти гов", "price": 12, "desc": "Гӯшти гови устухондор, сабзӣ, картошка, дунба ё равған, помидор", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Borscht_served_in_Minsk%2C_Belarus.jpg/800px-Borscht_served_in_Minsk%2C_Belarus.jpg"},
        {"name": "Ҷаварӣ", "price": 12, "desc": "Гӯшти қима ва гов, донагиҳо (мош, лубие ё фасол), сабзавот, равған", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Grilled-chicken.jpg/800px-Grilled-chicken.jpg"},
        {"name": "Мастова", "price": 12, "desc": "Гӯшти гов ё гӯсфанд, биринҷ, сабзавот, равган", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Fresh_made_Carbonara_from_Rome.jpg/800px-Fresh_made_Carbonara_from_Rome.jpg"},
        {"name": "Хом Шӯрбо бо гушти гӯсфанд", "price": 12, "desc": "Гӯшти гӯсфанди устухондор, сабзӣ, картошка, дунба ё равған, помидор", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Borscht_served_in_Minsk%2C_Belarus.jpg/800px-Borscht_served_in_Minsk%2C_Belarus.jpg"},
        {"name": "Рассолник", "price": 12, "desc": "Гӯшти қима ва гов, бодиринги намакӣ, сабзавот, ҷави марворид, биринҷ", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Grilled-chicken.jpg/800px-Grilled-chicken.jpg"},
    ],
    "Хӯрокҳои дуюм": [
        {"name": "Картошка бирен", "price": 12, "desc": "Картошка, равған, намак", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/800px-Eq_it-na_pizza-margherita_sep2005_sml.jpg"},
        {"name": "Картошка пюре", "price": 12, "desc": "Картошка, равғани маска, намак", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Supreme_pizza.jpg/800px-Supreme_pizza.jpg"},
        {"name": "Макарон", "price": 12, "desc": "Макарон, равған, намак, об", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/800px-Eq_it-na_pizza-margherita_sep2005_sml.jpg"},
        {"name": "Марҷумак (гречка)", "price": 12, "desc": "Марҷумак, об, намак, равғани маска", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Supreme_pizza.jpg/800px-Supreme_pizza.jpg"},
    ],
    "Нӯшокиҳо": [
        {"name": "Соки натуралӣ", "price": 3, "desc": "Олуча / зардолу / шафтолу", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/OrangeJuice.jpg/800px-OrangeJuice.jpg"},
        {"name": "Чойҳо", "price": 2, "desc": "Чойи сабз ё сиёҳ", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/A_small_cup_of_coffee.JPG/800px-A_small_cup_of_coffee.JPG"},
        {"name": "Обҳои газнок", "price": 3, "desc": "Оби газнок хунук", "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/A_small_cup_of_coffee.JPG/800px-A_small_cup_of_coffee.JPG"},
    ],
}

ENTER_NAME, ENTER_PHONE, ENTER_ADDRESS = range(3)
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

active_orders = {}
order_counter = [0]


def main_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📋 Меню", callback_data="menu")],
        [InlineKeyboardButton("🛒 Сабад", callback_data="cart")],
        [InlineKeyboardButton("📍 Суроғаи мо", callback_data="location")],
        [InlineKeyboardButton("📞 Тамос", callback_data="contacts")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        f"Хуш омадед ба {KITCHEN_INFO['name']}! 🍽️\n\nРо интихоб кунед:",
        reply_markup=main_kb()
    )


async def cb_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(
        f"Хуш омадед ба {KITCHEN_INFO['name']}! 🍽️\n\nРо интихоб кунед:",
        reply_markup=main_kb()
    )


async def cb_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    kb = [[InlineKeyboardButton(cat, callback_data="cat|" + cat)] for cat in MENU]
    kb.append([InlineKeyboardButton("🏠 Бош меню", callback_data="main_menu")])
    await q.edit_message_text("📋 Категорияро интихоб кунед:", reply_markup=InlineKeyboardMarkup(kb))


async def cb_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    category = q.data.split("|", 1)[1]
    context.user_data["cat"] = category
    dishes = MENU[category]
    kb = [[InlineKeyboardButton(f"{d['name']} - {d['price']} сомон", callback_data=f"dish|{i}")] for i, d in enumerate(dishes)]
    kb.append([InlineKeyboardButton("◀️ Бозгашт", callback_data="menu")])
    await q.edit_message_text(f"{category}\n\nТаомро интихоб кунед:", reply_markup=InlineKeyboardMarkup(kb))


async def cb_dish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    idx = int(q.data.split("|")[1])
    category = context.user_data.get("cat", "")
    dish = MENU[category][idx]
    context.user_data["dish"] = dish
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Ба сабад", callback_data=f"add|{idx}")],
        [InlineKeyboardButton("◀️ Бозгашт", callback_data="cat|" + category)],
    ])
    caption = f"{dish['name']}\n\n{dish['desc']}\n\nНарх: {dish['price']} сомон"
    try:
        await q.message.reply_photo(photo=dish["photo_url"], caption=caption, reply_markup=kb)
        await q.message.delete()
    except Exception as e:
        logging.error(f"Photo error: {e}")
        await q.edit_message_text(caption, reply_markup=kb)


async def cb_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer("✅ Ба сабад илова шуд!")
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
        [InlineKeyboardButton("🛒 Сабад", callback_data="cart")],
        [InlineKeyboardButton("📋 Идома", callback_data="menu")],
    ])
    try:
        await q.edit_message_caption(caption=f"✅ {dish['name']} илова шуд!\n\nЧи карданием?", reply_markup=kb)
    except Exception:
        await q.edit_message_text(f"✅ {dish['name']} илова шуд!\n\nЧи карданием?", reply_markup=kb)


async def cb_cart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    cart = context.user_data.get("cart", [])
    if not cart:
        await q.edit_message_text(
            "🛒 Сабад холист.\n\nТаом илова кунед!",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 Меню", callback_data="menu")],
                [InlineKeyboardButton("🏠 Бош меню", callback_data="main_menu")],
            ])
        )
        return
    text = "🛒 Сабади шумо:\n\n"
    total = 0
    for i, item in enumerate(cart):
        sub = item["price"] * item["qty"]
        total += sub
        text += f"{i+1}. {item['name']} x{item['qty']} = {sub} сомон\n"
    text += f"\nХамаги: {total} сомон"
    await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Фармоиш додан", callback_data="checkout")],
        [InlineKeyboardButton("🗑 Тоза кардан", callback_data="clear_cart")],
        [InlineKeyboardButton("📋 Идома", callback_data="menu")],
        [InlineKeyboardButton("🏠 Бош меню", callback_data="main_menu")],
    ]))


async def cb_clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer("🗑 Сабад тоза шуд")
    context.user_data["cart"] = []
    await q.edit_message_text("🗑 Сабад тоза шуд.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📋 Меню", callback_data="menu")]]))


async def cb_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text("📝 Фармоиш додан\n\nНоми худро нависед:")
    return ENTER_NAME


async def enter_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["order_name"] = update.message.text
    await update.message.reply_text("📞 Рақами телефонатонро нависед:")
    return ENTER_PHONE


async def enter_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["order_phone"] = update.message.text
    await update.message.reply_text(
        "📦 Усули гирифтанро интихоб кунед:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏃 Худ мегирам", callback_data="pickup")],
            [InlineKeyboardButton("🚚 Расонидан", callback_data="delivery")],
        ])
    )
    return ENTER_ADDRESS


async def choose_delivery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "pickup":
        context.user_data["order_addr"] = "Худ мегирад — " + KITCHEN_INFO["address"]
        await do_finalize(q, context)
        return ConversationHandler.END
    await q.edit_message_text("🏠 Суроғаи расонидан:")
    return ENTER_ADDRESS


async def enter_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["order_addr"] = "Расонидан: " + update.message.text
    await do_finalize(update, context)
    return ConversationHandler.END


async def do_finalize(src, context: ContextTypes.DEFAULT_TYPE):
    cart = context.user_data.get("cart", [])
    total = sum(i["price"] * i["qty"] for i in cart)
    name = context.user_data.get("order_name", "-")
    phone = context.user_data.get("order_phone", "-")
    addr = context.user_data.get("order_addr", "-")

    order_counter[0] += 1
    order_id = order_counter[0]

    # Сообщение клиенту
    client_text = (
        f"✅ Фармоиши шумо қабул шуд!\n\n"
        f"🔢 Рақами фармоиш: #{order_id}\n"
        f"👤 Ном: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"📦 {addr}\n\n"
        f"🛒 Таркиби фармоиш:\n"
    )
    for item in cart:
        client_text += f"• {item['name']} x{item['qty']} = {item['price']*item['qty']} сомон\n"
    client_text += f"\n💰 Хамаги: {total} сомон\n\nБо шумо тамос мегирем. Ташаккур! 🙏"

    kb = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Бош меню", callback_data="main_menu")]])

    if hasattr(src, "data"):
        client_chat_id = src.message.chat_id
        await src.edit_message_text(client_text, reply_markup=kb)
    else:
        client_chat_id = src.message.chat_id
        await src.message.reply_text(client_text, reply_markup=kb)

    # Сохраняем заказ
    active_orders[order_id] = {"client_id": client_chat_id, "name": name, "phone": phone}

    # Уведомление администратору
    admin_text = (
        f"🔔 ЯНГИ ФАРМОИШ #{order_id}!\n\n"
        f"👤 Ном: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"📦 {addr}\n\n"
        f"🛒 Таркиб:\n"
    )
    for item in cart:
        admin_text += f"• {item['name']} x{item['qty']} = {item['price']*item['qty']} сомон\n"
    admin_text += f"\n💰 Хамаги: {total} сомон"

    admin_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Қабул кардан", callback_data=f"accept|{order_id}")],
        [InlineKeyboardButton("❌ Бекор кардан", callback_data=f"reject|{order_id}")],
    ])

    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text, reply_markup=admin_kb)
    except Exception as e:
        logging.error(f"Admin notify error: {e}")

    context.user_data["cart"] = []


async def cb_admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    action, order_id_str = q.data.split("|")
    order_id = int(order_id_str)
    order = active_orders.get(order_id)

    if not order:
        await q.edit_message_text(q.message.text + "\n\n⚠️ Фармоиш ёфт нашуд.")
        return

    client_id = order["client_id"]
    name = order["name"]

    if action == "accept":
        try:
            await context.bot.send_message(
                chat_id=client_id,
                text=f"✅ {name}, фармоиши шумо #{order_id} қабул шуд!\n\nБа зудӣ омода мешавад. Ташаккур! 🙏"
            )
        except Exception as e:
            logging.error(f"Client notify error: {e}")
        await q.edit_message_text(q.message.text + f"\n\n✅ ҚАБУЛ ШУД — {name} огоҳ карда шуд.")

    elif action == "reject":
        try:
            await context.bot.send_message(
                chat_id=client_id,
                text=f"❌ {name}, мутаассифона фармоиши шумо #{order_id} бекор карда шуд.\n\nБарои маълумот занг занед: {KITCHEN_INFO['phone']}"
            )
        except Exception as e:
            logging.error(f"Client notify error: {e}")
        await q.edit_message_text(q.message.text + f"\n\n❌ БЕКОР ШУД — {name} огоҳ карда шуд.")

    active_orders.pop(order_id, None)


async def cb_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.message.reply_location(latitude=KITCHEN_INFO["location_lat"], longitude=KITCHEN_INFO["location_lon"])
    await q.message.reply_text(
        f"📍 {KITCHEN_INFO['name']}\n\nСуроға: {KITCHEN_INFO['address']}\nВақти кор: {KITCHEN_INFO['hours']}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Бош меню", callback_data="main_menu")]])
    )
    await q.message.delete()


async def cb_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text(
        f"📞 {KITCHEN_INFO['name']}\n\nТелефон: {KITCHEN_INFO['phone']}\nСуроға: {KITCHEN_INFO['address']}\nВақти кор: {KITCHEN_INFO['hours']}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Бош меню", callback_data="main_menu")]])
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бекор шуд.", reply_markup=main_kb())
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
    app.add_handler(CallbackQueryHandler(cb_admin_action, pattern="^(accept|reject)\\|"))
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
    
