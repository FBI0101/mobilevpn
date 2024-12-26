import os
import tempfile
import yt_dlp as youtube_dl
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Token do seu bot do Telegram
TOKEN = '7329791456:AAFd7GHgWxNey2FWdGpas5J-bvJvs3fuwFc'

# Função para baixar o vídeo usando yt-dlp
def download_video(url):
    try:
        # Cria um diretório temporário
        temp_dir = tempfile.mkdtemp()
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            title = info_dict.get('title', 'Sem título')
            return filename, title, temp_dir
    except Exception as e:
        print(f"Erro ao baixar o vídeo: {e}")
        return None, None, None

# Função para responder ao comando /start
async def start(update: Update, context):
    await update.message.reply_text('Olá! Envie um link do YouTube para baixar o vídeo.')

# Função para lidar com os links de vídeo
async def handle_video(update: Update, context):
    url = update.message.text
    if 'youtube.com' in url or 'youtu.be' in url:
        await update.message.reply_text('Baixando o vídeo, por favor, aguarde...')
        video_file, title, temp_dir = download_video(url)
        if video_file:
            try:
                # Aguarda 5 segundos antes de enviar o vídeo
                time.sleep(5)
                
                # Envia o vídeo com o título como legenda
                await update.message.reply_video(video=open(video_file, 'rb'), caption=f"**Título:** {title}", parse_mode='Markdown')
                await update.message.reply_text('Processo concluído!')
            except Exception as e:
                await update.message.reply_text(f"Erro ao enviar o vídeo: {e}")
            finally:
                # Limpa o diretório temporário
                if temp_dir and os.path.exists(temp_dir):
                    for file in os.listdir(temp_dir):
                        os.remove(os.path.join(temp_dir, file))
                    os.rmdir(temp_dir)
        else:
            await update.message.reply_text('Erro ao baixar o vídeo. Tente novamente mais tarde.')
    else:
        await update.message.reply_text('Por favor, envie um link válido do YouTube.')

# Função principal para inicializar o bot
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video))
    application.run_polling()

if __name__ == "__main__":
    main()
