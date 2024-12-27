import os
import yt_dlp as youtube_dl
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = '7329791456:AAFd7GHgWxNey2FWdGpas5J-bvJvs3fuwFc'

def download_video(url, download_path, resolution):
    if not os.path.exists(download_path):
        try:
            os.makedirs(download_path)
        except Exception as e:
            print(f"Erro ao criar diretório {download_path}: {e}")
            return None, None

    ydl_opts = {
        'format': f'bestvideo[height<={resolution}]+bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            title = info_dict.get('title', 'Sem título')
            return filename, title
        except Exception as e:
            print(f"Erro ao baixar o vídeo: {e}")
            return None, None

async def start(update: Update, context):
    await update.message.reply_text('Olá! Envie um link do YouTube para baixar o vídeo.')

async def handle_video(update: Update, context):
    url = update.message.text
    if 'youtube.com' in url or 'youtu.be' in url:
        await update.message.reply_text('Escolha a resolução do vídeo:\n1. 720p\n2. 1080p')
        return
    else:
        await update.message.reply_text('Por favor, envie um link válido do YouTube.')

async def handle_resolution(update: Update, context):
    resolution = update.message.text.strip()
    if resolution == "1":
        resolution = 720
    elif resolution == "2":
        resolution = 1080
    else:
        await update.message.reply_text('Escolha uma resolução válida (1 para 720p, 2 para 1080p).')
        return
    
    url = context.user_data.get("video_url")
    if not url:
        await update.message.reply_text('Erro: URL não encontrada.')
        return

    await update.message.reply_text(f'Baixando o vídeo em {resolution}p, aguarde...')
    
    download_path = '/tmp/'
    video_file, title = download_video(url, download_path, resolution)
    
    if video_file:
        with open(video_file, 'rb') as video:
            await update.message.reply_video(video, caption=title)
        os.remove(video_file)
    else:
        await update.message.reply_text('Erro ao baixar o vídeo. Tente novamente mais tarde.')

def start_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_resolution))

    application.run_polling()

if __name__ == "__main__":
    start_bot()
