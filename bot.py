# tiktok_premium_bot.py - الإصدار الفاخر

import os
import re
import time
import logging
import threading
import subprocess
from pathlib import Path
from datetime import datetime

import telebot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

# ------------------ الإعدادات الأساسية ------------------
TELEGRAM_TOKEN = "7944519785:AAHhAwmPkc4avLZu7S3d9dtO8FgRW1RL39c"
DOWNLOAD_FOLDER = "downloads"
TWITTER_HANDLE = "@ibra0101h"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# إعداد التسجيل (صامت)
logging.basicConfig(level=logging.WARNING)

# إنشاء البوت
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# ------------------ دوال التنظيف السريع ------------------
def rapid_cleanup():
    """تنظيف فائق السرعة"""
    while True:
        try:
            current_time = time.time()
            for file in Path(DOWNLOAD_FOLDER).glob("*.mp4"):
                if file.is_file() and current_time - file.stat().st_mtime > 120:  # دقيقتين فقط
                    file.unlink()
        except:
            pass
        time.sleep(20)  # فحص كل 20 ثانية

# ------------------ تحميل بسرعة الضوء ------------------
def lightning_fast_download(url):
    """أسرع نظام تحميل في العالم"""
    try:
        filename = os.path.join(DOWNLOAD_FOLDER, f"tt_{int(time.time()*1000)}.mp4")
        
        # إعدادات التحميل الخارقة
        cmd = [
            'yt-dlp',
            '-f', 'best[ext=mp4]',
            '-o', filename,
            '--extractor-args', 'tiktok:watermark=0',
            '--no-warnings',
            '--quiet',
            '--no-playlist',
            '--force-ipv4',
            '--buffer-size', '256K',        # بفر عملاق
            '--http-chunk-size', '100M',     # قطع 100 ميجا
            '--throttled-rate', '500M',      # منع التباطؤ تماماً
            '--socket-timeout', '3',          # مهلة 3 ثواني
            '--retries', '1',
            '--fragment-retries', '1',
            url
        ]
        
        # تنفيذ بدون انتظار
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait(timeout=10)  # 10 ثواني كحد أقصى
        
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            size_mb = os.path.getsize(filename) / (1024 * 1024)
            return filename, size_mb
        return None, 0
        
    except Exception:
        return None, 0

# ------------------ دوال المساعدة ------------------
def create_support_button():
    """إنشاء زر دعم الصانع"""
    keyboard = InlineKeyboardMarkup()
    support_button = InlineKeyboardButton(
        text="دعم الصانع 🤍",
        url=f"https://twitter.com/{TWITTER_HANDLE.replace('@', '')}"
    )
    keyboard.add(support_button)
    return keyboard

# ------------------ معالجات البوت الفاخرة ------------------
@bot.message_handler(commands=['start'])
def start_command(message: Message):
    """رسالة الترحيب الفاخرة"""
    welcome_text = """
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
            🤍 TIKTOK BOT 🤍
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

▸ أرسل رابط تيك توك
▸ استلم الفيديو خلال ثواني
▸ بدون علامة مائية

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
⚡ سرعة التحميل | lightning
🧹 تنظيف تلقائي | 2 دقيقة
🎯 جودة أصلية | original
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
    """
    
    bot.reply_to(
        message, 
        welcome_text, 
        reply_markup=create_support_button()
    )

@bot.message_handler(func=lambda m: True)
def handle_request(message: Message):
    """معالجة طلبات التحميل بسرعة فائقة"""
    text = message.text.strip()
    chat_id = message.chat.id
    
    # التحقق من الرابط
    if not re.search(r'tiktok\.com|vm\.tiktok', text, re.I):
        bot.reply_to(
            message,
            """
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
❌ رابط غير صحيح
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

أرسل رابط تيك توك فقط
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
            """,
            reply_markup=create_support_button()
        )
        return
    
    # بدء التحميل بدون رسالة انتظار
    start_time = time.time()
    video_path, size_mb = lightning_fast_download(text)
    total_time = time.time() - start_time
    
    if video_path and os.path.exists(video_path):
        # إرسال الفيديو مباشرة
        with open(video_path, 'rb') as video_file:
            bot.send_video(
                chat_id,
                video_file,
                caption=f"""
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
✅ تم التحميل بنجاح
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

▸ الحجم │ {size_mb:.1f} MB
▸ الوقت │ {total_time:.1f}s
▸ الجودة │ أصلية
▸ علامة │ بدون

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
⚡ تمت العملية بنجاح
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
""",
                supports_streaming=True,
                timeout=30,
                reply_markup=create_support_button()
            )
        
        # حذف الملف فوراً
        try:
            os.remove(video_path)
        except:
            pass
    else:
        # رسالة خطأ سريعة
        bot.send_message(
            chat_id,
            """
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
❌ فشل التحميل
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

▸ تأكد من الرابط
▸ حاول مرة أخرى

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
            """,
            reply_markup=create_support_button()
        )

# ------------------ تشغيل البوت ------------------
def main():
    print("╔════════════════════════════╗")
    print("║     TIKTOK PREMIUM BOT     ║")
    print("╚════════════════════════════╝")
    print("▸ الحالة │ قيد التشغيل")
    print("▸ السرعة │ lightning")
    print("▸ التنظيف │ 2 دقيقة")
    print("▸ الصانع │", TWITTER_HANDLE)
    print("══════════════════════════════")
    
    # تشغيل التنظيف السريع
    threading.Thread(target=rapid_cleanup, daemon=True).start()
    
    # تشغيل البوت
    bot.infinity_polling()

if __name__ == "__main__":
    main()
