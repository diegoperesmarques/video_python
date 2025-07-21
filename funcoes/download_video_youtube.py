import os
import re
import glob
import yt_dlp


def download_video_youtube(objeto): 

    objeto.limpar_tela()
    print("\n=== Programa de Download e Transcrição de Vídeos do YouTube ===")

    # --- NOVO: Perguntar quantos vídeos baixar e validar a entrada ---
    while True:
        try:
            num_videos_str = input("Quantos vídeos você deseja baixar? ")
            num_videos = int(num_videos_str)
            if num_videos > 0:
                break
            else:
                print("Por favor, digite um número maior que zero.")
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")

    # --- NOVO: Coletar todos os links dos vídeos ---
    urls = []
    for i in range(num_videos):
        link = input(f"Digite o link do vídeo {i+1}/{num_videos}: ")
        urls.append(link)

    print("\nColeta de links finalizada. Iniciando processamento dos vídeos...")

    # --- NOVO: Laço de repetição para processar cada vídeo da lista ---
    for i, url in enumerate(urls):
        print(f"\n{'='*20} PROCESSANDO VÍDEO {i+1}/{num_videos} {'='*20}")
        print(f"URL: {url}")
		
        nome_video = obter_info_video(url)
        print(f"Título do vídeo: {nome_video}")

        print("Baixando vídeo...")
        arquivo_video = download_mp4_from_youtube(url, nome_video)
        if not arquivo_video:
            print(f"Falha ao baixar o vídeo {url}. Pulando para o próximo.")
            continue  # Pula para o próximo vídeo da lista


    print("\nTodos os processos foram concluídos com sucesso!")
	
	
	
def download_mp4_from_youtube(url, nome_video):
    import yt_dlp
    filename = nome_video + '.%(ext)s'
    ydl_opts = {
        'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': filename,
        'noplaylist': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'headers': {'Accept-Language': 'en-US,en;q=0.9'},
        'sleep_interval': 1,
        'max_sleep_interval': 5,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Chegou na função download_mp4_from_youtube")
            print(f"Nome do vídeo recebido {nome_video}")
            ydl.extract_info(url, download=True)
            arquivos_baixados = glob.glob(f"{re.escape(nome_video)}.*")
            
            
            for arq in arquivos_baixados:
                if arq.endswith(('.mp4', '.mkv', '.webm')):
                    print(f"Vídeo baixado como: {arq}")
                    return arq
            print(f"Vídeo baixado, mas não encontrado. Verificando por: {nome_video}.mp4")
            return f"{nome_video}.mp4"
    except Exception as e:
        print(f"Erro ao baixar vídeo: {e}")
        return None


def obter_info_video(url):
    import yt_dlp
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'headers': {'Accept-Language': 'en-US,en;q=0.9'}
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            titulo = info.get('title', 'video')
            return limpar_nome_arquivo(titulo)
    except Exception as e:
        print(f"Erro ao obter informações do vídeo: {e}")
        return "video_sem_titulo"


def limpar_nome_arquivo(nome):
    # Remove caracteres não permitidos em nomes de arquivos
    nome_limpo = re.sub(r'[\\/*?:"<>|]', "", nome)
    return nome_limpo.strip()
