import os
import glob

def listar_videos(diretorio_pesquisa):
    """
    Lista todos os arquivos de vídeo com extensões comuns em um diretório específico.
    """
    extensoes = ['*.mp4', '*.avi', '*.mkv', '*.mov']
    arquivos_video = []

    if not os.path.isdir(diretorio_pesquisa):
        print(f"Erro: O diretório '{diretorio_pesquisa}' não foi encontrado.")
        return []

    for ext in extensoes:
        # Usamos o parâmetro 'diretorio_pesquisa' em vez de 'self.diretorio_atual'
        arquivos_video.extend(glob.glob(os.path.join(diretorio_pesquisa, ext)))

    if not arquivos_video:
        print(f"Nenhum arquivo de vídeo encontrado na pasta '{diretorio_pesquisa}'.")
        return []

    print("\nArquivos de vídeo disponíveis:")
    for i, arquivo in enumerate(arquivos_video, 1):
        nome_arquivo = os.path.basename(arquivo)
        print(f"[{i}] {nome_arquivo}")

    return arquivos_video
