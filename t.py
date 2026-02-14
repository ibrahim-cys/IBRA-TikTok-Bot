import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

# --- CONFIGURATION ---
# سيتم جلب التوكن من "Secrets" في ريبلت للأمان
TOKEN = os.environ.get('7944519785:AAHhAwmPkc4avLZu7S3d9dtO8FgRW1RL39c')
DOWNLOAD_DIR = 'downloads'

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚡ **Architect Downloader 2099 Online.**\nأرسل رابط المقطع للبدء.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"): return

    msg = await update.message.reply_text("🔍 جاري فحص الرابط وتجاوز القيود...")
    
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True, 'noplaylist': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            
            buttons = []
            seen_res = set()
            for f in formats:
                res = f.get('height')
                if res and res not in seen_res and f.get('vcodec') != 'none':
                    if res >= 360: # فلترة الجودات الضعيفة جداً
                        buttons.append([InlineKeyboardButton(f"🎬 {res}p - Ultra Fast", callback_data=f"{url}|{f['format_id']}|{res}")])
                        seen_res.add(res)

        if not buttons:
            await msg.edit_text("❌ لم يتم العثور على جودات مدعومة لهذا الرابط.")
            return

        reply_markup = InlineKeyboardMarkup(buttons[:6])
        await msg.edit_text("⚙️ اختر الجودة المطلوبة:", reply_markup=reply_markup)
    except Exception as e:
        await msg.edit_text(f"⚠️ فشل النظام في جلب البيانات: {str(e)}")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    url, format_id, res = query.data.split('|')
    file_path = f"{DOWNLOAD_DIR}/vid_{query.from_user.id}_{res}.mp4"

    await query.edit_message_text(f"🚀 جاري التحميل بجودة {res}p... يرجى الانتظار.")

    ydl_opts = {
        'format': f"{format_id}+bestaudio/best",
        'outtmpl': file_path,
        'merge_output_format': 'mp4',
        'quiet': True,
        'postprocessors': [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'}],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open(file_path, 'rb') as video:
            await context.bot.send_video(chat_id=query.message.chat_id, video=video, caption=f"✅ Done: {res}p\n@Architect_2099")
    except Exception as e:
        await query.message.reply_text(f"❌ خطأ أثناء المعالجة: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path) # المسح التلقائي الفوري

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("SYSTEM START: 100% EFFICIENCY")
    app.run_polling()
