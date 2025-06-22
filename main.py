import os
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from handlers.user import start, answer_callback, show_top, show_score, set_language
from handlers.admin import admin_panel

TOKEN = os.getenv("BOT_TOKEN") or "7951133862:AAFgVLJrMjNK-Rt_pwFCQX7SoperFfa40Wk"

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("top", show_top))
app.add_handler(CommandHandler("score", show_score))
app.add_handler(CommandHandler("lang", set_language))
app.add_handler(CallbackQueryHandler(answer_callback, pattern="^ans\\|"))
app.add_handler(CallbackQueryHandler(set_language, pattern="^lang\\|"))
app.add_handler(CommandHandler("admin", admin_panel))

if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()
