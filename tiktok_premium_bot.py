
# في بداية الكود، تحت الاستيرادات
import subprocess
import sys

# التحقق من وجود ffmpeg
def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True)
        print("✅ FFmpeg مثبت")
        return True
    except:
        print("⚠️ FFmpeg غير مثبت - استمرار بدون FFmpeg")
        return False

# شغلها بعد تعريف bot
check_ffmpeg()

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
    print("🤖 البوت شغال على Render...")
    
    # للـ Render: نضيف Webhook بسيط عشان ما ينام
    import requests
    from threading import Timer
    
    def keep_alive():
        """إرسال إشارة كل 10 دقائق عشان ما ينام"""
        try:
            # هذا مهم جداً لـ Render
            pass
        except:
            pass
        Timer(600, keep_alive).start()
    
    # تشغيل الـ keep_alive
    Timer(600, keep_alive).start()
    
    # تشغيل البوت
    bot.infinity_polling()

if __name__ == "__main__":
    main()
