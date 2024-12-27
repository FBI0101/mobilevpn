import os
import yt_dlp as youtube_dl
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = '7329791456:AAFd7GHgWxNey2FWdGpas5J-bvJvs3fuwFc'

# Função para baixar o vídeo e retornar o título
def download_video(url, download_path):
    ydl_opts = {
        'format': 'best',
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

# Função para iniciar o bot
async def start(update: Update, context):
    await update.message.reply_text('Bem-vindo ao painel de controle do bot. Envie um comando para interagir.')

# Função para painel
async def painel(update: Update, context):
    options = """
    Painel de Controle:
    1. /baixar_video <URL> - Baixa um vídeo do YouTube
    2. /status - Verifica o status do bot
    3. /parar_bot - Para o bot
    """
    await update.message.reply_text(f"Painel de Controle do Bot:\n{options}")

# Função para verificar status do bot
async def status(update: Update, context):
    await update.message.reply_text("O bot está funcionando corretamente.")

# Função para baixar vídeo com título e enviar ao Telegram
async def handle_video(update: Update, context):
    url = update.message.text
    if 'youtube.com' in url or 'youtu.be' in url:
        await update.message.reply_text('Baixando o vídeo...')
        download_path = '/tmp/'  # Usando diretório temporário
        video_file, title = download_video(url, download_path)
        if video_file:
            # Enviar o vídeo
            await update.message.reply_video(video=open(video_file, 'rb'))
            # Enviar o título
            await update.message.reply_text(f"Título do vídeo: {title}")
            # Enviar mensagem de conclusão
            await update.message.reply_text("Processo concluído!")
            os.remove(video_file)  # Remover o vídeo após enviar
        else:
            await update.message.reply_text('Erro ao baixar o vídeo. Tente novamente mais tarde.')
    else:
        await update.message.reply_text('Por favor, envie um link válido do YouTube.')

# Função para parar o bot
async def parar_bot(update: Update, context):
    await update.message.reply_text("O bot será parado. Até logo!")
    os._exit(0)  # Encerra o bot

# Função principal para iniciar o bot
def main():
    application = Application.builder().token(TOKEN).build()

    # Adiciona os manipuladores de comandos e mensagens
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("painel", painel))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("parar_bot", parar_bot))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video))

    # Inicia o bot
    application.run_polling()

if __name__ == "__main__":
    main()
