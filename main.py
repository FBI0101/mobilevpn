import os
import yt_dlp as youtube_dl
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Substitua com o token do seu bot
TOKEN = '7329791456:AAFd7GHgWxNey2FWdGpas5J-bvJvs3fuwFc'

# Função para baixar o vídeo usando yt-dlp
def download_video(url, download_path):
    # Verificar se o diretório de download existe, se não, cria-lo
    if not os.path.exists(download_path):
        try:
            os.makedirs(download_path, exist_ok=True)  # Criação do diretório
            print(f"Diretório {download_path} criado com sucesso!")
        except Exception as e:
            print(f"Erro ao criar o diretório: {e}")
            return None

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
            return filename
        except Exception as e:
            print(f"Erro ao baixar o vídeo: {e}")
            return None

# Função que será chamada quando o bot receber uma mensagem
async def start(update: Update, context):
    await update.message.reply_text('Olá! Envie um link do YouTube para baixar o vídeo.')

# Função para lidar com links de vídeos do YouTube
async def handle_video(update: Update, context):
    url = update.message.text
    if 'youtube.com' in url or 'youtu.be' in url:
        # Baixar o vídeo
        await update.message.reply_text('Baixando o vídeo, por favor, aguarde...')
        download_path = './downloads/'  # Caminho onde o vídeo será salvo dentro do projeto
        video_file = download_video(url, download_path)
        if video_file:
            # Enviar o vídeo de volta para o Telegram
            with open(video_file, 'rb') as video:
                await update.message.reply_video(video=video)
            os.remove(video_file)  # Remover o vídeo após enviar
        else:
            await update.message.reply_text('Erro ao baixar o vídeo. Tente novamente mais tarde.')
    else:
        await update.message.reply_text('Por favor, envie um link válido do YouTube.')

# Função para iniciar o bot
def start_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_video))

    application.run_polling()

# Função de controle do painel
def control_panel():
    while True:
        print("Painel de Controle do Bot:")
        print("1. Iniciar o Bot")
        print("2. Parar o Bot")
        print("3. Verificar Status")
        print("4. Sair")
        choice = input("Escolha uma opção (1/2/3/4): ")

        if choice == '1':
            start_bot()
        elif choice == '2':
            print("Bot parado (note que o Replit pode continuar executando).")
            break
        elif choice == '3':
            print("Bot está em execução.")  # Status simplificado
        elif choice == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if name == "main":
    control_panel()
