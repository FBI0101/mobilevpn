import os
import yt_dlp as youtube_dl
import tempfile
import shutil
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = '7329791456:AAFd7GHgWxNey2FWdGpas5J-bvJvs3fuwFc'

def download_video(url, download_path):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'quiet': False,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            return filename
        except Exception as e:
            print(f"Erro ao baixar o vídeo: {e}")
            return None

async def start(update: Update, context):
    await update.message.reply_text('Olá! Envie um link do YouTube para baixar o vídeo.')

async def handle_video(update: Update, context):
    url = update.message.text
    if 'youtube.com' in url or 'youtu.be' in url:
        await update.message.reply_text('Baixando o vídeo, por favor, aguarde...')
        download_path = tempfile.mkdtemp()  # Diretório temporário

        try:
            video_file = download_video(url, download_path)
            if video_file:
                await update.message.reply_video(video=open(video_file, 'rb'))
                os.remove(video_file)
            else:
                await update.message.reply_text('Erro ao baixar o vídeo. Certifique-se de que o link é público e tente novamente.')
        finally:
            # Limpa o diretório temporário
            shutil.rmtree(download_path)
    else:
        await update.message.reply_text('Por favor, envie um link válido do YouTube.')

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video))

    print("Bot iniciado. Aguardando mensagens...")
    application.run_polling()

if __name__ == "__main__":
    main()
