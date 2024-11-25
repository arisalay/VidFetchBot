import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from yt_dlp import YoutubeDL

# ضع هنا التوكن الخاص ببوتك
TOKEN = "7608094678:AAG6Ct3k29-Sbz9fvCvLz90RJ6eT1B6U8n0"

# إذا كنت تستخدم Webhook (للاستضافة)، أدخل رابط الـ Webhook هنا
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")  # ضع الرابط الخاص بـ Render أو أي استضافة
PORT = int(os.environ.get("PORT", 8443))  # المنفذ الافتراضي أو المنفذ المخصص

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تعريف الأمر /start"""
    await update.message.reply_text(
        "مرحبًا بك في VidFetchNow! 🚀\n"
        "أرسل لي رابط فيديو، وسأقوم بتنزيله لك."
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تنزيل الفيديو من الرابط"""
    url = update.message.text

    if not url.startswith("http"):
        await update.message.reply_text("❌ يرجى إرسال رابط صالح!")
        return

    await update.message.reply_text("🔄 جاري تنزيل الفيديو، الرجاء الانتظار...")

    ydl_opts = {
        'outtmpl': 'downloaded_video.mp4',  # اسم الفيديو بعد التنزيل
        'format': 'mp4',  # صيغة الفيديو
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open("downloaded_video.mp4", "rb") as video:
            await update.message.reply_video(video)

        await update.message.reply_text("✅ تم التنزيل بنجاح!")
        os.remove("downloaded_video.mp4")  # حذف الفيديو بعد الإرسال
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ أثناء التنزيل: {e}")

def main():
    """الإعدادات وتشغيل البوت"""
    app = ApplicationBuilder().token(TOKEN).build()

    # إضافة الأوامر والمعالجات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    # تشغيل البوت باستخدام Polling (للتشغيل المحلي)
    if not WEBHOOK_URL:
        print("🚀 تشغيل البوت باستخدام polling...")
        app.run_polling()
    else:
        # تشغيل البوت باستخدام Webhook (للاستضافة)
        print("🚀 تشغيل البوت باستخدام webhook...")
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=WEBHOOK_URL,
        )

if __name__ == "__main__":
    main()
