#!/usr/bin/env python3
# python-telegram-bot 22.6
# Мега-бот Ошхонаи ЗЕБО

import logging
import os
import random
from datetime import datetime
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
    "min_order": 10,  # Минимальная сумма заказа
}

MENU = {
    "🥗 Хӯришҳо": [
        {"name": "Цезарь бо гушти мург", "price": 5, "desc": "Гӯшти мурғ, барги салат, нончаҳои биреншуда, панири parmesan", "spicy": 0, "calories": 320},
        {"name": "Хӯриши Юнонӣ", "price": 5, "desc": "Сабзавои тару тоза, зайтун, панири фета", "spicy": 0, "calories": 180},
        {"name": "Алевия бо гушти мург", "price": 5, "desc": "Гӯшти мурғ, картошка, сабзӣ, тухм, майонез", "spicy": 0, "calories": 280},
        {"name": "Хуриши Агарот", "price": 5, "desc": "Бодиринги тару тоза, помидор, карам, сабзӣ, кабудиҳо", "spicy": 0, "calories": 150},
    ],
    "🍲 Хӯрокҳои гарм": [
        {"name": "Хом Шӯрбо бо гушти гов", "price": 12, "desc": "Гӯшти гови устухондор, сабзӣ, картошка, помидор", "spicy": 1, "calories": 420},
        {"name": "Ҷаварӣ", "price": 12, "desc": "Гӯшти қима ва гов, мош, лубие, сабзавот", "spicy": 1, "calories": 380},
        {"name": "Мастова", "price": 12, "desc": "Гӯшти гов ё гӯсфанд, биринҷ, сабзавот", "spicy": 0, "calories": 350},
        {"name": "Хом Шӯрбо бо гушти гӯсфанд", "price": 12, "desc": "Гӯшти гӯсфанди устухондор, сабзӣ, картошка", "spicy": 1, "calories": 450},
        {"name": "Рассолник", "price": 12, "desc": "Гӯшти қима, бодиринги намакӣ, сабзавот, биринҷ", "spicy": 0, "calories": 320},
    ],
    "🍽️ Хӯрокҳои дуюм": [
        {"name": "Картошка бирен", "price": 12, "desc": "Картошка, равған, намак", "spicy": 0, "calories": 300},
        {"name": "Картошка пюре", "price": 12, "desc": "Картошка, равғани маска, намак", "spicy": 0, "calories": 250},
        {"name": "Макарон", "price": 12, "desc": "Макарон, равған, намак", "spicy": 0, "calories": 280},
        {"name": "Марҷумак (гречка)", "price": 12, "desc": "Марҷумак, об, намак, равғани маска", "spicy": 0, "calories": 220},
    ],
    "🌭 Колбаса ва сосис": [
        {"name": "Сосиска", "price": 3, "desc": "Сосискаи тару тоза", "spicy": 0, "calories": 180},
        {"name": "Сарделька", "price": 9, "desc": "Сарделькаи калон ва хушмаза", "spicy": 0, "calories": 250},
        {"name": "Колбаса", "price": 4, "desc": "Колбасаи буришашуда", "spicy": 0, "calories": 200},
        {"name": "Сосиска бо картошка", "price": 8, "desc": "Сосиска + картошка пюре — комбои серсер!", "spicy": 0, "calories": 430},
    ],
    "🔥 Шашлик ва кабоб": [
        {"name": "Сихкабоб бо г. Гови қима", "price": 14, "desc": "Шашлики гӯшти қимаи гов, бо сабзавот", "spicy": 2, "calories": 480},
        {"name": "Сихкабоб бо г. Мурғин", "price": 14, "desc": "Шашлики гӯшти мурғ, мулоим ва хушмаза", "spicy": 1, "calories": 350},
        {"name": "Сихкабоб бо г. Биқин", "price": 20, "desc": "Шашлики гӯшти биқин — серравған ва бисёр хушмаза", "spicy": 2, "calories": 580},
        {"name": "Самбусаи танӯрӣ", "price": 8, "desc": "Самбусаи танӯрӣ бо гӯшт, тару тоза аз танӯр", "spicy": 1, "calories": 320},
        {"name": "Самбӯсаи Духобка", "price": 3, "desc": "Самбӯсаи хурд — гӯшти қима ва алафӣ", "spicy": 1, "calories": 180},
        {"name": "Комбо Шашлик", "price": 35, "desc": "2 сих кабоб + самбуса + нӯшокӣ — сарфакорона!", "spicy": 2, "calories": 850},
    ],
    "🎂 Шириниҳо": [
        {"name": "Наполеон", "price": 10, "desc": "Торти Наполеон — қабатҳои тунук бо кремии ширин", "spicy": 0, "calories": 420},
        {"name": "Медовик", "price": 12, "desc": "Торти асал — мулоим ва хушбӯй", "spicy": 0, "calories": 480},
        {"name": "Ширинии рӯз", "price": 8, "desc": "Ширинии махсуси имрӯза — ҳар рӯз фарқ!", "spicy": 0, "calories": 300},
    ],
    "🥤 Нӯшокиҳо": [
        {"name": "Соки натуралӣ", "price": 3, "desc": "Олуча / зардолу / шафтолу", "spicy": 0, "calories": 120},
        {"name": "Чойҳо", "price": 2, "desc": "Чойи сабз ё сиёҳ", "spicy": 0, "calories": 5},
        {"name": "Обҳои газнок", "price": 3, "desc": "Оби газнок хунук", "spicy": 0, "calories": 40},
    ],
}

PROMOCODES = {
    "ZEBO10": 10,
    "ISFARA": 15,
    "WELCOME": 20,
}

JOKES = [
    "Чаро ошпаз ҳамеша хушҳол аст? Чунки кораш хушмаза аст! 😄",
    "Меҳмон пурсид: Ин таом чӣ ном дорад? Ошпаз гуфт: Таоми дил! ❤️",
    "Беҳтарин дорухона — ошхона! 🍽️",
]

ENTER_NAME, ENTER_PHONE, ENTER_ADDRESS, ENTER_PROMO, ENTER_REVIEW, ENTER_BROADCAST, ENTER_PREORDER_TIME = range(7)

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

active_orders = {}
order_counter = [0]
all_users = set()
pause_mode = [False]
vip_users = set()
user_points = {}
user_orders_history = {}
user_birthdays = {}
referrals = {}

SPICY_ICONS = {0: "", 1: "🌶️", 2: "🌶️🌶️", 3: "🌶️🌶️🌶️•"}


def main_kb(user_id=None):
    lang = get_lang(user_id)
    if lang == "tj":
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("📋 Меню", callback_data="menu"),
             InlineKeyboardButton("🛒 Сабад", callback_data="cart")],
            [InlineKeyboardButton("🎁 Акция", callback_data="promo"),
             InlineKeyboardButton("⭐ Холҳо", callback_data="my_points")],
            [InlineKeyboardButton("📍 Суроға", callback_data="location"),
             InlineKeyboardButton("📞 Тамос", callback_data="contacts")],
            [InlineKeyboardButton("🔍 Ҷустуҷӯ", callback_data="search"),
             InlineKeyboardButton("🎰 Бахт", callback_data="lucky_wheel")],
            [InlineKeyboardButton("🌍 Забон", callback_data="lang")],
        ])
    elif lang == "uz":
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("📋 Menyu", callback_data="menu"),
             InlineKeyboardButton("🛒 Savat", callback_data="cart")],
            [InlineKeyboardButton("🎁 Aksiya", callback_data="promo"),
             InlineKeyboardButton("⭐ Ballar", callback_data="my_points")],
            [InlineKeyboardButton("📍 Manzil", callback_data="location"),
             InlineKeyboardButton("📞 Aloqa", callback_data="contacts")],
            [InlineKeyboardButton("🔍 Qidiruv", callback_data="search"),
             InlineKeyboardButton("🎰 Omad", callback_data="lucky_wheel")],
            [InlineKeyboardButton("🌍 Til", callback_data="lang")],
        ])
    else:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("📋 Меню", callback_data="menu"),
             InlineKeyboardButton("🛒 Корзина", callback_data="cart")],
            [InlineKeyboardButton("🎁 Акции", callback_data="promo"),
             InlineKeyboardButton("⭐ Баллы", callback_data="my_points")],
            [InlineKeyboardButton("📍 Адрес", callback_data="location"),
             InlineKeyboardButton("📞 Контакты", callback_data="contacts")],
            [InlineKeyboardButton("🔍 Поиск", callback_data="search"),
             InlineKeyboardButton("🎰 Колесо", callback_data="lucky_wheel")],
            [InlineKeyboardButton("🌍 Язык", callback_data="lang")],
        ])


def get_lang(user_id):
    if not hasattr(get_lang, "langs"):
        get_lang.langs = {}
    return get_lang.langs.get(user_id, "tj")


def set_lang(user_id, lang):
    if not hasattr(get_lang, "langs"):
        get_lang.langs = {}
    get_lang.langs[user_id] = lang


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    all_users.add(user_id)
    context.user_data.clear()

    # Реферальная программа
    args = context.args
    if args and args[0].startswith("ref"):
        ref_id = int(args[0][3:])
        if ref_id != user_id and ref_id not in referrals.get(user_id, []):
            referrals.setdefault(ref_id, []).append(user_id)
            user_points[ref_id] = user_points.get(ref_id, 0) + 20
            try:
                await context.bot.send_message(chat_id=ref_id, text="🎉 Дӯсти шумо ба бот пайваст шуд! +20 хол гирифтед!")
            except:
                pass

    name = update.effective_user.first_name or "Меҳмон"
    points = user_points.get(user_id, 0)
    vip = "👑 VIP | " if user_id in vip_users else ""

    welcome = (
        f"Хуш омадед, {vip}{name}! 🍽️\n"
        f"⭐ Холҳои шумо: {points}\n\n"
        f"Ошхонаи ЗЕБО — таоми хушмаза!\n"
        f"Рӯзи хушбахт барои шумо! 😊"
    )
    await update.message.reply_text(welcome, reply_markup=main_kb(user_id))


async def cb_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    user_id = q.from_user.id
    name = q.from_user.first_name or "Меҳмон"
    points = user_points.get(user_id, 0)
    vip = "👑 VIP | " if user_id in vip_users else ""
    await q.edit_message_text(
        f"Хуш омадед, {vip}{name}! 🍽️\n⭐ Холҳои шумо: {points}\n\nРо интихоб кунед:",
        reply_markup=main_kb(user_id)
    )


# ==================== ЯЗЫК ====================
async def cb_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🇹🇯 Тоҷикӣ", callback_data="setlang|tj")],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="setlang|ru")],
        [InlineKeyboardButton("🇺🇿 O'zbek", callback_data="setlang|uz")],
    ])
    await q.edit_message_text("🌍 Забонро интихоб кунед / Выберите язык:", reply_markup=kb)


async def cb_setlang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    lang = q.data.split("|")[1]
    set_lang(q.from_user.id, lang)
    msgs = {"tj": "✅ Забони тоҷикӣ интихоб шуд!", "ru": "✅ Русский язык выбран!", "uz": "✅ O'zbek tili tanlandi!"}
    await q.edit_message_text(msgs.get(lang, "✅"), reply_markup=main_kb(q.from_user.id))


# ==================== МЕНЮ ====================
async def cb_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if pause_mode[0]:
        await q.edit_message_text("⏸️ Айни ҳол қабули фармоиш муваққатан қатъ шудааст.\nОдатан тамос гиред: " + KITCHEN_INFO["phone"])
        return
    kb = [[InlineKeyboardButton(cat, callback_data="cat|" + cat)] for cat in MENU]
    kb.append([InlineKeyboardButton("🏠 Бош меню", callback_data="main_menu")])
    cart = context.user_data.get("cart", [])
    cart_info = f"\n🛒 Дар сабад: {len(cart)} таом" if cart else ""
    await q.edit_message_text(f"📋 Категорияро интихоб кунед:{cart_info}", reply_markup=InlineKeyboardMarkup(kb))


async def cb_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    category = q.data.split("|", 1)[1]
    context.user_data["cat"] = category
    dishes = MENU[category]
    cart = context.user_data.get("cart", [])
    cart_names = {item["name"]: item["qty"] for item in cart}
    kb = []
    for i, d in enumerate(dishes):
        spicy = SPICY_ICONS.get(d.get("spicy", 0), "")
        in_cart = f" ✅{cart_names[d['name']]}" if d["name"] in cart_names else ""
        kb.append([InlineKeyboardButton(f"{d['name']} {spicy} — {d['price']}с{in_cart}", callback_data=f"dish|{i}")])
    kb.append([InlineKeyboardButton("🛒 Сабад", callback_data="cart"),
               InlineKeyboardButton("◀️ Бозгашт", callback_data="menu")])
    await q.edit_message_text(f"{category}\n\nТаомро интихоб кунед:", reply_markup=InlineKeyboardMarkup(kb))


async def cb_dish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    idx = int(q.data.split("|")[1])
    category = context.user_data.get("cat", "")
    dish = MENU[category][idx]
    context.user_data["dish"] = dish
    context.user_data["dish_idx"] = idx

    spicy = SPICY_ICONS.get(dish.get("spicy", 0), "")
    cal = dish.get("calories", 0)

    cart = context.user_data.get("cart", [])
    in_cart = sum(item["qty"] for item in cart if item["name"] == dish["name"])
    in_cart_text = f"\n✅ Дар сабад: {in_cart} дона" if in_cart else ""

    text = (
        f"🍽️ *{dish['name']}* {spicy}\n\n"
        f"📝 {dish['desc']}\n"
        f"🔥 Калория: {cal} ккал\n"
        f"💰 Нарх: *{dish['price']} сомон*"
        f"{in_cart_text}"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Илова", callback_data=f"add|{idx}"),
         InlineKeyboardButton("➖ Кам кун", callback_data=f"remove|{idx}")],
        [InlineKeyboardButton("🛒 Сабад", callback_data="cart"),
         InlineKeyboardButton("◀️ Бозгашт", callback_data=f"cat|{category}")],
    ])
    await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)


async def cb_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    idx = int(q.data.split("|")[1])
    category = context.user_data.get("cat", "")
    dish = MENU[category][idx]
    context.user_data["dish"] = dish

    cart = context.user_data.setdefault("cart", [])
    for item in cart:
        if item["name"] == dish["name"]:
            item["qty"] += 1
            break
    else:
        cart.append({"name": dish["name"], "price": dish["price"], "qty": 1})

    await q.answer(f"✅ {dish['name']} илова шуд!")

    # Остаёмся на том же блюде — обновляем страницу
    in_cart = sum(item["qty"] for item in cart if item["name"] == dish["name"])
    spicy = SPICY_ICONS.get(dish.get("spicy", 0), "")
    cal = dish.get("calories", 0)
    text = (
        f"🍽️ *{dish['name']}* {spicy}\n\n"
        f"📝 {dish['desc']}\n"
        f"🔥 Калория: {cal} ккал\n"
        f"💰 Нарх: *{dish['price']} сомон*\n"
        f"✅ Дар сабад: {in_cart} дона"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Илова", callback_data=f"add|{idx}"),
         InlineKeyboardButton("➖ Кам кун", callback_data=f"remove|{idx}")],
        [InlineKeyboardButton("🛒 Сабад", callback_data="cart"),
         InlineKeyboardButton("◀️ Бозгашт", callback_data=f"cat|{category}")],
    ])
    await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)


async def cb_remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    idx = int(q.data.split("|")[1])
    category = context.user_data.get("cat", "")
    dish = MENU[category][idx]

    cart = context.user_data.get("cart", [])
    for item in cart:
        if item["name"] == dish["name"]:
            item["qty"] -= 1
            if item["qty"] <= 0:
                cart.remove(item)
            break

    await q.answer(f"➖ {dish['name']} камшуд")

    in_cart = sum(item["qty"] for item in cart if item["name"] == dish["name"])
    spicy = SPICY_ICONS.get(dish.get("spicy", 0), "")
    cal = dish.get("calories", 0)
    in_cart_text = f"\n✅ Дар сабад: {in_cart} дона" if in_cart else ""
    text = (
        f"🍽️ *{dish['name']}* {spicy}\n\n"
        f"📝 {dish['desc']}\n"
        f"🔥 Калория: {cal} ккал\n"
        f"💰 Нарх: *{dish['price']} сомон*"
        f"{in_cart_text}"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Илова", callback_data=f"add|{idx}"),
         InlineKeyboardButton("➖ Кам кун", callback_data=f"remove|{idx}")],
        [InlineKeyboardButton("🛒 Сабад", callback_data="cart"),
         InlineKeyboardButton("◀️ Бозгашт", callback_data=f"cat|{category}")],
    ])
    await q.edit_message_text(text, parse_mode="Markdown", reply_markup=kb)


# ==================== КОРЗИНА ====================
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
    text = "🛒 *Сабади шумо:*\n\n"
    total = 0
    for i, item in enumerate(cart):
        sub = item["price"] * item["qty"]
        total += sub
        text += f"{i+1}. {item['name']} x{item['qty']} = {sub} с\n"

    promo_discount = context.user_data.get("promo_discount", 0)
    if promo_discount:
        discount = int(total * promo_discount / 100)
        text += f"\n🎁 Тахфиф: -{discount} с ({promo_discount}%)"
        total -= discount

    points = user_points.get(q.from_user.id, 0)
    text += f"\n💰 *Хамаги: {total} сомон*"
    text += f"\n⭐ Холҳои шумо: {points} (фармоиш +{max(1, total//10)} хол)"

    if total < KITCHEN_INFO["min_order"]:
        text += f"\n\n⚠️ Ҳадди ақали фармоиш: {KITCHEN_INFO['min_order']} сомон"

    kb_rows = [
        [InlineKeyboardButton("✅ Фармоиш додан", callback_data="checkout")],
        [InlineKeyboardButton("🎁 Промокод", callback_data="enter_promo"),
         InlineKeyboardButton("📅 Пешфармоиш", callback_data="preorder")],
        [InlineKeyboardButton("📋 Идома", callback_data="menu"),
         InlineKeyboardButton("🗑 Тоза", callback_data="clear_cart")],
        [InlineKeyboardButton("🏠 Бош меню", callback_data="main_menu")],
    ]
    await q.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb_rows))


async def cb_clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer("🗑 Сабад тоза шуд")
    context.user_data["cart"] = []
    context.user_data.pop("promo_discount", None)
    await q.edit_message_text("🗑 Сабад тоза шуд.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📋 Меню", callback_data="menu")]]))


# ==================== ПРОМОКОД ====================
async def cb_enter_promo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text("🎁 Промокодро нависед:")
    return ENTER_PROMO


async def process_promo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip().upper()
    if code in PROMOCODES:
        discount = PROMOCODES[code]
        context.user_data["promo_discount"] = discount
        await update.message.reply_text(
            f"✅ Промокод қабул шуд! Тахфиф: {discount}%",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🛒 Сабад", callback_data="cart")]]))
    else:
        await update.message.reply_text(
            "❌ Промокод нодуруст аст.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🛒 Сабад", callback_data="cart")]]))
    return ConversationHandler.END


# ==================== ПОИСК ====================
async def cb_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text("🔍 Номи таомро нависед:")
    context.user_data["searching"] = True


async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("searching"):
        return
    context.user_data["searching"] = False
    query = update.message.text.lower()
    results = []
    for cat, dishes in MENU.items():
        for i, dish in enumerate(dishes):
            if query in dish["name"].lower() or query in dish["desc"].lower():
                results.append((cat, i, dish))
    if not results:
        await update.message.reply_text("❌ Ёфт нашуд.", reply_markup=main_kb(update.effective_user.id))
        return
    kb = []
    for cat, i, dish in results[:8]:
        context.user_data["cat"] = cat
        kb.append([InlineKeyboardButton(f"{dish['name']} — {dish['price']}с", callback_data=f"dish|{i}")])
    kb.append([InlineKeyboardButton("🏠 Бош меню", callback_data="main_menu")])
    await update.message.reply_text(f"🔍 Натиҷа ({len(results)}):", reply_markup=InlineKeyboardMarkup(kb))


# ==================== АКЦИИ ====================
async def cb_promo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    text = (
        "🎁 *Акцияҳои имрӯза:*\n\n"
        "🔥 Комбо Шашлик — 35с (сарфа 8с!)\n"
        "☕ Чой бо Наполеон — 11с (сарфа 1с)\n"
        "🌟 3 хуриш = 1 нӯшокӣ ройгон!\n\n"
        "💳 *Промокодҳо:*\n"
        "• ZEBO10 — 10% тахфиф\n"
        "• ISFARA — 15% тахфиф\n"
        "• WELCOME — 20% барои нав!\n\n"
        "👑 *VIP мизоҷон:* 50 хол = VIP статус + 25% тахфиф"
    )
    await q.edit_message_text(text, parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Бош меню", callback_data="main_menu")]]))


# ==================== БАЛЛЫ ====================
async def cb_my_points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    user_id = q.from_user.id
    points = user_points.get(user_id, 0)
    is_vip = user_id in vip_users
    orders = len(user_orders_history.get(user_id, []))

    ref_link = f"https://t.me/Oshoni_zebo_bot?start=ref{user_id}"

    text = (
        f"⭐ *Холҳои шумо: {points}*\n\n"
        f"{'👑 Шумо VIP мизоҷ ҳастед!' if is_vip else '👤 Барои VIP: 50 хол лозим'}\n"
        f"📦 Фармоишҳо: {orders}\n\n"
        f"📊 Чӣ тавр хол ҷамъ кунед:\n"
        f"• Ҳар 10с фармоиш = 1 хол\n"
        f"• Дӯст даъват кунед = +20 хол\n"
        f"• Отзыв нависед = +5 хол\n\n"
        f"🔗 Линки даъват:\n{ref_link}"
    )
    await q.edit_message_text(text, parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Бош меню", callback_data="main_menu")]]))


# ==================== КОЛЕСО ФОРТУНЫ ====================
async def cb_lucky_wheel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    user_id = q.from_user.id
    prizes = [
        ("🎉 10% тахфиф барои фармоиши навбатӣ!", "LUCKY10", 10),
        ("🎊 Нӯшокии ройгон!", None, 0),
        ("⭐ +10 хол!", None, 0),
        ("😢 Бахт набуд, дафъаи дигар!", None, 0),
        ("🎁 15% тахфиф!", "LUCKY15", 15),
        ("🍀 +5 хол!", None, 0),
    ]
    prize = random.choice(prizes)
    if "хол" in prize[0]:
        bonus = int(prize[0].split("+")[1].split(" ")[0])
        user_points[user_id] = user_points.get(user_id, 0) + bonus
    if prize[2] > 0:
        context.user_data["promo_discount"] = prize[2]

    await q.edit_message_text(
        f"🎰 *Чархи бахт!*\n\n{prize[0]}",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Бош меню", callback_data="main_menu")]]))


# ==================== ОФОРМЛЕНИЕ ЗАКАЗА ====================
async def cb_checkout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    cart = context.user_data.get("cart", [])
    total = sum(i["price"] * i["qty"] for i in cart)
    promo_discount = context.user_data.get("promo_discount", 0)
    if promo_discount:
        total -= int(total * promo_discount / 100)
    if total < KITCHEN_INFO["min_order"]:
        await q.edit_message_text(
            f"⚠️ Ҳадди ақали фармоиш {KITCHEN_INFO['min_order']} сомон аст.\nХозир: {total} сомон.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📋 Меню", callback_data="menu")]]))
        return
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


# ==================== ПРЕДЗАКАЗ ====================
async def cb_preorder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    await q.edit_message_text("📅 Вақти расонидан/гирифтанро нависед (масалан: 14:30):")
    return ENTER_PREORDER_TIME


async def enter_preorder_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["preorder_time"] = update.message.text
    await update.message.reply_text(
        f"✅ Вақти пешфармоиш: {update.message.text}\n\nАкнун номатонро нависед:",
    )
    return ENTER_NAME


async def do_finalize(src, context: ContextTypes.DEFAULT_TYPE):
    cart = context.user_data.get("cart", [])
    total = sum(i["price"] * i["qty"] for i in cart)
    name = context.user_data.get("order_name", "-")
    phone = context.user_data.get("order_phone", "-")
    addr = context.user_data.get("order_addr", "-")
    preorder = context.user_data.get("preorder_time", "")
    promo_discount = context.user_data.get("promo_discount", 0)

    if promo_discount:
        discount = int(total * promo_discount / 100)
        total -= discount

    order_counter[0] += 1
    order_id = order_counter[0]

    time_str = f"\n⏰ Вақт: {preorder}" if preorder else ""
    joke = random.choice(JOKES)

    client_text = (
        f"✅ Фармоиши шумо қабул шуд!\n\n"
        f"🔢 Рақами фармоиш: #{order_id}\n"
        f"👤 Ном: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"📦 {addr}{time_str}\n\n"
        f"🛒 Таркиби фармоиш:\n"
    )
    for item in cart:
        client_text += f"• {item['name']} x{item['qty']} = {item['price']*item['qty']} с\n"
    if promo_discount:
        client_text += f"🎁 Тахфиф: {promo_discount}%\n"
    client_text += f"\n💰 Хамаги: {total} сомон\n\n😄 {joke}\n\nБо шумо тамос мегирем. Ташаккур! 🙏"

    kb = InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Бош меню", callback_data="main_menu")]])

    if hasattr(src, "data"):
        client_chat_id = src.message.chat_id
        await src.edit_message_text(client_text, reply_markup=kb)
    else:
        client_chat_id = src.message.chat_id
        await src.message.reply_text(client_text, reply_markup=kb)

    # Начисляем баллы
    bonus_points = max(1, total // 10)
    user_points[client_chat_id] = user_points.get(client_chat_id, 0) + bonus_points
    if user_points[client_chat_id] >= 50:
        vip_users.add(client_chat_id)

    # История заказов
    user_orders_history.setdefault(client_chat_id, []).append({
        "id": order_id, "total": total, "items": cart.copy()
    })

    active_orders[order_id] = {"client_id": client_chat_id, "name": name, "phone": phone}

    admin_text = (
        f"🔔 ЯНГИ ФАРМОИШ #{order_id}!\n\n"
        f"👤 Ном: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"📦 {addr}{time_str}\n\n"
        f"🛒 Таркиб:\n"
    )
    for item in cart:
        admin_text += f"• {item['name']} x{item['qty']} = {item['price']*item['qty']} с\n"
    if promo_discount:
        admin_text += f"🎁 Тахфиф: {promo_discount}%\n"
    admin_text += f"\n💰 Хамаги: {total} сомон"

    admin_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Қабул", callback_data=f"accept|{order_id}"),
         InlineKeyboardButton("❌ Бекор", callback_data=f"reject|{order_id}")],
        [InlineKeyboardButton("🚗 Курьер роҳ шуд", callback_data=f"courier|{order_id}"),
         InlineKeyboardButton("✅ Омода аст", callback_data=f"ready|{order_id}")],
    ])

    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text, reply_markup=admin_kb)
    except Exception as e:
        logging.error(f"Admin notify error: {e}")

    context.user_data["cart"] = []
    context.user_data.pop("promo_discount", None)
    context.user_data.pop("preorder_time", None)

    # Напоминание об отзыве через 30 минут (имитация)
    context.job_queue.run_once(
        remind_review, 1800,
        data={"client_id": client_chat_id, "order_id": order_id},
        name=f"review_{order_id}"
    )


async def remind_review(context: ContextTypes.DEFAULT_TYPE):
    data = context.job.data
    try:
        await context.bot.send_message(
            chat_id=data["client_id"],
            text=f"⭐ Фармоиши #{data['order_id']} чӣ тавр буд?\nЛутфан баҳо гузоред!",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("⭐ Баҳо гузоред", callback_data=f"review|{data['order_id']}")
            ]])
        )
    except:
        pass


# ==================== СТАТУСЫ ЗАКАЗА ====================
async def cb_admin_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    parts = q.data.split("|")
    action = parts[0]
    order_id = int(parts[1])
    order = active_orders.get(order_id)

    if not order:
        await q.edit_message_text(q.message.text + "\n\n⚠️ Фармоиш ёфт нашуд.")
        return

    client_id = order["client_id"]
    name = order["name"]

    messages = {
        "accept": f"✅ {name}, фармоиши шумо #{order_id} қабул шуд!\n\nБа зудӣ омода мешавад. Ташаккур! 🙏",
        "reject": f"❌ {name}, мутаассифона фармоиши шумо #{order_id} бекор карда шуд.\nТамос: {KITCHEN_INFO['phone']}",
        "courier": f"🚗 {name}, курьер роҳ шуд!\n\nФармоиши #{order_id} ба зудӣ мерасад!",
        "ready": f"✅ {name}, фармоиши шумо #{order_id} омода аст!\n\nШумо метавонед гиред.",
    }

    status_text = {
        "accept": "✅ ҚАБУЛ ШУД",
        "reject": "❌ БЕКОР ШУД",
        "courier": "🚗 КУРЬЕР РОҲ ШУД",
        "ready": "✅ ОМОДА АСТ",
    }

    try:
        await context.bot.send_message(chat_id=client_id, text=messages.get(action, ""))
    except Exception as e:
        logging.error(f"Client notify error: {e}")

    await q.edit_message_text(q.message.text + f"\n\n{status_text.get(action, '')} — {name} огоҳ карда шуд.")

    if action in ["reject", "ready"]:
        active_orders.pop(order_id, None)


# ==================== ОТЗЫВЫ ====================
async def cb_review(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    order_id = q.data.split("|")[1]
    context.user_data["review_order"] = order_id
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton("⭐", callback_data="rate|1"),
        InlineKeyboardButton("⭐⭐", callback_data="rate|2"),
        InlineKeyboardButton("⭐⭐⭐", callback_data="rate|3"),
        InlineKeyboardButton("⭐⭐⭐⭐", callback_data="rate|4"),
        InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data="rate|5"),
    ]])
    await q.edit_message_text("⭐ Фармоишро баҳо гузоред:", reply_markup=kb)


async def cb_rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    rating = q.data.split("|")[1]
    await q.answer()
    user_id = q.from_user.id
    user_points[user_id] = user_points.get(user_id, 0) + 5
    await q.edit_message_text(
        f"{'⭐' * int(rating)} Раҳмат барои баҳо!\n\n+5 хол гирифтед! ⭐",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Бош меню", callback_data="main_menu")]]))
    try:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"⭐ Баҳои нав: {'⭐'*int(rating)}\nАз мизоҷ: {q.from_user.first_name}"
        )
    except:
        pass


# ==================== КОМАНДЫ АДМИНИСТРАТОРА ====================
async def cmd_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    total_users = len(all_users)
    total_orders = order_counter[0]
    total_revenue = sum(
        sum(o["total"] for o in orders)
        for orders in user_orders_history.values()
    )
    vip_count = len(vip_users)
    text = (
        f"📊 *Омор:*\n\n"
        f"👤 Корбарон: {total_users}\n"
        f"📦 Фармоишҳо: {total_orders}\n"
        f"💰 Даромад: {total_revenue} сомон\n"
        f"👑 VIP: {vip_count}\n"
        f"⏸️ Пауза: {'Да' if pause_mode[0] else 'Нет'}"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def cmd_pause(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    pause_mode[0] = not pause_mode[0]
    status = "⏸️ ҚАТЪ" if pause_mode[0] else "▶️ ФАЪОЛ"
    await update.message.reply_text(f"Қабули фармоиш: {status}")


async def cmd_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("📣 Паёмро нависед (ба ҳама мефиристем):")
    return ENTER_BROADCAST


async def process_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return ConversationHandler.END
    msg = update.message.text
    sent = 0
    for uid in all_users:
        try:
            await context.bot.send_message(chat_id=uid, text=f"📣 {msg}")
            sent += 1
        except:
            pass
    await update.message.reply_text(f"✅ Фиристода шуд: {sent} нафар")
    return ConversationHandler.END


# ==================== МЕСТОПОЛОЖЕНИЕ ====================
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
    await update.message.reply_text("Бекор шуд.", reply_markup=main_kb(update.effective_user.id))
    return ConversationHandler.END


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # ConversationHandler для заказа
    order_conv = ConversationHandler(
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

    promo_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(cb_enter_promo, pattern="^enter_promo$")],
        states={ENTER_PROMO: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_promo)]},
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=False,
    )

    broadcast_conv = ConversationHandler(
        entry_points=[CommandHandler("broadcast", cmd_broadcast)],
        states={ENTER_BROADCAST: [MessageHandler(filters.TEXT & ~filters.COMMAND, process_broadcast)]},
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=False,
    )

    preorder_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(cb_preorder, pattern="^preorder$")],
        states={
            ENTER_PREORDER_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_preorder_time)],
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
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CommandHandler("pause", cmd_pause))
    app.add_handler(order_conv)
    app.add_handler(promo_conv)
    app.add_handler(broadcast_conv)
    app.add_handler(preorder_conv)
    app.add_handler(CallbackQueryHandler(cb_admin_action, pattern="^(accept|reject|courier|ready)\\|"))
    app.add_handler(CallbackQueryHandler(cb_review, pattern="^review\\|"))
    app.add_handler(CallbackQueryHandler(cb_rate, pattern="^rate\\|"))
    app.add_handler(CallbackQueryHandler(cb_main_menu, pattern="^main_menu$"))
    app.add_handler(CallbackQueryHandler(cb_menu,       pattern="^menu$"))
    app.add_handler(CallbackQueryHandler(cb_category,   pattern="^cat\\|"))
    app.add_handler(CallbackQueryHandler(cb_dish,       pattern="^dish\\|"))
    app.add_handler(CallbackQueryHandler(cb_add,        pattern="^add\\|"))
    app.add_handler(CallbackQueryHandler(cb_remove,     pattern="^remove\\|"))
    app.add_handler(CallbackQueryHandler(cb_cart,       pattern="^cart$"))
    app.add_handler(CallbackQueryHandler(cb_clear,      pattern="^clear_cart$"))
    app.add_handler(CallbackQueryHandler(cb_location,   pattern="^location$"))
    app.add_handler(CallbackQueryHandler(cb_contacts,   pattern="^contacts$"))
    app.add_handler(CallbackQueryHandler(cb_promo,      pattern="^promo$"))
    app.add_handler(CallbackQueryHandler(cb_my_points,  pattern="^my_points$"))
    app.add_handler(CallbackQueryHandler(cb_lucky_wheel, pattern="^lucky_wheel$"))
    app.add_handler(CallbackQueryHandler(cb_lang,       pattern="^lang$"))
    app.add_handler(CallbackQueryHandler(cb_setlang,    pattern="^setlang\\|"))
    app.add_handler(CallbackQueryHandler(cb_search,     pattern="^search$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search))

    print("Мега-бот запущен! 🚀")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
