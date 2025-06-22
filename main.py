import json
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from handlers.user import start, answer_callback, show_top, show_score, set_language
from handlers.admin import admin_panel

TOKEN = "7951133862:AAFgVLJrMjNK-Rt_pwFCQX7SoperFfa40Wk"

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("top", show_top))
app.add_handler(CommandHandler("score", show_score))
app.add_handler(CommandHandler("lang", set_language))
app.add_handler(CallbackQueryHandler(answer_callback))
app.add_handler(MessageHandler(filters.TEXT & filters.User(user_id=7342925788), admin_panel))

if __name__ == "__main__":
    print("Zakovat bot ishga tushdi...")
    app.run_polling()
