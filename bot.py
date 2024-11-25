import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from yt_dlp import YoutubeDL

TOKEN = "7608094678:AAG6Ct3k29-Sbz9fvCvLz90RJ6eT1B6U8n0"
WEBHOOK_URL = "https://your-deployed-url"

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

    ydl_opts = {
        'outtmpl': 'downloaded_video.mp4',
        'format': 'mp4',
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open("downloaded_video.mp4", "rb") as video:
            await update.message.reply_video(video)

        os.remove("downloaded_video.mp4")
        await update.message.reply_text("✅ تم التنزيل بنجاح!")
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ أثناء التنزيل: {e}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    # ضبط Webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8443)),
        webhook_url=WEBHOOK_URL
    )

if __name__ == '__main__':
    main()
