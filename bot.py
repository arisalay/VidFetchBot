import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from yt_dlp import YoutubeDL

# أدخل التوكن الخاص ببوتك هنا
TOKEN = "7608094678:AAE-Rn-jJpxmrwXeSXH59MpLnOVi5BfabfM"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحبًا بك في VidFetchNow! 🚀\n"
        "أرسل لي رابط فيديو، وسأقوم بتنزيله لك."
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if not url.startswith("http"):
        await update.message.reply_text("❌ يرجى إرسال رابط صالح!")
        return

    await update.message.reply_text("🔄 جاري تنزيل الفيديو، الرجاء الانتظار...")

    # إعدادات yt-dlp لتحميل الفيديو
    ydl_opts = {
        'outtmpl': 'downloaded_video.mp4',  # اسم الفيديو بعد التنزيل
        'format': 'mp4',  # صيغة الفيديو
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # إرسال الفيديو بعد التنزيل
        with open("downloaded_video.mp4", "rb") as video:
            await update.message.reply_video(video)

        await update.message.reply_text("✅ تم التنزيل بنجاح!")
        os.remove("downloaded_video.mp4")  # حذف الفيديو بعد الإرسال
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ أثناء التنزيل: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    app.run_polling()

if __name__ == '__main__':
    main()
