import json
from telegram import Update
from telegram.ext import ContextTypes

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    if msg.startswith("savol:"):
        try:
            parts = msg.split("\n")
            text = parts[0][6:].strip()
            options = [x.strip() for x in parts[1:5]]
            correct = int(parts[5].split(":")[1].strip())
            explanation = parts[6].split(":", 1)[1].strip()

            new_question = {
                "text": text,
                "options": options,
                "correct": correct,
                "explanation": explanation
            }

            with open("data/questions.json", "r", encoding="utf-8") as f:
                questions = json.load(f)
            questions.append(new_question)
            with open("data/questions.json", "w", encoding="utf-8") as f:
                json.dump(questions, f, ensure_ascii=False, indent=2)

            await update.message.reply_text("✅ Savol qo‘shildi.")
        except Exception as e:
            await update.message.reply_text(f"Xato: {str(e)}")
