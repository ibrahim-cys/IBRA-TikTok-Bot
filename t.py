import os
import shutil
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQuery_handler, ContextTypes
import yt_dlp

# --- CONFIGURATION ---
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
DOWNLOAD_DIR = './downloads/'

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# --- CORE FUNCTIONS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚡ **Architect Downloader 2099 Online.**\nأرسل رابط المقطع للبدء.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"):
        return

    await update.message.reply_text("🔍 جاري فحص الرابط وتجاوز القيود...")
    
    # خيارات استخراج المعلومات والجودات
    ydl_opts = {'quiet': True, 'no_warnings': True, 'noplaylist': True}
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get('formats', [])
        
        # تصفية الجودات المتاحة (فيديو فقط مع صوت)
        buttons = []
        seen_resolutions = set()
        for f in formats:
            res = f.get('height')
            if res and res not in seen_resolutions and f.get('vcodec') != 'none':
                buttons.append([InlineKeyboardButton(f"{res}p - High Speed", callback_data=f"{url}|{f['format_id']}|{res}")])
                seen_resolutions.add(res)

    reply_markup = InlineKeyboardMarkup(buttons[:5]) # عرض أفضل 5 جودات
    await update.message.reply_text("⚙️ اختر الجودة المطلوبة:", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data.split('|')
    url, format_id, res = data[0], data[1], data[2]
    user_id = query.from_user.id
    file_path = f"{DOWNLOAD_DIR}{user_id}_{res}.mp4"

    await query.edit_message_text(f"🚀 جاري التحميل بجودة {res}p... يرجى الانتظار.")

    # إعدادات التحميل النهائية (تخطي الحماية + بدون علامة مائية)
    ydl_download_opts = {
        'format': f"{format_id}+bestaudio/best",
        'outtmpl': file_path,
        'merge_output_format': 'mp4',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_download_opts) as ydl:
            ydl.download([url])

        # إرسال الملف للمستخدم
        with open(file_path, 'rb') as video:
            await context.bot.send_video(chat_id=query.message.chat_id, video=video, caption="✅ تم التحميل بنجاح بواسطة 2099 Engine")

    except Exception as e:
        await query.message.reply_text(f"❌ خطأ في النظام: {str(e)}")
    
    finally:
        # --- AUTO-CLEANUP (ميزة المسح التلقائي) ---
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"🧹 تم تنظيف المساحة: {file_path}")

# --- EXECUTION ---
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    print("SYSTEM START: 100% EFFICIENCY")
    app.run_polling()
