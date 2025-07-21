import os
import ffmpeg


def fazer_transcricao(objeto):
	"""Cria um arquivo de texto com a transcrição do vídeo usando o Whisper"""
	objeto.limpar_tela()
	print("== FAZER TRANSCRIÇÃO ==")

	if objeto.model is None:
		print("Modelo Whisper não está carregado. Tentando carregar...")
		objeto.carregar_whisper()
		if objeto.model is None:
			print("Não foi possível carregar o modelo Whisper.")
			input("Pressione ENTER para voltar ao menu principal...")
			return

	arquivos_video = objeto.listar_videos()
	if not arquivos_video:
		input("Pressione ENTER para voltar ao menu principal...")
		return

	arquivo_selecionado = objeto.selecionar_arquivo(arquivos_video)
	if not arquivo_selecionado:
		input("Pressione ENTER para voltar ao menu principal...")
		return

	nome_base = os.path.splitext(os.path.basename(arquivo_selecionado))[0]
	arquivo_audio_temp = os.path.join(objeto.diretorio_atual, f"{nome_base}_temp_audio_for_txt.mp3")
	arquivo_txt = os.path.join(objeto.diretorio_atual, f"{nome_base}_transcricao.txt")

	try:
		print(f"\nProcessando vídeo {os.path.basename(arquivo_selecionado)}...")
		print("Extraindo áudio temporário...")
		ffmpeg.input(arquivo_selecionado).output(arquivo_audio_temp, acodec='libmp3lame', q=4).run(quiet=True, overwrite_output=True)

		print("Transcrevendo áudio com Whisper (isso pode demorar um pouco)...")
		resultado = objeto.model.transcribe(arquivo_audio_temp, fp16=False)

		with open(arquivo_txt, 'w', encoding='utf-8') as f:
			f.write(resultado["text"])
		
		print(f"Transcrição concluída com sucesso! Salva como: {os.path.basename(arquivo_txt)}")
	except Exception as e:
		print(f"Erro ao fazer transcrição: {e}")
	finally:
		if os.path.exists(arquivo_audio_temp):
			os.remove(arquivo_audio_temp)

	if input("\nDeseja fazer transcrição de outro vídeo? (s/n): ").lower() == 's':
		objeto.fazer_transcricao()
