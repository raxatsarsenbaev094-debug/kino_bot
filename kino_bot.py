from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# 🔑 Tokeningiz
BOT_TOKEN = "8228111732:AAETn07Qu9x4AW4yWWITWRc9YCbHiEfkNcY"

# 🔗 Kanal linklari (aniq channel)
CHANNELS = [
    "https://t.me/UdarKinoUz",
    "https://t.me/kaaanaal2",
    "https://t.me/kaaanaal3",
    "https://t.me/kaaanaal4"
]

# 🎬 Filmlar bazasi (kod → link)
FILMS = {
    "164": "https://t.me/UdarKinoUz/4",
    "2005": "https://t.me/UdarKinoUz/5",
    "310": "https://t.me/UdarKinoUz/6",
    "930": "https://t.me/UdarKinoUz/7",
    "420": "https://t.me/UdarKinoUz/8",
    "452": "https://t.me/UdarKinoUz/9"
}

# ✅ Obunani tekshirish funksiyasi
async def is_subscribed(user_id, channel, context: ContextTypes.DEFAULT_TYPE):
    try:
        username = channel.split("/")[-1]
        member = await context.bot.get_chat_member(chat_id=f"@{username}", user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    for channel in CHANNELS:
        subscribed = await is_subscribed(user.id, channel, context)
        if not subscribed:
            text = "❗ Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling 👇"
            buttons = [[InlineKeyboardButton("Kanalga o'tish", url=ch)] for ch in CHANNELS]
            buttons.append([InlineKeyboardButton("✅ Tekshirish", callback_data="check")])
            await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))
            return

    await update.message.reply_text(
        "👋 Assalomu alaykum, hurmatli foydalanuvchi!\n"
        "Botimizga xush kelibsiz.\n\n"
        "🎬 Iltimos, kino yoki serial kodini yuboring."
    )

# ✅ Tekshirish tugmasi
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    for channel in CHANNELS:
        subscribed = await is_subscribed(user_id, channel, context)
        if not subscribed:
            await query.answer("❌ Siz hali barcha kanallarga obuna bo'lmadingiz!", show_alert=True)
            return

    await query.message.reply_text(
        "👋 Assalomu alaykum, hurmatli foydalanuvchi!\n"
        "Botimizga xush kelibsiz.\n\n"
        "🎬 Iltimos, kino yoki serial kodini yuboring."
    )
    await query.answer()

# 🔑 Kod qabul qilish va film yuborish
async def get_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip()

    if code in FILMS:
        link = FILMS[code]
        await update.message.reply_text(f"🎥 Sizning fil'mingiz: {link}")
    else:
        await update.message.reply_text("❌ Kechirasiz, bunday kod topilmadi.")

# Botni ishga tushirish
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check, pattern="check"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_code))

    print("🤖 Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
