import json
import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from obuna_checker import check_subscription

MAX_ATTEMPTS = 2

def load_json(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇺🇿 O‘zbek", callback_data="lang|uz")],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang|ru")]
    ]
    await update.message.reply_text("Tilni tanlang:", reply_markup=InlineKeyboardMarkup(keyboard))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = str(user.id)
    if not await check_subscription(user.id, context.bot):
        await update.message.reply_text("❗ Botdan foydalanish uchun @zakovatprogr kanaliga obuna bo‘ling.")
        return

    users = load_json("data/users.json")
    today = str(datetime.date.today())
    if chat_id not in users:
        users[chat_id] = {"lang": "uz", "date": today, "attempts": 0, "score": 0}

    if users[chat_id]["date"] != today:
        users[chat_id]["date"] = today
        users[chat_id]["attempts"] = 0

    if users[chat_id]["attempts"] >= MAX_ATTEMPTS:
        await update.message.reply_text("❌ Bugungi urinishlar soni tugagan.")
        save_json("data/users.json", users)
        return

    lang = users[chat_id].get("lang", "uz")
    questions = load_json("data/questions.json")
    question = questions[-1]
    options = question["options"]
    keyboard = [[InlineKeyboardButton(opt, callback_data=f"ans|{i}")] for i, opt in enumerate(options)]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.user_data["correct"] = question["correct"]
    context.user_data["explanation"] = question["explanation"]
    users[chat_id]["attempts"] += 1
    save_json("data/users.json", users)

    await update.message.reply_text(question["text"], reply_markup=reply_markup)

async def answer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = str(query.from_user.id)
    users = load_json("data/users.json")
    correct = context.user_data.get("correct")
    explanation = context.user_data.get("explanation")
    selected = int(query.data.split("|")[1])
    if selected == correct:
        users[user_id]["score"] += 1
        response = f"✅ To‘g‘ri javob!\n\nℹ️ Izoh: {explanation}"
    else:
        response = f"❌ Noto‘g‘ri javob.\n\nℹ️ Izoh: {explanation}"
    save_json("data/users.json", users)
    await query.edit_message_text(response)

async def show_top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_json("data/users.json")
    top_users = sorted(users.items(), key=lambda x: x[1].get("score", 0), reverse=True)[:10]
    msg = "🏆 TOP 10:\n"
    for i, (uid, data) in enumerate(top_users, 1):
        msg += f"{i}. ID: {uid} — {data.get('score', 0)} ball\n"
    await update.message.reply_text(msg)

async def show_score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    users = load_json("data/users.json")
    score = users.get(user_id, {}).get("score", 0)
    attempts = users.get(user_id, {}).get("attempts", 0)
    percent = int((score / (attempts or 1)) * 100)
    await update.message.reply_text(f"📊 Ballar: {score}\n🎯 Foiz: {percent}%")
