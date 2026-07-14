import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8777558498:AAGTq666BAspySWoAEm1Fks9CmZvRyf3VnQ"

# ---------- БАНДЛЫ STANDOFF 2 ----------
STANDOFF_BUNDLES = {
    "🔫 Оружие (скины)": "/storage/emulated/0/files_for_bot/weapons.zip",
    "🎨 Текстуры": "/storage/emulated/0/files_for_bot/textures.zip",
    "⚙️ Конфиг (прицел, чувка)": "/storage/emulated/0/files_for_bot/config.cfg",
    "📱 HUD / Интерфейс": "/storage/emulated/0/files_for_bot/hud.zip",
    "🎵 Музыка и звуки": "/storage/emulated/0/files_for_bot/sounds.zip",
    "🖼 Обои Standoff 2": "/storage/emulated/0/files_for_bot/wallpapers.zip",
}
# ---------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for name in STANDOFF_BUNDLES.keys():
        keyboard.append([InlineKeyboardButton(name, callback_data=f"bundle_{name}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🎯 Бандлы Standoff 2\n\nВыбери, что скачать:",
        reply_markup=reply_markup
    )

async def send_bundle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    bundle_name = query.data.replace("bundle_", "")
    bundle_path = STANDOFF_BUNDLES.get(bundle_name)
    
    if bundle_path:
        try:
            with open(bundle_path, "rb") as f:
                await context.bot.send_document(
                    chat_id=query.message.chat_id,
                    document=f,
                    filename=bundle_name
                )
        except FileNotFoundError:
            await query.answer("Файл не найден!", show_alert=True)
    else:
        await query.answer("Ошибка!", show_alert=True)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(send_bundle, pattern="^bundle_"))
    
    logger.info("Бот запущен...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()