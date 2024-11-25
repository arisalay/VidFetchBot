import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import yt_dlp

TOKEN = '7608094678:AAG6Ct3k29-Sbz9fvCvLz90RJ6eT1B6U8n0'

def start(update, context):
    update.message.reply_text("مرحباً بك! أرسل لي رابط فيديو وسأقوم بتنزيله لك.")

def download_video(update, context):
    url = update.message.text
    try:
        with yt_dlp.YoutubeDL({'outtmpl': '%(title)s.%(ext)s'}) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            format = ydl.prepare_filename(info_dict)
            ydl.download([url])
            update.message.reply_text(f"تم تنزيل الفيديو: {info_dict['title']}")
    except Exception as e:
        update.message.reply_text(f"حدث خطأ أثناء التنزيل: {e}")

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
download_handler = MessageHandler(Filters.text & (~Filters.command), download_video)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(download_handler)

updater.start_polling()
updater.idle()
