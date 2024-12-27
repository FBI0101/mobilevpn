import os
import yt_dlp as youtube_dl
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Substitua com o token do seu bot
TOKEN = '7329791456:AAFd7GHgWxNey2FWdGpas5J-bvJvs3fuwFc'

# Função para baixar o vídeo usando yt-dlp
def download_video(url, download_path):
    ydl_opts = {
        'format': 'best',  # Melhor formato disponível sem mesclagem
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),  # Nome do arquivo
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

# Comando /start
async def start(update: Update, context):
    await update.message.reply_text('Olá! Envie um link do YouTube para baixar o vídeo.')

# Handler para links de vídeos
async def handle_video(update: Update, context):
    url = update.message.text
    if 'youtube.com' in url or 'youtu.be' in url:
        await update.message.reply_text('Baixando o vídeo, por favor, aguarde...')
        download_path = os.path.join(os.getcwd(), 'downloads')  # Diretório para salvar os vídeos

        # Certificar-se de que o diretório existe
        if not os.path.exists(download_path):
            os.makedirs(download_path)

        # Baixar o vídeo
        video_file = download_video(url, download_path)
        if video_file:
            # Enviar o vídeo de volta para o Telegram
            await update.message.reply_video(video=open(video_file, 'rb'))
            os.remove(video_file)  # Remover o vídeo após enviar
        else:
            await update.message.reply_text(
                'Erro ao baixar o vídeo. Certifique-se de que o link é público e tente novamente.'
            )
    else:
        await update.message.reply_text('Por favor, envie um link válido do YouTube.')

# Função principal para iniciar o bot
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video))

    print("Bot iniciado. Aguardando mensagens...")
    application.run_polling()

if __name__ == "__main__":
    main()
