import os
import ffmpeg

def extrair_audio(objeto):
	"""Extrai o áudio de um arquivo de vídeo"""
	objeto.limpar_tela()
	print("== EXTRAIR ÁUDIO ==")

	arquivos_video = objeto.listar_videos()
	if not arquivos_video:
		input("Pressione ENTER para voltar ao menu principal...")
		return

	arquivo_selecionado = objeto.selecionar_arquivo(arquivos_video)
	if not arquivo_selecionado:
		input("Pressione ENTER para voltar ao menu principal...")
		return

	nome_base = os.path.splitext(os.path.basename(arquivo_selecionado))[0]
	arquivo_saida = os.path.join(objeto.diretorio_atual, f"{nome_base}_audio.mp3")

	try:
		print(f"\nExtraindo áudio de {os.path.basename(arquivo_selecionado)}...")
		ffmpeg.input(arquivo_selecionado).output(arquivo_saida, acodec='libmp3lame', q=4).run(quiet=True, overwrite_output=True)
		print(f"Áudio extraído com sucesso! Salvo como: {os.path.basename(arquivo_saida)}")
	except Exception as e:
		print(f"Erro ao extrair áudio: {e}")

	if input("\nDeseja extrair áudio de outro vídeo? (s/n): ").lower() == 's':
		objeto.extrair_audio()
