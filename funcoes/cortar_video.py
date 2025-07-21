import os
import ffmpeg
from datetime import datetime



def cortar_video(objeto):
	"""Corta um vídeo com base nos tempos de início e fim"""
	objeto.limpar_tela()
	print("== CORTAR VÍDEO ==")

	arquivos_video = objeto.listar_videos()
	if not arquivos_video:
		input("Pressione ENTER para voltar ao menu principal...")
		return

	arquivo_selecionado = objeto.selecionar_arquivo(arquivos_video)
	if not arquivo_selecionado:
		input("Pressione ENTER para voltar ao menu principal...")
		return

	try:
		print("\nDigite os tempos no formato HH:MM:SS")
		tempo_inicio = input("Tempo de início: ")
		tempo_fim = input("Tempo de fim: ")

		nome_base, extensao = os.path.splitext(os.path.basename(arquivo_selecionado))
		timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
		arquivo_saida = os.path.join(objeto.diretorio_atual, f"{nome_base}_cortado_{timestamp}{extensao}")

		print(f"\nCortando vídeo {os.path.basename(arquivo_selecionado)}...")
		ffmpeg.input(arquivo_selecionado, ss=tempo_inicio, to=tempo_fim).output(
			arquivo_saida, c='copy').run(quiet=True, overwrite_output=True)
		print(f"Vídeo cortado com sucesso! Salvo como: {os.path.basename(arquivo_saida)}")
	except Exception as e:
		print(f"Erro ao cortar vídeo: {e}")

	if input("\nDeseja cortar outro vídeo? (s/n): ").lower() == 's':
		objeto.cortar_video()
